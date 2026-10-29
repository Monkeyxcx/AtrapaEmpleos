"""Utilidades comunes para detectar y normalizar salarios."""

import re


def extraer_salario_robusto(texto: str):
    """Extrae el primer salario con formato colombiano del texto."""
    if not texto:
        return 0, "No indica"

    match = re.search(r"\$\s*([\d\.\,]+)", texto.replace("'", ""))
    if not match:
        return 0, texto

    num_str = re.sub(r"[,.]\d{2}$", "", match.group(1))
    num_str = num_str.replace(".", "").replace(",", "")
    if not num_str.isdigit():
        return 0, texto

    valor = int(num_str)
    return valor, f"$ {valor:,}"
