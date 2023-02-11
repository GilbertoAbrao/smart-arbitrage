from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from api_app.models import Profile
from api_app.models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'email': {'read_only': True}
        }

        model = Profile

        fields = (
            'id',
            'inserted_at',
            'updated_at',
            'first_name',
            'last_name',
            'email',
        )




class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	first_name = serializers.CharField(style={'input_type': 'first_name'}, write_only=True)
	last_name = serializers.CharField(style={'input_type': 'last_name'}, write_only=True)
	cellphone = serializers.CharField(style={'input_type': 'cellphone'}, write_only=True)

	class Meta:
		model = User
		fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'cellphone']
		extra_kwargs = {
				'password': {'write_only': True},
		}	


	def	save(self):

		user = User(
					email=self.validated_data['email'],
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		user.set_password(password)
		user.save()

		return user
