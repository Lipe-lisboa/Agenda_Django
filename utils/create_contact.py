import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000


sys.path.append(str(DJANGO_BASE_DIR))
os.environ ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    from faker import Faker
    import faker
    
    from contact.models import Category, Contact
    
    Category.objects.all().delete()
    Contact.objects.all().delete()
    
    fake: faker= Faker('pt_BR')
    
    categories = ['Family', 'Friends', 'colleagues']
    
    list_category = [Category(name=name) for name in categories]
    
    for category in list_category:
        category.save()
        
        
    list_contact = []
    
    for i in range(NUMBER_OF_OBJECTS):
        profile = fake.profile()
        firts_name, last_name = profile['name'].split(' ', 1)
        email = profile['mail']
        phone = fake.phone_number()
        date: datetime = fake.date_this_year()
        description = fake.text(max_nb_chars=100)
        category = choice(list_category)
        
        list_contact.append(
            Contact(
                first_name=firts_name,
                last_name=last_name,
                phone=phone,
                email=email,
                created_date=date,
                description=description,
                category=category,
            )
        )
        
    if len(list_contact) > 0:
        Contact.objects.bulk_create(list_contact)
    
        

        
        
    