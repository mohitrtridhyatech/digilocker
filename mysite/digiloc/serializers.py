from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

# from .models import get_password_reset_token_expiry_time
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import  MetaData

class FileSerializers(serializers.ModelSerializer):
  
	class Meta:
		model = MetaData
		fields = ('user', 'file', 'file_details','uu_id')



class userSerializers(serializers.ModelSerializer):
  
	class Meta:
		model = User
		fields =  '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
	email = serializers.CharField(required=True)
	# password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	# password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('username', 'password', 'email')


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self,data):
		username = data.get("username", "")
		password = data.get("password", "")
		
		if username and password:
			user = authenticate(username=username,password=password)
			print(user)
			if user:
				if user.is_active:
					data["user"]=user
				else:
					msg = "user is deactive"
					raise ValidationError(msg)
			else:
				msg = "Enter correct credentials"
				raise ValidationError(msg)
		else:
			msg = "Must provide username and password"
			raise ValidationError(msg)
		return data

# class PasswordValidateMixin:
#     def validate(self, data):
#         token = data.get('token')

#         # get token validation time
#         password_reset_token_validation_time = get_password_reset_token_expiry_time()

#         # find token
#         try:
#             reset_password_token = _get_object_or_404(models.ResetPasswordToken, key=token)
#         except (TypeError, ValueError, ValidationError, Http404,
#                 models.ResetPasswordToken.DoesNotExist):
#             raise Http404(_("The OTP password entered is not valid. Please check and try again."))

#         # check expiry date
#         expiry_date = reset_password_token.created_at + timedelta(
#             hours=password_reset_token_validation_time)

#         if timezone.now() > expiry_date:
#             # delete expired token
#             reset_password_token.delete()
#             raise Http404(_("The token has expired"))
#         return data


# class PasswordTokenSerializer(PasswordValidateMixin, serializers.Serializer):
#     password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
#     token = serializers.CharField()

