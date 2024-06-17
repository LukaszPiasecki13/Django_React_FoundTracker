from django.contrib import admin
from .models import Operation, AssetClass, Currency, Pocket, Asset, AssetAllocation
# Register your models here.




admin.site.register(Operation)
admin.site.register(AssetClass)
admin.site.register(Currency)
admin.site.register(Pocket)
admin.site.register(Asset)
admin.site.register(AssetAllocation)

