from django.core.exceptions import ValidationError
from django.db import models

class SpyCat(models.Model):
    name = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Check if the SpyCat has an associated mission safely
        try:
            if self.mission:
                raise ValidationError("Cannot delete SpyCat because it is assigned to a mission.")
        except SpyCat.mission.RelatedObjectDoesNotExist:
            pass  # No mission, safe to delete
        super().delete(*args, **kwargs)


class Mission(models.Model):
    cat = models.OneToOneField(SpyCat, null=True, blank=True, on_delete=models.SET_NULL, related_name="mission")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.id}"

    def delete(self, *args, **kwargs):
        if self.cat:  # If Mission has an associated SpyCat
            raise ValidationError("Cannot delete mission because it is assigned to a SpyCat.")
        super().delete(*args, **kwargs)


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Prevent modifications if mission is completed
        if self.mission.is_completed and not self.is_completed:
            raise ValidationError("Cannot modify target for a completed mission.")
        if self.is_completed and self.notes:
            self.notes = None  # Prevent updating notes once a target is completed.
        super().save(*args, **kwargs)
