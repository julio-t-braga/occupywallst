r"""

    occupywallst.feeds
    ~~~~~~~~~~~~~~~~~~

    Tools for syndicating articles via RSS and stuff.

    Some delay is added before publishing content to allow people to
    sneak in ninja edits if necessary.  This is currently set to 15
    minutes for articles and 5 minutes for comments.

"""

import re
from datetime import datetime, timedelta

from django.contrib.syndication.views import Feed

from occupywallst import models as db


class RSSNewsFeed(Feed):
    title = "OccupyWallSt News"
    link = "https://occupywallst.org/"
    description = "News and updates relating to the Sept. 17th protest"
    description_template = 'occupywallst/feed-article.html'
    delay = timedelta(seconds=60 * 15)

    def items(self):
        return (db.Article.objects
                .filter(is_deleted=False, is_visible=True,
                        published__lt=datetime.now() - self.delay)
                .order_by('-published'))[:10]

    def item_title(self, article):
        return article.title

    def item_pubdate(self, article):
        return article.published

    def item_author_name(self, article):
        return article.author.username

    def item_author_link(self, article):
        return article.author.userinfo.get_absolute_url()


class RSSCommentFeed(Feed):
    title = "OccupyWallSt Comments"
    link = "https://occupywallst.org/"
    description = "Comments users posted on news articles"
    description_template = 'occupywallst/feed-comment.html'
    delay = timedelta(seconds=60 * 5)

    def items(self):
        return (db.Comment.objects
                .filter(is_deleted=False, is_removed=False,
                        published__lt=datetime.now() - self.delay)
                .order_by('-published'))[:50]

    def item_title(self, comment):
        return re.split(r'\s+', comment.content)[:7]

    def item_pubdate(self, comment):
        return comment.published

    def item_author_name(self, comment):
        return comment.user.username

    def item_author_link(self, comment):
        return comment.user.userinfo.get_absolute_url()