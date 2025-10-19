from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    views_by_region = models.JSONField(default=dict, blank=True)
    orders_by_region = models.JSONField(default=dict, blank=True)

    def like_ratio(self):
        total_ratings = self.rating_set.count()
        if total_ratings == 0:
            return "N/A"
        likes = self.rating_set.filter(liked=True).count()
        return int((likes / total_ratings) * 100)


    def __str__(self):
        return str(self.id) + ' - ' + self.name

    def increment_views(self, region_name):
        """Increment view count for a specific region"""
        print("before views: ", self.views_by_region)
        if region_name not in self.views_by_region:
            self.views_by_region[region_name] = 1
        else:
            self.views_by_region[region_name] += 1
        print("after views: ", self.views_by_region)
        self.save()

    def increment_orders(self, region_name):
        """Increment order count for a specific region"""
        print("before orders: ", self.orders_by_region)
        if region_name not in self.orders_by_region:
            self.orders_by_region[region_name] = 1
        else:
            self.orders_by_region[region_name] += 1
        print("after orders: ", self.orders_by_region)
        self.save()

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.user.username}'s rating for {self.movie.title}"