from rest_framework.test import APIClient
import pytest
from authentication.models import UserProfile
from api.models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation
from django.urls import reverse
from api.tests.TransactionFactory import TransactionFactory
from django.db.models import Sum
from decimal import Decimal
from api.serializers import UserSerializer, OperationSerializer, AssetAllocationSerializer

from ..lib.AssetProcessor import AssetProcessor

ASSET_COUNT = 50


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(username, password, email):
        return UserProfile.objects.create_user(username=username, password=password, email=email)
    return _create_user


@pytest.fixture
def create_currency():
    def _create_currency(name, exchange_rate):
        return Currency.objects.create(name=name, exchange_rate=exchange_rate)
    return _create_currency


@pytest.mark.django_db
class TestUserViews:

    def test_user_list(self, api_client, create_user):
        user1 = create_user('user1', 'password', 'email@email.com')
        user2 = create_user('user2', 'password', 'email1@email.com')

        url = reverse('user-list')
        response = api_client.get(url)

        assert response.status_code == 200

        expected_response = UserSerializer([user1, user2], many=True).data
        assert response.json() == expected_response

    def test_user_detail(self, api_client, create_user):
        user = create_user('user1', 'password', 'email@email.com')

        api_client.force_authenticate(user=user)
        url = reverse('user-detail', args=[user.id])
        response = api_client.get(url)

        assert response.status_code == 200
        expected_response = UserSerializer(user).data
        assert response.json() == expected_response

    def test_user_destroy(self, api_client, create_user):
        user = create_user('user1', 'password', 'email@email.com')

        api_client.force_authenticate(user=user)
        url = reverse('user-detail', args=[user.id])
        response = api_client.delete(url)

        assert response.status_code == 204
        assert UserProfile.objects.filter(id=user.id).exists() == False


@pytest.mark.django_db
class TestOperationViews:

    @pytest.fixture(autouse=True)
    def setup_method(self, create_user, create_currency):
        self.user = create_user('user1', 'password', 'email@email.com')

        usd = create_currency('USD', 1)
        pln = create_currency('PLN', 4)
        eur = create_currency('EUR', 1.2)

        self.pocket_name = 'TestPocket'

        Pocket.objects.create(name=self.pocket_name,
                              owner=self.user, currency=usd, fees=0)

    def test_operations_list(self, api_client):
        api_client.force_authenticate(user=self.user)

        operation1 = Operation.objects.create(owner=self.user, ticker='AAPL', operation_type='buy',
                                              quantity=10, price=100,  fee=5,  currency='USD', date='2022-01-01', comment='Test comment')
        operation2 = Operation.objects.create(
            owner=self.user, ticker='TSLA', operation_type='buy', quantity=5, price=245, fee=1, currency='PLN', date='2022-01-01', comment='Test comment')

        url = reverse('operation-list')
        response = api_client.get(url)

        assert response.status_code == 200
        expected_response = OperationSerializer(
            [operation1, operation2], many=True).data
        assert response.json() == expected_response

    def test_operations_create(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('operation-list')

        data = {
            'asset_class': 'Equity',
            'ticker': 'AAPL',
            'operation_type': 'buy',
            'quantity': 10,
            'price': 100,
            'fee': 5,
            'currency': 'USD',
            "purchase_currency_price": 1,
            'date': '2022-01-01',
            'comment': 'Test comment',
            'pocket_name': self.pocket_name
        }

        response = api_client.post(url, data)

        assert response.status_code == 201
        assert Operation.objects.filter(ticker='AAPL').exists()
        assert Asset.objects.filter(ticker='AAPL').exists()
        pocket = Pocket.objects.get(name=self.pocket_name, owner=self.user)
        assert AssetAllocation.objects.filter(
            asset__ticker='AAPL', pocket=pocket).exists()
        assert pocket.fees == 5

    def test_operations_destroy(self, api_client):
        api_client.force_authenticate(user=self.user)
        operation = Operation.objects.create(owner=self.user, ticker='AAPL', operation_type='buy',
                                             quantity=10, price=100,  fee=5,  currency='USD', date='2022-01-01', comment='Test comment')

        url = reverse('operation-detail', args=[operation.id])
        response = api_client.delete(url)

        assert response.status_code == 204
        assert Operation.objects.filter(id=operation.id).exists() == False
        assert Asset.objects.filter(ticker='AAPL').exists() == False
        pocket = Pocket.objects.get(name=self.pocket_name, owner=self.user)
        assert AssetAllocation.objects.filter(
            asset__ticker='AAPL', pocket=pocket).exists() == False
        assert pocket.fees == 0

    def test_buy_random_assets_with_replacement(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('operation-list')

        # Create X operations by drawing without replacement
        transactionFactory = TransactionFactory(
            user=self.user, pocket_name=self.pocket_name)
        beckup_data = []

        for _ in range(ASSET_COUNT):
            draw_data = transactionFactory.draw_buy(allow_duplicates=True)
            beckup_data.append(draw_data)

            response = api_client.post(url, draw_data)
            assert response.status_code == 201

        for asset_allocation in AssetAllocation.objects.all():
            if asset_allocation == None:
                break

            ticker = asset_allocation.asset.ticker
            veryfication_list = [
                data for data in beckup_data if data['ticker'] == ticker]
            assert asset_allocation.quantity == sum(
                item['quantity'] for item in veryfication_list)
            assert asset_allocation.fee == sum(
                item['fee'] for item in veryfication_list)
            average_purchase_price = sum(item['quantity']*item['price']+item['fee']
                                         for item in veryfication_list) / sum(item['quantity'] for item in veryfication_list)
            assert asset_allocation.average_purchase_price == pytest.approx(
                Decimal(average_purchase_price), abs=0.01)

    def test_buy_sell_random(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('operation-list')

        transactionFactory = TransactionFactory(
            user=self.user, pocket_name=self.pocket_name)
        beckup_data = []

        for _ in range(ASSET_COUNT):
            draw_data = transactionFactory.draw_buy(allow_duplicates=True)
            beckup_data.append(draw_data)

            response = api_client.post(url, draw_data)
            assert response.status_code == 201

        tickers = list(set([operation["ticker"] for operation in beckup_data]))
        pocket = Pocket.objects.get(name=draw_data['pocket_name'])

        total_fee = sum(item['fee'] for item in beckup_data)

        for _ in range(ASSET_COUNT):
            if tickers:
                draw_data = transactionFactory.draw_sell(tickers=tickers)
                tickers.remove(draw_data['ticker'])
                beckup_data.append(draw_data)

                buy_operations = [
                    data for data in beckup_data if data['operation_type'] == 'buy' and data['ticker'] == draw_data['ticker']]
                sell_operations = [
                    data for data in beckup_data if data['operation_type'] == 'sell' and data['ticker'] == draw_data['ticker']]
                
                buy_quantity = sum(item['quantity'] for item in buy_operations)
                sell_quantity = sum(item['quantity'] for item in sell_operations)

                response = api_client.post(url, draw_data)

                if buy_quantity < sell_quantity:
                    assert response.status_code == 400
                    assert response.content == b'{"error":"Not enough assets to sell"}'
                elif buy_quantity == sell_quantity:
                    assert response.status_code == 201  
                    assert not AssetAllocation.objects.filter(
                        asset__ticker=draw_data['ticker'], pocket=pocket).exists()
                    total_fee += draw_data['fee']
                elif buy_quantity > sell_quantity:
                    assert response.status_code == 201
                    asset_allocation = AssetAllocation.objects.get(
                        asset__ticker=draw_data['ticker'], pocket=pocket)

                    assert asset_allocation.quantity == buy_quantity - sell_quantity
                    assert asset_allocation.fee == sum(item['fee'] for item in buy_operations+sell_operations)

                    buy_transactions = [(price, quantity, fee) for operation in buy_operations for price, quantity, fee in [(operation['price'], operation['quantity'], operation['fee'])]]
                    sell_transactions = [(price, quantity, fee) for operation in sell_operations for price, quantity, fee in [(operation['price'], operation['quantity'], operation['fee'])]] 

                    average_purchase_price = AssetProcessor._calculate_average_purchase_price(buy_transactions=buy_transactions, sell_transactions=sell_transactions)

                    try:
                        assert asset_allocation.average_purchase_price == pytest.approx(
                            Decimal(average_purchase_price), abs=0.01)
                    except AssertionError:
                        ...
                    total_fee += draw_data['fee']
            else:
                break

        pocket = Pocket.objects.get(name=self.pocket_name)
        assert pocket.fees == total_fee




 

@pytest.mark.django_db
class TestAssetAllocationViews:

    @pytest.fixture(autouse=True)
    def setup_method(self, create_user, create_currency):
        self.user = create_user('user1', 'password', 'email@email.com')

        usd = create_currency('USD', 1)
        pln = create_currency('PLN', 4)
        eur = create_currency('EUR', 1.2)

        self.pocket_name = 'TestPocket'
        Pocket.objects.create(name=self.pocket_name,
                              owner=self.user, currency=usd, fees=0)

    def test_asset_allocation_list(self, api_client):
        api_client.force_authenticate(user=self.user)
        url_send_data = reverse('operation-list')
        url_get = reverse('asset-allocation-list')

        # Create X operations by drawing without replacement
        transactionFactory = TransactionFactory(
            user=self.user, pocket_name=self.pocket_name)
        beckup_data = []

        for _ in range(ASSET_COUNT):
            draw_data = transactionFactory.draw_buy(allow_duplicates=True)
            beckup_data.append(draw_data)

            response = api_client.post(url_send_data, draw_data)
            assert response.status_code == 201

        # Get asset allocations
        response = api_client.get(url_get, {'pocket_name': self.pocket_name})
        assert response.status_code == 200

        test_participation_dic = {}
        for asset_allocation in response.json():
            ticker = asset_allocation['asset']['ticker']
            test_participation_dic[float(asset_allocation['participation'])] = float(
                asset_allocation['total_value_XXX'])

            veryfication_list = [
                data for data in beckup_data if data['ticker'] == ticker]
            assert float(asset_allocation['quantity']) == sum(
                item['quantity'] for item in veryfication_list)
            assert float(asset_allocation['fee']) == sum(
                item['fee'] for item in veryfication_list)
            average_purchase_price = sum(item['quantity']*item['price']+item['fee']
                                         for item in veryfication_list) / sum(item['quantity'] for item in veryfication_list)
            average_purchase_currency_price = sum(item['quantity']*item['purchase_currency_price']
                                                  for item in veryfication_list) / sum(item['quantity'] for item in veryfication_list)
            assert float(asset_allocation['average_purchase_price']) == pytest.approx(
                average_purchase_price, abs=0.01)
            assert float(asset_allocation['average_purchase_currency_price']) == pytest.approx(
                average_purchase_currency_price, abs=0.01)

        # Participation test
        total_sum = sum(value for value in test_participation_dic.values())
        participation_sum = sum(key for key in test_participation_dic.keys())
        assert participation_sum == pytest.approx(100, abs=0.1)

        for participation, total_value in test_participation_dic.items():
            assert participation == pytest.approx(
                total_value/total_sum*100, abs=0.1)
