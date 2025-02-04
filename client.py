from enum import Enum


class Role(Enum):
    LOUP = "loup"
    VILLAGEOIS = "villageois"

class GameState(Enum):
    WAITING = "en_attente"
    RUNNING = "en_cours"
    FINISHED = "terminé"

class PlayerStatus(Enum):
    ALIVE = "vivant"
    DEAD = "mort"