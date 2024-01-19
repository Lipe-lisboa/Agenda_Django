from contact.models import Contact 
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation



class ContactForm(forms.ModelForm):
    
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs= {
                'placeholder': 'Your name',
            }
        ),
        
        label='first_name', #posso mudar se quiser
        help_text='Menssagem de ajuda'
    )
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept':'image/',
            }
        ),
        required=False
    )
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        #self.fields['first_name'].widget.attrs.update({
        #    'placeholder': 'Your name'
        #})
        
        
    class Meta:
        model = Contact
        fields = 'first_name', 'last_name', 'phone', 'email','description', 'category','picture'
        
        
        #widgets = {
            # mudar o type do campo
        #    'first_name' : forms.TextInput(
        #        attrs={
        #            'placeholder': 'Your name'
        #        }
        #        ) 
        #}
        
    def clean(self):
        # esse metodo tem acesso a todos os campo do form
        # ele pega os dados enviados antes de serem salvos
        
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name == last_name:
            
            msg_erro = ValidationError(
                'o primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            
            self.add_error(
                'first_name',
                msg_erro
            )
            self.add_error(
                'last_name',
                msg_erro
            )
            
        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == "abc":
            self.add_error(
                'first_name',
                ValidationError(
                    'não digite abc',
                    code='invalid'
                )
            ) 
                 
        return first_name
    
    
class RegisterForm(UserCreationForm):
    
    first_name = forms.CharField(
        required=True,
        min_length= 3,
    )
    
    last_name = forms.CharField(
        required=True,
        min_length= 3,
    )
    
    email = forms.EmailField()
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )
    def clean(self):    
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name == last_name:
            
            msg_erro = ValidationError(
                'o primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            
            self.add_error(
                'first_name',
                msg_erro
            )
            self.add_error(
                'last_name',
                msg_erro
            )
            
        return super().clean()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Ja existe esse email', code='invalid')
            )
        
        
        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )
        
    def save(self, commit=True):
        cleaned_date = self.cleaned_data
        user = super().save(commit=False)
        
        password1 = cleaned_date.get('password1')
        
        if password1:
            user.set_password(password1)
            
        if commit:
            user.save()
        
        return user
        
    def clean(self):
        passsword1 = self.cleaned_data.get('password1')
        passsword2 = self.cleaned_data.get('password2')
        
        if passsword1 or passsword2:
            if passsword1 != passsword2:
                self.add_error(
                    'password2',
                    ValidationError('senhas não batem', code='invalid')
                )
                
        return super().clean()
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_atual = self.instance.email
        
        if email_atual != email:
            if User.objects.filter(email=email_atual).exists():
                self.add_error(
                    'email',
                    ValidationError('Ja existe esse email', code='invalid')
                )
        
        
        return email
    
    def clean_password1(self):
        password1= self.cleaned_data.get('password1')
        
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as erros:
                self.add_error(
                    'password1',
                    ValidationError(erros)
                )
        return password1