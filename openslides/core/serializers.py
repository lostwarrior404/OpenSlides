from openslides.utils.rest_api import Field, ModelSerializer, ValidationError

from .models import ChatMessage, ProjectionDefault, Projector, Tag


class JSONSerializerField(Field):
    """
    Serializer for projector's JSONField.
    """
    def to_internal_value(self, data):
        """
        Checks that data is a dictionary. The key is a hex UUID and the
        value is a dictionary with must have a key 'name'.
        """
        if type(data) is not dict:
            raise ValidationError({'detail': 'Data must be a dictionary.'})
        for element in data.values():
            if type(element) is not dict:
                raise ValidationError({'detail': 'Data must be a dictionary.'})
            elif element.get('name') is None:
                raise ValidationError({'detail': "Every dictionary must have a key 'name'."})
        return data


class ProjectionDefaultSerializer(ModelSerializer):
    """
    Serializer for core.models.ProjectionDefault objects.
    """
    class Meta:
        model = ProjectionDefault
        fields = ('id', 'name', 'display_name', 'projector', )


class ProjectorSerializer(ModelSerializer):
    """
    Serializer for core.models.Projector objects.
    """
    config = JSONSerializerField(write_only=True)
    projectiondefaults = ProjectionDefaultSerializer(many=True, read_only=True)

    class Meta:
        model = Projector
        fields = ('id', 'config', 'elements', 'scale', 'scroll', 'name', 'blank', 'width', 'height', 'projectiondefaults', )
        read_only_fields = ('scale', 'scroll', 'blank', 'width', 'height', )


class TagSerializer(ModelSerializer):
    """
    Serializer for core.models.Tag objects.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', )


class ChatMessageSerializer(ModelSerializer):
    """
    Serializer for core.models.ChatMessage objects.
    """
    class Meta:
        model = ChatMessage
        fields = ('id', 'message', 'timestamp', 'user', )
        read_only_fields = ('user', )
