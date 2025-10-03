from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} by {self.artist}"

class UserProfile(models.Model):  # We'll use this to extend Django's built-in User model later
    username = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username

class Recommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)

    def __str__(self):
        return f"Recommendation for {self.user} -> {self.song}"
