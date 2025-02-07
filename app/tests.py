from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import Item

class ItemTests(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()
        self.item = Item.objects.create(name="Test Item", description="Test Description")

    def test_item_create_view(self):
        """Test creating a new item via POST request."""
        response = self.client.post(reverse('item_create'), {
        'name': 'New Item',  # Provide required field
        'description': 'New Description'
    }, follow=True)  # 🔥 FOLLOW REDIRECTS

    # Check if response.context exists before accessing it
        form_errors = response.context['form'].errors if response.context and 'form' in response.context else "No form errors"
    
        print("Form errors:", form_errors)  # Debugging
        print("Response status:", response.status_code)  # Debugging

        self.assertEqual(response.status_code, 200)  # Ensure we landed on the correct page
        self.assertTrue(Item.objects.filter(name="New Item").exists())  # Check item was created


    def test_item_create_view(self):
    
        response = self.client.post(reverse('item_create'), {
        'name': 'New Item',  # Providing a valid name
        'description': 'New Description'
    })
    
        print("Form errors:", response.context['form'].errors)  # Debug form errors
        print("Response status:", response.status_code)  # Debug response status

        self.assertEqual(response.status_code, 302)  # Expected redirect
        self.assertTrue(Item.objects.filter(name="New Item").exists())  # Check if item was created


    def test_item_update_view(self):
        """Test updating an item."""
        response = self.client.post(reverse('item_update', args=[self.item.id]), {
        'name': 'Updated Item',
        'description': 'Updated Description'
    }, follow=True)  # <-- Follow redirects

        self.item.refresh_from_db()
        print("Response status:", response.status_code)  

        self.assertEqual(response.status_code, 200)  # Now checking the correct expected status
        self.assertEqual(self.item.name, 'Updated Item')


    def test_item_delete_view(self):
        """Test deleting an item."""
        response = self.client.post(reverse('item_delete', args=[self.item.id]), follow=True)  # <-- Follow redirects

        print("Response status:", response.status_code)  
        self.assertEqual(response.status_code, 200)  # Expected redirect is now handled
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())  # Ensure item is deleted
