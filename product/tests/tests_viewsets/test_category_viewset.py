import json
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.urls import reverse

from product.models.product import Product
from product.tests.factories import CategoryFactory, ProductFactory
from order.tests.factories import UserFactory


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(title="Pro Controller", price=200.00)

    def test_get_all_products(self):
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Unexpected status code returned.",
        )

        product_data = json.loads(response.content)["results"][0]

        self.assertEqual(product_data["title"], self.product.title)
        self.assertEqual(product_data["price"], self.product.price)
        self.assertEqual(product_data["active"], self.product.active)

    def test_create_product(self):
        category = CategoryFactory()
        data = json.dumps(
            {"title": "Notebook", "price": 900.00, "categories_id": [category.id]}
        )

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Unexpected status code returned.",
        )

        created_product = Product.objects.get(title="Notebook")
        self.assertEqual(created_product.title, "Notebook")
        self.assertEqual(created_product.price, 900.00)
