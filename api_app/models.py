from django.db import models
from core_app.models import User


class Profile(models.Model):
    """Tutorial from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html"""

    inserted_at = models.DateTimeField('Inserted at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField('First Name', max_length=150, blank=True)
    last_name = models.CharField('Last Name', max_length=150, blank=True)
    email_confirmed = models.BooleanField('Confimed Email', default=False)
    cellphone = models.CharField('Cellphone', max_length=150, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField('E-Mail', max_length=100, blank=True)
    # photo = models.ImageField('Photo', upload_to="uploads/", default=None, null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users Profiles"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):

        # if isn't adding
        if not self._state.adding:
            # sinc related user
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.email = self.email
            self.user.username = self.email
            self.user.save()

        super(Profile, self).save(*args, **kwargs)
