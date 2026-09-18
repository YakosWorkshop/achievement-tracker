import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class TrophyData:
    name: str
    trophy_id: str
    hidden: bool
    type: Literal['P', 'B', 'G', 'S']
    pid: str
    detail: str
    
@dataclass
class GameData:
    title: str
    title_detail: str
    game_id: str
    version: str
    trophies: list[TrophyData] = field(default_factory=list)
    
    @classmethod
    def from_rpcs3 (cls, file_path: str) -> GameData:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        trophies: list[TrophyData] = []
        
        for child in root:
            if child.tag != "trophy":
                continue
            
            trophies.append(
                TrophyData(
                    name=child.find("name"),
                    trophy_id=child.attrib.get("id"),
                    hidden=child.attrib.get("hidden"),
                    type=child.attrib.get("ttype"),
                    pid=child.attrib.get("pid"),
                    detail=child.find("detail")
                )
            )
        
        return cls(
            title=root.find("title-name").text,
            title_detail=root.find("title-detail").text,
            game_id=root.find("npcommid").text,
            version=root.find("trophyset-version").text,
            trophies=trophies
        )
        
    