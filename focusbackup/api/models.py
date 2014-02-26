# -*- coding: utf-8 -*-

import random
import hashlib

from django.contrib.auth.models import User
from django.db import models


def generate_token():
    """
    Generates a 40 character long token, remember to check for uniqueness when used
    """
    return hashlib.sha1(str(random.random())).hexdigest()


class Token(models.Model):
    """
    Token for accessing curtain API functions
    """
    api_token = models.CharField(default=generate_token(), max_length=40, editable=False)
    api_user = models.OneToOneField(User, related_name="api_tokens")
    active = models.BooleanField(default=True, verbose_name="Is token active")

    def __unicode__(self):
        return "%s" % self.api_token