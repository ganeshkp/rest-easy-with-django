from rest_framework import serializers
from datetime import datetime

class CustomDateTimeSerializerField(serializers.Field):
    def to_representation(self, value):
        # Convert the datetime object to a custom date format for the API response
        # For example: 2023-07-30T12:34:56 -> "30 Jul 2023, 12:34 PM"
        return value.strftime('%d %b %Y, %I:%M %p')

    def to_internal_value(self, data):
        # Parse the incoming date string back to a datetime object
        # For example: "2023-07-30T12:34:56" -> datetime.datetime(2023, 7, 30, 12, 34, 56)
        try:
            return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            raise serializers.ValidationError("Invalid date format.")
        
class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)
        return {"id": value.pk}
    
class MyHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):

    def to_representation(self, value):
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)
        return {"id": value.pk}
    
class CustomHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        url = super().get_url(obj, view_name, request, format)
        return f"{url}?name={obj.name}"  # Append the platform's name as a query parameter

    def to_representation(self, value):
        representation = super().to_representation(value)
        return f"{representation} ({value.name})"  # Add the platform's name to the representation
    
class CustomChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        # Custom representation of the choice field value
        # Here, we convert the value to lowercase
        return value.lower()