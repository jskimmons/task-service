from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User  # adjust if your app name differs
import uuid


class UserAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            name="User One", email="user1@example.com", phone_number="1234567890"
        )
        self.existing_user_url = reverse("user-detail", args=[self.user.id])
        self.user_list_url = reverse("user-list")

    def test_create_user(self):
        """
        POST a new user
        """
        data = {
            "name": "User Two",
            "email": "user2@example.com",
            "phone_number": "5551234567",
        }
        response = self.client.post(self.user_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(response.data["phone_number"], data["phone_number"])
        self.assertTrue(User.objects.filter(email="user2@example.com").exists())

    def test_update_existing_user(self):
        """
        UPDATE or PATCH for an existing user
        """
        data = {"name": "User Updated"}
        response = self.client.patch(self.existing_user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": str(self.user.id),
                "name": "User Updated",
                "email": "user1@example.com",
                "phone_number": "1234567890",
            },
        )

    def test_update_non_existing_user(self):
        """
        UPDATE or PATCH for a non-existing user
        """
        non_existing_id = uuid.uuid4()
        url = reverse("user-detail", args=[non_existing_id])
        data = {"name": "Does Not Exist"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_user(self):
        """
        DELETE an existing user
        """
        response = self.client.delete(self.existing_user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_non_existing_user(self):
        """
        DELETE a user that doesn't exist should return 404
        """
        non_existing_id = uuid.uuid4()
        url = reverse("user-detail", args=[non_existing_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_existing_user(self):
        """
        GET an existing user
        """
        response = self.client.get(self.existing_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_get_non_existing_user(self):
        """
        GET for a user that doesn't exist should return a 404
        """
        non_existing_id = uuid.uuid4()
        url = reverse("user-detail", args=[non_existing_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
