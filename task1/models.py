import enum
import logging
import datetime

from sqlalchemy import Integer, Column, ForeignKey, Table, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_SCORE_INCREASE = 5


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)


player_boost_rel = Table(
    "player_boost_rel",
    Base.metadata,
    Column("player_id", ForeignKey("player.id", ondelete="CASCADE"), primary_key=True),
    Column("boost_id", ForeignKey("boost.id", ondelete="CASCADE"), primary_key=True),
)


class Player(Base):
    __tablename__ = "player"

    name: Mapped[str]
    score: Mapped[float] = mapped_column(default=0, nullable=False)
    first_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    boosts: Mapped[list["Boost"]] = relationship(secondary=player_boost_rel, lazy="selectin")

    def fake_login(self):
        now = datetime.datetime.now()
        self.last_login = now
        if self.first_login is None:
            self.first_login = now

        logger.info(f"Player \"{self.name}\" logged in at {now.strftime(DATE_FORMAT)}")

        self.calculate_boosts()
        self.increase_score(DEFAULT_SCORE_INCREASE)

    def assign_boost(self, boost: "Boost"):
        self.boosts.append(boost)
        logger.info(f"Player {self.name} has been assigned boost \"{boost.name}\"")

    def increase_score(self, value: int):
        boost_value = value

        if self.boosts:
            boost_value = 0
            for boost in self.boosts:
                boost_value += boost.apply(value)

        logger.info(f"Player \"{self.name}\" has increased score by {boost_value}")
        self.score += boost_value
        logger.info(f"Player \"{self.name}\"'s score is now {self.score}")
        return boost_value

    def calculate_boosts(self):
        now = datetime.datetime.now()
        to_remove = []
        for boost in self.boosts:
            if boost.date_start <= now <= boost.date_end:
                continue
            to_remove.append(boost)

        self.boosts = [boost for boost in self.boosts if boost not in to_remove]



class Boost(Base):
    __tablename__ = "boost"

    class ModifierType(enum.Enum):
        MULTIPLY = "multiply"
        ADD = "add"
        PERCENTAGE = "percentage"

    name: Mapped[str]
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    modifier: Mapped[float] = mapped_column(default=1, nullable=False)
    modifier_type: Mapped[ModifierType] = mapped_column(default=ModifierType.PERCENTAGE, nullable=False)

    _operator_mapping = {
        ModifierType.MULTIPLY: lambda x, y: x * y,
        ModifierType.ADD: lambda x, y: x + y,
        ModifierType.PERCENTAGE: lambda x, y: x * (1 + y / 100),
    }

    def apply(self, value):
        return self._operator_mapping[self.modifier_type](value, self.modifier)
