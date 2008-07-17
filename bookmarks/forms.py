from django import newforms as forms
from django.utils.translation import ugettext_lazy as _

from bookmarks.models import Bookmark, BookmarkInstance


class BookmarkInstanceForm(forms.ModelForm):
    
    url = forms.URLField(label = "URL", verify_exists=True, widget=forms.TextInput(attrs={"size": 40}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"size": 40}))
    redirect = forms.BooleanField(label="Redirect", required=False)
    
    def __init__(self, *args, **kwargs):
        super(BookmarkInstanceForm, self).__init__(*args, **kwargs)
        # hack to order fields
        self.fields.keyOrder = ['url', 'description', 'note', 'redirect']
                
    def should_redirect(self):
        if self.cleaned_data["redirect"]:
            return True
        else:
            return False
    
    def save(self, commit=True):
        self.instance.url = self.cleaned_data['url']
        return super(BookmarkInstanceForm, self).save(commit)
    
    class Meta:
        model = BookmarkInstance
        #fields = ('url', 'description', 'note', 'redirect')
