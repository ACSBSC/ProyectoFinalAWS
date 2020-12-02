from django import forms
from django.forms import Textarea
import boto3
import requests

def get_items():
    resp = requests.get('https://kho2r9vl95.execute-api.us-east-1.amazonaws.com/dev')
    items = resp.json()
    tipos = [(elem, elem) for elem in items]
    return tipos

class ActividadForm(forms.Form):
    nombre = forms.CharField(label="Nombre de la actividad*", 
        required=True, 
        max_length=200, 
        error_messages={'required': 'Campo obligatorio', 
                        'max_length': 'Máximo 200 caracteres'})
    descripcion = forms.CharField(label="Descripcion de la actividad*", 
        required=True, 
        max_length=200, 
        error_messages={'required': 'Campo obligatorio', 
                        'max_length': 'Máximo 200 caracteres'})
    instrucciones = forms.CharField(label="Instrucciones de la actividad*", 
        required=True, 
        max_length=3000,
        widget=Textarea,
        error_messages={'required': 'Campo obligatorio', 
                        'max_length': 'Máximo 200 caracteres'})
    tipo = forms.ChoiceField(label="Tipo de actividad*", 
        choices=get_items, 
        required=True,
        error_messages={'required': 'Campo obligatorio'})

    imagen = forms.FileField(label="Imagen", 
        required=False)

class UpdateActividadForm(forms.Form):
    nombre = forms.CharField(label="Nombre de la actividad*", 
        required=False, 
        max_length=200, 
        error_messages={ 'max_length': 'Máximo 200 caracteres' })

    descripcion = forms.CharField(label="Descripcion de la actividad*", 
        required=False, 
        max_length=200, 
        error_messages={ 'max_length': 'Máximo 200 caracteres' })

    instrucciones = forms.CharField(label="Instrucciones de la actividad*", 
        required=False, 
        max_length=3000, 
        widget=Textarea,
        error_messages={'max_length': 'Máximo 3000 caracteres'})

    tipo = forms.ChoiceField(label="Tipo de actividad*", 
        choices=get_items, 
        required=False)

    imagen = forms.FileField(label="Imagen", 
        required=False)

class CategoriaForm(forms.Form):
    nombre = forms.CharField(label="Nombre de la categoria", 
        required=True, 
        max_length=200, 
        error_messages={'required': 'Campo obligatorio', 
                        'max_length': 'Máximo 200 caracteres'})
