import random
import datetime
import time
import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Player, Boost


def create_players(db):
    players = []
    for i in range(1, random.randint(25, 50)):
        player = Player(name=f"Player {i}")
        players.append(player)

    db.add_all(players)
    db.commit()
    return players


def create_boosts(db):
    date_start = datetime.datetime.now() - datetime.timedelta(days=1)
    date_end = datetime.datetime.now() + datetime.timedelta(days=1)

    boost_1 = Boost(
        name="x2",
        date_start=date_start,
        date_end=date_end,
        modifier_type=Boost.ModifierType.MULTIPLY,
        modifier=2
    )
    boost_2 = Boost(
        name="+100",
        date_start=date_start,
        date_end=date_end,
        modifier_type=Boost.ModifierType.ADD,
        modifier=100
    )
    boost_3 = Boost(
        name="+10%",
        date_start=date_start,
        date_end=date_end,
        modifier_type=Boost.ModifierType.PERCENTAGE,
        modifier=10
    )
    boosts = [boost_1, boost_2, boost_3]
    db.add_all(boosts)
    db.commit()
    return boosts


def random_player(players):
    return random.choice(players)


def random_boost(boosts):
    return random.choice(boosts)


def simulate_level_complete(player, boosts):
    level = random.randint(1, 10)
    logger.info(f"Player {player.name} has completed level {level}")

    player.assign_boost(random_boost(boosts))


def main():
    random.seed("dfgijsvdfijpsdfijps'")

    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    db = Session(engine)

    players = create_players(db)
    boosts = create_boosts(db)

    player = random_player(players)

    player.fake_login()
    db.commit()

    simulate_level_complete(player, boosts)
    db.commit()

    time.sleep(5)

    player.fake_login()
    db.commit()

    db.close()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)
    main()
