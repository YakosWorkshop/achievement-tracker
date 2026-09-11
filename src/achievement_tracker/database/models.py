from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from achievement_tracker.database.base import Base


class Games(Base):
    __tablename__ = "games"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    is_completed: Mapped[bool]
    
class Achievements(Base):
    __tablename__ = "achievements"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    game_source_id: Mapped[int] = mapped_column(ForeignKey("game_sources.id"))
    name: Mapped[str]
    description: Mapped[str]
    icon: Mapped[str] = mapped_column(default=None)
  
class Platforms(Base):
    __tablename__ = "platforms"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
        
class GameSources(Base):
    __tablename__ = "game_sources"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id"))
    external_id: Mapped[str]
    
class UserAchievements(Base):
    __tablename__ = "user_achievements"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    achievements_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"))
    time_unlocked: Mapped[datetime]