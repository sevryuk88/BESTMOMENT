import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import get_user_model
from . models import User
from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL
 
# авторизация 
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='USERNAME', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
    
    class Meta:
        model = get_user_model
        fields = ['username', 'password']
        
        
        



class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="E-MAIL",
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    
        

# регистрация                      
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='LOGIN', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
 
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-MAIL',
            'first_name': 'NAME',
            'last_name': 'SURNAME',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
        
           
        
    def clean_email(self):
        email = self.cleaned_data['email']
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Such an E-mail already exists!")
        return email

                
# Профиль        
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='LOGIN', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-MAIL', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.date.today().year
    #date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))
 
 
    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name'] #'date_birth',
        labels = {
            'first_name': 'NAME',
            'last_name': 'SURNAME',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

                

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="OLD PASSWORD", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="NEW PASSWORD", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="NEW PASSWORD", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
        