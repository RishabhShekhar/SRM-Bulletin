from django.contrib import admin
from News.models import Post,Comment,Subscription
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Subscription)
