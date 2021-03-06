from django.db import models
from django.utils import timezone, html
from django.urls import reverse
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.core.mail import send_mail
from django.core.validators import RegexValidator

class Post(models.Model):
    author= CurrentUserField()
    title=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True, null=True)
    published_date=models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def send_emails(self):
        send_mail(self.title,html.strip_tags(self.text),"bulletinsrm@gmail.com",list(Subscription.objects.all().values_list('official_email',flat=True)), html_message=self.text , fail_silently = False)


    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey('News.Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now)
    approved_comment=models.BooleanField(default=False)

    def approve(self):
        self.approved_comment= True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text

class Subscription(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    official_email = models.EmailField(max_length=254)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)

    def __str__(self):
        return self.official_email

