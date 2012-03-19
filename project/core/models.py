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

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])