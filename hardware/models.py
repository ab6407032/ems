from django.db import models
from common.models import BaseModel

class Hardware(BaseModel):
    # Common attributes for all hardware types
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)
    purchase_date = models.DateField()
    warranty_expiration = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True  # This model will not create a separate table
        verbose_name = "Hardware"
        verbose_name_plural = "Hardwares"

    def __str__(self):
        return self.name

class Computer(Hardware):
    # Expanded attributes for computers
    processor = models.CharField(max_length=100)
    ram_capacity = models.IntegerField(help_text="RAM capacity in GB")
    storage_capacity = models.IntegerField(help_text="Storage capacity in GB")
    operating_system = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100, blank=True)
    form_factor = models.CharField(max_length=100, blank=True)  # e.g., Desktop, Laptop, All-in-One

    class Meta:
        verbose_name = "Computer"
        verbose_name_plural = "Computers"

class NetworkDevice(Hardware):
    # Expanded attributes for network devices
    device_type = models.CharField(max_length=100, help_text="E.g., Router, Switch, Modem")
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17)
    network_speed = models.CharField(max_length=100, blank=True)
    port_count = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Network Device"
        verbose_name_plural = "Network Devices"

class Printer(Hardware):
    # Expanded attributes for printers
    printer_type = models.CharField(max_length=100, help_text="E.g., Laser, Inkjet, Dot matrix")
    is_color = models.BooleanField(default=False)
    is_network_printer = models.BooleanField(default=False)
    resolution = models.CharField(max_length=100, blank=True)  # E.g., 1200x1200 DPI
    paper_sizes_supported = models.CharField(max_length=255, blank=True)  # E.g., A4, Letter, Legal

    class Meta:
        verbose_name = "Printer"
        verbose_name_plural = "Printers"

# You can add more child models for other types of devices with their specific attributes
