from django import forms
from .models import Prediction

# creating a form
# class PredictionForm(forms.ModelForm):
#     patient_name = forms.CharField(max_length = 250,label="Patient's Name", required=True)
#     patient_id   = forms.CharField(max_length = 8,label="Patient's ID", required=True)
#     image        = forms.ImageField(label="Patient's Paps Smear image.", required=True)
#     class Meta:
#         model = Prediction
#         fields = ['patient_name','patient_id', 'image']
#         widgets = {'username': forms.TextInput(attrs={ 'class': "form-control",}),}
#         help_texts = {
#         'image':"Upload .jpg, png"
#         }

class PredictionForm(forms.ModelForm):
    patient_name = forms.CharField(
        max_length=250,
        label="Patient's Name",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter patient's name"})
    )
    patient_id = forms.CharField(
        max_length=8,
        label="Patient's ID",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter patient's ID"})
    )
    image = forms.ImageField(
        label="Patient's Paps Smear image.",
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Prediction
        fields = ['patient_name', 'patient_id', 'image']

