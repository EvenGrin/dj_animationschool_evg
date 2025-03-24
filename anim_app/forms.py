from django.contrib.auth.forms import UserCreationForm

from anim_app.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields=('surname', 'name', 'patronymic', 'username', 'email', 'password1', 'password2')