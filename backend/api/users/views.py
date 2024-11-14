from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from api.users.serializers import UserCreateSerializer, UserListSerializer, UserSerializer
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

User = get_user_model()

class CustomUserViewSet1(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif (self.request.method == 'POST'):
            return UserCreateSerializer


from api.recipes.views import CreateListRetrievePatchViewSet

class CustomUserViewSet(CreateListRetrievePatchViewSet):
    """Класс представления пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAdminPermission,)
    lookup_field = 'username'
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('username',)

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me',)
    def user_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @user_profile.mapping.patch
    def update_user_profile(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)