from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os
from django.db import models
from django.dispatch import receiver
from django.conf import settings


def upload_to(instance, filename):
    """Store images in 'newsletters/{id}/' directory."""
    return f'newsletters/{instance.id}'

def upload_too(instance, filename):
    """Store images in 'newsletters/{id}/' directory."""
    return f'newsletters/{instance.parent.id}'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="authors", blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True,null=True)

    def __str__(self):
        return self.user.full_name

class Newsletter(models.Model):
    id = models.CharField(max_length=255,unique=True,primary_key=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    banner = models.ImageField(upload_to=upload_to,blank=True,null=True)
    categories = models.ManyToManyField(Category, related_name="newsletters")
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_time = models.CharField(max_length=10,blank=True,null=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name="author_blogs", blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Save the blog, ensuring the ID is available before saving the image."""
        if not self.id:
            super().save(*args, **kwargs)
        self.banner.field.upload_to = upload_to(self, self.banner.name)
        super().save(*args, **kwargs)

class NewsletterBlock(models.Model):
    parent = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name="blocks")
    text = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to=upload_too,blank=True,null=True)
    image_source_text = models.TextField(blank=True,null=True)

    def save(self, *args, **kwargs):
        """Save the blog, ensuring the ID is available before saving the image."""
        if not self.parent.id:
            super().save(*args, **kwargs)
        self.image.field.upload_to = upload_too(self, self.image.name)
        super().save(*args, **kwargs)

@receiver(models.signals.post_delete, sender=Newsletter)
def delete_newsletter_media(sender, instance, **kwargs):
    """Delete newsleter's image folder when the newsletter is deleted."""
    folder_path = os.path.join(settings.MEDIA_ROOT, f'newsletters/{instance.id}/')
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            os.remove(os.path.join(folder_path, file))
        os.rmdir(folder_path)

class Query(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name