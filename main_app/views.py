from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Dino, Feeding, PeopleToEat
from .serializers import DinoSerializer, FeedingSerializer, PeopleToEatSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the dino-collector api home route!'}
    return Response(content)


class DinoList(generics.ListCreateAPIView):
    serializer_class = DinoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Dino.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class DinoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DinoSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user = self.request.user
        return Dino.objects.filter(user=user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
    
        people_not_associated = PeopleToEat.objects.exclude(id__in=instance.people.all())
        people_serializer = PeopleToEatSerializer(people_not_associated, many=True)
        return Response({
            'dino': serializer.data,
            'people_not_associated': people_serializer.data
        })
        
    def perform_update(self, serializer):
        dino = self.get_object()
        if dino.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this dino")
        serializer.save()
        
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this dino")
        instance.delete()
    

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


class PeopleToEatListCreate(generics.ListCreateAPIView):
  queryset = PeopleToEat.objects.all()
  serializer_class = PeopleToEatSerializer
  

class PeopleToEatDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = PeopleToEat.objects.all()
  serializer_class = PeopleToEatSerializer
  lookup_field = 'id'
  
  
class AddPersonToDino(APIView):
  def post(self, request, dino_id, person_id):
    dino = Dino.objects.get(id=dino_id)
    person = PeopleToEat.objects.get(id=person_id)
    dino.people.add(person)
    return Response({'message': 'Person added to dino'})


class RemovePersonFromDino(APIView):
  def post(self, request, dino_id, person_id):
    dino = Dino.objects.get(id=dino_id)
    person = PeopleToEat.objects.get(id=person_id)
    dino.people.remove(person)
    return Response({'message': 'Person removed from dino'})


# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })


# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })