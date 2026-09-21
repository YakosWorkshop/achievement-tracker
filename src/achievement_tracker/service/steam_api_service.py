from dataclasses import dataclass, field

import requests


class SteamAPIError(Exception):
    """Raised when a Steam request fails or returns an invalid JSON response."""



@dataclass
class AchievementData:
    """Metadata for an achievement from a Steam game's schema.

    Attributes:
        name: Display name of the achievement.
        detail: Description of the achievement.
        hidden: Whether the achievement is hidden.
        icon: URL of the achievement's unlocked icon.
    """

    name: str
    detail: str
    hidden: bool
    icon: str

@dataclass
class GameData:
    """Game metadata and achievements retrieved from Steam.

    Attributes:
        title: Display name of the game.
        detail: Short description from the Steam store.
        app_id: Steam application identifier.
        icon: URL of the game's store header image.
        achievements: Achievements associated with the game; defaults to an
            empty list.
    """

    title: str
    detail: str
    app_id: int
    icon: str
    achievements: list[AchievementData] = field(default_factory=list)
    
    @staticmethod
    def _get_json(url: str, params: dict) -> dict:
        """Send a GET request and return its JSON object.

        Args:
            url: Endpoint to request.
            params: Query parameters to include in the request.

        Returns:
            The response's decoded JSON dictionary.

        Raises:
            SteamAPIError: The request fails, the HTTP status indicates an
                error, the response is invalid JSON, or the decoded value is
                not a dictionary.
        """

        try:
            response = requests.get(url=url,params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exec:
            raise SteamAPIError(
                "Unable to retrieve data from Steam."
                ) from exec
        
        if not isinstance(data, dict):
            raise SteamAPIError("Steam returned an unexpected response format.")
        
        return data
    
    @staticmethod
    def get_achievements(apiKey, appId) -> list[AchievementData]:
        """Retrieve achievement metadata from a Steam game's schema.

        Args:
            apiKey: Steam Web API key used to authenticate the request.
            appId: Steam application identifier for the game.

        Returns:
            Achievements in schema order, or an empty list if the schema's
            achievements list is empty. A nonzero hidden flag is treated as
            hidden.

        Raises:
            SteamAPIError: The request fails or its response is not a valid
                JSON object.
            KeyError: Required game, achievement, or metadata fields are
                missing from the response.
        """

        #game_url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={apiKey}&appid={appId}"

        url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
        params = {'key': apiKey, 'appid':appId}
        
        data = GameData._get_json(url=url, params=params)
        
        achievements: list[AchievementData] = []
        
        for achievement in data["game"]["availableGameStats"]["achievements"]:
            
            if achievement["hidden"] == 0:
                isHidden = False
            else:
                isHidden = True
            
            achievements.append(
                AchievementData(
                    name=achievement["displayName"],
                    detail=achievement["description"],
                    hidden=isHidden,
                    icon=achievement["icon"]
                )
            )
        
        return achievements
    
    @classmethod
    def get_game(cls, apiKey, appId) -> GameData:
        """Retrieve a game's store metadata and achievement schema from Steam.

        Args:
            apiKey: Steam Web API key used to retrieve achievements.
            appId: Steam application identifier for the game.

        Returns:
            An instance of this class containing the game's title, short
            description, application identifier, header image URL, and
            achievements.

        Raises:
            SteamAPIError: Either request fails or returns a response that is
                not a valid JSON object.
            KeyError: Required game or achievement fields are missing from
                either response.
        """

        url = "https://store.steampowered.com/api/appdetails"
        params = {"appids": appId}
        
        data = GameData._get_json(url=url,params=params)
        
        return cls(
            title=data[f"{appId}"]["data"]["name"],
            detail=data[f"{appId}"]["data"]["short_description"],
            app_id=appId,
            icon=data[f"{appId}"]["data"]["header_image"],
            achievements=GameData.get_achievements(apiKey=apiKey, appId=appId)
        )
        
        
        
        
        
        
        
        
        
