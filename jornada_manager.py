import json
from pathlib import Path

JORNADA_FILE = Path(__file__).parent / "jornada_activa.json"
BACKUP_FILE = Path(__file__).parent / "jornada_activa_backup.json"

DEFAULT_JORNADA = [
    {"casilla": 1, "local": "América", "visita": "Guadalajara", "id": None},
    {"casilla": 2, "local": "Cruz Azul", "visita": "Pumas UNAM", "id": None},
    {"casilla": 3, "local": "Tigres UANL", "visita": "Monterrey", "id": None},
    {"casilla": 4, "local": "Toluca", "visita": "Pachuca", "id": None},
    {"casilla": 5, "local": "Santos Laguna", "visita": "León", "id": None},
    {"casilla": 6, "local": "Atlas", "visita": "Puebla", "id": None},
    {"casilla": 7, "local": "Querétaro", "visita": "Necaxa", "id": None},
    {"casilla": 8, "local": "Tijuana", "visita": "FC Juárez", "id": None},
    {"casilla": 9, "local": "Real Madrid", "visita": "Barcelona", "id": None},
    {"casilla": 10, "local": "Atlético Madrid", "visita": "Sevilla", "id": None},
    {"casilla": 11, "local": "Manchester City", "visita": "Liverpool", "id": None},
    {"casilla": 12, "local": "Arsenal", "visita": "Chelsea", "id": None},
    {"casilla": 13, "local": "Bayern München", "visita": "Dortmund", "id": None},
    {"casilla": 14, "local": "Paris Saint Germain", "visita": "Marseille", "id": None}
]

def cargar_jornada_activa() -> list[dict]:
    """Carga los 14 partidos activos con tolerancia a fallos y auto-recuperación de respaldo."""
    # 1. Intentar cargar desde el archivo principal
    if JORNADA_FILE.exists():
        try:
            with open(JORNADA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) == 14:
                    # Sincronizar respaldo preventivo silencioso
                    try:
                        if not BACKUP_FILE.exists() or BACKUP_FILE.stat().st_size != JORNADA_FILE.stat().st_size:
                            with open(BACKUP_FILE, "w", encoding="utf-8") as bf:
                                json.dump(data, bf, ensure_ascii=False, indent=2)
                    except Exception:
                        pass
                    return data
        except Exception:
            pass

    # 2. Intentar recuperar desde el archivo de respaldo automático
    if BACKUP_FILE.exists():
        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as bf:
                data = json.load(bf)
                if isinstance(data, list) and len(data) == 14:
                    # Restaurar archivo principal corrupto o ausente
                    try:
                        with open(JORNADA_FILE, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                    except Exception:
                        pass
                    return data
        except Exception:
            pass

    return DEFAULT_JORNADA

def guardar_jornada_activa(partidos: list[dict]) -> bool:
    """Guarda los 14 partidos simultáneamente en el archivo principal y en el respaldo espejo."""
    if not isinstance(partidos, list) or len(partidos) != 14:
        return False
    try:
        # Guardar en archivo principal
        with open(JORNADA_FILE, "w", encoding="utf-8") as f:
            json.dump(partidos, f, ensure_ascii=False, indent=2)
            
        # Guardar en archivo de respaldo espejo
        with open(BACKUP_FILE, "w", encoding="utf-8") as bf:
            json.dump(partidos, bf, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        print(f"Error al guardar jornada activa: {e}")
        return False
