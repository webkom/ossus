from app.backup.models import Company
from core.templatetags.menu_tags import active
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    company = models.ForeignKey(Company, blank=True, null=True)

    def set_company(self, company):
        self.company = company
        self.save()

    def get_available_companies(self):

        company_ids = []

        for company in Company.objects.all():
            if self.user in company.users.all():
                company_ids.append(company.id)

        return Company.objects.filter(id__in=company_ids)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])