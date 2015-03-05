from django import forms
from django.contrib.auth.models import User


class UserCreationNoPasswordForm(forms.ModelForm):
    """A form that creates a user with an unusable password."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserCreationNoPasswordForm, self).save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user
