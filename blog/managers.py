from django.db import models
from django.utils import timezone

# Create your custom database managers here.


class ActivePostManager(models.Manager):
    """
    first we get all objects from the database by
    calling the get_queryset method of the inherited class
    i.e. Manager class using super().get_queryset().
    After that we are filtering objects having city attribute equal to a_posts
    and return the filtered objects.
    """

    def get_queryset(self):
        return super().get_queryset().filter(active=True).exclude(status="0").\
            filter(pub_datetime__lte=timezone.now()).exclude(category__active=False)
