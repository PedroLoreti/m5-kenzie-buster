from rest_framework.views import APIView
from rest_framework.response import Response
from movies.models import Movie
from movies_orders.serializers import MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class MoviesOrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id: int = None):
        if movie_id:
            try:
                movie = Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                return Response({"details": "Movie not found"}, status=404)

        serializer = MovieOrderSerializer(data=request.data, context={"request": request, "movie": movie})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
