from django.core.management.base import BaseCommand, CommandError
from sd.models import Author, Post
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.delete_author()

    def delete_author(self):
        # referencing: https://vilimpoc.org/blog/2013/07/04/django-testing-creating-and-removing-test-users/
        # test_author = Author.objects.filter(Q(username='Selenium'))
        # test_author = Author.objects.get(username="Selenium")
        posts = Post.objects.all()
        print(posts)