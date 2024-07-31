
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms
from .models import Organization
from django.forms import ModelForm
from captcha.fields import CaptchaField

 
 
class signupform(UserCreationForm):
        password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
        password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
        captcha = CaptchaField()
        class Meta:	
            model = User
            fields = [ 'username','email',]
            labels ={'email':"Email"}

        def __init__(self,*args,**kwargs):
                super().__init__(*args,**kwargs)
                for field in self.fields.values():
                    field.widget.attrs.update({'class':'form-control my-1','placeholder':field.label})
    
 

class organization_register_form(ModelForm): 
    class Meta:
        model = Organization
        exclude = ['user', 'parent_id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'name':
                field.widget.attrs.update({'class': 'form-control my-2', 'placeholder': field.label})
            else:
                field.widget.attrs.update({'class': 'my-2', 'placeholder': field.label})



#Forms for the password change                 

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



#Forms for the logo change 
class OrganizationLogoForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['logo']             
 