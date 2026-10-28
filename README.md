# 🚀 Pegaso Job Scout

Buscador asistido de ofertas laborales para Colombia. Pegaso consulta portales de empleo, aplica filtros configurables, calcula un puntaje de prioridad y genera reportes en Excel junto con un dashboard HTML.

> El proyecto solo recopila y organiza ofertas. No envía hojas de vida ni aplica automáticamente a las vacantes.

## Funcionalidades

- Consulta ofertas en Computrabajo, Magneto365, ElEmpleo y LinkedIn.
- Filtra por palabras clave y ciudades.
- Filtra por modalidad remota, híbrida o presencial.
- Aplica salarios mínimos distintos para ofertas remotas y no remotas.
- Descarta ofertas antiguas según el número máximo de días configurado.
- Evita reprocesar ofertas ya analizadas usando SQLite.
- Calcula un puntaje de prioridad para encontrar las mejores vacantes.
- Genera archivos Excel con ofertas válidas, mejores ofertas y descartadas.
- Genera `index.html` con búsqueda, filtro por ciudad y filtro por score.
- Incluye un formulario web en Streamlit para modificar los parámetros sin editar código.

## Requisitos

- Windows, macOS o Linux.
- Python 3.10 o superior.
- Acceso a internet.

## Instalación en Windows

Desde PowerShell:

```powershell
cd C:\Github\proyecto-directores-estructuracion
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

## Usar el formulario de configuración

Inicia la interfaz:

```powershell
streamlit run app.py
```

Abre en el navegador:

```text
http://localhost:8501
```

El formulario permite modificar:

- Palabras clave, por ejemplo `software, php, laravel`.
- Ciudades.
- Salario mínimo remoto.
- Salario mínimo híbrido/presencial.
- Días máximos desde la publicación.
- Cantidad de mejores ofertas.

Al guardar, los parámetros quedan en `config_usuario.json`. Este archivo es local y está excluido de Git.

## Ejecutar directamente el scraper

También puede ejecutarse sin el formulario:

```powershell
python main.py
```

La ejecución consulta las combinaciones de palabras clave y ciudades configuradas, procesa los resultados y genera los reportes.

## Filtros actuales

La configuración inicial utiliza:

- Palabras clave: `software` y `php`.
- Ciudades: Medellín, Bogotá, Cali y Barranquilla.
- Salario remoto mínimo: `$3.000.000`.
- Salario híbrido/presencial mínimo: `$3.500.000`.
- Antigüedad máxima: 7 días.
- Para ofertas no remotas se priorizan Medellín y sus alrededores.

Los valores se pueden cambiar desde el formulario.

## Puntaje de prioridad

Las ofertas aprobadas reciben un puntaje explicable:

| Criterio | Puntos |
|---|---:|
| Salario desde $6.000.000 | +30 |
| Salario desde $5.000.000 | +20 |
| Modalidad remota | +20 |
| Coincidencia con palabra clave | +15 |
| Publicada hoy o ayer | +15 |
| Publicada hace máximo 3 días | +10 |
| Nivel senior, especialista o lead | +10 |
| Temporal o prestación de servicios | -10 |
| Salario no indicado | -10 |

## Archivos generados

```text
data/
├── TODOS_multi_*.xlsx          # Todas las ofertas válidas
├── MEJORES_multi_*.xlsx        # Ofertas ordenadas por prioridad
├── PREMIUM_multi_*.xlsx        # Reporte principal de ofertas válidas
└── DESCARTADOS_multi_*.xlsx    # Ofertas y motivo del descarte

data/vacantes.db                # SQLite local, no se sube al repositorio
index.html                      # Dashboard generado automáticamente
config_usuario.json             # Configuración local del formulario
```

## Dashboard HTML

El archivo `index.html` se genera al terminar cada búsqueda. Incluye:

- Búsqueda por cargo o empresa.
- Filtro por ciudad.
- Filtro por score mínimo.
- Enlace directo a cada oferta.

Puede abrirse directamente o mediante un servidor local:

```powershell
python -m http.server 8000
```

Después visita `http://localhost:8000`.

## Base de datos SQLite

SQLite se crea automáticamente en `data/vacantes.db`. Contiene:

- `ofertas`: ofertas válidas encontradas.
- `procesados`: identificadores usados para evitar duplicados.

No requiere instalar un servidor de base de datos.

## Estructura principal

```text
app.py                         # Formulario Streamlit
main.py                        # Punto de entrada del scraper
scraper/
├── config_inicial.py          # Configuración predeterminada y del usuario
├── filtro_inicial.py          # Validación y puntaje
├── main_multi.py              # Flujo multifuente
├── dashboard_generator.py     # Generación de index.html
├── db.py                      # SQLite
└── portales/                  # Adaptadores de cada portal
```

## Consideraciones

- Los portales pueden cambiar su HTML y romper selectores.
- Deben respetarse los términos de uso y límites de cada portal.
- No se deben enviar solicitudes masivas ni automatizar aplicaciones sin revisión humana.
- La interfaz está pensada inicialmente para uso local.
