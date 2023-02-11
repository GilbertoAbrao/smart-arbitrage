from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.authtoken.models import Token
from api_app.serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view

from api_app.models import Profile
from .serializers import RegistrationSerializer


class ProfileAPIView(APIView):
    """
    Profiles endpoints
    """
    
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)



@api_view(['POST', ])
def registration_view(request):

        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['message'] = 'successfully registered new user.'
            data['email'] = user.email

            # lets create a Profile to the user
            profile = Profile()
            profile.user = user
            profile.first_name = serializer.validated_data['first_name']
            profile.last_name = serializer.validated_data['last_name']
            profile.cellphone = serializer.validated_data['cellphone']
            profile.email = serializer.validated_data['email']
            profile.save()

            # let's create a Token to the user
            token = Token.objects.create(user=user)


            data['token'] = token.key


            return Response(data)
        else:
            # data = serializer.errors
            raise APIException(serializer.errors, code=400)





        """
        if request.method == 'POST':

            form = RegisterForm(request.POST)

            if form.is_valid():

                user = form.save()

                user.email = user.username
                user.save()

                # lets create related Entity
                entity = Entity()
                entity.owner = user
                entity.name = user.get_full_name()
                entity.email = user.email
                entity.save()

                # lets create Profile
                profile = Profile()
                profile.user = user
                profile.entity = entity
                profile.first_name = user.first_name
                profile.last_name = user.last_name
                profile.cellphone = form.cleaned_data.get('cellphone')
                profile.save()

                # lets login the new user
                # raw_password = form.cleaned_data.get('password1')
                # user = authenticate(username=user.username, password=raw_password)
                # login(request, user)
                return redirect('base:login')

            else:

                return render(request, 'register.html', {'form': form})

        elif request.method == 'GET':

            form = RegisterForm()

            return render(request, 'register.html', {'form': form})
        """
