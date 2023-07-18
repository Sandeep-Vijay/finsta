from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from myapp.models import UserProfile,Posts,Comments
from myapp.forms import SignUpForm,SignInForm,ProfileEditForm,PostForm,CoverpicForm,ProfilePicForm
from django.views.generic import CreateView,TemplateView,FormView,UpdateView,ListView,DetailView
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login to perform this action")
            return redirect("signin")
        return fn(request,*args,**kwargs)
    return wrapper


class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name='registration.html'
    success_url=reverse_lazy('login')


    def form_valid(self, form):
        messages.success(self.request,'Registration Successful')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'Registration failed')
        return super().form_invalid(form)

class SignInView(FormView):
    template_name='login.html'
    form_class=SignInForm
    
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,'Login Successful')
                return redirect('home')
            messages.error(request,'Login Failed')
            return render(request,self.template_name,{form:'form'})
            
@method_decorator(signin_required,name="dispatch")      
class IndexView(CreateView,ListView):
    template_name='index.html'
    form_class=PostForm
    model=Posts
    context_object_name='posts'
    success_url=reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
@method_decorator(signin_required,name="dispatch")  
class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=ProfileEditForm
    template_name='profileedit.html'
    success_url=reverse_lazy('index')
@signin_required
def add_like_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    post_obj=Posts.objects.get(id=id)
    post_obj.liked_by.add(request.user)
    return redirect('index')

@signin_required
def comments_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    post_obj=Posts.objects.get(id=id)
    comment=request.POST.get('comment')
    user=request.user
    Comments.objects.create(user=user,comment_text=comment,post=post_obj)
    return redirect('index')

@signin_required
def comment_remove_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    
    comment_obj=Comments.objects.get(id=id)
    if request.user==comment_obj.user:
        comment_obj.delete()
        return redirect('index')
    else:
        messages.error(request,'please contact admin')
        return redirect('login')
    
@method_decorator(signin_required,name="dispatch")    
class ProfileDetailView(DetailView):

    model=UserProfile
    template_name='profile.html'
    context_object_name='profile'

@signin_required   
def coverpic_change_view(request,*args,**kwargs):

    id=kwargs.get('pk')
    pro_obj=UserProfile.objects.get(id=id)
    form=CoverpicForm(instance=pro_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('profile-detail',pk=id)
    return redirect('profile-detail',pk=id)

@signin_required  
def profilepic_change_view(request,*args,**kwargs):

    id=kwargs.get('pk')
    pro_obj=UserProfile.objects.get(id=id)
    form=ProfilePicForm(instance=pro_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('profile-detail',pk=id)
    return redirect('profile-detail',pk=id)

@method_decorator(signin_required,name="dispatch")  
class ProfileListView(ListView):
    model=UserProfile
    template_name='profile-list.html'
    context_object_name='profiles'

    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)
    
    def post(self,request,*args,**kwargs):
        pname=request.POST.get('username')
        qs=UserProfile.objects.filter(Q(user__username__icontains=pname) | Q(user__first_name__icontains=pname) | Q(user__last_name__icontains=pname))
        return render(request,self.template_name,{"profiles":qs})
    
@signin_required   
def follow_user_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    prof_obj=UserProfile.objects.get(id=id) 
    user_prof=request.user.profile
    user_prof.following.add(prof_obj) 
    user_prof.save()
    return redirect('profile-list')
@signin_required
def unfollow_user_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    prof_obj=UserProfile.objects.get(id=id)
    user_prof=request.user.profile
    
    user_prof.following.remove(prof_obj)
    user_prof.save()
    return redirect('profile-list')
@signin_required
def post_delete_view(request,*args,**kwargs):

    post_id=kwargs.get('pk')

    post_obj=Posts.objects.get(id=post_id)
    if request.user==post_obj.user:
        post_obj.delete()
        return redirect('index')
    else:
        messages.error(request,"contact admin")
        return redirect('login')
    
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")


