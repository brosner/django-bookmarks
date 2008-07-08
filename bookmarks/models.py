from datetime import datetime
import urlparse

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

class Bookmark(models.Model):
    
    url = models.URLField(unique=True)
    description = models.CharField(_('description'), max_length=100)
    note = models.TextField(_('note'), blank=True)
    
    has_favicon = models.BooleanField(_('has favicon'))
    favicon_checked = models.DateTimeField(_('favicon checked'), default=datetime.now)
    
    adder = models.ForeignKey(User, related_name="added_bookmarks", verbose_name=_('adder'))
    added = models.DateTimeField(_('added'), default=datetime.now)

    def get_favicon_url(self):
        base_url = '%s://%s' % urlparse.urlsplit(self.url)[:2]
        favicon_url = urlparse.urljoin(base_url, 'favicon.ico')
        return favicon_url

    
    class Meta:
        ordering = ('-added', )
    
    class Admin:
        list_display = ('url', 'description', 'added', 'adder',)

