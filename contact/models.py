from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

# Create your models here.

# id (primary key - automático)
# first_name (string), last_name (string), phone (string)
# email (email), created_date (date), description (text)

# Depois
# show (boolean), owner (foreign key), picture (imagem)
# category (foreign key)  default=True -> valor padrão

# blank=True -> campo  opicional

#verbose_name="Telefone" ->muda o nome do campo

# show -> exibir ou não o contato

class Category(models.Model):
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
        
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, verbose_name="Phone")
    email = models.EmailField(max_length=254, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictureS/%Y/%m/') #python -m pip installPillow
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True 
        )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True 
        )
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    