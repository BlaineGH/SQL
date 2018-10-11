from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from random import randint
from datetime import datetime
from .models import User

def index(request):
	return redirect('/users')

def index1(request):
	return render(request, 'restfulusers/index.html', {'users':User.objects.all()})

def show(request, id):
	context = {
		'userid' : User.objects.get(id=id).id,
		'first_name' : User.objects.get(id=id).firstname,
		'last_name' : User.objects.get(id=id).lastname,
		'email' : User.objects.get(id=id).email,
		'created_at' : User.objects.get(id=id).created_at,
	}
	return render(request, 'restfulusers/show.html/', context)

def new(request):
	return render(request, 'restfulusers/new.html')

def edit(request, id):
	context = {
		'userid' : User.objects.get(id=id).id,
	}
	return render(request, 'restfulusers/edit.html/', context)

def create(request):
	errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/new')
        else:
			User.objects.create(firstname=request.POST['first_name'],lastname=request.POST['last_name'],email=request.POST['email'])
	return redirect('/')

def delete(request, id):
	User.objects.get(id=id).delete()
	return redirect('/')

def update(request, id):
	errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/'+id+'/edit')
        else:
            user = User.objects.get(id = id)
            user.firstname = request.POST['first_name']
            user.lastname = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return redirect('/users/'+id)

