from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.permissions import IsAdminOrReadOnly
from movies.serializers import MovieSerializer
from movies.models import Movie


class MoviesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get(self, request: Request, movie_id: int = None) -> Response:
        if movie_id:
            try:
                movie = Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                return Response({"details": "Movie not found"}, status=404)

            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=200)

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=200)

    def delete(self, request: Request, movie_id: int) -> Response:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"details": "Movie not found"}, status=404)

        movie.delete()
        return Response(status=204)
