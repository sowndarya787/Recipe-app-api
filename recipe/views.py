from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers
from rest_framework import mixins, viewsets

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retrieve recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        return serializers.RecipeSerializer  # for create, update, etc.

    
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

class TagViewSet(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retrieve tags for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
        