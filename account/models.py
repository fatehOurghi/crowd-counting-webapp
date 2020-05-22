from djongo import models
from datetime import datetime as dt
from django.conf import settings 
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
root_path = ""

User = get_user_model()


class Language(models.Model):
    language = models.CharField(max_length=32, default="English", primary_key=True)

    def __str__(self):
        return self.language

    def as_json(self):
        doc = {
            "language": self.language
        }
        return doc


class GeneralSetting(models.Model):
    user = models.ForeignKey(User, 
                        default = 1, 
                        null = True,  
                        on_delete = models.CASCADE 
                        )
    language = models.ForeignKey(to=Language, on_delete=models.PROTECT)
    display_framerate = models.IntegerField(default=20) # in fps
    db_event_lifetime = models.IntegerField(default=30) # in days

    def as_json(self):
        doc = {
            "language": self.language.__str__(),
            "display_framerate": self.display_framerate,
            "db_event_lifetime": self.db_event_lifetime
        }
        return doc


class EmailSetting(models.Model):
    user = models.ForeignKey(User, 
                        default = 1, 
                        null = True,  
                        on_delete = models.CASCADE 
                        )
    notification_email = models.EmailField(default="notifyme@example.com")
    smtp_server = models.CharField(default="smtp.gmail.com", max_length=32)
    server_port = models.IntegerField(default=587)
    login = models.EmailField(default="login@example.com")
    password = models.CharField(default="login_password", max_length=32)

    def as_json(self):
        doc = {
            "notification_email": self.notification_email,
            "smtp_server": self.smtp_server,
            "server_port": self.server_port,
            "login": self.login,
            "password": self.password
        }
        return doc


class Scenario(models.Model):
    name = models.CharField(default="Camera events disabled", max_length=64, unique=True) # crowd counting, motion detection, PAR, ... default Camera events disabled
    description = models.TextField(max_length=255)
    
    def __str__(self):
        return self.name

    def as_json(self):
        doc = {
            "name": self.name,
            "description": self.description
        }
        return doc


class Model(models.Model):
    DEPTH = (
        (1, 'GRAY'),
        (3, 'RGB')
    )
    ORDER = (
        ("bdhw","batch_size, depth, height, width"),
        ("bdwh","batch_size, depth, width, height"),
        ("bhwd","batch_size, height, width, depth"),
        ("bhdw","batch_size, height, depth, width"),
        ("bwdh","batch_size, width, depth, height"),
        ("bwhd","batch_size, width, height, depth"),
        ("wbhd","width, batch_size, height, depth"),
        ("wbdh","width, batch_size, depth, height"),
        ("whdb","width, height, depth, batch_size"),
        ("whbd","width, height, batch_size, depth"),
        ("wdbh","width, depth, batch_size, height"),
        ("wdhb","width, depth, height, batch_size"),
        ("hdwb","height, depth, width, batch_size"),
        ("hdbw","height, depth, batch_size, width"),
        ("hwbd","height, width, batch_size, depth"),
        ("hwdb","height, width, depth, batch_size"),
        ("hbdw","height, batch_size, depth, width"),
        ("hbdw","height, batch_size, width, depth"),
        ("dbwh","depth, batch_size, width, height"),
        ("dbhw","depth, batch_size, height, width"),
        ("dwhb","depth, width, height, batch_size"),
        ("dwbh","depth, width, batch_size, height"),
        ("dhbw","depth, height, batch_size, width"),
        ("dhwb","depth, height, width, batch_size"),
    )
    user = models.ForeignKey(User, 
                        default = 1, 
                        null = True,  
                        on_delete = models.CASCADE 
                        )
    model_name = models.CharField(max_length=32)
    model_framework = models.CharField(max_length=32)
    date_added = models.DateTimeField(default=dt.utcnow)
    in_batchsize = models.IntegerField(default=1)
    in_height = models.IntegerField(default=0)
    in_width = models.IntegerField(default=0)
    in_depth = models.IntegerField(default=1, choices=DEPTH)
    out_batchsize = models.IntegerField(default=1)
    out_height = models.IntegerField(default=0)
    out_width = models.IntegerField(default=0)
    out_depth = models.IntegerField(default=1, choices=DEPTH)
    shape_order = models.CharField(max_length=4, choices=ORDER)
    is_converted = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model_name}: {self.model_framework}"

    def as_json(self):
        doc = {
            "model_name": self.model_name,
            "model_framework": self.model_framework,
            "date_added": self.date_added,
            "input_shape": [self.in_batchsize, self.in_height, self.in_width, self.in_depth],
            "output_shape": [self.out_batchsize, self.out_height, self.out_width, self.out_depth],
            "shape_order": self.shape_order,
            "is_converted": self.is_converted,
            "is_public": self.is_public
        }
        return doc
    def input_shape(self):
        doc = {
            "batch_size": self.in_batchsize,
            "height": self.in_height,
            "width": self.in_width,
            "depth": self.in_depth,
            "order": self.shape_order
        }
        return doc


class Camera(models.Model):
    DEPTH = (
        (1, 'GRAY'),
        (3, 'RGB')
    )
    user = models.ForeignKey(User, 
                        default = 1, 
                        null = True,  
                        on_delete = models.CASCADE 
                        )
    name = models.CharField(default="Not Specified", max_length=32, blank=True)
    is_enabled = models.BooleanField(default=False)
    logging = models.BooleanField(default=False)
    email_notification = models.BooleanField(default=False)
    crowd_threshold = models.IntegerField(default=20)
    position = models.CharField(default="Not Specified", max_length=64)
    output_width = models.IntegerField(default=720)
    output_height = models.IntegerField(default=480)
    output_depth = models.IntegerField(default=1, choices=DEPTH)
    camera_usage_scenario = models.ForeignKey(to=Scenario, on_delete=models.PROTECT)
    model_used = models.ForeignKey(to=Model, on_delete=models.PROTECT)
    def __str__(self):
        return self.name

    def as_json(self):
        doc = {
            "used_model": self.model_used.model_name,
            "name": self.name,
            "is_enabled": self.is_enabled,
            "logging": self.logging,
            "email_notification": self.email_notification,
            "crowd_threshold": self.crowd_threshold,
            "position": self.position,
            "output_width": self.output_width,
            "output_height": self.output_height,
            "output_depth": self.output_depth,
            "camera_usage_scenario": self.camera_usage_scenario.__str__()
        }
        return doc


class Event(models.Model):
    user = models.ForeignKey(User, 
                        default = 1, 
                        null = True,  
                        on_delete = models.CASCADE 
                        )
    event_time = models.DateTimeField(default=dt.utcnow)
    event_type = models.CharField(max_length=32)
    event_name = models.CharField(max_length=32)
    count = models.IntegerField(default=0)
    media_type = models.CharField(default="image", max_length=32) # video or image
    media_path = models.CharField(default=root_path + "/media", max_length=64) # link to location of media associated to the event
    heatmap = models.CharField(default=root_path + "/media", max_length=64) # link to location of media heatmap associated to the event
    camera = models.ForeignKey(to=Camera, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.event_name}: {self.event_type}, count: {self.count}"

    def as_json(self):
        doc = {
            "event_time": self.event_time,
            "event_type": self.event_type,
            "event_name": self.event_name,
            "count": self.count,
            "media_type": self.media_type,
            "media_path": self.media_path,
            "heatmap": self.heatmap,
            "camera": self.camera.__str__()
        }
        return doc


class ServerConfig(models.Model):
    SERVERS = (
        ("INFERENCE", "Inference Server"),
        ("CONVERSION", "Conversion Server")
    )
    server_name = models.CharField(max_length=16, choices=SERVERS)
    url = models.CharField(max_length=32, default="http://127.0.0.1")
    port = models.IntegerField(default=8001)
    def __str__(self):
        return "{} on {}:{}".format(self.server_name, self.url, self.port)
    
    def as_json(self):
        doc = {
            "server_name": self.server_name,
            "url": self.url,
            "port": self.port
        }
        return doc

    def full_url(self):
        return "{}:{}".format(self.url, self.port)