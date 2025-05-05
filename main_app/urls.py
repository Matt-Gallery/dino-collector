from django.urls import path
from .views import Home, DinoList, DinoDetail, FeedingListCreate, FeedingDetail


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('dinos/', DinoList.as_view(), name='dino_list'),
  path('dinos/<int:id>/', DinoDetail.as_view(), name='dino_detail'),
  path('dinos/<int:dino_id>/feedings/', FeedingListCreate.as_view(), name='feeding-list-create'),
  path('dinos/<int:dino_id>/feedings/<int:id>/', FeedingDetail.as_view(), name='feeding-detail'),
]
