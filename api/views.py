from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import views,viewsets,status
from .serializers import (UsersLoginSerializer,
                          UsersRegisterSerializer,
                          Uploadfile,
                          FileUploadSerializers,AdminLoginSerializer
                          ,Get_Address_Serializers)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserUploads,Address
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from .adminpermission import IsAdminPermission
import os
from django.shortcuts import get_object_or_404
User = get_user_model()

class UserHome(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        instance = UserUploads.objects.filter(user=request.user.pk)
        serializer = FileUploadSerializers(instance=instance,many=True)
        response = []
        for data in serializer.data:

            data['filename'] = os.path.basename(data['file'])
            data['file'] = "http://localhost:8000"+ str(data['file'])
            response.append(data)

        return Response(response,status=status.HTTP_200_OK)


class FileUpload_View(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    CATEGORY_EXTENSIONS = {
            'excel': ['xlsx', 'xls'],
            'word': ['docx', 'doc'],
            'pdf': ['pdf'],
            'text': ['txt','text'], 
        }
    def get_category_by_extension(self,extension):
        for category, extensions in self.CATEGORY_EXTENSIONS.items():
            if extension in extensions:
                return category
        return None  # Return None if no matching category is found

    def post(self, request, *args, **kwargs):
        serializer = Uploadfile(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            data['user'] = User.objects.get(pk=request.user.pk)
            data['file_type'] =self.get_category_by_extension(data['file'].name.split('.')[-1]) 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        
upload_file = FileUpload_View.as_view()


class Profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        instance = User.objects.get(pk=request.user.pk)
        response = {
            "name":instance.name,
            "phone":instance.phone_number
        }

        return Response(response,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        instance = User.objects.get(pk=request.user.pk)
        instance.name = request.data.get("name")
        instance.phone_number = request.data.get("phone")
        instance = instance.save()
        response = {
            "msg":"profile Scessful Updated"
        }
        return Response(response,status=status.HTTP_200_OK)

profile = Profile.as_view()


class User_LoginView(views.APIView):
    serializer_class = UsersLoginSerializer     
    def post(self, request, *args, **kwargs):
        serializer = UsersLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        # Create the response data
        response_data = {
            'access_token': str(access_token),
            'refresh_token': str(refresh),
             'user':{ 
                "user_id":user.pk,
                "name":user.name,
            }
        }
        return Response(response_data)

user_login_view = User_LoginView.as_view()

class User_RegisterView(views.APIView):
    serializer_class = UsersRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = UsersRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # Create the response data
            response_data = {
                'user':user.email,
                'name':user.name,
                'Msg': "User Singup successful",

            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    
    def perform_create(self, serializer):
        return serializer.save()
user_register_view = User_RegisterView.as_view()



class Admin_User_LoginView(views.APIView):
    serializer_class = AdminLoginSerializer     
    def post(self, request, *args, **kwargs):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        # Create the response data
        name = user.name
        if name == "":
            name = "Admin"
        
        response_data = {
            'access_token': str(access_token),
            'refresh_token': str(refresh),
             'user':{ 
                "user_id":user.pk,
                 "name":name,
            }
        }
        return Response(response_data)

admin_user = Admin_User_LoginView.as_view()
from django.db.models import Count
class Deshboard(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdminPermission,)
    serializer_class = UsersLoginSerializer     
    def get(self,request,*args,**kwargs):
        total_file = len(UserUploads.objects.all())
        total_users = len(User.objects.all())
        response = {
            "total_file":total_file,
            "total_user":total_users
        }
        
        
        return Response(response)

deshboard = Deshboard.as_view()


class ByUsers(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdminPermission,)
    serializer_class = UsersLoginSerializer     
    def get(self,request,*args,**kwargs):
        queryset = UserUploads.objects.all().values('user__name').annotate(file_count=Count('user')).order_by('user__name')
        return Response(queryset)

byusers = ByUsers.as_view()

class ByFiletypes(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdminPermission,)
    serializer_class = UsersLoginSerializer     
    def get(self,request,*args,**kwargs):
        queryset = UserUploads.objects.values('file_type').annotate(item_count=Count('file_type'))
        return Response(queryset)

byfiles = ByFiletypes.as_view()




class Get_Address(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication,]
    permission_classes = (IsAuthenticated,)
    serializer_class = Get_Address_Serializers
    queryset = Address.objects.all()
    
    
    def get_queryset(self):
        # Filter the queryset based on the current user
        return Address.objects.filter(user=self.request.user.pk).all()
    
    def get_object(self, pk):
        return get_object_or_404(self.queryset, pk=pk)
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset,many=True,context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        serializer = self.serializer_class(self.get_object(pk=pk),context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        serializer =self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["user"] = User.objects.get(pk=request.user.pk)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def update(self,request,pk=None):
        serializer =self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid()
        instance = self.get_object(pk=pk)
        validated_data = serializer.validated_data
        validated_data["user"] = User.objects.get(pk=request.user.pk)
        serializer.update(instance,validated_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk=pk)
        instance.delete()
        msg = {
            "message":"Address Scessfully Deleted"
        }
        return Response(msg,status=status.HTTP_204_NO_CONTENT)