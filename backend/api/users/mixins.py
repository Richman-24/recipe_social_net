from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class PatchModelMixin():
    """Миксин для PATCH"""

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CreateListRetrievePatchViewSet(CreateModelMixin,
                                     DestroyModelMixin,
                                     ListModelMixin,
                                     PatchModelMixin,
                                     RetrieveModelMixin,
                                     GenericViewSet):
    """Кастомный миксин."""