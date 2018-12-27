from django import forms
from .models import myuser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm



class CreateUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = myuser
        fields = UserCreationForm.Meta.fields + ('first_name', 'email', 'profile_pic')

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = myuser
#         fields = ['username', 'password']
#         widgets = {
#             'password': forms.PasswordInput()
#         }


class LoginForm(AuthenticationForm):
    class Meta:
        model = myuser


class UserEditForm(forms.ModelForm):
    #id  = forms.IntegerField(widget = forms.HiddenInput)
    class Meta:
        model = myuser
        fields = ['username', 'first_name', 'email', 'profile_pic']

    
    #when you call clean username it only gives you the username in the cleaned data so we had to grab id from data it self
    #which is all in string so had to convert it to int

    # def clean_username(self):
    #     id = self.data.get('id')              
    #     # print(self.cleaned_data)
    #     # print(self.data)
    #     # print(id)
    #     username = self.cleaned_data.get('username')
    #     qs = myuser.objects.filter(username__exact = username)
    #     # print(id != (qs.first().id))
    #     if qs.exists() and qs.first().id != id:
    #         # print(qs.first().id)
    #         raise forms.ValidationError("This username already exists")
    #     return self.cleaned_data.get('username')
    
    # def clean_email(self):
    #     id = self.data.get('id')
    #     email = self.cleaned_data.get('email')
    #     qs = myuser.objects.filter(email__exact=email)
    #     if qs.exists() and qs.first().id != id:
    #         raise forms.ValidationError("This email is already used")
    #     return self.cleaned_data.get('email')

class ChangePassForm(forms.Form):
    current_pass = forms.CharField(max_length = 100, widget = forms.PasswordInput)
    new_pass = forms.CharField(max_length = 100, widget = forms.PasswordInput)
    confirm_new_pass = forms.CharField(max_length = 100, widget = forms.PasswordInput)

    def clean_new_pass(self):
        first = self.data.get('new_pass')
        second = self.data.get('confirm_new_pass')
        if first == second:
            return first
        raise forms.ValidationError("New passwords don't match")
        