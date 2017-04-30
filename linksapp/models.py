from django.db import models
from django.contrib.auth.models import User

class FavoriteLinksManager(models.Model):
    def get_queryset(self):
        qs = super(FavoriteLinksManager,self).get_queryset()
        return qs.filter(is_favorite=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name

class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    description = models.TextField(blank=True)
    shortened_url = models.URLField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    hits = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)
    owner = models.ForeignKey(User,verbose_name='owner',related_name='links')
    tags = models.ManyToManyField(Tag,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'link'
        verbose_name_plural = 'links'
        ordering = ['-date_created']