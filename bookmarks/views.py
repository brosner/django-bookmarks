from datetime import datetime
import urlparse
import urllib2

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkInstanceForm

def bookmarks(request):
    bookmarks = Bookmark.objects.all().order_by("-added")
    
    return render_to_response("bookmarks/bookmarks.html", {
        "bookmarks": bookmarks,
    }, context_instance=RequestContext(request))

@login_required
def add(request):
    
    if request.method == "POST":
        bookmark_form = BookmarkInstanceForm(request.POST)
        if bookmark_form.is_valid():
            bookmark = bookmark_form.save(commit=False)
            bookmark.user = request.user
            
            try:
                headers = {
                    "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                    "Accept-Language" : "en-us,en;q=0.5",
                    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                    "Connection" : "close",
                    ##"User-Agent": settings.URL_VALIDATOR_USER_AGENT
                    }
                req = urllib2.Request(bookmark.get_favicon_url(force=True), None, headers)
                u = urllib2.urlopen(req)
                has_favicon = True
            except:
                has_favicon = False
            
            bookmark.has_favicon = has_favicon
            bookmark.favicon_checked = datetime.now() 
            bookmark.save()
            if bookmark_form.should_redirect():
                return HttpResponseRedirect(bookmark.url)
            else:
                return HttpResponseRedirect(reverse("bookmarks.views.bookmarks"))
    else:
        initial = {}
        if "url" in request.GET:
            initial["url"] = request.GET["url"]
        if "description" in request.GET:
            initial["description"] = request.GET["description"]
        if "redirect" in request.GET:
            initial["redirect"] = request.GET["redirect"]
        
        if initial:
            bookmark_form = BookmarkInstanceForm(initial=initial)
        else:
            bookmark_form = BookmarkInstanceForm()
    
    return render_to_response("bookmarks/add.html", {
        "bookmark_form": bookmark_form,
    }, context_instance=RequestContext(request))
