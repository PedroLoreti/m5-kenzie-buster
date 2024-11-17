from django.db import models


class RatingChoices(models.TextChoices):

    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, blank=True, default="")
    rating = models.CharField(max_length=20, choices=RatingChoices.choices, default=RatingChoices.G)
    synopsis = models.TextField(blank=True, default="")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="movies")

    users = models.ManyToManyField("users.User", through="movies_orders.MovieOrder", related_name="moviesMany")
