from django.db import models
from django.utils import timezone
from common.models import BaseModel
from master.models import Keyword, Counter


# class Status:
#     DEFAULT = 0
#     SUCCESS = 1
#     INFO = 2
#     WARNING = 3
#     DANGER = 4
#     STATUS_CHOICES = (
#         (DEFAULT, "secondary"),
#         (SUCCESS, "positive"),
#         (INFO, "primary"),
#         (WARNING, "warning"),
#         (DANGER, "negative"),
#     )


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

class RouterLogFile(BaseModel):
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    upload_date = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()  # Store the size in bytes
    processed = models.BooleanField(default=False)
    metric_calculation = models.BooleanField(default=False)
    traffic_voice_2g = models.FloatField(null=True, blank=True)
    tchdrop = models.FloatField(null=True, blank=True)
    sdcch_drop = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically set the size of the file before saving
        self.size = self.file.size
        self.name = self.file.name
        super().save(*args, **kwargs)

class RouterLogScore(BaseModel):
    logfile = models.OneToOneField(RouterLogFile, null=True, blank=True, default='', on_delete=models.CASCADE)
    traffic_voice_2g = models.FloatField(null=True, blank=True)
    tchdrop = models.FloatField(null=True, blank=True)
    sdcch_drop = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.logfile.name

class RouterLog(BaseModel):
    timestamp = models.DateTimeField(null=True, blank=True, default='')
    logfile = models.ForeignKey(RouterLogFile, null=True, blank=True, default='', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=30, verbose_name="Keyword")
    keyword_no = models.CharField(max_length=50, verbose_name="Keyword No")
    counter_no = models.CharField(max_length=50, verbose_name="Counter No")
    counter_name = models.CharField(max_length=50, verbose_name="Counter Name")
    counter_value = models.IntegerField()

    class Meta:
        verbose_name = "Router Log"
        verbose_name_plural = "Router Logs"

    # def __str__(self):
    #     return self.timestamp + "-" + self.keyword.code + "-" +  self.counter_name
    