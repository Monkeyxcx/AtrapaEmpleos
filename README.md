# AtrapaEmpleos

Buscador asistido de ofertas laborales para Colombia. AtrapaEmpleos consulta portales de empleo, aplica filtros configurables, calcula un puntaje de prioridad y genera reportes en Excel junto con un dashboard HTML.

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

## Instalación y primer inicio en Windows

Los comandos siguientes deben ejecutarse desde la carpeta raíz del proyecto, es decir, la carpeta que contiene `app.py`, `main.py` y `requirements.txt`.

Si todavía no has descargado el proyecto:

```cmd
git clone https://github.com/Monkeyxcx/AtrapaEmpleos.git
cd AtrapaEmpleos
```

Si ya lo descargaste en otra ubicación, abre CMD o PowerShell directamente dentro de esa carpeta. También puedes navegar hasta ella usando la ruta donde clonaste el repositorio.

### Opción A: CMD

Abre **Símbolo del sistema (CMD)** y ejecuta:

```cmd
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m streamlit run app.py
```

### Opción B: PowerShell

Abre PowerShell y ejecuta:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m streamlit run app.py
```

> Usar `python -m streamlit` es más confiable que escribir `streamlit` directamente, porque garantiza que se utilice el Streamlit instalado dentro de `.venv`.

Si el entorno virtual ya existe, no es necesario crearlo nuevamente. Basta con activarlo y ejecutar:

```cmd
.venv\Scripts\activate.bat
python -m streamlit run app.py
```

Al iniciar Streamlit por primera vez puede aparecer:

```text
Welcome to Streamlit!
Email:
```

Deja el campo vacío y presiona **Enter**. El correo es opcional.

La interfaz se abrirá en:

```text
http://localhost:8501
```

Para detener el servidor, vuelve a la ventana de CMD o PowerShell y presiona:

```text
Ctrl + C
```

### Problemas frecuentes

Si aparece:

```text
'streamlit' no se reconoce como un comando interno o externo
```

usa la forma explícita:

```cmd
.venv\Scripts\python.exe -m streamlit run app.py
```

Si el puerto `8501` está ocupado, inicia Streamlit en otro puerto:

```cmd
.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502
```

En ese caso, abre `http://localhost:8502`.

## Usar el formulario de configuración

Si la interfaz ya está instalada, inicia únicamente con:

```powershell
python -m streamlit run app.py
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

También puede ejecutarse sin abrir Streamlit. Con el entorno virtual activado:

```cmd
.venv\Scripts\activate.bat
python main.py
```

O sin activar el entorno virtual:

```cmd
.venv\Scripts\python.exe main.py
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

data/vacantes.db                # SQLite local
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
├── db.py                      # SQLite local
└── portales/                  # Adaptadores de cada portal
```

## Consideraciones

- Los portales pueden cambiar su HTML y romper selectores.
- Deben respetarse los términos de uso y límites de cada portal.
- No se deben enviar solicitudes masivas ni automatizar aplicaciones sin revisión humana.
- La interfaz está pensada inicialmente para uso local.
