
from django.contrib.auth.models import User  
from .models import MetaData
from django.contrib.auth import login, logout

from django.contrib.auth.hashers import make_password


from django.core.mail import send_mail 
from .serializers import userSerializers, LoginSerializer, RegistrationSerializer ,FileSerializers

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, redirect
import requests

from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view

from rest_framework import generics
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
# import the library
# Create your views here.

class metadataViewSet(
	mixins.CreateModelMixin,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):

	queryset = MetaData.objects.all()
	serializer_class = FileSerializers
	lookup_field ='uu_id'
	# permission_classes = [IsAuthenticated, ]


	def create(self, request, *args, **kwargs):
		user = self.request.user.id
		print(self.request.data)
		# print(user)
		# print(self.request.user.id)
		file =  self.request.FILES.getlist('file')
		
		file_details = self.request.POST.getlist('file_details')
		print(file)
		print(file[1])
		print(file_details)
		n=len(file)
		sdata= []
		for i in range(n):
			data={
				"user":user,
				"file":file[i],
				"file_details":file_details[i],
				

			}
			
			s1 = FileSerializers(data=data)
			
			if s1.is_valid():
				
				s1.save()
				sdata.append(s1.data)
		
		return Response(sdata,status=status.HTTP_201_CREATED)
		# return Response(s1.errors, status=status.HTTP_400_BAD_REQUEST)

	def list(self, request, *args, **kwargs):
		
		data= MetaData.objects.filter(user=request.user)
		
		s1 = FileSerializers(data,many=True)
		return Response(s1.data)

	def update(self, request, *args, **kwargs):
		user = self.request.data['user']
		file =  self.request.data['file']
		file_details = self.request.data['file_details']
		uu_id = self.kwargs.get('uu_id')

		data= MetaData.objects.filter(user=request.user)
		mdata=data.get(uu_id=uu_id)
		print(mdata)
		
		if str(mdata.uu_id)==uu_id:
			data={
			"user":user,
			"file":file,
			"file_details":file_details,
			}
			s1 = FileSerializers(mdata,data=data)
			if s1.is_valid():
				s1.save()
				return Response(s1.data,status=status.HTTP_201_CREATED)
			else:
				return Response({"msg":"ERORRRRRR"})
		else:
			return Response({"msg":"You do not have permission to update this task"})

	
	def destroy(self, request, *args, **kwargs):
		uu_id = self.kwargs.get('uu_id')
		data= MetaData.objects.filter(user=request.user)
		mdata=data.get(uu_id=uu_id)
		
		if str(mdata.uu_id)==uu_id:
			mdata.delete()
			return Response({"msg":"Done"})
		else:
			return Response({"msg":"You do not have permission to delete this task"})


	def retrive(self, request, *args, **kwargs):
		uu_id = self.kwargs.get('uu_id')

		data= MetaData.objects.filter(user=request.user)
		mdata=data.get(uu_id=uu_id)
		s1 = FileSerializers(mdata)
		return Response(s1.data)


class AuthViewSet(viewsets.GenericViewSet):

	permission_classes = [AllowAny, ]
	serializer_classes = {
	   
	}

	@action(methods=['POST', ], detail=False)
	def register(self, request):
		s1 = RegistrationSerializer(data=request.data)
		s1.is_valid(raise_exception=True)
		user = create_user_account(**s1.validated_data)
		user.save()
		data={"success":"user created successfully"}
	   
		return Response(data=data,status=status.HTTP_201_CREATED)
		
	@action(methods=['POST', ], detail=False)	
	def login(self, request):
		username = self.request.data['username']
		password = self.request.data['password']

		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			token, created = Token.objects.get_or_create(user=user)
			# request.session['user_token']=token.key
			# print(request.session['user_token'])
			# return Response({"msg":"working well so far","token":token.key})
			return Response({"token":str(token)})
			# return render(request,"home.html")
		return Response({"msg":"ERROR"})

	@action(methods=['POST', ], detail=False)
	def logout(self, request):
		print(request.META.get('HTTP_AUTHORIZATION'))
		print(request.user)
		request.user.auth_token.delete()
		logout(request)

		return Response({"message":'logout sucessfully.'},status=204)




# class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin,mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):

# 	queryset = MetaData.objects.all()
# 	serializer_class = FileSerializers
# 	lookup_field ='uu_id'


# 	def get(self,request,uu_id=None):
# 		if uu_id:
# 			return self.retrieve(request)
# 		else:
# 			return self.list(request)
		

# 	def post(self,request):
# 		return self.create(request)

# 	def put(self,request, uu_id=None):
# 		return self.update(request,uu_id)

# 	def delete(self,request, uu_id):
# 		return self.destroy(request,uu_id)
	 
	 



def home_page(request):
	
	return render(request, 'home.html')




class userAPIView(APIView):
	def get(self,request):
		users= User.objects.all()
		s1 = userSerializers(users,many=True)
		return Response(s1.data)

class UserLoginView(APIView):

	def post(self,request):
		username = self.request.data['username']
		password = self.request.data['password']

		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			token, created = Token.objects.get_or_create(user=user)
			# request.session['user_token']=token.key
			# print(request.session['user_token'])
			# return Response({"msg":"working well so far","token":token.key})
			return Response({"token":str(token)})
			# return render(request,"home.html")
		return Response({"msg":"ERROR"})

	def get(self,request):
		return render(request,"login.html")


class LogoutView(APIView):
	authentication_classes = [TokenAuthentication]

	def post(self, request):
		print(request.META.get('HTTP_AUTHORIZATION'))
		print(request.user)
		request.user.auth_token.delete()
		logout(request)

		return Response({"message":'logout sucessfully.'},status=204)

def create_user_account(username, email, password, **extra_fields):
	user = get_user_model().objects.create_user(
		email=email,
		username=username,
		password=password,
		**extra_fields
	)
	return user

class RegistrationView(APIView):
	def post(self,request):

		s1 = RegistrationSerializer(data=request.data)
		s1.is_valid(raise_exception=True)
		user = create_user_account(**s1.validated_data)
		user.save()
		data={"success":"user created successfully"}
	   
		return Response(data=data,status=status.HTTP_201_CREATED)
		
	def get(self,request):
		return render(request,"register.html")    



class FileuploadView(APIView):
	def post(self,request):
		user = self.request.data['user']
		file =  self.request.data['file']
		file_details = self.request.data['file_details']
		
		
		data={
			"user":user,
			"file":file,
			"file_details":file_details,
			

		}
		
		s1 = FileSerializers(data=data)
		
		if s1.is_valid():
			
			s1.save()
			return Response(s1.data,status=status.HTTP_201_CREATED)
		return Response(s1.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self,request):
		data= MetaData.objects.all()
		s1 = FileSerializers(data,many=True)
		return Response(s1.data)

	def put(self,request,id):
		user = self.request.data['user']
		file =  self.request.data['file']
		file_details = self.request.data['file_details']
		

		print(request.session['user_token'])
		user=User.objects.get(pk=(Token.objects.filter(key=request.session['user_token']).values_list('user_id',flat=True).first()))
		print(user)
		mdata=MetaData.objects.get(pk=id)
		if mdata.user==user:
			data={
			"user":user,
			"file":file,
			"file_details":file_details,
			}
			s1 = FileSerializers(mdata,data=data)
			if s1.is_valid():
				s1.save()
				return Response(s1.data,status=status.HTTP_201_CREATED)
			else:
				return Response({"msg":"ERORRRRRR"})
		else:
			return Response({"msg":"You do not have permission to update this task"})


# {
#     "user" : "roy123",
#     "file" : "",
#     "file_details" : "detail here ",
#     "uu_id" : "10"
# }