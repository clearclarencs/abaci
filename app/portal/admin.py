from django.contrib import admin
from .models import topic, clss, comment
''' PORTAL APP, ADMIN, For loading databases into admin page to control data from there'''
admin.site.register(topic)
admin.site.register(clss) # Add these models to admin portal for admins to edit data
admin.site.register(comment)