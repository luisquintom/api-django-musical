# musica/spotify_client.py
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token_url = "https://accounts.spotify.com/api/token"
        self.search_url = "https://api.spotify.com/v1/search"

    def obtener_token(self):
        creds = f"{self.client_id}:{self.client_secret}"
        creds_b64 = base64.b64encode(creds.encode()).decode()
        
        headers = {"Authorization": f"Basic {creds_b64}"}
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(self.token_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        return None

    # Función para buscar canciones
    def buscar_cancion(self, query):
        token = self.obtener_token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": query, "type": "track", "limit": 5}
        
        response = requests.get(self.search_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    # Función para buscar info del artista
    def obtener_info_artista(self, nombre_artista):
        token = self.obtener_token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": nombre_artista, "type": "artist", "limit": 1}
        
        response = requests.get(self.search_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            items = data.get("artists", {}).get("items", [])
            if items:
                artista = items[0]
                return {
                    "nombre": artista["name"],
                    "generos": artista["genres"],
                    "imagen": artista["images"][0]["url"] if artista["images"] else None
                }
        return None