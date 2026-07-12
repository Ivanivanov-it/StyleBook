from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Style, Favourite
from .serializers import (
    StyleSerializer,
    StyleCreateSerializer,
    StyleListSerializer,
    StyleDetailSerializer,
)

class StyleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Style.objects.all().order_by('-id')

    def get_queryset(self):
        queryset = super().get_queryset()
        game_class = self.request.query_params.get("class")

        if game_class:
            queryset = queryset.filter(game_class=game_class)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return StyleCreateSerializer
        if self.action == 'list':
            return StyleListSerializer
        if self.action == 'retrieve':
            return StyleDetailSerializer

        return StyleSerializer

    def retrieve(self,request,*args,**kwargs):
        instance = self.get_object()
        if request.user != instance.user:
            instance.views += 1
            instance.save(update_fields=['views'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only edit your own styles.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own styles.")
        instance.delete()

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mine(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = StyleListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def classes(self, request):
        classes = [
            {"value": value, "label": label}
            for value, label in Style._meta.get_field("game_class").choices
        ]
        return Response(classes)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self,request,pk=None):
        style = self.get_object()
        user = request.user

        if style.likes.filter(pk=user.pk).exists():
            style.likes.remove(user)
            return Response({"liked": False, "likes": style.likes.count()})

        style.likes.add(user)
        return Response({"liked": True, "likes": style.likes.count()})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self,request,pk=None):
        style = self.get_object()
        user = request.user

        fav,created = Favourite.objects.get_or_create(user=user,style=style)

        if not created:
            fav.delete()
            return Response({"favorited": False, "favorites": style.favourite_set.count()})

        return Response({"favorited": True, "favorites": style.favourite_set.count()})

    @action(detail=True, methods=['post'])
    def download(self,request,pk=None):
        style = self.get_object()
        style.downloads += 1
        style.save(update_fields=['downloads'])

        return Response({"downloads": style.downloads})


