# Step 1 - Installing VENV
`python3 -m venv .venv`

`source .venv/bin/activate`


# Step 2 - Installing Django
`pip install django`

`pipenv shell`

`django-admin startproject nome_projeto .` (don't forget the fuck . dot)

- To check it

`python manage.py runserver`

# Step 3 - Deploying Heroku


- settings.py 
  

    ALLOWED_HOSTS['*']
    

- Create ProcFile at root folder
    

    release: python manage.py migrate --noinput
    web: gunicorn nome_projeto.wsgi --timeout 15 --keep-alive 5 --log-file -
  
  
`pipenv install gunicorn`

`heroku apps:create nome-projeto --buildpack heroku/python`   (don't use _ underscore, use - dash instead)

- Check if remote branch was created

`git remote -v`

- If heroku's remote branch was not be created

`git remote add heroku https://git.heroku.com/site_personal_shopper.git`

- If need to remove heroku branch to recreate it

`git remote remove heroku`

- If you didn't configurete staticfiles you have deactivete it

`heroku config:set DISABLE_COLLECTSTATIC=1`

- Deploy to Heroku

  OBS: Before you deploy on Heroku you have to commit the project localy

`git push heroku main`


- Run django manage

`heroku run python manage.py ...`


# Step 4 - SettingUp Database sqlite3:postgreSql

`pipenv install dj-database-url`

`pipenv install psycopg2-binary`

`pipenv install python-decouple`

-  settings.py
   
    
    import os
    from functools import partial
    from pathlib import Path
    import dj_database_url
    from decouple import config, Csv

    ... 

    #Database

    default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    
    parse_database = partial(dj_database_url.parse, conn_max_age=600)
    
    DATABASES = {
        'default': config('DATABASE_URL', default=default_db_url, cast=parse_database)
    }


# Setp 5 - SettingUp Static Files


- Watch videos
  
  - Create an IAM user on AWS with permission for S3FullAcces
  - Copy ACCES KEY ID and SECRET ACCES KEY to .env file

  https://plataforma.dev.pro.br/31937-django/695738-criacao-de-usuario-na-amazon
  
  https://plataforma.dev.pro.br/31937-django/695739-criacao-e-configuracao-do-s3
  
  
- Create bucket and user on AWS S3

- .env
  

    DEBUG=True
    SECRET_KEY=
    ALLOWED_HOSTS='localhost, 127.0.0.1'
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_STORAGE_BUCKET_NAME=
    AWS_S3_SIGNATURE_VERSION='s3v4'
    AWS_S3_REGION_NAME='us-east-2'


- Lib django_s3_folder_storage to upload static files to AWS S3

`pipenv install django_s3_folder_storage`


- setting (Static files)


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/
    
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

    COLLECTFAST_ENABLED = False

- setting (storage configuration).py


    # STORAGE CONFIGURATION IN S3 AWS
    # ------------------------------------------------------------------------------
    
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')

    if AWS_ACCESS_KEY_ID:
        AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
        AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', }
        AWS_PRELOAD_METADATA = True
        AWS_AUTO_CREATE_BUCKET = False
        AWS_QUERYSTRING_AUTH = True
        AWS_S3_CUSTOM_DOMAIN = None
        AWS_S3_SIGNATURE_VERSION = config('AWS_S3_SIGNATURE_VERSION')
        AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
    
        COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
        COLLECTFAST_ENABLED = True
    
        AWS_DEFAULT_ACL = 'private'
    
        # Static Assets
        # ------------------------------------------------------------------------------
        STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
        STATIC_S3_PATH = 'static'
        STATIC_ROOT = f'/{STATIC_S3_PATH}/'
        STATIC_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{STATIC_S3_PATH}/'
        ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
    
        # Upload Media Folder
        DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
        DEFAULT_S3_PATH = 'media'
        MEDIA_ROOT = f'/{DEFAULT_S3_PATH}/'
        MEDIA_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{DEFAULT_S3_PATH}/'
    
        INSTALLED_APPS.append('s3_folder_storage')
        INSTALLED_APPS.append('storages')


- Check if staticfiles config is working

`python manage.py collectstatic --no-input`


- Create the file /contrib/env-sample


    DEBUG=True
    SECRET_KEY=''
    ALLOWED_HOSTS='localhost, 127.0.0.1'
    _AWS_ACCESS_KEY_ID=
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_STORAGE_BUCKET_NAME=nome-do-bucket
    AWS_S3_SIGNATURE_VERSION='s3v4'
    AWS_S3_REGION_NAME='us-east-2'

- Install Collectfast lib

`pipenv install Collectfast`

    settings.py - INSTALLED_APPS

    'collectfast',
    
    before that line 'django.contrib.staticfiles',

    
    COLLECTFAST_ENABLED = False
    

- Set up all enviroment varibles from .env file to Heroku


`pipenv shell`

`heroku config:set VARIABLE_NAME=VARIABLE_VALUE`

`heroku config:unset DISABLE_COLLECTSTATIC`

# Step 6 - Creating App Base


Ir para pasta RAIZ do projeto no PyCharm
e nao dentro da pasta do projeto Django, ou seja, no mesmo nível
da pasta .venv, staticfiles, e dos arquivos Pipfile e Pipfile.lock

`pipenv shell`

`python manage.py startapp app_base`


- Registering app_base at setting.py


    INSTALLED_APPS

    ...

    'app_base',
  


- Setting up urls and views

    
At projectname/urls.py file:
    
    from django.contrib import admin
    from django.urls import path, include
    from django.conf.urls.static import static
    from django.conf import settings
    
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('app_base.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



At app_base/urls.py file:
    
    from django.urls import path
    
    from .views import home
    
    urlpatterns = [
        path('', home, name='home'),
    ]


At app_base/views.py

    from django.http import HttpResponse
    from django.shortcuts import render
    
    # Create your views here.
    
    
    def home(request):
        return HttpResponse('Hello App_Base!')


# Overwritting Django Users models

At app_base/models.py

    from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
    from django.contrib.auth.models import PermissionsMixin
    from django.core.mail import send_mail
    from django.db import models
    from django.utils import timezone
    from django.utils.translation import gettext_lazy as _
    
    
    class UserManager(BaseUserManager):
        use_in_migrations = True
    
        def _create_user(self, email, password, **extra_fields):
            """
            Creates and saves a User with the given email and password.
            """
            if not email:
                raise ValueError('The given email must be set')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    
        def create_user(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_superuser', False)
            return self._create_user(email, password, **extra_fields)
    
        def create_superuser(self, email, password, **extra_fields):
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_staff', True)
    
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')
            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
    
            return self._create_user(email, password, **extra_fields)
    
    
    class User(AbstractBaseUser, PermissionsMixin):
        """
        App base User class.
    
        Email and password are required. Other fields are optional.
        """
    
        first_name = models.CharField(_('first name'), max_length=150, blank=True)
        email = models.EmailField(_('email address'), unique=True)
        is_staff = models.BooleanField(
            _('staff status'),
            default=False,
            help_text=_('Designates whether the user can log into this admin site.'),
        )
        is_active = models.BooleanField(
            _('active'),
            default=True,
            help_text=_(
                'Designates whether this user should be treated as active. '
                'Unselect this instead of deleting accounts.'
            ),
        )
        date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
        objects = UserManager()
    
        EMAIL_FIELD = 'email'
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []
    
        class Meta:
            verbose_name = _('user')
            verbose_name_plural = _('users')
    
        def clean(self):
            super().clean()
            self.email = self.__class__.objects.normalize_email(self.email)
    
        def get_full_name(self):
            """
            Return the first_name plus the last_name, with a space in between.
            """
            full_name = '%s' % (self.first_name)
            return full_name.strip()
    
        def get_short_name(self):
            """Return the short name for the user."""
            return self.first_name
    
        def email_user(self, subject, message, from_email=None, **kwargs):
            """Send an email to this user."""
            send_mail(subject, message, from_email, [self.email], **kwargs)



At settings.py file:


    AUTH_USER_MODEL = 'app_base.User'


- Database migrations

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py showmigrations`


- Create SuperUser 

`python manage.py createsuperuser`

`heroku run python manage.py createsuperuser`



- Setting up our own User on Django ADMIN

At app_base/admin.py file:

    from django.contrib import admin
    
    from django.conf import settings
    from django.contrib import admin, messages
    from django.contrib.admin.options import IS_POPUP_VAR
    from django.contrib.admin.utils import unquote
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import (
        AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
    )
    from django.contrib.auth.models import Group
    from django.core.exceptions import PermissionDenied
    from django.db import router, transaction
    from django.http import Http404, HttpResponseRedirect
    from django.template.response import TemplateResponse
    from django.urls import path, reverse
    from django.utils.decorators import method_decorator
    from django.utils.html import escape
    from django.utils.translation import gettext, gettext_lazy as _
    from django.views.decorators.csrf import csrf_protect
    from django.views.decorators.debug import sensitive_post_parameters
    
    from app_base.models import User
    
    
    csrf_protect_m = method_decorator(csrf_protect)
    sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())
    
    
    @admin.register(User)
    class UserAdmin(admin.ModelAdmin):
        add_form_template = 'admin/auth/user/add_form.html'
        change_user_password_template = None
        fieldsets = (
            (None, {'fields': ('first_name', 'email', 'password')}),
            (_('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('first_name', 'email', 'password1', 'password2'),
            }),
        )
        form = UserChangeForm
        add_form = UserCreationForm
        change_password_form = AdminPasswordChangeForm
        list_display = ('email', 'first_name', 'is_staff')
        list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
        search_fields = ('first_name', 'email')
        ordering = ('first_name',)
        filter_horizontal = ('groups', 'user_permissions',)
    
        def get_fieldsets(self, request, obj=None):
            if not obj:
                return self.add_fieldsets
            return super().get_fieldsets(request, obj)
    
        def get_form(self, request, obj=None, **kwargs):
            """
            Use special form during user creation
            """
            defaults = {}
            if obj is None:
                defaults['form'] = self.add_form
            defaults.update(kwargs)
            return super().get_form(request, obj, **defaults)
    
        def get_urls(self):
            return [
                path(
                    '<id>/password/',
                    self.admin_site.admin_view(self.user_change_password),
                    name='auth_user_password_change',
                ),
            ] + super().get_urls()
    
        def lookup_allowed(self, lookup, value):
            # Don't allow lookups involving passwords.
            return not lookup.startswith('password') and super().lookup_allowed(lookup, value)
    
        @sensitive_post_parameters_m
        @csrf_protect_m
        def add_view(self, request, form_url='', extra_context=None):
            with transaction.atomic(using=router.db_for_write(self.model)):
                return self._add_view(request, form_url, extra_context)
    
        def _add_view(self, request, form_url='', extra_context=None):
            # It's an error for a user to have add permission but NOT change
            # permission for users. If we allowed such users to add users, they
            # could create superusers, which would mean they would essentially have
            # the permission to change users. To avoid the problem entirely, we
            # disallow users from adding users if they don't have change
            # permission.
            if not self.has_change_permission(request):
                if self.has_add_permission(request) and settings.DEBUG:
                    # Raise Http404 in debug mode so that the user gets a helpful
                    # error message.
                    raise Http404(
                        'Your user does not have the "Change user" permission. In '
                        'order to add users, Django requires that your user '
                        'account have both the "Add user" and "Change user" '
                        'permissions set.')
                raise PermissionDenied
            if extra_context is None:
                extra_context = {}
            username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
            defaults = {
                'auto_populated_fields': (),
                'username_help_text': username_field.help_text,
            }
            extra_context.update(defaults)
            return super().add_view(request, form_url, extra_context)
    
        @sensitive_post_parameters_m
        def user_change_password(self, request, id, form_url=''):
            user = self.get_object(request, unquote(id))
            if not self.has_change_permission(request, user):
                raise PermissionDenied
            if user is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                    'name': self.model._meta.verbose_name,
                    'key': escape(id),
                })
            if request.method == 'POST':
                form = self.change_password_form(user, request.POST)
                if form.is_valid():
                    form.save()
                    change_message = self.construct_change_message(request, form, None)
                    self.log_change(request, user, change_message)
                    msg = gettext('Password changed successfully.')
                    messages.success(request, msg)
                    update_session_auth_hash(request, form.user)
                    return HttpResponseRedirect(
                        reverse(
                            '%s:%s_%s_change' % (
                                self.admin_site.name,
                                user._meta.app_label,
                                user._meta.model_name,
                            ),
                            args=(user.pk,),
                        )
                    )
            else:
                form = self.change_password_form(user)
    
            fieldsets = [(None, {'fields': list(form.base_fields)})]
            adminForm = admin.helpers.AdminForm(form, fieldsets, {})
    
            context = {
                'title': _('Change password: %s') % escape(user.get_username()),
                'adminForm': adminForm,
                'form_url': form_url,
                'form': form,
                'is_popup': (IS_POPUP_VAR in request.POST or
                             IS_POPUP_VAR in request.GET),
                'add': True,
                'change': False,
                'has_delete_permission': False,
                'has_change_permission': True,
                'has_absolute_url': False,
                'opts': self.model._meta,
                'original': user,
                'save_as': False,
                'show_save': True,
                **self.admin_site.each_context(request),
            }
    
            request.current_app = self.admin_site.name
    
            return TemplateResponse(
                request,
                self.change_user_password_template or
                'admin/auth/user/change_password.html',
                context,
            )
    
        def response_add(self, request, obj, post_url_continue=None):
            """
            Determine the HttpResponse for the add_view stage. It mostly defers to
            its superclass implementation but is customized because the User model
            has a slightly different workflow.
            """
            # We should allow further modification of the user just added i.e. the
            # 'Save' button should behave like the 'Save and continue editing'
            # button except in two scenarios:
            # * The user has pressed the 'Save and add another' button
            # * We are adding a user in a popup
            if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
                request.POST = request.POST.copy()
                request.POST['_continue'] = 1
            return super().response_add(request, obj, post_url_continue)



# Backup Postgresql Heroku 

`heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Sao_Paulo'`




# Rollback admin migrations

    python manage.py migrate admin zero
    python manage.py migrate auth zero
    python manage.py migrate contenttypes zero
    python manage.py migrate sessions zero

