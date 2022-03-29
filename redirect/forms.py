from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        username = cleaned_data.get('username')
        if username is None:
            username = ''
        cleaned_data['userdisplay'] = username
        cleaned_data['username'] = username.lower()
        return cleaned_data
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        user.profile.userdisplay = self.cleaned_data['userdisplay']
        if commit:
            user.save()
        return user
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        form_data = self.cleaned_data
        username = form_data['username'].lower()
        password = form_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(_('Username or password was incorrect.'), code='incorrect1')
        return user
        
        
        
        
        
        
        
        
