from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import UserProfile, Tournament
from .serializers import TournamentSerializer, TournamentConfirmedSerializer

class TournamentViewSet(ModelViewSet):
	serializer_class = TournamentSerializer
	queryset = Tournament.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
		except ValidationError as e:
			return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save(creator=UserProfile.objects.get(user=request.user.pk))
		except UserProfile.DoesNotExist as e:
			return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	@action(detail=True, methods=['post'], serializer_class = TournamentConfirmedSerializer)
	def confirm(self, request, pk, *args, **kwargs):
		update_tourn = Tournament.objects.get(pk=pk)
		update_tourn.confirmed.clear()

		if 'confirmed' in request.data:
			update_tourn.add_to_confirmed(request.data.get("confirmed"))

		context = "updated confirmed for tournament=%s" % update_tourn.pk
		return Response(context, status=status.HTTP_200_OK)
