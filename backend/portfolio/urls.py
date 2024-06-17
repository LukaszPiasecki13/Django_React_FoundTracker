from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.MainDashboardView.as_view(), name='main_dashboard'),
    path('pocket/', views.PocketView.as_view(), name='pocket'),
    path('pocket/pocket_history/', views.PocketHistoryView.as_view(), name='pocket_history'),

]
