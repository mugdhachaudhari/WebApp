from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Form to upload image
class imageUploadForm(forms.Form):
    image = forms.ImageField()
    caption = forms.CharField(required=False)

# Form to edit caption
class imageEditForm(forms.Form):
    caption = forms.CharField(required=False)

# Form to sign up user
class RegistrationForm(forms.Form):
    firstname = forms.CharField(required=False, label=_("First Name"))
    lastname = forms.CharField(required=False, label=_("Last Name"))
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, min_length = 8, render_value=False)), label=_("Password"))

    # It will make sure that username is uniq
    def clean_username(self):
    	try:
    		user = User.objects.get(username__iexact=self.cleaned_data['username'])
    	except User.DoesNotExist:
    		return self.cleaned_data['username']
    	raise forms.ValidationError(_("The username already exists. Please try another one."))