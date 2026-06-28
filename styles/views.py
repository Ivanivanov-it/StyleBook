from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Style, Favourite
from .serializers import (
    StyleSerializer,
    StyleCreateSerializer,
    StyleListSerializer,
)

class StyleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Style.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create':
            return StyleCreateSerializer
        if self.action == 'list':
            return StyleListSerializer

        return StyleSerializer

    def retrieve(self,request,*args,**kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self,request,pk=None):
        style = self.get_object()
        user = request.user

        if user in style.likes.all():
            style.likes.remove(user)
            return Response({"liked": False})

        style.likes.add(user)
        return Response({"liked": True})

    @action(detail=True, methods=['post'])
    def favorite(self,request,pk=None):
        style = self.get_object()
        user = request.user

        fav,created = Favourite.objects.get_or_create(user=user,style=style)

        if not created:
            fav.delete()
            return Response({"favorited": False})

        return Response({"favorited": False})

    @action(detail=True, methods=['post'])
    def download(self,request,pk=None):
        style = self.get_object()
        style.downloads += 1
        style.save(update_fields=['downloads'])

        return Response({"downloads": style.downloads})


