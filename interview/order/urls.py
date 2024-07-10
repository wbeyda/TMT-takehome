
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderListByDateRangeView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('by-date/', OrderListByDateRangeView.as_view(), name='order-list-by-date-range'),
]