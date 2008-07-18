from django.core.management.base import NoArgsCommand

from bookmarks.models import Bookmark, BookmarkInstance

class Command(NoArgsCommand):
    help = 'Creates missing BookInstances from when there were just Bookmarks.'
    
    def handle_noargs(self, **options):
        for bookmark in Bookmark.objects.all():
            print bookmark,
            if bookmark.saved_instances.count() == 0:
                instance = BookmarkInstance(bookmark=bookmark, user=bookmark.adder, saved=bookmark.added, description=bookmark.description, note=bookmark.note)
                # we have to save this way because BookmarkInstance.save() overrides in an undesirable way
                super(BookmarkInstance, instance).save()
                print "[upgraded]"
            else:
                print
