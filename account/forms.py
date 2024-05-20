from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import User, Restaurant, Rider, Customer

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "type": 'email',
                "placeholder": 'example@example.com'
            }
        )
    )
    
    
    is_customer = forms.BooleanField(required=False)
    is_restaurant = forms.BooleanField(required=False)
    is_rider = forms.BooleanField(required=False)

    # Additional fields for customer
    customer_first_name = forms.CharField(required=False)
    customer_last_name = forms.CharField(required=False)
    customer_contact_number = forms.CharField(required=False)
    customer_address = forms.CharField(required=False)
    # customer_image = forms.ImageField(required=False)
    
    # Additional fields for restaurant
    restaurant_name = forms.CharField(required=False)
    restaurant_contact_number = forms.CharField(required=False)
    restaurant_address = forms.CharField(required=False)
    restaurant_hrs = forms.CharField(required=False)
    # restaurant_image = forms.ImageField(required=False)

    # Additional fields for rider
    rider_first_name = forms.CharField(required=False)
    rider_last_name = forms.CharField(required=False)
    rider_contact_number = forms.CharField(required=False)
    rider_dln = forms.CharField(required=False)
    rider_age = forms.IntegerField(required=False)
    # rider_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_customer', 'is_restaurant', 'is_rider')

        
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data['is_customer']:
                customer = Customer.objects.create(
                    user=user,
                    first_name=self.cleaned_data.get('customer_first_name'),
                    last_name=self.cleaned_data.get('customer_last_name'),
                    contact_number=self.cleaned_data.get('customer_contact_number'),
                    default_address=self.cleaned_data.get('customer_address'),
                    # customer_image=self.cleaned_data.get('customer_image')
                )
            elif self.cleaned_data['is_restaurant']:
                restaurant = Restaurant.objects.create(
                    user=user,
                    name=self.cleaned_data.get('restaurant_name'),
                    contact_number=self.cleaned_data.get('restaurant_contact_number'),
                    address=self.cleaned_data.get('restaurant_address'),
                    business_hours=self.cleaned_data.get('restaurant_hrs'),
                    # resto_image=self.cleaned_data.get('restaurant_image')
                )
            elif self.cleaned_data['is_rider']:
                rider = Rider.objects.create(
                    user=user,
                    first_name=self.cleaned_data.get('rider_first_name'),
                    last_name=self.cleaned_data.get('rider_last_name'),
                    contact_number=self.cleaned_data.get('rider_contact_number'),
                    driver_license=self.cleaned_data.get('rider_dln'),
                    age=self.cleaned_data.get('rider_age'),
                    # rider_image=self.cleaned_data.get('rider_image')
                )
        return user

from django.contrib.auth.models import User

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    contact_number = forms.CharField(required=False)
    default_address = forms.CharField(required=False)
    customer_image = forms.ImageField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'contact_number', 'default_address', 'customer_image', 'password', 'confirm_password']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'default_address': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_image': forms.FileInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        if user_type == 'customer':
            instance = kwargs.get('instance')
            if instance:
                profile = instance.customer 
                self.fields['first_name'].initial = profile.first_name
                self.fields['last_name'].initial = profile.last_name
                self.fields['contact_number'].initial = profile.contact_number
                self.fields['default_address'].initial = profile.default_address
                self.fields['customer_image'].initial = profile.customer_image

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match")

        if first_name and not first_name.isalpha():
            self.add_error('first_name', "First name should only contain alphabetic characters")

        if last_name and not last_name.isalpha():
            self.add_error('last_name', "Last name should only contain alphabetic characters")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        if commit:
            instance.save()
            if hasattr(instance, 'customer'):
                instance.customer.first_name = self.cleaned_data['first_name']
                instance.customer.last_name = self.cleaned_data['last_name']
                instance.customer.contact_number = self.cleaned_data['contact_number']
                instance.customer.default_address = self.cleaned_data['default_address']
                instance.customer.customer_image = self.cleaned_data['customer_image']
                instance.customer.save()
        return instance

