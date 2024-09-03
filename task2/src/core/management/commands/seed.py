import random
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Player, Level, Prize, PlayerLevel, LevelPrize, PlayerPrize

# python manage.py seed

logger = logging.getLogger(__name__)

SEED = "dfsodfsjko;dfsijkop[;dfsjkop["

adj = [
    'shocking', 'well-off', 'responsible', 'bent', 'past', 'glorious', 'hollow', 'plastic', 'redundant', 'volatile'
    , 'sudden', 'tall', 'wretched', 'fierce', 'salty', 'sore', 'stupendous', 'tense', 'witty', 'wonderful',
     'zealous', 'aberrant', 'curious', 'glib', 'hollow', 'incandescent', 'quixotic', 'vivacious', 'wary', 'wistful'
]

noun = [
    'account', 'advice', 'afterthought', 'air', 'animal', 'answer', 'apparatus', 'art', 'attack', 'bait', 'ball',
    'bead', 'bottle', 'building', 'cabbage', 'cable', 'calculator', 'camera', 'canvas', 'carriage', 'cart', 'cast',
    'cattle', 'celery', 'channel', 'cheese', 'chess', 'coat', 'craft', 'credit', 'cricket', 'crook', 'cup', 'current',
    'damage', 'deer', 'development', 'direction', 'discussion', 'dime', 'dinner', 'direction', 'dirt', 'dust', 'education'
]


class Command(BaseCommand):
    help = "Seed database"


    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        self.run_seed()
        self.stdout.write('Done.')


    def clear_data(self):
        self.stdout.write('Clearing all data')
        models = Player, Level, Prize, PlayerLevel, LevelPrize, PlayerPrize
        for model in models:
            model.objects.all().delete()

    @staticmethod
    def create_players():
        players = []
        for i in range(1, random.randint(150, 200)):
            random_user_id = f"{random.choice(adj)}-{random.choice(noun)}{random.randint(1, 1000)}"
            player = Player.objects.create(player_id=random_user_id)
            players.append(player)

        return players

    @staticmethod
    def create_levels():
        levels = []
        for i in range(1, 31):
            level = Level.objects.create(title=f"Level {i}", order=i)
            levels.append(level)

        return levels

    @staticmethod
    def create_prizes():
        common_prize = Prize.objects.create(title="Common Prize")
        rare_prize = Prize.objects.create(title="Rare Prize")
        legendary_prize = Prize.objects.create(title="Legendary Prize")

        return [common_prize, rare_prize, legendary_prize]

    @staticmethod
    def create_level_prizes(levels, prizes):
        for level in levels:
            LevelPrize.objects.create(level=level, prize=random.choice(prizes))


    def simulate_level_completion(self, players, levels):
        self.stdout.write('Simulating level completion')

        random.seed(SEED)
        fake_today = timezone.now() - timezone.timedelta(days=250)

        for i in range(1, random.randint(4000, 5000)):
            random.seed()
            fake_today += timezone.timedelta(hours=2)

            completed = random.choice([True, False])
            PlayerLevel.objects.create(
                player=random.choice(players),
                level=random.choice(levels),
                score=random.normalvariate(1000, 200),
                is_completed=completed,
                completed=fake_today if completed else None
            )


    def run_seed(self):
        self.clear_data()
        random.seed(SEED)

        levels = self.create_levels()
        self.stdout.write('Levels created')

        prizes = self.create_prizes()
        self.create_level_prizes(levels, prizes)
        self.stdout.write('Prizes created')

        players = self.create_players()
        self.stdout.write('Players created')

        self.simulate_level_completion(players, levels)
