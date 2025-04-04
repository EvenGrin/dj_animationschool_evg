from django.contrib.auth.forms import UserCreationForm

from anim_app.models import User


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['email'].label = 'Эл. почта'

    class Meta:
        model = User
        fields=('surname', 'name', 'patronymic', 'username', 'email', 'password1', 'password2')