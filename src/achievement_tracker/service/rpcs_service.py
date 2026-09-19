import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Literal
from pathlib import Path


@dataclass
class TrophyData:
    name: str
    trophy_id: str
    hidden: bool
    type: Literal['P', 'B', 'G', 'S']
    pid: str
    detail: str
    icon: str
    
@dataclass
class GameData:
    title: str
    detail: str
    game_id: str
    version: str
    icon: str
    trophies: list[TrophyData] = field(default_factory=list)
    
    @classmethod
    def from_rpcs3 (cls, game_folder: str) -> GameData:
        directory = Path(game_folder)
        
        trophyConf = str(directory / "TROPCONF.SFM")
        
        tree = ET.parse(trophyConf)
        root = tree.getroot()
        
        trophies: list[TrophyData] = []
        
        for child in root:
            if child.tag != "trophy":
                continue
            
            id = child.attrib.get("id")
            
            trophies.append(
                TrophyData(
                    name=child.find("name"),
                    trophy_id=id,
                    hidden=child.attrib.get("hidden"),
                    type=child.attrib.get("ttype"),
                    pid=child.attrib.get("pid"),
                    detail=child.find("detail"),
                    icon=str(directory / f"TROP{id}.PNG")
                )
            )
        
        return cls(
            title=root.find("title-name").text,
            detail=root.find("title-detail").text,
            game_id=root.find("npcommid").text,
            version=root.find("trophyset-version").text,
            trophies=trophies,
            icon=str(directory / "ICON0.PNG")
        )
        
    