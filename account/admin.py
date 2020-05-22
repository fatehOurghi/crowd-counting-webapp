from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Language, GeneralSetting, EmailSetting, Scenario, Camera, Event, Model, ServerConfig])