from rest_framework import serializers
from datetime import datetime


class CustomDateTimeField(serializers.Field):
    def to_internal_value(self, data: dict) -> datetime:
        date_string = data["$date"]
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")

    def to_representation(self, value: datetime) -> dict:
        return {"$date": value.strftime("%Y-%m-%dT%H:%M:%S.%f%z")}


class CustomListField(serializers.ListField):
    """Deletes all empty strings from list"""

    def to_internal_value(self, data: list[str]) -> list[str]:
        for value in data:
            if value == "":
                data.remove(value)
        return super().to_internal_value(data)
