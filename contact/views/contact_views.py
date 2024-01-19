from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from contact.models import Contact 
from django.http import Http404
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')
    p = Paginator(contacts, 10)

    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    
    title = f'Contacts -'
    context = {
        'title':title,
        'page_obj': page_obj
    }
    return render(
        request=request,
        template_name= 'contact/index.html',
        context=context
           
    )
    
def search(request):
    search_value = request.GET.get('q', '').strip()
    
    if search_value == '':
        return  redirect('contact:index')
    
    contacts = Contact.objects\
        .filter(show=True)\
        .filter(Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value))\
        .order_by('-id')
    
    p = Paginator(contacts, 10)

    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    title = f'search -'

    context = {
        'value':search_value,
        'title':title,
        'page_obj': page_obj
    }
    
    
    return render(
        request=request,
        template_name= 'contact/index.html',
        context=context
           
    )



def contact(request,contact_id):
    single_contact = get_object_or_404(
        Contact.objects,
        id=contact_id,
        show=True
        )
    
    '''
        single_contact = Contact.objects.filter(id=contact_id).first()
    
        if single_contact is None:
            raise Http404
    
    '''
    title = f'{single_contact.first_name} {single_contact.last_name} -'
    
    user = request.user
    
    context = {
        'title':title,
        'contact':single_contact,
        'user':user
    }
    return render(
        request=request,
        template_name= 'contact/contact.html',
        context=context
           
    )
    