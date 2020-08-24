from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, PasswordChangeForm
from django.core.validators import EmailValidator
from .models import *


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        """check if the email already exists"""
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('email already exists')
        return email

    def clean_password2(self):
        """check if the both passwords match"""
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.client = True
        user.active = True
        user.save()


class AdminUserCreationForm(forms.ModelForm):
    """form for creating new admin users with all fields and repeated password field"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        """check if the email already exists"""
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('email already exists')
        return email

    def clean_password2(self):
        """check if the both passwords match"""
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('passwords don\'t match')
        return password2

    def save(self, commit=False):
        """save the password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """a form for updating users including all the fields but hashed password field"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class clientChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm password',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'age', 'phn_no', 'pro_pic', 'background_pic')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'age': forms.NumberInput(attrs={'class': 'form-control'}),
                   'phn_no': forms.NumberInput(attrs={'class': 'form-control'})}


class TrackingForm(forms.ModelForm):
    class Meta:
        model = Tracking
        fields = ('addr', 'status', 'billid')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('pid', 'commentbody')
