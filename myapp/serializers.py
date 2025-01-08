from rest_framework import serializers
import re


class TextRequestSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=5000)
    length = serializers.IntegerField(default=100, min_value=10)

    def validate_text(self, value):
        # Ensure the text starts with an uppercase letter and has at least 10 words
        if len(value.split()) < 10:
            raise serializers.ValidationError("Text must be at least 10 words long.")
        if not value[0].isupper():
            raise serializers.ValidationError("Text must start with an uppercase letter.")
        return value
