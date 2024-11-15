from rest_framework import serializers

from .models import Mission, SpyCat, Target
from .utils import is_valid_breed


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']
        
        def validate_breed(self, value):
            if not is_valid_breed(value):
                raise serializers.ValidationError("Invalid breed.")
            return value


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "name", "country", "notes", "is_completed"]
        read_only_fields = ["id", "is_completed"]

    def validate_notes(self, value):
        # Prevent updating notes if target or mission is completed
        target = self.instance
        if target and target.mission.is_completed:
            raise serializers.ValidationError("Cannot update notes for a completed mission.")
        return value

    def validate(self, data):
        if self.instance and self.instance.mission.is_completed:
            if data.get('notes') != self.instance.notes:
                raise serializers.ValidationError("Cannot update notes for a completed mission.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)  # Accept multiple targets in the request

    class Meta:
        model = Mission
        fields = ["id", "cat", "is_completed", "targets"]
        read_only_fields = ["id", "is_completed"]

    def create(self, validated_data):
        targets_data = validated_data.pop('targets', [])
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', [])
        instance = super().update(instance, validated_data)
        # Update targets if present
        if targets_data:
            for target_data in targets_data:
                target = Target.objects.get(id=target_data['id'])
                target.name = target_data.get('name', target.name)
                target.country = target_data.get('country', target.country)
                target.notes = target_data.get('notes', target.notes)
                target.is_completed = target_data.get('is_completed', target.is_completed)
                target.save()
        return instance
