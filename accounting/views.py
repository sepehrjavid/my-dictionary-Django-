from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import (
    View, 
    FormView, 
    DetailView,
    UpdateView,
    CreateView,
    FormView,
)
from django.contrib.auth import (
    login, 
    logout, 
    authenticate,
)
from django.contrib.auth.forms import AuthenticationForm
from .forms import (
    CreateUser, 
    LoginForm, 
    UserEditForm
)
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import myuser
from words.models import word
from django.core.paginator import Paginator

class SignOut(View):
    def get(self, request):
        logout(request)
        return redirect('words:words_list')



# class Sign_In(FormView):
#     form_class = LoginForm()
#     def get(self,request):
#         return render(request, 'accounting/signin.html', {'form':self.form_class})

#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username = username, password = password)
#         if user is not None:
#             login(request, user)
#             return redirect('words:words_list')
#         else:
#             return render(request, 'accounting/signin.html', {'form': self.form_class})

class Sign_In(LoginView):
    template_name = 'accounting/signin.html'




class SignUp(CreateView):
    model = myuser
    def get(self,request):
        form = CreateUser()
        return render(request, 'accounting/signup.html', {'form':form})
    
    def post(self, request):
        form = CreateUser(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('words:words_list')
        else:
            return render(request, 'accounting/signup.html', {'form': form})


class UserDetail(LoginRequiredMixin, DetailView):
    login_url = 'accounting:signin'
    queryset = myuser.objects.all()
    template_name = 'accounting/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    #lines 62 & 63 should be there together to change the sug filed to whatever we want
    model = myuser
    context_object_name = 'person'
    def get_context_data(self, *args, **kwargs):
        context = super(UserDetail, self).get_context_data(*args, **kwargs)
        print(kwargs)
        # context = {}
        # context['person'] = myuser.objects.get(username = self.request.user.username)
        #lines 68 & 69 are also right together
        # it could also be self.request.user.pk
        qs = word.objects.filter(user__username__iexact=self.kwargs.get("username")).order_by('-date')
        if self.request.GET.get('q'):
            print(qs.search(self.request.GET.get('q')))
            qs = qs.search(self.request.GET.get('q'))
            context['words'] = qs
        else:
            context['words'] = qs
        print(self.request.GET.get('q'))
        print(qs)
        paginated = Paginator(qs,3)
        if paginated.num_pages == 1:
            context['is_paginated'] = False
        else:
            context['is_paginated'] = True
            context['paginator'] = paginated
            if self.request.GET.get('page') == None:
                page = paginated.page(1)
                context['page_obj'] = page
            else:
                page = paginated.page(self.request.GET.get('page'))
                context['page_obj'] = page
            context['object_list'] = page.object_list
            context['words'] = page.object_list
        print(context)
        return context
        #since we needed words in our context, we had to use this def to make it our self. if we only needed the person in our context, the def was not neccessary
        #get returns only one object and cannot return more whearas filter returns more than one


class UserEdit(UpdateView, FormView):
    queryset = myuser.objects.all()
    model = myuser
    form_class = UserEditForm
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'accounting/edit.html'
    context_object_name = 'person'
    success_url = '/'
    def post(self, request, username):
        # print(request.POST)
        # print(request.GET)
        # print(request.FILES)
        obj = myuser.objects.get(username=username)
        form = UserEditForm(data = request.POST, instance = obj, files=request.FILES)
        if form.is_valid():
            obj = form.save()
            print(form.data)
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'person':obj, 'form':form})


class ChangePass(PasswordChangeView):
    template_name = 'accounting/changepass.html'
    success_url = '/'
