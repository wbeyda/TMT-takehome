from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import Inventory, InventoryType, InventoryLanguage
from .schemas import InventoryMetaData

class InventoryCreatedAfterDateAPIViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Type1")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        
        metadata = InventoryMetaData(
            year=2024,
            actors=['Actor1', 'Actor2'],
            imdb_rating=float(8.5),
            rotten_tomatoes_rating=int(90)
        ).dict()

        self.inventory1 = Inventory.objects.create(
            name="Inventory1",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata=metadata,
            created_at=datetime.now() - timedelta(days=2)
        )
        self.inventory2 = Inventory.objects.create(
            name="Inventory2",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata=metadata,
            created_at=datetime.now()
        )
        self.url = reverse('inventory-created-after-date')

    def test_list_inventory_created_after_date(self):
        response = self.client.get(self.url, {'date': '2024-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Inventory1')
        self.assertEqual(response.data[1]['name'], 'Inventory2')

    def test_list_inventory_invalid_date_format(self):
        response = self.client.get(self.url, {'date': 'invalid-date'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid date format or no records found.')

    def test_list_inventory_no_records_found(self):
        response = self.client.get(self.url, {'date': '2025-01-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid date format or no records found.')
    
