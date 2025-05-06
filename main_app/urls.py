from django.urls import path
from .views import (Home, 
                    DinoList, 
                    DinoDetail, 
                    FeedingListCreate, 
                    FeedingDetail, 
                    PeopleToEatListCreate, 
                    PeopleToEatDetail, 
                    AddPersonToDino, 
                    RemovePersonFromDino,
                    CreateUserView,
                    LoginView,
                    VerifyUserView
                    )


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('dinos/', DinoList.as_view(), name='dino_list'),
  path('dinos/<int:id>/', DinoDetail.as_view(), name='dino_detail'),
  path('dinos/<int:dino_id>/feedings/', FeedingListCreate.as_view(), name='feeding-list-create'),
  path('dinos/<int:dino_id>/feedings/<int:id>/', FeedingDetail.as_view(), name='feeding-detail'),
  path('dinos/<int:dino_id>/people/', PeopleToEatListCreate.as_view(), name='people-list-create'),
  path('dinos/<int:dino_id>/people/<int:person_id>/', PeopleToEatDetail.as_view(), name='people-detail'),
  path('dinos/<int:dino_id>/add_person/<int:person_id>/', AddPersonToDino.as_view(), name='dino_add_person'),
  path('dinos/<int:dino_id>/remove_person/<int:person_id>/', RemovePersonFromDino.as_view(), name='dino_remove_person'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]
