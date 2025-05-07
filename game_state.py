from enum import Enum, auto

class GameState(Enum):
    MENU             = auto()   # головне меню
    DIFFICULTY       = auto()   # підменю вибору складності
    RESOLUTION       = auto()   # підменю вибору роздільної здатності
    PLAY             = auto()   # ігровий режим
    PAUSE            = auto()   # пауза
    GAME_OVER_MENU   = auto()   # меню після поразки
    VICTORY_MENU     = auto()   # меню після перемоги