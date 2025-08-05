from rest_framework import serializers


class URLSerializer(serializers.Serializer):
    original_url = serializers.URLField(max_length=200)
    short_code = serializers.CharField(max_length=6, required=False, allow_blank=True)