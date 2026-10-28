"""Filtros iniciales de ofertas para software/PHP."""

import re
import unicodedata
from datetime import datetime, timedelta

from .config_inicial import (
    DIAS_MAX_DESDE_PUBLICACION,
    MODALIDAD_HIBRIDA,
    MODALIDAD_PRESENCIAL,
    MODALIDAD_REMOTA,
    PALABRAS_CLAVE,
    SALARIO_MINIMO_NO_REMOTO,
    SALARIO_MINIMO_REMOTO,
    UBICACIONES_MEDELLIN,
)


def puntuar_mejor_oferta(cargo: dict) -> tuple[int, str]:
    """Calcula una prioridad explicable para ordenar las ofertas válidas."""
    puntos = 0
    motivos = []
    salario = int(cargo.get("salario_num") or 0)
    modalidad = cargo.get("modalidad", "")
    dias = cargo.get("dias_desde_publicacion")
    texto = _normalizar(" ".join((cargo.get("titulo", ""), cargo.get("descripcion", ""))))

    if salario >= 6_000_000:
        puntos += 30
        motivos.append("salario >= 6M")
    elif salario >= 5_000_000:
        puntos += 20
        motivos.append("salario >= 5M")

    if modalidad == "remoto":
        puntos += 20
        motivos.append("remoto")

    if any(_normalizar(palabra) in texto for palabra in PALABRAS_CLAVE):
        puntos += 15
        motivos.append("keyword exacta")

    if dias in (0, 1):
        puntos += 15
        motivos.append("publicada <= 1 día")
    elif isinstance(dias, int) and dias <= 3:
        puntos += 10
        motivos.append("publicada <= 3 días")

    if any(palabra in texto for palabra in ("senior", "senior", "especialista", "lead")):
        puntos += 10
        motivos.append("nivel senior/especialista")

    if any(palabra in texto for palabra in ("temporal", "prestacion de servicios", "prestación de servicios")):
        puntos -= 10
        motivos.append("temporal/prestación de servicios")

    if salario == 0:
        puntos -= 10
        motivos.append("salario no indicado")

    return puntos, "; ".join(motivos)


def _normalizar(valor) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    return "".join(c for c in texto if not unicodedata.combining(c)).lower()


def _salario(cargo, texto):
    valor = cargo.get("salario_num") or cargo.get("salario_numerico") or 0
    if valor:
        return int(valor)
    encontrados = re.findall(r"\$\s*([\d.,]+)", texto)
    if not encontrados:
        return 0
    numero = re.sub(r"[,.]\d{2}$", "", encontrados[0])
    numero = numero.replace(".", "").replace(",", "")
    try:
        return int(numero)
    except ValueError:
        return 0


def _modalidad(texto):
    tiene_remoto = any(palabra in texto for palabra in map(_normalizar, MODALIDAD_REMOTA))
    tiene_presencial = any(palabra in texto for palabra in map(_normalizar, MODALIDAD_PRESENCIAL))
    if any(palabra in texto for palabra in map(_normalizar, MODALIDAD_HIBRIDA)) or (tiene_remoto and tiene_presencial):
        return "hibrido"
    if tiene_remoto:
        return "remoto"
    if tiene_presencial:
        return "presencial"
    return "no especificada"


def _dias_desde_publicacion(texto, cargo):
    for campo in ("fecha_publicacion", "fecha_publicado", "date_posted"):
        valor = cargo.get(campo)
        if isinstance(valor, datetime):
            return (datetime.now() - valor).days
        if valor:
            texto = f"{texto} {valor}"

    texto = _normalizar(texto)
    if re.search(r"hace\s+(\d+)\s*(hora|horas)", texto):
        return 0
    match = re.search(r"hace\s+(\d+)\s*(dia|dias|semana|semanas)", texto)
    if match:
        cantidad = int(match.group(1))
        return cantidad * (7 if "semana" in match.group(2) else 1)
    if "hoy" in texto or "ayer" in texto:
        return 0 if "hoy" in texto else 1

    # Acepta fechas explícitas comunes en español o ISO.
    for patron, formato in ((r"(\d{4}-\d{2}-\d{2})", "%Y-%m-%d"),
                            (r"(\d{1,2}/\d{1,2}/\d{4})", "%d/%m/%Y")):
        match = re.search(patron, texto)
        if match:
            try:
                fecha = datetime.strptime(match.group(1), formato)
                return max(0, (datetime.now() - fecha).days)
            except ValueError:
                pass
    return None


def filtrar_oferta_inicial(cargo: dict):
    titulo = _normalizar(cargo.get("titulo"))
    descripcion = _normalizar(cargo.get("descripcion"))
    fuente = _normalizar(cargo.get("texto_fuente"))
    texto = " ".join((titulo, descripcion, fuente, _normalizar(cargo.get("ubicacion"))))

    keywords = [k for k in PALABRAS_CLAVE if _normalizar(k) in texto]
    if not keywords:
        return None, "No contiene software ni PHP"

    modalidad = _modalidad(texto)
    # Algunos portales colocan la calificación de la empresa en "ubicacion";
    # incluir también la ciudad solicitada evita perder ofertas válidas.
    ubicacion = _normalizar(
        f"{cargo.get('ubicacion', '')} {cargo.get('ciudad', '')}"
    )
    es_remoto = modalidad == "remoto"
    ubicacion_valida = es_remoto or any(lugar in ubicacion for lugar in UBICACIONES_MEDELLIN)
    if not ubicacion_valida:
        return None, "Oferta no remota fuera de Medellín y alrededores"

    salario = _salario(cargo, texto)
    minimo = SALARIO_MINIMO_REMOTO if es_remoto else SALARIO_MINIMO_NO_REMOTO
    if salario < minimo:
        return None, f"Salario inferior al mínimo ({salario:,} < {minimo:,}) o no indicado"

    dias = _dias_desde_publicacion(texto, cargo)
    if dias is None:
        return None, "No se pudo determinar la fecha de publicación"
    if dias > DIAS_MAX_DESDE_PUBLICACION:
        return None, f"Publicada hace {dias} días (máximo {DIAS_MAX_DESDE_PUBLICACION})"

    cargo["palabras_clave_encontradas"] = ", ".join(keywords)
    cargo["modalidad"] = modalidad
    cargo["salario_num"] = salario
    cargo["dias_desde_publicacion"] = dias
    cargo["puntaje_mejor_oferta"], cargo["motivos_puntaje"] = puntuar_mejor_oferta(cargo)
    return cargo, None
