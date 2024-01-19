from django.shortcuts import render, redirect
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# user.is_authenticated == request.user
def register(request):
    form = RegisterForm()

    context = {
        'form': form,
    }
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Formulario enviado com sucesso')
            return redirect('contact:login')
            
    return render(
        request=request,
        template_name= 'contact/register.html',
        context=context
        
    )
    
@login_required(login_url='contact:login') #se não estiver logado ira para contact:login
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)
    context ={
        'form':form,
    }
        
    if request.method == 'POST':
        form = RegisterUpdateForm(data=request.POST, instance=request.user)
        context ={
            'form':form,
        }
         
        if form.is_valid():   
            form.save()
            return redirect('contact:user_update')


    return render(
        request=request,
        template_name='contact/user_update.html',
        context=context,
    )
    
def login_view(request):
    form = AuthenticationForm(request)

    context = {
        'form': form,
    }
    
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso')
            return redirect('contact:index')
        else:
            messages.error(request,'Login invalido')
            
    return render(
        request=request,
        template_name= 'contact/login.html',
        context=context
        
    )


@login_required(login_url='contact:login') #se não estiver logado ira para contact:login
def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')