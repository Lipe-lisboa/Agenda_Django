from django.shortcuts import render, redirect, get_object_or_404
from contact.forms import ContactForm
from django.urls import reverse
from contact.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.
# method GET -> ler algo
# method POST -> enviar algo

# Os dicionários possuem um método específico para busca de valores, o get(), no qual podemos passar como parâmetros a chave que queremos e um valor padrão para retornar caso essa chave não seja encontrada:

@login_required(login_url='contact:login')
def create (request):  
    first_name_value  = request.POST.get('first_name')
    
    form_action = reverse('contact:create')
    if  request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        context = {
            'form': form,
            'form_action': form_action
        }
        
        if form.is_valid():
            #commit=False faz com que eu não salve o contato na base de dados (por enquanto)
           contact = form.save(commit=False)
           contact.owner = request.user
           contact.save()
           return redirect(f'contact:update', contact_id = contact.id)
       
            
            
        return render(
            request=request,
            template_name= 'contact/create.html',
            context=context
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action
    }
    return render(
    request=request,
    template_name= 'contact/create.html',
    context=context
    )


@login_required(login_url='contact:login')
def update (request, contact_id):
    
    contact = get_object_or_404(Contact, id=contact_id, show=True, owner=request.user)
    
    form_action = reverse('contact:update', args=(contact_id,))
    
    if  request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        context = {
            
            'form': form,
            'form_action': form_action
        }
        
        if form.is_valid():
           contact = form.save()
           return redirect(f'contact:update', contact_id = contact.id)
       
            
            
        return render(
            request=request,
            template_name= 'contact/create.html',
            context=context
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action
    }
    return render(
    request=request,
    template_name= 'contact/create.html',
    context=context
    )
    
@login_required(login_url='contact:login')
def delete (request, contact_id):
    
    contact = get_object_or_404(Contact, id=contact_id, show=True, owner=request.user)
    
    #dictionary.get(keyname, value)
    confirmation = request.POST.get('confirmation', 'no')
    print('confirmation', confirmation)
    
    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')
    
    
    context = {
        'contact':contact,
        'confirmation':confirmation
    }
    
    return render(
        request=request,
        template_name='contact/contact.html',
        context=context
        
    )