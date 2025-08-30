import os
import random
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 151251251)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return f"post_images/{new_filename}/{final_filename}"

def unique_slug_generator(instance, title, slug_field='slug'):
    slug = slugify(title) if title else f'post-{random.randint(1000,9999)}'
    ModelClass = instance.__class__
    unique_slug = slug
    num = 1
    while ModelClass.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug

class Post(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"

def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.title:
        instance.title = f'Default Post {instance.pk or random.randint(1000,9999)}'
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.title)

pre_save.connect(post_pre_save_receiver, sender=Post)
