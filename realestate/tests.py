from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Estate, ForSaleEstate, OnAuctionEstate, Bid


class RealEstateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.estate = Estate.objects.create(
            type='apartment',
            name='Test Estate',
            address='123 Test St',
            description='A test estate',
            rooms=5,
            bedrooms=3,
            bathrooms=2,
            size=120,
            architectural_style='contemporary'
        )
        self.for_sale_estate = ForSaleEstate.objects.create(
            user=self.user,
            estate=self.estate,
            price=100000
        )
        self.on_auction_estate = OnAuctionEstate.objects.create(
            user=self.user,
            estate=self.estate,
            starting_price=50000,
            asking_price=60000,
            end_date='2024-12-31'
        )

    def test_user_creation(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_property_creation(self):
        for_sale_count = ForSaleEstate.objects.count()
        on_auction_count = OnAuctionEstate.objects.count()
        self.assertEqual(for_sale_count, 1)
        self.assertEqual(on_auction_count, 1)

    def test_place_bid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('place_bid'), {
            'user_id': self.user.id,
            'estate_id': self.on_auction_estate.id,
            'bidding_sum': 60000
        })
        self.assertEqual(response.status_code, 302)
        bid_count = Bid.objects.count()
        self.assertEqual(bid_count, 1)

    def test_book_estate(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('book_estate'), {
            'user_id': self.user.id,
            'estate_id': self.for_sale_estate.id
        })
        self.assertEqual(response.status_code, 302)
        self.for_sale_estate.refresh_from_db()
        self.assertEqual(self.for_sale_estate.user, self.user)

    def test_view_property_details(self):
        response = self.client.get(reverse('estate_detail', args=[self.for_sale_estate.estate.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Estate')