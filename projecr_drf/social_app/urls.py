from django.urls import path
from .views import UpdateProfileView, UserDetailAPI, GetRequestsReceived, GetFriendList, GetRequestsSent, SendFriendRequest,  AcceptFriendRequest, SearchByKeyword


urlpatterns = [
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path("get-details",UserDetailAPI.as_view()),
    path('get-friend-requests',GetRequestsReceived.as_view()),
    path('get-friend-list',GetFriendList.as_view()),
    path('get-sent-list',GetRequestsSent.as_view()),
    path('send-friend-requests',SendFriendRequest.as_view()),
    path('accept-friend-requests',AcceptFriendRequest.as_view()),
    path('search',SearchByKeyword.as_view()),
]