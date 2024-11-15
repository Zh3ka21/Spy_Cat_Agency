import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound

from .models import Mission, SpyCat, Target
from .serializers import MissionSerializer, SpyCatSerializer, TargetSerializer


@pytest.mark.django_db
class TestSpyCatModel:

    def test_create_spycat(self):
        # Create a SpyCat instance
        cat = SpyCat.objects.create(name="Cat A", years_of_experience=5, breed="Siamese", salary=50000.00)

        # Test if it was created
        assert SpyCat.objects.count() == 1
        assert cat.name == "Cat A"
        assert cat.years_of_experience == 5
        assert cat.salary == 50000.00

    def test_update_spycat_salary(self):
        # Create a SpyCat instance
        cat = SpyCat.objects.create(name="Cat B", years_of_experience=3, breed="Bengal", salary=40000.00)

        # Update the salary
        cat.salary = 45000.00
        cat.save()

        # Test if the salary is updated
        cat.refresh_from_db()
        assert cat.salary == 45000.00

    def test_delete_spycat_assigned_to_mission(self):
        # Create a SpyCat and Mission
        cat = SpyCat.objects.create(name="Cat C", years_of_experience=4, breed="Persian", salary=60000.00)
        mission = Mission.objects.create(cat=cat)

        # Try to delete the SpyCat assigned to a mission
        with pytest.raises(ValidationError):
            cat.delete()  # This will raise ValidationError

    def test_delete_spycat_not_assigned_to_mission(self):
        # Create a SpyCat with no assigned mission
        cat = SpyCat.objects.create(name="Cat D", years_of_experience=6, breed="Sphynx", salary=70000.00)

        # Now delete the SpyCat
        cat.delete()

        # Test if the SpyCat is deleted
        assert SpyCat.objects.count() == 0

    def test_list_spycats(self):
        # Create two SpyCats
        SpyCat.objects.create(name="Cat E", years_of_experience=7, breed="Maine Coon", salary=80000.00)
        SpyCat.objects.create(name="Cat F", years_of_experience=5, breed="Siberian", salary=65000.00)

        # List all SpyCats
        spycats = SpyCat.objects.all()

        # Test if the number of SpyCats is correct
        assert spycats.count() == 2

    def test_get_single_spycat(self):
        # Create a SpyCat
        cat = SpyCat.objects.create(name="Cat G", years_of_experience=8, breed="Scottish Fold", salary=55000.00)

        # Get a single SpyCat by ID
        spycat = SpyCat.objects.get(id=cat.id)

        # Test if we correctly get the SpyCat
        assert spycat.name == "Cat G"
        assert spycat.salary == 55000.00


@pytest.mark.django_db
class TestMissionModel:

    def test_create_mission_with_targets(self):
        # Create a SpyCat
        cat = SpyCat.objects.create(name="Cat H", years_of_experience=5, breed="Siamese", salary=50000.00)

        # Create a Mission with targets
        mission_data = {
            "cat": cat.id,
            "is_completed": False,
            "targets": [
                {"name": "Target 1", "country": "USA", "notes": "Important", "is_completed": False},
                {"name": "Target 2", "country": "Germany", "notes": "Sensitive", "is_completed": False}
            ]
        }
        mission_serializer = MissionSerializer(data=mission_data)
        mission_serializer.is_valid(raise_exception=True)
        mission_serializer.save()

        # Test if the mission is created with targets
        mission = Mission.objects.first()
        assert mission.targets.count() == 2
        assert mission.cat.name == "Cat H"

    def test_update_mission_targets(self):
        # Create a SpyCat and Mission
        cat = SpyCat.objects.create(name="Cat I", years_of_experience=6, breed="Sphynx", salary=70000.00)
        mission = Mission.objects.create(cat=cat)
        target = Target.objects.create(mission=mission, name="Target 1", country="USA", notes="Important", is_completed=False)

        # Update target's notes
        target.notes = "Updated Notes"
        target.save()

        # Test if the notes are updated
        target.refresh_from_db()
        assert target.notes == "Updated Notes"

    def test_delete_mission_assigned_to_spycat(self):
        # Create a SpyCat and Mission
        cat = SpyCat.objects.create(name="Cat J", years_of_experience=4, breed="British Shorthair", salary=45000.00)
        mission = Mission.objects.create(cat=cat)

        # Try to delete the Mission assigned to a SpyCat
        with pytest.raises(ValidationError):
            mission.delete()  # This will raise ValidationError in the Mission model

    def test_delete_mission_not_assigned_to_spycat(self):
        # Create a Mission without a SpyCat
        mission = Mission.objects.create(cat=None)

        # Now delete the Mission
        mission.delete()

        # Test if the mission is deleted
        assert Mission.objects.count() == 0

    def test_assign_cat_to_mission(self):
        # Create a SpyCat and Mission
        cat = SpyCat.objects.create(name="Cat K", years_of_experience=6, breed="Bengal", salary=65000.00)
        mission = Mission.objects.create(cat=None)

        # Assign the SpyCat to the Mission
        mission.cat = cat
        mission.save()

        # Test if the SpyCat is assigned
        mission.refresh_from_db()
        assert mission.cat == cat

    def test_list_missions(self):
        # Create a Mission
        cat = SpyCat.objects.create(name="Cat L", years_of_experience=3, breed="Maine Coon", salary=50000.00)
        Mission.objects.create(cat=cat)

        # List all missions
        missions = Mission.objects.all()

        # Test if the number of Missions is correct
        assert missions.count() == 1

    def test_get_single_mission(self):
        # Create a SpyCat and Mission
        cat = SpyCat.objects.create(name="Cat M", years_of_experience=5, breed="Siberian", salary=75000.00)
        mission = Mission.objects.create(cat=cat)

        # Get a single Mission by ID
        mission_from_db = Mission.objects.get(id=mission.id)

        # Test if we correctly get the Mission
        assert mission_from_db.id == mission.id
        assert mission_from_db.cat.name == "Cat M"

