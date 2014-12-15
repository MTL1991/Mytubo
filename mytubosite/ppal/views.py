#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import *
from django.core.urlresolvers import reverse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required

from braces.views import LoginRequiredMixin # sudo pip install django-braces

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy

from ppal.models import *
from ppal.forms import *


def index(request):
    tubo_list = Tubo.objects.order_by('-last_editing_date')[:5]
    
    return render(request, 'index.html', {
        'tubo_list': tubo_list,
    })

def tuber_login(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse(index))
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                dest = request.GET.get('next') if request.GET.get('next') != None else reverse(index)
                return HttpResponseRedirect(dest)
            else:
                return HttpResponse('not valid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login')
def tuber_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(index))

def tuber_view(request, num):
    try:
        user = User.objects.get(id=num)
    except User.DoesNotExist:
        raise Http404()
    else:
        tubo_list = Tubo.objects.filter(tuber=user.tuber)
        return render(request, 'tuber_view.html', {
            'tuber': user.tuber,
            'user': request.user, # footer
            'tubo_list': tubo_list,
            })

def create_tuber(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            tuber = Tuber(user=user)
            tuber.save()
            u = authenticate(username=request.POST['username'],
                             password=request.POST['password'])
            login(request, u)
            return HttpResponseRedirect(reverse(index))
        else:
            return HttpResponse('user not valid')
    else:
        form = UserForm()
    return render(request, 'tuber_form.html', {'form': form})


class TuboDefinitiveView(DetailView):
    template_name = 'tubo_view.html'

    def get_context_data(self, **kwargs):
        context = super(TuboDefinitiveView, self).get_context_data(**kwargs)
        return context

class TuboView(TuboDefinitiveView):
    model = Tubo

def create_tubo(request):
    if request.method == 'POST':
        form = TuboForm(request.POST, request.FILES)
        if form.is_valid():
            tubo = form.save()
            tubo.save()
            return HttpResponseRedirect(reverse(index))
    else:
        form = TuboForm()
    return render(request, 'tubo_form.html', {'form': form})


class TuboDefinitiveDelete(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('index') # in the future, this will redirect to the user profile
    template_name = 'confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(TuboDefinitiveDelete, self).get_object()
        if not obj.tuber == self.request.user.tuber:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(TuboDefinitiveDelete, self).post(request, *args, **kwargs)

class TuboDelete(TuboDefinitiveDelete):
    model = Tubo