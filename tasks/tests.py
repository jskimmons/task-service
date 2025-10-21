import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.constants import IN_PROGRESS, PENDING, DONE
from .models import Task, User  # Adjust import if needed


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid.uuid4(),
            name="John Doe",
            email="john@example.com",
            phone_number="555-5555",
        )
        self.task = Task.objects.create(
            title="Initial Task",
            status=PENDING,
            due_date="2025-12-31T23:59:00Z",
            user=self.user,
        )

        self.list_url = reverse("task-list")  # from DefaultRouter
        self.detail_url = reverse("task-detail", args=[self.task.id])
        self.summary_url = reverse("tasks_summary")

    def test_create_task(self):
        """
        POST a new task
        """
        data = {
            "title": "New Task",
            "status": PENDING,
            "due_date": "2025-10-31T10:00:00Z",
            "user_id": str(self.user.id),
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")
        self.assertEqual(response.data["status"], PENDING)
        self.assertEqual(response.data["due_date"], "2025-10-31T10:00:00Z")
        self.assertEqual(response.data["user_id"], self.user.id)

    def test_update_existing_task(self):
        """
        UPDATE or PATCH an existing task
        """
        data = {"title": "Updated Task", "status": IN_PROGRESS}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.status, IN_PROGRESS)

    def test_update_non_existing_task(self):
        """
        UPDATE or PATCH a non-existing task
        """
        fake_id = uuid.uuid4()
        url = reverse("task-detail", args=[fake_id])
        data = {"title": "Does Not Exist"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_task(self):
        """
        DELETE an existing task
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_non_existing_task(self):
        """
        DELETE for a non existing task returns a 404
        """
        fake_id = uuid.uuid4()
        url = reverse("task-detail", args=[fake_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_existing_task(self):
        """
        GET for an existing task
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_get_non_existing_task(self):
        """
        GET for a non existing task returns a 404
        """
        fake_id = uuid.uuid4()
        url = reverse("task-detail", args=[fake_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_tasks_filtered_and_ordered(self):
        """
        Test the filtering and pagination of the task list response
        """
        Task.objects.create(
            title="Task 2",
            status="done",
            due_date="2025-11-01T00:00:00Z",
            user=self.user,
        )
        response = self.client.get(
            f"{self.list_url}?status=pending&ordering=due_date&limit=1&offset=0"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_idempotency_key_returns_existing_task(self):
        """
        Test an existing task cannot be overwritten by a new POST request with the same `idempotency_key`
        """
        key = "abc123"
        data = {
            "title": "First Task",
            "status": PENDING,
            "due_date": "2025-10-31T10:00:00Z",
            "user_id": str(self.user.id),
            "idempotency_key": key,
        }

        response1 = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        task_id = response1.data["id"]

        # Second request with same idempotency_key should return same task
        new_data = {
            "title": "Overwrite Task",
            "status": PENDING,
            "due_date": "2025-10-31T10:00:00Z",
            "user_id": str(self.user.id),
            "idempotency_key": key,
        }
        response2 = self.client.post(self.list_url, new_data, format="json")

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["id"], task_id)
        self.assertEqual(response2.data["title"], "First Task")
        self.assertEqual(Task.objects.filter(idempotency_key=key).count(), 1)


class TaskSummaryViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            id=uuid.uuid4(),
            name="John Doe",
            email="john@example.com",
            phone_number="555-5555",
        )
        Task.objects.create(
            title="Initial Task",
            status=PENDING,
            due_date="2025-12-31T23:59:00Z",
            user=self.user,
        )

        Task.objects.create(
            title="Initial Task",
            status=IN_PROGRESS,
            due_date="2025-12-31T23:59:00Z",
            user=self.user,
        )

        Task.objects.create(
            title="Initial Task",
            status=DONE,
            due_date="2025-12-31T23:59:00Z",
            user=self.user,
        )
        self.summary_url = reverse("tasks_summary")

    def test_summary_endpoint(self):
        """
        Test the summary endpoint returns the correct shape and counts
        """
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual({"pending": 1, "in_progress": 1, "done": 1}, response.data)
