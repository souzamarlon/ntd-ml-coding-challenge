from rest_framework import serializers


class DocumentResultSerializer(serializers.Serializer):
    document_type = serializers.CharField()
    entities = serializers.JSONField()


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()