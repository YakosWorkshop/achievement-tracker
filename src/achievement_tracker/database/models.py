
from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=1000)
    is_completed = models.BooleanField()
    
    class Meta:
        db_table =  "games"

class Platform(models.Model):
    title = models.CharField(max_length=1000, unique=True)
    
    class Meta:
            db_table =  "platforms"

class GameSource(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platforms = models.ForeignKey(Platform, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=1000)

    class Meta:
            db_table =  "game_sources"

class Achievement(models.Model):
    game_source = models.ForeignKey(GameSource, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField()
    
    class Meta:
            db_table =  "achievements"
            
class UserAchievement(models.Model):
    achievements = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    time_unlocked = models.DateTimeField()
    
    class Meta:
            db_table =  "user_achievements"
