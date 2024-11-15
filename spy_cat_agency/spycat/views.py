from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def destroy(self, request, *args, **kwargs):
        cat = self.get_object()
        if cat.mission:
            return Response(
                {"error": "Cannot delete SpyCat because it is assigned to a mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.prefetch_related('targets').all()
    serializer_class = MissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response({"error": "Cannot delete assigned mission"}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        mission = self.get_object()
        # Prevent updates if mission is completed
        if mission.is_completed:
            return Response({"error": "Cannot update a completed mission."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().partial_update(request, *args, **kwargs)

    def update_targets(self, request, pk=None):
        mission = self.get_object()
        if mission.is_completed:
            return Response({"error": "Cannot update targets for a completed mission."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the target data from the request and update them
        target_data = request.data.get("targets", [])
        for target_info in target_data:
            try:
                target = Target.objects.get(id=target_info['id'], mission=mission)
                if 'notes' in target_info:
                    target.notes = target_info['notes']
                if 'is_completed' in target_info:
                    target.is_completed = target_info['is_completed']
                target.save()
            except Target.DoesNotExist:
                return Response({"error": f"Target with id {target_info['id']} not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Targets updated successfully"}, status=status.HTTP_200_OK)

    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        if mission.cat:
            return Response({"error": "This mission already has an assigned SpyCat."}, status=status.HTTP_400_BAD_REQUEST)

        cat_id = request.data.get("cat_id")
        try:
            cat = SpyCat.objects.get(id=cat_id)
        except SpyCat.DoesNotExist:
            return Response({"error": "SpyCat not found."}, status=status.HTTP_404_NOT_FOUND)

        mission.cat = cat
        mission.save()

        return Response(MissionSerializer(mission).data, status=status.HTTP_200_OK)

