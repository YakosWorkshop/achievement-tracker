import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


class InvalidGameConfigError(Exception):
    """Raised when game or trophy XML contains missing or invalid required data."""

@dataclass
class TrophyData:
    """Metadata for a trophy loaded from a game's configuration.

    Attributes:
        name: Display name of the trophy.
        trophy_id: Trophy identifier from the configuration.
        hidden: Whether the trophy is hidden.
        type: Trophy grade: platinum (P), bronze (B), gold (G), or silver (S).
        pid: Value recorded in the trophy's ``pid`` element.
        detail: Description of the trophy.
        icon: Path to the trophy's PNG icon.
    """

    name: str
    trophy_id: str
    hidden: bool
    type: Literal['P', 'B', 'G', 'S']
    pid: str
    detail: str
    icon: str
    
@dataclass
class GameData:
    """Game metadata and trophies loaded from a trophy configuration folder.

    Attributes:
        title: Display name of the game.
        detail: Description of the game.
        game_id: Network communication identifier from ``npcommid``.
        version: Trophy set version.
        icon: Path to the game's ``ICON0.PNG`` icon.
        trophies: Trophies associated with the game; defaults to an empty list.
    """

    title: str
    detail: str
    game_id: str
    version: str
    icon: str
    trophies: list[TrophyData] = field(default_factory=list)
    
    @staticmethod
    def _required_trophy_type(element: ET.Element[str]) -> Literal['P', 'B', 'G', 'S']:
        """Read and validate a trophy element's ``ttype`` attribute.

        Args:
            element: Trophy element containing the type attribute.

        Returns:
            The trophy grade code: P, B, G, or S.

        Raises:
            InvalidGameConfigError: The attribute is missing or unsupported.
        """
        value = element.attrib.get("ttype")
        
        if value is None:
            raise InvalidGameConfigError(
                "Missing required field: ttype"
            )
        
        if value not in ('P', 'B', 'G', 'S'):
            raise InvalidGameConfigError(
                f"Invalid trophy type: {value!r}. Expected P, B, G, or S"
            )
        
        return value   
    
    @staticmethod
    def _required_trophy_attribute(element: ET.Element[str], tag: str) -> str:
        """Return a required, non-empty attribute from a trophy element.

        Args:
            element: Trophy element containing the attribute.
            tag: Name of the required attribute.

        Returns:
            The attribute value without modifying its whitespace.

        Raises:
            InvalidGameConfigError: If the attribute is missing or contains
                only whitespace.
        """
        value = element.attrib.get(tag)

        if value is None or not value.strip():
            raise InvalidGameConfigError(
                f"Missing required field: {tag}"
            )

        return value
    
    @staticmethod
    def _required_text(element: ET.Element[str], tag) -> str:
        """Return the text of a required child element.


        Args:
            element: Parent element to search.
            tag: Child tag or path accepted by ``Element.find``.

        Raises:
            InvalidGameConfigError: The child is missing or has no text.

        Returns:
            The child's text without stripping whitespace.
        """
        found = element.find(tag)
        
        if found is None or found.text is None:
            raise InvalidGameConfigError(
                f"Missing required field: {tag}"
            )
        
        return found.text
            
            
    @staticmethod
    def get_trophies(game_folder: str) -> list[TrophyData]:
        """Load trophies from ``TROPCONF.SFM`` in the given folder.

        Only direct ``trophy`` children are processed. A trophy is considered
        hidden unless its ``hidden`` attribute is ``no``. Icon paths are
        constructed without checking whether the image files exist.

        Args:
            game_folder: Path to the folder containing the trophy configuration.

        Returns:
            Trophies in configuration order, or an empty list if none exist.

        Raises:
            OSError: The configuration file cannot be opened or read.
            ET.ParseError: The configuration is not well-formed XML.
            InvalidGameConfigError: Required trophy text is missing or a trophy
                type is missing or unsupported.
        """
        directory = Path(game_folder)
        
        trophyConf = str(directory / "TROPCONF.SFM")
        
        tree = ET.parse(trophyConf)
        root = tree.getroot()
        
        trophies: list[TrophyData] = []
        
        for child in root:
                    if child.tag != "trophy":
                        continue
                    
                    if child.attrib.get("hidden") == "no":
                        isHidden = False
                    else: isHidden = True
                    
                    trophies.append(
                        TrophyData(
                            name=GameData._required_text(element=child,tag="name"),
                            trophy_id=GameData._required_trophy_attribute(child,tag="id"),
                            hidden=isHidden,
                            type=GameData._required_trophy_type(child),
                            pid=GameData._required_trophy_attribute(element=child,tag="pid"),
                            detail=GameData._required_text(element=child,tag="detail"),
                            icon=str(directory / f"TROP{id}.PNG")
                        )
                    )
        
        return trophies
    
    @classmethod
    def get_game (cls, game_folder: str) -> GameData:
        """Load game metadata and trophies from a trophy configuration folder.

        Args:
            game_folder: Path to the folder containing ``TROPCONF.SFM`` and icons.

        Returns:
            An instance of this class containing the game metadata, trophies,
            and the constructed ``ICON0.PNG`` path. Icon existence is not checked.

        Raises:
            OSError: The configuration file cannot be opened or read.
            ET.ParseError: The configuration is not well-formed XML.
            InvalidGameConfigError: Required game or trophy text is missing,
                or a trophy type is missing or unsupported.
        """
        directory = Path(game_folder)
        
        trophyConf = str(directory / "TROPCONF.SFM")
        
        tree = ET.parse(trophyConf)
        root = tree.getroot()

        return cls(
            title=GameData._required_text(element=root, tag="title-name"),
            detail=GameData._required_text(element=root, tag="title-detail"),
            game_id=GameData._required_text(element=root, tag="npcommid"),
            version=GameData._required_text(element=root, tag="trophyset-version"),
            trophies=GameData.get_trophies(game_folder=game_folder),
            icon=str(directory / "ICON0.PNG")
        )
        