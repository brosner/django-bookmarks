from datetime import datetime
import urlparse

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

"""
A Bookmark is unique to a URL whereas a BookmarkInstance represents a
particular Bookmark saved by a particular person.

This not only enables more than one user to save the same URL as a
bookmark but allows for per-user tagging.
"""

# at the moment Bookmark has some fields that are determined by the
# first person to add the bookmark (the adder) but later we may add
# some notion of voting for the best description and note from
# amongst those in the instances.

class Bookmark(models.Model):
    
    url = models.URLField(unique=True)
    description = models.CharField(_('description'), max_length=100)
    note = models.TextField(_('note'), blank=True)
    
    has_favicon = models.BooleanField(_('has favicon'))
    favicon_checked = models.DateTimeField(_('favicon checked'), default=datetime.now)
    
    adder = models.ForeignKey(User, related_name="added_bookmarks", verbose_name=_('adder'))
    added = models.DateTimeField(_('added'), default=datetime.now)
    
    def get_favicon_url(self, force=False):
        """
        return the URL of the favicon (if it exists) for the site this
        bookmark is on other return None.
        
        If force=True, the URL will be calculated even if it doesn't
        exist.
        """
        if self.has_favicon or force:
            base_url = '%s://%s' % urlparse.urlsplit(self.url)[:2]
            favicon_url = urlparse.urljoin(base_url, 'favicon.ico')
            return favicon_url
        return None
    
    def __unicode__(self):
        return self.url
    
    class Meta:
        ordering = ('-added', )


class BookmarkInstance(models.Model):
    
    bookmark = models.ForeignKey(Bookmark, related_name="saved_instances", verbose_name=_('bookmark'))
    user = models.ForeignKey(User, related_name="saved_bookmarks", verbose_name=_('user'))
    saved = models.DateTimeField(_('saved'), default=datetime.now)
    
    description = models.CharField(_('description'), max_length=100)
    note = models.TextField(_('note'), blank=True)
    
    def save(self):
        try:
            bookmark = Bookmark.objects.get(url=self.url)
        except Bookmark.DoesNotExist:
            bookmark = Bookmark(url=self.url, description=self.description, note=self.note, adder=self.user)
            bookmark.save()
        self.bookmark = bookmark
        super(BookmarkInstance, self).save()
    
    def __unicode__(self):
        return u"%s for %s" % (self.bookmark, self.user)
