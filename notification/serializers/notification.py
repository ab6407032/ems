from notification.models.notification import Template
from rest_framework import  serializers

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ( 'id', 'name', 'used_for', 'subject', 'body', 'body_html', 'used_for', 'active')