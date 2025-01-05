from django.db import models
from django.utils.text import slugify
import itertools

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=100,null=True)
    author = models.CharField(max_length=100,null=True)
    content = models.TextField()
    category = models.CharField(max_length=30,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True,max_length=200,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            for i in itertools.count(1):
                if not post.objects.filter(slug=slug).exists():
                    break
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title