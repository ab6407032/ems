from rest_framework import serializers
from .models import Node, NodeLogFile, NodeMetric

class NodeMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeMetric
        fields = ['metric', 'value']

class NodeLogFileSerializer(serializers.ModelSerializer):
    metrics = NodeMetricSerializer(source='nodemetric_set', many=True)

    class Meta:
        model = NodeLogFile
        fields = ['name', 'size', 'metrics', 'start_time', 'end_time']

class NodeSerializer(serializers.ModelSerializer):
    logfiles = NodeLogFileSerializer(source='nodelogfile_set', many=True)

    class Meta:
        model = Node
        fields = ['id', 'node_name', 'logfiles']
