"""
Módulo de plantillas oficiales y probables para la Liga MX, Liga MX Femenil y Torneos Top Internacionales
"""
import zlib

PLANTILLAS_POR_EQUIPO = {
    # LIGA MX Y LIGA EXPANSIÓN
    "america": ["L. Malagón (POR)", "K. Álvarez (DEF)", "I. Lichnovsky (DEF)", "S. Cáceres (DEF)", "C. Borja (DEF)", "J. dos Santos (MED)", "Á. Fidalgo (MED)", "D. Valdés (MED)", "A. Zendejas (DEL)", "H. Martín (DEL)", "B. Rodríguez (DEL)"],
    "cruz azul": ["K. Mier (POR)", "J. Sánchez (DEF)", "W. Ditta (DEF)", "G. Piovi (DEF)", "C. Rotondi (DEF)", "C. Rodríguez (MED)", "L. Faravelli (MED)", "A. Gutiérrez (MED)", "U. Antuna (DEL)", "G. Giakoumakis (DEL)", "Á. Sepúlveda (DEL)"],
    "guadalajara": ["R. Rangel (POR)", "A. Mozo (DEF)", "G. Sepúlveda (DEF)", "J. Orozco (DEF)", "M. Chávez (DEF)", "E. Gutiérrez (MED)", "F. Beltrán (MED)", "V. Guzmán (MED)", "R. Alvarado (DEL)", "A. Cowell (DEL)", "J. Hernández (DEL)"],
    "chivas": ["R. Rangel (POR)", "A. Mozo (DEF)", "G. Sepúlveda (DEF)", "J. Orozco (DEF)", "M. Chávez (DEF)", "E. Gutiérrez (MED)", "F. Beltrán (MED)", "V. Guzmán (MED)", "R. Alvarado (DEL)", "A. Cowell (DEL)", "J. Hernández (DEL)"],
    "tigres": ["N. Guzmán (POR)", "J. Aquino (DEF)", "G. Pizarro (DEF)", "Joaquim (DEF)", "J. Angulo (DEF)", "R. Carioca (MED)", "F. Gorriarán (MED)", "J. Brunetta (MED)", "D. Lainez (DEL)", "A.P. Gignac (DEL)", "M. Flores (DEL)"],
    "atlas": ["C. Vargas (POR)", "H. Nervo (DEF)", "M. Santamaría (DEF)", "G. Aguirre (DEF)", "L. Reyes (DEF)", "A. Rocha (MED)", "J. Márquez (MED)", "R. Fulgencio (MED)", "E. Aguirre (DEL)", "U. Djurdjevic (DEL)", "J. Murillo (DEL)"],
    "atletico san luis": ["A. Sánchez (POR)", "I. Moreno (DEF)", "J. Domínguez (DEF)", "E. Águila (DEF)", "A. Cruz (DEF)", "R. Dourado (MED)", "J. Sanabria (MED)", "S. Salles-Lamononge (MED)", "M. Klimowicz (DEL)", "F. Boli (DEL)", "V. Vitinho (DEL)"],
    "san luis": ["A. Sánchez (POR)", "I. Moreno (DEF)", "J. Domínguez (DEF)", "E. Águila (DEF)", "A. Cruz (DEF)", "R. Dourado (MED)", "J. Sanabria (MED)", "S. Salles-Lamononge (MED)", "M. Klimowicz (DEL)", "F. Boli (DEL)", "V. Vitinho (DEL)"],
    "queretaro": ["G. Allison (POR)", "O. Mendoza (DEF)", "F. Venegas (DEF)", "K. Escamilla (DEF)", "P. Ortíz (DEF)", "F. Lértora (MED)", "M. Rio (MED)", "R. Cisneros (MED)", "P. Barrera (DEL)", "A. Loba (DEL)", "S. Rubio (DEL)"],
    "querétaro": ["G. Allison (POR)", "O. Mendoza (DEF)", "F. Venegas (DEF)", "K. Escamilla (DEF)", "P. Ortíz (DEF)", "F. Lértora (MED)", "M. Rio (MED)", "R. Cisneros (MED)", "P. Barrera (DEL)", "A. Loba (DEL)", "S. Rubio (DEL)"],
    "pachuca": ["C. Moreno (POR)", "L. Rodríguez (DEF)", "G. Cabral (DEF)", "A. Arroyo (DEF)", "B. González (DEF)", "P. Pedraza (MED)", "N. Deossa (MED)", "E. Sánchez (MED)", "O. Idrissi (DEL)", "S. Rondón (DEL)", "A. Mena (DEL)"],
    "necaxa": ["E. Unsain (POR)", "E. Martínez (DEF)", "A. Montes (DEF)", "A. Mayorga (DEF)", "A. Oliveros (DEF)", "F. Arce (MED)", "A. Palavecino (MED)", "B. Garnica (MED)", "D. Cambindo (DEL)", "J. Paradela (DEL)", "R. Monreal (DEL)"],
    "atlante": ["H. Hernández (POR)", "C. Partida (DEF)", "E. Reyes (DEF)", "D. Cruz (DEF)", "A. Escobar (DEF)", "R. González (MED)", "E. Partida (MED)", "M. Bermúdez (MED)", "R. Durán (DEL)", "D. Lajud (DEL)", "E. Jiménez (DEL)"],
    "pumas": ["J. González (POR)", "P. Bennevendo (DEF)", "N. Silva (DEF)", "L. Magallán (DEF)", "R. Ergas (DEF)", "J. Caicedo (MED)", "U. Rivas (MED)", "P. Quispe (MED)", "I. Pussetto (DEL)", "G. Martínez (DEL)", "C. Huerta (DEL)"],
    "monterrey": ["E. Andrada (POR)", "S. Medina (DEF)", "V. Guzmán (DEF)", "H. Moreno (DEF)", "G. Arteaga (DEF)", "J. Rodríguez (MED)", "S. Canales (MED)", "O. Torres (MED)", "M. Meza (DEL)", "G. Berterame (DEL)", "B. Vázquez (DEL)"],
    "toluca": ["T. Volpi (POR)", "B. García (DEF)", "L. Luan (DEF)", "F. Pereira (DEF)", "J. Gallardo (DEF)", "C. Baeza (MED)", "M. Ruiz (MED)", "J. Angulo (MED)", "J. Domínguez (DEL)", "Paulinho (DEL)", "A. Vega (DEL)"],
    "santos": ["C. Acevedo (POR)", "I. Govea (DEF)", "S. Núñez (DEF)", "E. Echeverría (DEF)", "B. Amione (DEF)", "A. Cervantes (MED)", "P. Aquino (MED)", "R. Sordo (MED)", "F. Fagúndez (DEL)", "A. Lozano (DEL)", "H. Preciado (DEL)"],
    "leon": ["A. Blanco (POR)", "J. Barreiro (DEF)", "A. Frías (DEF)", "P. Bellón (DEF)", "S. Santos (DEF)", "F. Ambriz (MED)", "L. Romero (MED)", "E. Guerra (MED)", "A. Medina (DEL)", "J. Cádiz (DEL)", "J. Alvarado (DEL)"],
    "puebla": ["M. Jiménez (POR)", "G. Ferrareis (DEF)", "S. Olmedo (DEF)", "E. Gularte (DEF)", "B. Angulo (DEF)", "D. de Buen (MED)", "P. González (MED)", "A. Organista (MED)", "L. Cavallini (DEL)", "S. Ormeño (DEL)", "E. Gómez (DEL)"],
    "juarez": ["B. Díaz (POR)", "J. Abella (DEF)", "M. Mosquera (DEF)", "C. Salcedo (DEF)", "R. Ralph (DEF)", "J. Venegas (MED)", "D. Valoyes (MED)", "G. Castilho (MED)", "A. García (DEL)", "Ó. Estupiñán (DEL)", "J. Torres (DEL)"],
    "mazatlan": ["H. González (POR)", "B. Colula (DEF)", "F. Almada (DEF)", "L. Merolla (DEF)", "J. Esquivel (DEF)", "R. Meraz (MED)", "J. Intriago (MED)", "Y. Bárcenas (MED)", "R. Arciga (DEL)", "L. Amarilla (DEL)", "G. del Prete (DEL)"],
    "tijuana": ["J. Corona (POR)", "A. Mejía (DEF)", "K. Balanta (DEF)", "U. Bilbao (DEF)", "F. Contreras (DEF)", "C. Rivera (MED)", "I. Tona (MED)", "E. Álvarez (MED)", "E. Emanuel (DEL)", "C. González (DEL)", "J. Zúñiga (DEL)"],

    # LIGA MX FEMENIL
    "pachuca f": ["E. Barreras (POR)", "K. Robles (DEF)", "Y. Madrid (DEF)", "O. Ocampo (DEF)", "A. Peregrina (DEF)", "K. Nieto (MED)", "V. Salazar (MED)", "A. Soto (MED)", "C. Corral (DEL)", "J. Hermoso (DEL)", "S. Ibarra (DEL)"],
    "guadalajara f": ["B. Félix (POR)", "D. Rodríguez (DEF)", "K. Guzmán (DEF)", "J. Torres (DEF)", "A. Godínez (DEF)", "C. Jaramillo (MED)", "V. Montoya (MED)", "A. Castillo (MED)", "A. Cervantes (DEL)", "A. Iturbide (DEL)", "R. Valenzuela (DEL)"],
    "chivas f": ["B. Félix (POR)", "D. Rodríguez (DEF)", "K. Guzmán (DEF)", "J. Torres (DEF)", "A. Godínez (DEF)", "C. Jaramillo (MED)", "V. Montoya (MED)", "A. Castillo (MED)", "A. Cervantes (DEL)", "A. Iturbide (DEL)", "R. Valenzuela (DEL)"],
    "tigres f": ["C. Santiago (POR)", "G. Espinoza (DEF)", "A. Rodríguez (DEF)", "N. Villarreal (DEF)", "N. Antonio (DEF)", "L. Ovalle (MED)", "S. Mayor (MED)", "A. Delgado (MED)", "J. Hermoso (DEL)", "T. Kgatlana (DEL)", "S. Thembi (DEL)"],
    "america f": ["S. Paños (POR)", "K. Luna (DEF)", "A. Pereira (DEF)", "J. Orejel (DEF)", "K. Rodríguez (DEF)", "A. Kaci (MED)", "N. Mauleón (MED)", "S. Luebbert (MED)", "K. Palacios (DEL)", "S. Camberos (DEL)", "M. Zuazua (DEL)"],
    "américa f": ["S. Paños (POR)", "K. Luna (DEF)", "A. Pereira (DEF)", "J. Orejel (DEF)", "K. Rodríguez (DEF)", "A. Kaci (MED)", "N. Mauleón (MED)", "S. Luebbert (MED)", "K. Palacios (DEL)", "S. Camberos (DEL)", "M. Zuazua (DEL)"],
    "monterrey f": ["P. Tajonar (POR)", "R. Bernal (DEF)", "M. Flores (DEF)", "D. Evangelista (DEF)", "K. García (DEF)", "D. Garcia (MED)", "N. Pérez (MED)", "A. Delgadillo (MED)", "J. Burkenroad (DEL)", "C. Martinez (DEL)", "M. Salas (DEL)"],
    "rayadas f": ["P. Tajonar (POR)", "R. Bernal (DEF)", "M. Flores (DEF)", "D. Evangelista (DEF)", "K. García (DEF)", "D. Garcia (MED)", "N. Pérez (MED)", "A. Delgadillo (MED)", "J. Burkenroad (DEL)", "C. Martinez (DEL)", "M. Salas (DEL)"],

    # CLUBES INTERNACIONALES TOP
    "real madrid": ["T. Courtois (POR)", "D. Carvajal (DEF)", "E. Militão (DEF)", "A. Rüdiger (DEF)", "F. Mendy (DEF)", "F. Valverde (MED)", "A. Tchouaméni (MED)", "J. Bellingham (MED)", "Rodrygo (DEL)", "K. Mbappé (DEL)", "Vinícius Jr. (DEL)"],
    "barcelona": ["M. ter Stegen (POR)", "J. Koundé (DEF)", "P. Cubarsí (DEF)", "I. Martínez (DEF)", "A. Balde (DEF)", "M. Casadó (MED)", "Pedri (MED)", "D. Olmo (MED)", "L. Yamal (DEL)", "R. Lewandowski (DEL)", "Raphinha (DEL)"],
    "manchester city": ["Ederson (POR)", "K. Walker (DEF)", "R. Dias (DEF)", "M. Akanji (DEF)", "J. Gvardiol (DEF)", "Rodri (MED)", "K. De Bruyne (MED)", "B. Silva (MED)", "P. Foden (DEL)", "E. Haaland (DEL)", "J. Doku (DEL)"],
    "man city": ["Ederson (POR)", "K. Walker (DEF)", "R. Dias (DEF)", "M. Akanji (DEF)", "J. Gvardiol (DEF)", "Rodri (MED)", "K. De Bruyne (MED)", "B. Silva (MED)", "P. Foden (DEL)", "E. Haaland (DEL)", "J. Doku (DEL)"],
    "liverpool": ["Alisson (POR)", "T. Alexander-Arnold (DEF)", "I. Konaté (DEF)", "V. van Dijk (DEF)", "A. Robertson (DEF)", "R. Gravenberch (MED)", "A. Mac Allister (MED)", "D. Szoboszlai (MED)", "M. Salah (DEL)", "D. Núñez (DEL)", "L. Díaz (DEL)"],
    "arsenal": ["D. Raya (POR)", "B. White (DEF)", "W. Saliba (DEF)", "G. Magalhães (DEF)", "O. Zinchenko (DEF)", "D. Rice (MED)", "M. Ødegaard (MED)", "K. Havertz (MED)", "B. Saka (DEL)", "G. Jesus (DEL)", "G. Martinelli (DEL)"],
    "chelsea": ["R. Sánchez (POR)", "M. Gusto (DEF)", "W. Fofana (DEF)", "L. Colwill (DEF)", "M. Cucurella (DEF)", "M. Caicedo (MED)", "E. Fernández (MED)", "C. Palmer (MED)", "N. Madueke (DEL)", "N. Jackson (DEL)", "J. Félix (DEL)"],
    "bayern": ["M. Neuer (POR)", "S. Boey (DEF)", "D. Upamecano (DEF)", "K. Min-jae (DEF)", "A. Davies (DEF)", "J. Kimmich (MED)", "A. Pavlović (MED)", "J. Musiala (MED)", "M. Olise (DEL)", "H. Kane (DEL)", "S. Gnabry (DEL)"],
    "psg": ["G. Donnarumma (POR)", "A. Hakimi (DEF)", "Marquinhos (DEF)", "W. Pacho (DEF)", "N. Mendes (DEF)", "W. Zaïre-Emery (MED)", "Vitinha (MED)", "J. Neves (MED)", "O. Dembélé (DEL)", "R. Kolo Muani (DEL)", "B. Barcola (DEL)"],
    "boca": ["S. Romero (POR)", "L. Advíncula (DEF)", "C. Lema (DEF)", "M. Rojo (DEF)", "L. Blanco (DEF)", "E. Fernández (MED)", "P. Fernández (MED)", "K. Zenón (MED)", "C. Medina (DEL)", "M. Merentiel (DEL)", "E. Cavani (DEL)"],
    "river": ["F. Armani (POR)", "A. Sant'Anna (DEF)", "G. Pezzella (DEF)", "P. Díaz (DEF)", "M. Acuña (DEF)", "M. Kranevitter (MED)", "I. Fernández (MED)", "M. Meza (MED)", "C. Echeverri (DEL)", "F. Colidio (DEL)", "M. Borja (DEL)"],
    "inter miami": ["D. Callender (POR)", "M. Weigandt (DEF)", "T. Avilés (DEF)", "H. Martínez (DEF)", "J. Alba (DEF)", "S. Busquets (MED)", "F. Redondo (MED)", "D. Gómez (MED)", "L. Messi (DEL)", "L. Suárez (DEL)", "R. Taylor (DEL)"],
}

def obtener_plantilla_probable_equipo(nombre_equipo: str) -> list[str]:
    eq_clean = str(nombre_equipo).lower().strip()
    
    # 1. Coincidencia directa
    for key, squad in PLANTILLAS_POR_EQUIPO.items():
        if key in eq_clean:
            return squad

    # 2. Si es liga femenil
    es_femenil = any(k in eq_clean for k in [" f", "femenil", "(f)", "women", " w"])
    if es_femenil:
        eq_base = eq_clean.replace(" femenil", "").replace(" f", "").replace(" (f)", "").replace(" women", "").strip()
        for key, squad in PLANTILLAS_POR_EQUIPO.items():
            if key in eq_base:
                return squad

    seed = zlib.crc32(eq_clean.encode('utf-8'))

    if es_femenil:
        nombres_pool = ["C. Corral", "L. Cervantes", "C. Jaramillo", "L. Ovalle", "S. Mayor", "S. Luebbert", "K. Palacios", "B. Félix", "E. Barreras", "P. Tajonar", "R. Bernal", "A. Pereira", "J. Hermoso", "S. Paños", "M. Zuazua"]
    elif any(k in eq_clean for k in ["real", "madrid", "barca", "barcelona", "atletico", "sevilla", "betis", "valencia", "athletic"]):
        nombres_pool = ["Rodrygo", "K. Mbappé", "Vinícius Jr.", "Pedri", "L. Yamal", "D. Olmo", "F. Valverde", "J. Bellingham", "A. Rüdiger", "T. Courtois", "R. Lewandowski"]
    elif any(k in eq_clean for k in ["manchester", "city", "liverpool", "arsenal", "chelsea", "tottenham", "newcastle", "villa"]):
        nombres_pool = ["E. Haaland", "P. Foden", "K. De Bruyne", "M. Salah", "B. Saka", "D. Rice", "C. Palmer", "V. van Dijk", "Alisson", "R. Dias", "Rodri"]
    else:
        nombres_pool = ["García", "Martínez", "López", "Hernández", "González", "Pérez", "Rodríguez", "Sánchez", "Ramírez", "Cruz", "Gómez", "Flores", "Morales", "Vázquez", "Jiménez"]

    idx_start = seed % len(nombres_pool)
    squad = []
    positions = ["(POR)", "(DEF)", "(DEF)", "(DEF)", "(DEF)", "(MED)", "(MED)", "(MED)", "(DEL)", "(DEL)", "(DEL)"]
    
    for i, pos in enumerate(positions):
        nombre = nombres_pool[(idx_start + i * 2) % len(nombres_pool)]
        squad.append(f"{nombre} {pos}")
        
    return squad
