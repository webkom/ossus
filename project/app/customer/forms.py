from django.forms.models import ModelForm
from app.backup.models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('name','address','contact_person','contact_phone' ,'contact_email')
