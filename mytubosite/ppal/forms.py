from django.forms import *

from django.contrib.admin import widgets
from ppal.models import *

class TuboForm(ModelForm):
    class Meta:
        model = Tubo
        docfile = forms.FileField(
            label='Selecciona un archivo'
        )
        exclude = ['last_editing_date']


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())
    password2 = CharField(widget=PasswordInput(), label="Password confirmation")

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError('Passwords do not match')

        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

