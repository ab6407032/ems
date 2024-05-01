from django.contrib import admin
from .models import Hardware, Computer, NetworkDevice, Printer


class AbstractModelAdmin(admin.ModelAdmin):
    """Classe to dont repeat same fields to all"""

    actions = None
    list_per_page = 15

class HardwareAdmin(AbstractModelAdmin):
    fieldsets = [
        (
            None,
            {"fields": ["name", "serial_number", "manufacturer", "purchase_date", "warranty_expiration", "description"]},
        ),
    ]
    list_display = (
        "name",
        "serial_number",
        "manufacturer",
    )
    search_fields = ["name", "serial_number", "manufacturer"]
    ordering = ("-name",)

class ComputerAdmin(AbstractModelAdmin):
    fieldsets = [
        (
            'Foundation',
            {"fields": ["name", "serial_number", "manufacturer", "purchase_date", "warranty_expiration", "description"]},
        ),
        (
            'Details',
            {"fields": ["processor", "ram_capacity", "storage_capacity", "operating_system", "gpu"]},
        ),
    ]
    list_display = (
        "name",
        "serial_number",
        "manufacturer",
        "processor",
        "operating_system"
    )
    search_fields = ["name", "serial_number", "manufacturer", "processor", "ram_capacity", "storage_capacity", "operating_system", "gpu"]
    ordering = ("-name",)

class NetworkDeviceAdmin(AbstractModelAdmin):
    fieldsets = [
        (
            'Foundation',
            {"fields": ["name", "serial_number", "manufacturer", "purchase_date", "warranty_expiration", "description"]},
        ),
        (
            'Details',
            {"fields": ["device_type", "ip_address", "mac_address", "network_speed", "port_count"]},
        ),
    ]
    list_display = (
        "name",
        "serial_number",
        "manufacturer",
        "device_type"
    )
    search_fields = ["name", "serial_number", "manufacturer", "device_type", "ip_address", "mac_address", "network_speed", "port_count"]
    ordering = ("-name",)

# admin.site.register(Hardware, HardwareAdmin)
admin.site.register(Computer, ComputerAdmin)
admin.site.register(NetworkDevice, NetworkDeviceAdmin)
