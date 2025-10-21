from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD for users.
    """

    queryset = User.objects.all().order_by("name")
    serializer_class = UserSerializer
