from django.urls import path
from . import views
from .views import HomeView, ItemDetailView, OrderSummaryView, CheckoutView

app_name = 'core'

urlpatterns = [
    path('items-list', views.items_list, name='items-list'),
    path('', HomeView.as_view(), name='home'),
    path('order-summary', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
]