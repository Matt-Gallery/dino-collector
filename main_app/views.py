from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Dino, Feeding
from .serializers import DinoSerializer, FeedingSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the dino-collector api home route!'}
    return Response(content)

class DinoList(generics.ListCreateAPIView):
    queryset = Dino.objects.all()
    serializer_class = DinoSerializer

class DinoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dino.objects.all()
    serializer_class = DinoSerializer
    lookup_field = 'id'

class FeedingListCreate(generics.ListCreateAPIView):
  serializer_class = FeedingSerializer

  def get_queryset(self):
    dino_id = self.kwargs['dino_id']
    return Feeding.objects.filter(dino_id=dino_id)

  def perform_create(self, serializer):
    dino_id = self.kwargs['dino_id']
    dino = Dino.objects.get(id=dino_id)
    serializer.save(dino=dino)
    
class FeedingDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FeedingSerializer
  lookup_field = 'id'

  def get_queryset(self):
    dino_id = self.kwargs['dino_id']
    return Feeding.objects.filter(dino_id=dino_id)