from rest_framework import fields, serializers

from db.models.notebooks import NotebookJob
from db.models.tensorboards import TensorboardJob
from libs.spec_validation import validate_notebook_spec_config, validate_tensorboard_spec_config


class PluginJobBaseSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'user',
            'name',
            'config',
            'tags',  # Need ti implement TagsSerializerMixin
        )

    def get_user(self, obj):
        return obj.user.username

    def _validate_spec(self, config):
        pass

    def validate_config(self, config):
        # content is optional
        if not config:
            return config

        self._validate_spec(config)
        # Resume normal creation
        return config


class TensorboardJobSerializer(PluginJobBaseSerializer):
    def _validate_spec(self, config):
        validate_tensorboard_spec_config(config)

    class Meta(PluginJobBaseSerializer.Meta):
        model = TensorboardJob


class NotebookJobSerializer(PluginJobBaseSerializer):
    def _validate_spec(self, config):
        validate_notebook_spec_config(config)

    class Meta(PluginJobBaseSerializer.Meta):
        model = NotebookJob
        fields = PluginJobBaseSerializer.Meta.fields + ('data_refs',)


class ProjectTensorboardJobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()

    class Meta:
        model = TensorboardJob
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'user',
            'description',
            'created_at',
            'updated_at',
            'started_at',
            'finished_at',
            'last_status',
            'tags',
            'project',
            'experiment_group',
            'experiment',
        )

    def get_user(self, obj):
        return obj.user.username

    def get_project(self, obj):
        return obj.project.unique_name
