from django.test import Client
import pytest
from authentication.models import UserProfile
from portfolio.models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation
from django.urls import reverse
from portfolio.tests.TransactionFactory import TransactionFactory
from django.db.models import Sum
from decimal import Decimal


@pytest.mark.django_db
class TestMainDashboardView:
    def setup_method(self):
        self.client = Client()
        self.url = reverse('main_dashboard')

    def test_get_login(self):
        self.user = UserProfile.objects.create_user(
            username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        response = self.client.get(self.url)
        assert response.status_code == 200
        assert 'portfolio/main_dashboard.html' in [
            template.name for template in response.templates]

    def test_get_not_login(self):
        response = self.client.get(self.url)
        assert response.status_code == 302

    def test_post(self):
        pass


@pytest.mark.django_db
class TestPocketView:
    class TestGET:
        def setup_method(self):
            self.client = Client()
            self.user = UserProfile.objects.create_user(
                username='testuser', password='password')
            Pocket.objects.create(name='TestPocket', owner=self.user, fees=0)
            Currency.objects.create(name='USD', exchange_rate=1)
            Currency.objects.create(name='EUR', exchange_rate=1.2)
            Currency.objects.create(name='PLN', exchange_rate=1)

            self.url = reverse('pocket')

        def test_get_with_pocket_name(self):
            """
            Test case to check the behavior of the view when a pocket name is set in the session.
            """
            # Test the behavior when the user is not logged in
            response = self.client.get(self.url)
            assert response.status_code == 302

            self.client.login(username='testuser', password='password')

            session = self.client.session
            session['pocket_name'] = 'TestPocket'
            session.save()

            # Test the behavior when the user is logged in
            response = self.client.get(self.url)
            assert response.status_code == 200
            assert 'asset_classes' in response.context
            assert 'currencies' in response.context
            assert 'pocket_name' in response.context
            assert 'asset_allocations' in response.context

        def teardown_method(self):
            self.client.logout()
            AssetClass.objects.all().delete()
            Currency.objects.all().delete()
            Operation.objects.all().delete()
            Pocket.objects.all().delete()
            Asset.objects.all().delete()
            AssetAllocation.objects.all().delete()
            UserProfile.objects.all().delete()

    class TestPOSTBuyOperation:
        def setup_method(self):
            self.client = Client()
            self.user = UserProfile.objects.create_user(
                username='testuser', password='password')
            Pocket.objects.create(name='TestPocket', owner=self.user, fees=0)
            Currency.objects.create(name='USD', exchange_rate=1)
            Currency.objects.create(name='EUR', exchange_rate=1.2)
            Currency.objects.create(name='PLN', exchange_rate=1)

            self.url = reverse('pocket')

        def test_post(self):

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'NAME'
            session.save()
            self.pocket = Pocket.objects.create(
                name='NAME', owner=self.user, fees=0)

            response = self.client.post(self.url, {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '5',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'NAME'

            })

            assert response.status_code == 200
            assert 'portfolio/pocket.html' in [
                template.name for template in response.templates]

            operation = Operation.objects.filter(ticker='AAPL').last()

            assert operation
            assert operation.owner == self.user

        def test_buy_asset_first_operation(self):
            '''
            Test case to check the behavior of the view when the asset does not exist in the database and it is the first operation for the asset
            '''
            assert Asset.objects.all().count() == 0
            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'NAME'
            session.save()
            self.pocket = Pocket.objects.create(
                name='NAME', owner=self.user, fees=0)

            response = self.client.post(self.url, {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '5',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'NAME'

            })

            asset = Asset.objects.filter(ticker='AAPL').last()
            assert asset
            assert asset.name == 'Apple Inc.'
            assert asset.currency.name == 'USD'

            pocket = Pocket.objects.get(name='NAME')
            assert pocket.fees == 5

            asset_allocation = AssetAllocation.objects.filter(
                pocket=self.pocket, asset=asset).last()
            assert asset_allocation
            assert asset_allocation.quantity == 10
            assert asset_allocation.average_purchase_price == 100

        def test_buy_asset_not_first_operation(self):
            # CONSTANTS
            buy_data1 = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'NAME'
            }

            buy_data2 = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '40',
                'price': '150',
                'fee': '9',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'NAME'
            }

            assert Asset.objects.all().count() == 0

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'NAME'
            session.save()
            self.pocket = Pocket.objects.create(
                name='NAME', owner=self.user, fees=0)

            self.client.post(self.url, buy_data1)

            self.client.post(self.url, buy_data2)

            pocket = Pocket.objects.get(name='NAME')
            assert pocket.fees == float(
                buy_data1["fee"]) + float(buy_data2["fee"])

            asset = Asset.objects.filter(ticker='AAPL').last()
            asset_allocation = AssetAllocation.objects.filter(
                pocket=self.pocket, asset=asset).last()

            assert asset_allocation.quantity == float(
                buy_data1["quantity"]) + float(buy_data2["quantity"])
            assert asset_allocation.average_purchase_price == (float(buy_data1["quantity"])*float(buy_data1["price"]) + float(
                buy_data2["quantity"])*float(buy_data2["price"]))/(float(buy_data1["quantity"])+float(buy_data2["quantity"]))

        def test_update_data_method(self):
            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'NAME'
            session.save()
            self.pocket = Pocket.objects.create(
                name='NAME', owner=self.user, fees=0)

            # Create 5 operations by drawing without replacement
            transactionFactory = TransactionFactory(
                self.user, session['pocket_name'])
            verification_dict = {}
            for _ in range(5):
                draw_data, verification_data = transactionFactory.draw()
                verification_dict[draw_data['ticker']] = verification_data
                self.client.post(self.url, draw_data)

            for asset_allocation in AssetAllocation.objects.all():
                if asset_allocation == None:
                    break

                ticker = asset_allocation.asset.ticker
                assert asset_allocation.quantity == verification_dict[ticker]['quantity']
                assert asset_allocation.average_purchase_price == verification_dict[
                    ticker]['price']

            total_participation = AssetAllocation.objects.aggregate(
                Sum('participation'))
            assert total_participation['participation__sum'] == pytest.approx(
                100, abs=1)

        def teardown_method(self):
            self.client.logout()
            AssetClass.objects.all().delete()
            Currency.objects.all().delete()
            Operation.objects.all().delete()
            Pocket.objects.all().delete()
            Asset.objects.all().delete()
            AssetAllocation.objects.all().delete()
            UserProfile.objects.all().delete()

    class TestPOSTSellOperation:
        def setup_method(self):
            self.client = Client()
            self.user = UserProfile.objects.create_user(
                username='testuser', password='password')
            Pocket.objects.create(name='TestPocket', owner=self.user)
            Currency.objects.create(name='USD', exchange_rate=1)
            Currency.objects.create(name='EUR', exchange_rate=1.2)
            Currency.objects.create(name='PLN', exchange_rate=1)

            self.url = reverse('pocket')

        def teardown_method(self):
            self.client.logout()
            AssetClass.objects.all().delete()
            Currency.objects.all().delete()
            Operation.objects.all().delete()
            Pocket.objects.all().delete()
            Asset.objects.all().delete()
            AssetAllocation.objects.all().delete()
            UserProfile.objects.all().delete()

        def test_sell_not_all_asset(self):
            # CONSTANTS
            buy_data = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': 10,
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }
            sell_data = {
                'operation': 'sell',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': 9,
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'TestPocket'
            session.save()

            self.client.post(self.url, buy_data)
            self.client.post(self.url, sell_data)

            pocket = Pocket.objects.get(name='TestPocket', owner=self.user)
            asset = Asset.objects.filter(ticker='AAPL').last()
            asset_allocation = AssetAllocation.objects.filter(
                pocket=pocket, asset=asset).last()

            assert asset_allocation.quantity == float(
                buy_data["quantity"])-float(sell_data["quantity"])

            # Check calculations
            assert pocket.fees == float(
                buy_data["fee"]) + float(sell_data["fee"])

        def test_sell_all_asset(self):
            # CONSTANTS
            buy_data = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': 10,
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }
            sell_data = {
                'operation': 'sell',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': 10,
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'TestPocket'
            session.save()

            self.client.post(self.url, buy_data)
            self.client.post(self.url, sell_data)

            pocket = Pocket.objects.get(name='TestPocket', owner=self.user)
            asset = Asset.objects.filter(ticker='AAPL').last()
            assert AssetAllocation.objects.filter(
                pocket=pocket, asset=asset).exists() == False

            # Check calculations
            assert pocket.fees == float(
                buy_data["fee"]) + float(sell_data["fee"])


@pytest.mark.django_db
class TestPocketHistoryView:
    class TestPOSTDelete:
        def setup_method(self):
            self.client = Client()
            self.user = UserProfile.objects.create_user(
                username='testuser', password='password')
            Pocket.objects.create(name='TestPocket', owner=self.user)
            Currency.objects.create(name='USD', exchange_rate=1)
            Currency.objects.create(name='EUR', exchange_rate=1.2)
            Currency.objects.create(name='PLN', exchange_rate=1)

            self.url = reverse('pocket_history')

        def teardown_method(self):
            self.client.logout()
            AssetClass.objects.all().delete()
            Currency.objects.all().delete()
            Operation.objects.all().delete()
            Pocket.objects.all().delete()
            Asset.objects.all().delete()
            AssetAllocation.objects.all().delete()
            UserProfile.objects.all().delete()

        def test_delete_first_buy_operation(self):
            # CONSTANTS
            buy_data = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'TestPocket'
            session.save()

            # Create a buy operation
            self.client.post(reverse('pocket'), buy_data)
            assert Asset.objects.filter(ticker=buy_data['ticker']).exists()

            operation = Operation.objects.filter(
                ticker=buy_data['ticker']).last()

            # Delete the operation
            response = self.client.post(
                self.url, {'operation_id': operation.id})
            assert response.status_code == 200

            assert not Asset.objects.filter(ticker=buy_data['ticker']).exists()
            assert not Operation.objects.filter(
                ticker=buy_data['ticker']).exists()

        def test_delete_not_first_buy_operation(self):
            # CONSTANTS
            buy_data = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'TestPocket'
            session.save()

            # Create a buy operation
            self.client.post(reverse('pocket'), buy_data)
            self.client.post(reverse('pocket'), buy_data)
            self.client.post(reverse('pocket'), buy_data)

            operation = Operation.objects.filter(
                ticker=buy_data['ticker']).last()

            # Delete the operation
            self.client.post(self.url, {'operation_id': operation.id})

            pocket = Pocket.objects.get(name='TestPocket', owner=self.user)
            asset = Asset.objects.filter(ticker=buy_data['ticker']).last()
            asset_allocation = AssetAllocation.objects.filter(
                pocket=pocket, asset=asset).last()

            assert asset_allocation.quantity == 20

        def test_delete_first_sell_operation(self):
            # CONSTANTS
            buy_data = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            sell_data = {
                'operation': 'sell',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'TestPocket'
            session.save()

            # Create a buy operation
            self.client.post(reverse('pocket'), buy_data)
            assert Asset.objects.filter(ticker=buy_data['ticker']).exists()

            # Create a sell operation
            self.client.post(reverse('pocket'), sell_data)
            assert not Asset.objects.filter(ticker=buy_data['ticker']).exists()

            operation_id = Operation.objects.filter(
                ticker=buy_data['ticker']).last().id

            # Delete the operation
            response = self.client.post(
                self.url, {'operation_id': operation_id})
            assert response.status_code == 200

            assert Asset.objects.filter(ticker=buy_data['ticker']).exists()
            assert not Operation.objects.filter(id=operation_id).exists()

        def test_delete_not_first_sell_operation(self):
            # CONSTANTS
            buy_data = {
                'operation': 'buy',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            sell_data = {
                'operation': 'sell',
                'ticker': 'AAPL',
                'date': '2022-01-01',
                'currency': 'USD',
                'quantity': '10',
                'price': '100',
                'fee': '3',
                'comment': 'Test comment',
                'asset_class': 'Equity',
                'owner': self.user,
                'pocket_name': 'TestPocket'
            }

            self.client.login(username='testuser', password='password')
            session = self.client.session
            session['pocket_name'] = 'TestPocket'
            session.save()

            # Create a buy operation
            self.client.post(reverse('pocket'), buy_data)
            self.client.post(reverse('pocket'), buy_data)
            self.client.post(reverse('pocket'), buy_data)

            # Create a sell operation
            self.client.post(reverse('pocket'), sell_data)
            self.client.post(reverse('pocket'), sell_data)
            self.client.post(reverse('pocket'), sell_data)

            operation_id = Operation.objects.filter(
                ticker=buy_data['ticker']).last().id

            # Delete the operation
            self.client.post(self.url, {'operation_id': operation_id})

            pocket = Pocket.objects.get(name='TestPocket', owner=self.user)
            asset = Asset.objects.filter(ticker=buy_data['ticker']).last()
            asset_allocation = AssetAllocation.objects.filter(
                pocket=pocket, asset=asset).last()
            
            assert Asset.objects.filter(ticker=buy_data['ticker']).exists()
            assert asset_allocation.quantity == 10
