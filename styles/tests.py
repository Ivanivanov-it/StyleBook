from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Favourite, Style


class StyleInteractionTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username="owner", password="password123")
        self.other_user = user_model.objects.create_user(username="other", password="password123")
        self.style = Style.objects.create(
            user=self.owner,
            title="Owner style",
            description="",
            thumbnail=SimpleUploadedFile("thumb.jpg", b"file", content_type="image/jpeg"),
        )
        self.client = APIClient()
        self.client.force_authenticate(self.other_user)

    def test_different_user_can_like_style(self):
        response = self.client.post(f"/api/styles/{self.style.id}/like/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"liked": True, "likes": 1})
        self.assertTrue(self.style.likes.filter(pk=self.other_user.pk).exists())

    def test_different_user_can_favorite_style(self):
        response = self.client.post(f"/api/styles/{self.style.id}/favorite/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"favorited": True, "favorites": 1})
        self.assertTrue(Favourite.objects.filter(user=self.other_user, style=self.style).exists())
