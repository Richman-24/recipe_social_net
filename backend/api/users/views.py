from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination

from api.users.serializers import UserCreateSerializer, UserListSerializer


User = get_user_model()

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif (self.request.method == 'POST'):
            return UserCreateSerializer