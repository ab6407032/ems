from django.db import models
from django.utils import timezone
from common.models import BaseModel
from master.models import Keyword, Counter
import os
from helpers import extract_details
from datetime import datetime, time

def upload_to_original_filename(instance, filename):
    return os.path.join('uploads/', filename)

METRIC_CHOICES = (
        ("iub_throughput_utilization", "IUB throughput utilization"),
        ("voice_traffic", "Voice Traffic"),
        ("nas_success_rate_cs", "NAS success rate cs"),
        ("rrc_success_rate_cs", "RRC success rate cs"),
        ("rrc_success_rate_ps", "RRC success rate ps"),
        ("hs_drop", "HS drop"),
        ("csfb_success_rate", "CSFB success rate"),
    )
class Status:
    DEFAULT = 0
    SUCCESS = 1
    INFO = 2
    WARNING = 3
    DANGER = 4
    STATUS_CHOICES = (
        (DEFAULT, "secondary"),
        (SUCCESS, "positive"),
        (INFO, "primary"),
        (WARNING, "warning"),
        (DANGER, "negative"),
    )
    


# class Host(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=200, blank=True)
#     ipv4 = models.GenericIPAddressField(protocol="IPv4")
#     last_check = models.DateTimeField("last check", default=timezone.now)
#     last_status_change = models.DateTimeField(
#         "last status change", default=timezone.now
#     )
#     status_info = models.CharField(max_length=200, blank=True, default="")
#     network = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True)
#     circuit = models.IntegerField(null=True, blank=True)
#     retries = models.IntegerField(default=0)
#     max_retries = models.IntegerField(default=1)
#     local = models.CharField(max_length=200, null=True, blank=True)
#     switch_manager = models.IntegerField(null=True, blank=True, default=0)
#     status = models.IntegerField(choices=Status.STATUS_CHOICES, default=Status.DEFAULT)

#     def __str__(self):
#         return self.name

#     @property
#     def ports(self):
#         return Port.objects.filter(host=self)

#     @property
#     def monitored_ports(self):
#         return Port.objects.filter(host=self, is_monitored=True)


# class Port(models.Model):
#     """Ports used to check status using telnet"""

#     host = models.ForeignKey(Host, on_delete=models.CASCADE)
#     number = models.CharField(max_length=20)
#     is_monitored = models.BooleanField(default=False)
#     counter_status = models.IntegerField(
#         choices=Status.STATUS_CHOICES, default=Status.DEFAULT
#     )
#     counter_last_change = models.DateTimeField(
#         "last status change", default=timezone.now
#     )
#     error_counter = models.BigIntegerField(default=0)

#     def __str__(self):
#         return self.number


# class Dio(models.Model):

#     pop = models.ForeignKey(Host, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name


# class Fiber(models.Model):
    
#     dio = models.ForeignKey(Dio, on_delete=models.CASCADE)
#     number = models.CharField(max_length=20)
#     port = models.CharField(max_length=20, blank=True, default="")
#     description = models.CharField(max_length=200, blank=True)

#     def __str__(self):
#         return self.number


# class HostLog(models.Model):
#     """Host Logs showed in host detail view"""

#     host = models.ForeignKey(Host, on_delete=models.CASCADE)
#     status = models.IntegerField(choices=Status.STATUS_CHOICES, default=Status.DEFAULT)
#     status_change = models.DateTimeField()
#     status_info = models.CharField(max_length=200, blank=True, default="")

#     def __str__(self):
#         return self.host.name


# class PortLog(models.Model):
#     """Port Logs showed in host detail view"""

#     port = models.ForeignKey(Port, on_delete=models.CASCADE, null=True)
#     host = models.ForeignKey(Host, on_delete=models.CASCADE, null=True)
#     counter_status = models.IntegerField(
#         choices=Status.STATUS_CHOICES, default=Status.DEFAULT
#     )
#     counter_last_change = models.DateTimeField(
#         "last status change", default=timezone.now
#     )
#     error_counter = models.IntegerField(default=0)

#     def __str__(self):
#         return self.port.number

class Node(BaseModel):
    node_name = models.CharField(max_length=100)
    active =  models.BooleanField(default=True)

    def __str__(self):
        return f"{self.node_name}"

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"

class NodeLogFile(BaseModel):
    node = models.ForeignKey(Node, null=True, blank=True, default='', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_original_filename)
    name = models.TextField(null=True, blank=True, default='')
    upload_date = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()  # Store the size in bytes
    processed = models.BooleanField(default=False)
    metric_calculation = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True, default=None)
    end_time = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('node', 'file')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically set the size of the file before saving
        self.size = self.file.size
        self.name = self.file.name
        super().save(*args, **kwargs)

class NodeMetric(BaseModel):
    node = models.ForeignKey(Node, null=True, blank=True, default='', on_delete=models.CASCADE)
    logfile = models.ForeignKey(NodeLogFile, null=True, blank=True, default='', on_delete=models.CASCADE)
    metric = models.CharField(max_length = 255, choices=METRIC_CHOICES, default='', null=True, blank=True, )
    value = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('node', 'logfile', 'metric')

    def __str__(self):
        return f"{self.node.node_name} {self.logfile.name}"

    