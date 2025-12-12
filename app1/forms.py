from django import forms
from app1.models import Coustomer_Details

class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = Coustomer_Details
        fields = ['user', 'name', 'mobile','category', 'address', 'city','pincode', 'state','country']
        
        exclude = ['user']  

        widgets = {
            'Address': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Enter Building Number,Street Name & Locality'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'pincode':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Postalcode'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter State'}),
            'country': forms.HiddenInput(),  
        }




from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


