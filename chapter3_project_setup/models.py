from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ("MOVIE", "MOVIE"),
    ("SERIES", "SERIES"),
)

# Create your models here.
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    class Meta:
        verbose_name = "Stream Platform"
        verbose_name_plural = "Stream Platforms"
        permissions = (
            ("can_view_stream_platform", "User can view stream platform"),
            ("can_create_stream_platform", "User can create stream platform"),
            ("can_update_stream_platform", "User can update stream platform"),
            ("can_partially_update_stream_platform", "User can partially update stream platform"),
            ("can_delete_stream_platform", "User can delete stream platform"),            
        )

    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey("StreamPlatform", on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    imdb_rating = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    episodes = models.IntegerField(default=0)
    category = models.CharField("Category", 
                                max_length=30, 
                                blank=True, 
                                null=True, 
                                choices=CATEGORY_CHOICES,
                                help_text="Watchlist category")
    
    class Meta:
        verbose_name = "Watch List"
        verbose_name_plural = "Watchlists"
        permissions = (
            ("can_view_watchlist", "User can view watchlist"),
            ("can_create_watchlist", "User can create watchlist"),
            ("can_update_watchlist", "User can update watchlist"),
            ("can_partially_update_watchlist", "User can partially update watchlist"),
            ("can_delete_watchlist", "User can delete watchlist"),            
        )    

    def __str__(self):
        return self.title
    
    @property
    def full_title(self):
        if(self.category=="MOVIE"):
            full_title = f"Movie Name: {self.title}"
        else:
            full_title = f"Series Name: {self.title}"
        return full_title 
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    review_date = models.DateField()
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        # permissions = (
        #     ("can_view_review", "User can review"),
        #     ("can_create_review", "User can create review"),
        #     ("can_update_review", "User can update review"),
        #     ("can_partially_update_review", "User can partially update review"),
        #     ("can_delete_review", "User can delete review"),            
        # )

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)
