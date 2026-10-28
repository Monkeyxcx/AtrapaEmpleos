"""Interfaz local para configurar y ejecutar el buscador de ofertas."""

import json
import subprocess
import sys
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config_usuario.json"
DEFAULTS = {
    "palabras_clave": ["software", "php"],
    "ciudades": ["Medellin", "Bogota", "Cali", "Barranquilla"],
    "salario_minimo_remoto": 3_000_000,
    "salario_minimo_no_remoto": 3_500_000,
    "dias_max_desde_publicacion": 7,
    "mejores_max_resultados": 10,
}


def load_config():
    if not CONFIG_PATH.exists():
        return DEFAULTS.copy()
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            saved = json.load(file)
        config = DEFAULTS.copy()
        config.update(saved)
        return config
    except (OSError, json.JSONDecodeError):
        return DEFAULTS.copy()


def save_config(config):
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)


st.set_page_config(page_title="Buscador de ofertas", page_icon="🔎", layout="centered")
st.title("🔎 Buscador de ofertas laborales")
st.caption("Configura los criterios y ejecuta el scraping de forma asistida.")

config = load_config()

with st.form("configuracion"):
    st.subheader("Criterios de búsqueda")
    keywords_text = st.text_input(
        "Palabras clave (separadas por coma)",
        value=", ".join(config["palabras_clave"]),
        help="Ejemplo: software, php, laravel",
    )
    cities_text = st.text_input(
        "Ciudades (separadas por coma)",
        value=", ".join(config["ciudades"]),
    )

    col1, col2 = st.columns(2)
    with col1:
        remote_salary = st.number_input(
            "Salario mínimo remoto",
            min_value=0,
            value=int(config["salario_minimo_remoto"]),
            step=100_000,
        )
        max_days = st.number_input(
            "Máximo de días desde publicación",
            min_value=1,
            value=int(config["dias_max_desde_publicacion"]),
            step=1,
        )
    with col2:
        local_salary = st.number_input(
            "Salario mínimo híbrido/presencial",
            min_value=0,
            value=int(config["salario_minimo_no_remoto"]),
            step=100_000,
        )
        best_count = st.number_input(
            "Cantidad de mejores ofertas",
            min_value=1,
            value=int(config["mejores_max_resultados"]),
            step=1,
        )

    submitted = st.form_submit_button("Guardar parámetros", type="primary")

if submitted:
    keywords = [item.strip() for item in keywords_text.split(",") if item.strip()]
    cities = [item.strip() for item in cities_text.split(",") if item.strip()]
    if not keywords or not cities:
        st.error("Debes indicar al menos una palabra clave y una ciudad.")
    else:
        save_config({
            "palabras_clave": keywords,
            "ciudades": cities,
            "salario_minimo_remoto": int(remote_salary),
            "salario_minimo_no_remoto": int(local_salary),
            "dias_max_desde_publicacion": int(max_days),
            "mejores_max_resultados": int(best_count),
        })
        st.success("Parámetros guardados correctamente.")

st.divider()
st.subheader("Ejecución")
st.warning("La búsqueda puede tardar varios minutos y realiza consultas a los portales configurados.")

if st.button("🚀 Ejecutar búsqueda", type="secondary"):
    with st.spinner("Ejecutando scraper. Esto puede tardar varios minutos..."):
        resultado = subprocess.run(
            [sys.executable, "main.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    if resultado.returncode == 0:
        st.success("Búsqueda terminada correctamente.")
    else:
        st.error(f"El scraper terminó con código {resultado.returncode}.")
    st.code(resultado.stdout[-12000:] or "Sin salida del scraper.")
    if resultado.stderr:
        st.error(resultado.stderr[-4000:])

st.divider()
st.subheader("Resultados")
st.markdown("El dashboard se genera en `index.html` después de cada búsqueda.")
st.code(str(ROOT / "index.html"))
