from tastypie.resources import ModelResource
from app.backup.models import Customer, Company
from tastypie import fields


class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all()
        resource_name = 'company'
        

class CustomerResource(ModelResource):
    company = fields.ForeignKey(CompanyResource, 'company')

    class Meta:
        queryset = Customer.objects.all()
        resource_name = 'customer'

