import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from .models import Answer, ErrorPost


class IndexSitemap(Sitemap):
    changfreq = 'daily'
    priority = 1

    def items(self):
        return ['error_posts:list']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        try:
            item = ErrorPost.publisheds.latest('modified')
            return item.answers.latest('modified').modified
        except ErrorPost.DoesNotExist:
            return datetime.date.today()
        except Answer.DoesNotExist:
            return item.modified


class ErrorPostSitemap(Sitemap):
    changfreq = 'daily'
    priority = 0.5

    def items(self):
        return ErrorPost.publisheds.all()

    def location(self, item):
        return reverse('error_posts:detail', kwargs={'slug': item.slug})

    def lastmod(self, item):
        try:
            return item.answers.latest('modified').modified
        except Answer.DoesNotExist:
            return item.modified
