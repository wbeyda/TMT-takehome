from datetime import datetime, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order, Inventory
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from interview.inventory.schemas import InventoryMetaData
from django.urls import reverse

class DeactivateOrderViewTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Type1")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        
        metadata_dict = InventoryMetaData(
            year=2024,
            actors=['Actor1', 'Actor2'],
            imdb_rating=float(8.5),
            rotten_tomatoes_rating=int(90)
        ).dict()

        self.inventory1 = Inventory.objects.create(
            name="Inventory1",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata=metadata_dict,
            created_at=datetime.now() - timedelta(days=2)
        )
        self.inventory2 = Inventory.objects.create(
            name="Inventory2",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata=metadata_dict,
            created_at=datetime.now()
        )
        self.order = Order.objects.create(
            inventory=self.inventory1,
            start_date='2024-07-20',
            embargo_date='2024-07-25',
        )
        
        self.url = reverse('deactivate-order', kwargs={'pk': self.order.pk})
    
    def test_deactivate_order(self):
        response = self.client.put(self.url, {'is_active': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertFalse(updated_order.is_active)
    
    def test_deactivate_order_invalid_payload(self):
        response = self.client.delete(self.url, {}, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_405_METHOD_NOT_ALLOWED])
        
        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertTrue(updated_order.is_active)

    def test_deactivate_order_not_found(self):
        response = self.client.put(reverse('deactivate-order', kwargs={'pk': 999}), {'is_active': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)