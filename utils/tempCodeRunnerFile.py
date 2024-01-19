    if len(list_contact) > 0:
        Contact.objects.bulk_create(list_contact)