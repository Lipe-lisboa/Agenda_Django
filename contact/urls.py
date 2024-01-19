from django.urls import path
from contact import views


app_name ='contact'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    
    # contact (GRUD)
    path('contact/<int:contact_id>/', views.contact, name='contact'),
    path('contact/create/', views.create, name='create'), #logada
    path('contact/<int:contact_id>/update/', views.update, name='update'), #logada e dona do contacto
    path('contact/<int:contact_id>/delete/', views.delete, name='delete'), #logada e dona do contacto
    
    
    #user
    path('user/create/', views.register, name='register'), #não logado
    path('user/login/', views.login_view, name='login'), # nao logado
    path('user/logout/', views.logout_view, name='logout'), #logado
    path('user/update/', views.user_update, name='user_update') #logado
       
]
