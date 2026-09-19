from django.db import models


class Platform(models.Model):
    system = models.CharField(max_length=1000, unique=True)
    
    class Meta:
            db_table =  "platform"

class Game(models.Model):
    external_id = models.CharField(max_length=1000)
    platform_id = models.ForeignKey(Platform,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    detail = models.TextField()
    icon = models.ImageField()
    
    
    class Meta:
        db_table =  "game"
        constraints = [
            models.UniqueConstraint(
                fields=["platform_id","external_id"],
                name="unique_game_per_platform"
            )
        ]

class Achievement(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
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
