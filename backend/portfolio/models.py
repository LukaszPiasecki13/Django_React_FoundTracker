from django.db import models
from authentication.models import UserProfile

# Create your models here.


class Operation(models.Model):
    id = models.AutoField(primary_key=True)
    operation_type = models.CharField(max_length=20) # buy, sell
    asset_class = models.CharField()
    ticker = models.CharField(max_length=20)
    date = models.DateField()
    currency = models.CharField(max_length=3)
    quantity = models.FloatField()
    price = models.FloatField()
    fee = models.FloatField()
    comment = models.TextField()
    owner = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    pocket_name = models.CharField(max_length=100)
    

    def __str__(self):
        return ("{}_{}".format(self.id, self.operation_type))


class AssetClass(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Asset classes"

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=3, default=1.0) # exchange rate to base currency

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name


class Asset(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    asset_class = models.CharField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=8, decimal_places=3, default=0.0)

    def __str__(self):
        return self.name


class Pocket(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    assets = models.ManyToManyField('Asset', through='AssetAllocation')
    fees = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


class AssetAllocation(models.Model):
    pocket = models.ForeignKey(Pocket, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=3, default=0.0)
    average_purchase_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    daily_change_percent = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    daily_change_XXX = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    participation = models.DecimalField(max_digits=8, decimal_places=1, default=0.0)
    rate_of_return = models.DecimalField(max_digits=8, decimal_places=1, default=0.0)
    rate_of_return_XXX = models.DecimalField(max_digits=8, decimal_places=1, default=0.0)
    profit_XXX = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    dividends = models.DecimalField(max_digits=8, decimal_places=1, default=0.0)

    def __str__(self):
        return self.pocket.name + "_" + self.asset.name
