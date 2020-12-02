from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Actividad
from .forms import ActividadForm, UpdateActividadForm, CategoriaForm
import requests
import boto3
from uuid import uuid4

# Create your views here.

def index(request):
    actividades = Actividad.objects.all()
    return render(request, 'actividades/index.html', { 'actividades': actividades })

def random(request):
    resp = requests.get('https://393e9s4nch.execute-api.us-east-1.amazonaws.com/dev')
    rand = resp.json()
    print(resp)
    act = Actividad.objects.filter(nombre=rand['nombre']).get()
    print(act)
    return render(request, 'actividades/random.html', { 'act': act })

def create(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST, request.FILES)
        if form.is_valid():
            #Crea la instancia del efecto de video con la información básica
            act = Actividad(nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                instrucciones=form.cleaned_data['instrucciones'],
                tipo=form.cleaned_data['tipo'],
                imagen=form.cleaned_data['imagen'])
            act.save()

            return HttpResponseRedirect(reverse('actividades:index'))
    else:
        form = ActividadForm()

    return render(request, 'actividades/create.html', { 'form': form })

def update(request, id):
    act = Actividad.objects.filter(id=id).get()
    
    if request.method == 'POST':
        form = UpdateActividadForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['nombre'] and act.nombre != form.cleaned_data['nombre']:
                act.nombre = form.cleaned_data['nombre']
                act.save()
            if form.cleaned_data['descripcion'] and act.descripcion != form.cleaned_data['descripcion']:
                act.descripcion = form.cleaned_data['descripcion']
                act.save()
            if form.cleaned_data['instrucciones'] and act.instrucciones != form.cleaned_data['instrucciones']:
                act.instrucciones = form.cleaned_data['instrucciones']
                act.save()
            if form.cleaned_data['tipo'] and act.tipo != form.cleaned_data['tipo']:
                act.tipo = form.cleaned_data['tipo']
                act.save()
            if form.cleaned_data['imagen']:
                act.imagen.delete()
                act.imagen = form.cleaned_data['imagen']
                act.save()

            return HttpResponseRedirect(reverse('actividades:index'))
    else:
        # Información que recibe el formulario para volver a popularlo
        form_data = {
            'nombre': act.nombre,
            'descripcion': act.descripcion,
            'instrucciones': act.instrucciones,
            'tipo': act.tipo }

        form = UpdateActividadForm(form_data)

    return render(request, 'actividades/update.html', { 'form': form, 
                                                        'act': Actividad.objects.filter(id=id).get()} )

def remove(request, id):
    act = Actividad.objects.filter(id=id).get()
    act.imagen.delete()
    act.delete()
    return HttpResponseRedirect(reverse('actividades:index'))

def cat(request):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('categoria_rutinas')
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():    
            nombre = form.cleaned_data['nombre']
            table.put_item(
                Item={
                    'Id': uuid4().int % 100000 // 1,
                    'Tipo': form.cleaned_data['nombre']
                }
            )

            return HttpResponseRedirect(reverse('actividades:cat'))
    else:
        data = table.scan()
        items = data['Items']
        print(items)
    
    return render(request, 'actividades/act.html', { 'categorias': items, 'form': CategoriaForm() })