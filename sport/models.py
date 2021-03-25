from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s , %s' % (self.name, self.email)

    class Meta:
        verbose_name_plural = _("Enquiry Contacts")
