from django.db import models



class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField()


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)


    def assign_prize(self):
        level_prize = LevelPrize.objects.filter(level=self.level).first()

        if level_prize:
            PlayerPrize.objects.create(
                player_level=self,
                prize=level_prize,
                received=self.completed
            )


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)


class PlayerPrize(models.Model):
    player_level = models.ForeignKey(PlayerLevel, on_delete=models.CASCADE)
    prize = models.ForeignKey(LevelPrize, on_delete=models.CASCADE)
    received = models.DateField()
