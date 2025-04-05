from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SarataniUser
from django.core.validators import MaxValueValidator, MinValueValidator

class UserRegisterForm(UserCreationForm):
    email             = forms.EmailField(label = "Email Address")
    age               = forms.IntegerField(label="Age", required=True, validators=[MinValueValidator(18), MaxValueValidator(100)])
    first_name        = forms.CharField(max_length=250,label="First Name", required=True)
    last_name         = forms.CharField(max_length=250,label="Last Name", required=True)
    username          = forms.CharField(max_length=8, min_length=8, label="ID", required=True)
    class Meta:
        model        = SarataniUser
        fields       = ['username','first_name','last_name', 'email','sex','age','password1', 'password2']
        labels       = {"sex":"Sex"}
        widgets      = {'username': forms.TextInput(attrs={ 'class': "form-control",}),}

class UserUpdateForm(forms.ModelForm):
    email            = forms.EmailField(label="Email Address")

    class Meta:
        model        = SarataniUser
        fields       = ['username','first_name','last_name', 'email','sex']
        labels       = {'username': 'ID',}
        help_texts   = {'username': None,}