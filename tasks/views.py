from rest_framework import viewsets, filters
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.response import Response

from tasks.constants import DONE, IN_PROGRESS, PENDING


from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD for tasks
    Supports:
        - fetch all tasks for a user with ?user_id=<uuid>
        - filter by ?status=<status>
        - ordering by due_date via ?ordering=due_date or ?ordering=-due_date
        - pagination via ?limit=&offset=
        - Does not overwrite existing task with the same passed `idempotency_key`
    """

    queryset = Task.objects.all().order_by("due_date")
    serializer_class = TaskSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["due_date"]

    def get_queryset(self):
        """
        Modify the queryset used to fulfill the GET requests to include proper filters and pagination
        """
        task_queryset = super().get_queryset()

        # filter by user id if present
        user_id = self.request.query_params.get("user_id")
        if user_id:
            task_queryset = task_queryset.filter(user__id=user_id)

        # filter by status if present
        status_param = self.request.query_params.get("status")
        if status_param:
            task_queryset = task_queryset.filter(status=status_param)
        return task_queryset

    def create(self, request, *args, **kwargs):
        idempotency_key = request.data.get("idempotency_key")
        if idempotency_key:
            existing = Task.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                serializer = self.get_serializer(existing)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)


class TasksSummaryView(APIView):
    """
    Returns counts of tasks per status.
    Response shape:
    {
      "pending": 10,
      "in_progress": 2,
      "done": 5
    }
    """

    def get(self, request):
        counts = Task.objects.values("status").annotate(count=Count("id"))
        result = {
            PENDING: 0,
            IN_PROGRESS: 0,
            DONE: 0,
        }
        for row in counts:
            result[row["status"]] = row["count"]
        return Response(result)
