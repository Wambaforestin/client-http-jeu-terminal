# 🐺 Jeu du Loup & villageois - Partie Client HTTP Terminal

# Documentation du Jeu Loup-Garou

## 1. Client HTTP Terminal (Groupe 8)

### Structure des Classes

#### `Role` et `PlayerStatus`
```python
class Role(Enum):
    LOUP = "loup"
    VILLAGEOIS = "villageois"

class PlayerStatus(Enum):
    ALIVE = "vivant"
    DEAD = "mort"
```
Ces énumérations définissent les rôles possibles et les états des joueurs.

#### `Position`
```python
@dataclass
class Position:
    x: int
    y: int
```
Structure simple pour gérer les coordonnées x,y d'un joueur sur la carte.

#### `GameClient`
La classe principale qui gère toutes les interactions avec le serveur.

### Méthodes Principales

#### 1. `inscription()`
```python
def inscription(self, login: str, role: Role) -> Tuple[bool, str]:
```
- **Objectif**: Inscrire un nouveau joueur
- **Paramètres**:
  - `login`: nom du joueur (3-20 caractères)
  - `role`: LOUP ou VILLAGEOIS
- **Retour**: (succès, message)

#### 2. `deplacer()`
```python
def deplacer(self, nouvelle_position: Position) -> Tuple[bool, str]:
```
- **Objectif**: Déplacer le joueur
- **Paramètres**:
  - `nouvelle_position`: où aller
- **Retour**: (succès, message)

#### 3. `get_vision()`
```python
def get_vision(self) -> Optional[Dict]:
```
- **Objectif**: Voir ce qui entoure le joueur
- **Retour**: Carte et informations visibles

#### 4. `afficher_carte()`
```python
def afficher_carte(self, vision: Dict):
```
- **Objectif**: Afficher la carte dans le terminal
- **Affichage**:
  - `.` : Case vide
  - `L` : Loup
  - `V` : Villageois
  - `?` : Inconnu
  - `X` : Obstacle
