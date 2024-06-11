from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User 
import re

from .serializers import ProfileSerializer, UserSerializer, UserRequest, UserFriendList, UserSent

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        profile.email = request.data.get('email')
        profile.save()
        return Response({"status": "profile updated"})
    
class SendFriendRequest(APIView):
    """
    Add email of acceptor's in sender's sent_list
    Add email of sender's email in acceptor's received list
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        sent_to = request.data.get('send_to')
        profile = Profile.objects.get(user=user)
        profile_sent = Profile.objects.get(user=sent_to)

        if profile.email not in profile_sent.request_received.split(";") and profile_sent.email not in profile.request_sent.split(";"):
            profile.request_sent = profile.request_sent + ";" + profile_sent.email
            profile_sent.request_received = profile_sent.request_received + ";" + profile.email
            profile_sent.save()
            profile.save()
            return Response({"status": "Request Sent"})
        
        else:
            print(profile.request_sent)
            print(profile_sent.request_received)
            return Response({"status": "Already Sent"})

    
class AcceptFriendRequest(APIView):
    """
    Remove from acceptor pending freind requst list
    Remove from sender's sent friend requst list
    Add sender's email in acceptor's freind list
    Add acceptor's email in sender's freind list
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        accept_id = request.data.get('accept_id')
        accept_profile = Profile.objects.get(user=accept_id)
        profile = Profile.objects.get(user=user)

        updated_profile_req_rec = profile.request_received.split(";")
        updated_accept_profile_sent_req = accept_profile.request_sent.split(";")

        if profile.email in updated_accept_profile_sent_req or accept_profile.email in updated_profile_req_rec:

            profile.friend_list = profile.friend_list + ";" + accept_profile.email
            accept_profile.friend_list = accept_profile.friend_list + ";" + profile.email

            updated_profile_req_rec.remove(accept_profile.email)
            updated_accept_profile_sent_req.remove(profile.email)
            profile.request_received = ";".join(updated_profile_req_rec)
            accept_profile.request_sent = ";".join(updated_accept_profile_sent_req)
            accept_profile.save()
            profile.save()

            print(profile.request_received)
            print(accept_profile.request_sent)
            return Response({f"status": "Request Accepted"})
        else:
            return Response({f"status": "User Request Doesn't exist, please check your friend request list"})


class UserDetailAPI(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self,request,*args,**kwargs):
    userlist = User.objects.values('username','id')
    serializer = UserSerializer(userlist)
    return Response(serializer.data)

class GetRequestsReceived(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        user = request.user
        requestList = Profile.objects.get(user=user)
        serializer = UserRequest(requestList)
        return Response(serializer.data)
    
class GetRequestsSent(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        user = request.user
        requestList = Profile.objects.get(user=user)
        serializer = UserSent(requestList)
        return Response(serializer.data)

class GetFriendList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        user = request.user
        requestList = Profile.objects.get(user=user)
        serializer = UserFriendList(requestList)
        return Response(serializer.data)
    
def is_valid_email(email):
    # Regular expression for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # If the string matches the regex, it is a valid email
    if re.match(regex, email):
        return True
    else:
        return False
    
class SearchByKeyword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        keyword = (request.data.get('keyword'))
        userlist = User.objects.values('username','id')
        temp_dict = {}
        for i in userlist:
            profileList = Profile.objects.get(user=i['id'])
            temp_dict.update({profileList.email:{'id':i['id'],'username':i['username']}})
        if is_valid_email(keyword):
            return Response(temp_dict.get(keyword,"Not Found"))
        else:
            matched = []
            for i in userlist:
                if keyword.lower() in i['username'].lower():
                    matched.append(i)
            return Response(matched)