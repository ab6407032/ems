from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    pass


class ActiveKeywordSerailizer(serializers.ListSerializer):

    def to_representation(self, data):
        # data = data.filter(is_active=True)
        return super(ActiveKeywordSerailizer, self).to_representation(data)
