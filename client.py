import requests
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import sys
from datetime import datetime

class Role(Enum):
    LOUP = "loup"
    VILLAGEOIS = "villageois"

class PlayerStatus(Enum):
    ALIVE = "vivant"
    DEAD = "mort"

@dataclass
class Position:
    x: int
    y: int

class GameClient:
    def __init__(self, base_url: str = "http://localhost:5000/api/v1", timeout: int = 5):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = timeout
        self.player_id = None
        self.role = None
        self.position = None
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def inscription(self, login: str, role: Role) -> Tuple[bool, str]:
        """
        Inscription d'un joueur
        
        Args:
            login (str): 3-20 chars alphanum
            role (Role): LOUP/VILLAGEOIS
        """
        try:
            if not 3 <= len(login) <= 20 or not login.isalnum():
                raise ValueError("Login invalide (3-20 caractères alphanumériques)")

            response = self.session.post(
                f"{self.base_url}/inscription",
                json={"login": login, "role": role.value},
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                self.player_id = data["player_id"]
                self.role = role
                self.position = Position(data["x"], data["y"])
                return True, "Inscription réussie"

            error_msg = response.json().get("error", "Erreur inconnue")
            return False, error_msg

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erreur réseau: {e}")
            return False, str(e)

    def deplacer(self, nouvelle_position: Position) -> Tuple[bool, str]:
        """
        Déplacement du joueur
        
        Args:
            nouvelle_position (Position): Nouvelle position x,y
        """
        if not self.player_id:
            return False, "Non inscrit"

        try:
            response = self.session.post(
                f"{self.base_url}/deplacement/{self.player_id}",
                json={
                    "x": nouvelle_position.x,
                    "y": nouvelle_position.y,
                    "tour": self.get_tour_actuel()
                },
                timeout=self.timeout
            )

            if response.status_code == 200:
                self.position = nouvelle_position
                return True, "Déplacement réussi"

            error_msg = response.json().get("error", "Erreur inconnue")
            return False, error_msg

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erreur réseau: {e}")
            return False, str(e)

    def get_vision(self) -> Optional[Dict]:
        """
        Récupère la vision du joueur
        """
        if not self.player_id:
            return None

        try:
            response = self.session.get(
                f"{self.base_url}/vision/{self.player_id}",
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()

            self.logger.error(f"Erreur vision: {response.text}")
            return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erreur réseau: {e}")
            return None

    def afficher_carte(self, vision: Dict):
        """
        Affiche la carte en mode terminal
        """
        if not vision:
            print("Aucune vision disponible")
            return

        print("\n=== État du jeu ===")
        print(f"Tour: {vision['tour_actuel']}")
        print(f"Temps restant: {vision['temps_restant']:.1f}s")
        
        # Légende
        print("\nLégende: . (vide) L (loup) V (villageois) ? (inconnu) X (obstacle)")
        
        # Carte
        for ligne in vision["carte"]:
            print(" ".join(str(case) for case in ligne))
        
        # Informations sur les joueurs proches
        if vision.get("joueurs_proches"):
            print("\nJoueurs proches:")
            for joueur in vision["joueurs_proches"]:
                print(f"- {joueur['role']} à {joueur.get('distance', '?')} cases")
        
        # État du joueur
        if vision.get("elimine"):
            print("\n⚠️ Vous avez été éliminé!")

    def get_tour_actuel(self) -> int:
        """Récupère le numéro du tour actuel"""
        try:
            response = self.session.get(f"{self.base_url}/tour")
            if response.status_code == 200:
                return response.json()["tour_actuel"]
            return 0
        except:
            return 0

def main():
    # Configuration du client
    client = GameClient()
    
    # Menu principal
    print("=== Loup-Garou Terminal ===")
    login = input("Login: ")
    role = input("Rôle (loup/villageois): ").lower()
    
    # Inscription
    role_enum = Role.LOUP if role == "loup" else Role.VILLAGEOIS
    success, message = client.inscription(login, role_enum)
    
    if not success:
        print(f"Erreur: {message}")
        sys.exit(1)
    
    print("Inscription réussie! Commandes: zqsd pour se déplacer, q pour quitter")
    
    # Boucle principale
    while True:
        # Afficher l'état actuel
        vision = client.get_vision()
        if vision:
            client.afficher_carte(vision)
        
        # Gestion des commandes
        cmd = input("> ").lower()
        if cmd == "q":
            break
            
        # Déplacement
        delta = {"z": (0, -1), "s": (0, 1), "q": (-1, 0), "d": (1, 0)}.get(cmd)
        if delta:
            nouvelle_pos = Position(
                client.position.x + delta[0],
                client.position.y + delta[1]
            )
            success, msg = client.deplacer(nouvelle_pos)
            if not success:
                print(f"Erreur de déplacement: {msg}")

if __name__ == "__main__":
    main()