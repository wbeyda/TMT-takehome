from datetime import datetime, timedelta

from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderListByDateRangeView(generics.ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        start_date_str = self.request.query_params.get('start_date', None)
        embargo_date_str = self.request.query_params.get('embargo_date', None)
        
        if not start_date_str or not embargo_date_str:
            return Order.objects.none()
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            embargo_date = datetime.strptime(embargo_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Order.objects.none()
        
        queryset = Order.objects.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
        return queryset