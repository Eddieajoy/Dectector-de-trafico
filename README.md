# AI Vehicle Detection System

Sistema de detección y clasificación de vehículos usando inteligencia artificial.

## Características
- Detección en tiempo real de vehículos
- Clasificación en 4 categorías: autos, camiones, buses y motocicletas
- Interfaz web interactiva
- Generación de reportes PDF
- Estadísticas en tiempo real

## Requisitos Previos
1. Python 3.8 o superior (https://www.python.org/downloads/)
2. Git (https://git-scm.com/download/win)
3. Visual Studio Code (recomendado) (https://code.visualstudio.com/)

## Instalación en Windows 11

1. Abrir PowerShell como administrador:
   - Presiona Windows + X
   - Selecciona "Windows PowerShell (Admin)" o "Terminal (Admin)"

2. Clonar el repositorio:
```powershell
git clone 
cd ai-vehicle-detection
```

3. Crear y activar entorno virtual:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

4. Instalar dependencias:
```powershell
pip install -r requirements.txt
```

5. ejecutar el modelo:
```powershell
python src/utils/setup.py
```

## Uso

1. Coloca tu video de prueba(oh usa el que ya viene):
   - Renombra tu video a `input_video.mp4`
   - Cópialo a la carpeta `data/videos/`

2. Ejecuta la aplicación:
```powershell
python main.py
```

3. Abre tu navegador y ve a:
```
http://localhost:5000
```

4. En la interfaz web podrás:
   - Iniciar/pausar la detección con los botones Play/Pause
   - Ver las detecciones en tiempo real
   - Reiniciar el video con el botón Replay cuando termine
   - Generar un reporte PDF con las estadísticas

5. Para generar el reporte PDF manualmente:
```powershell
python -m src.generate_report
```
   El reporte se guardará en `data//vehicle_detection_report.pdf`

## Solución de Problemas

1. Si hay error al instalar dependencias:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

2. Si hay error con el modelo:
```powershell
# Limpiar la carpeta de modelos
Remove-Item -Path "data/models/*" -Force
# Volver a configurar
python -m src.utils.setup
```

3. Si el video no se reproduce:
   - Asegúrate de que el video esté en formato MP4
   - Verifica que el nombre sea exactamente `input_video.mp4`
   - Comprueba que esté en la carpeta `data/videos/`

## Estructura del Proyecto
- `src/`: Código fuente del proyecto
  - `api/`: Endpoints y rutas
  - `services/`: Servicios principales
  - `templates/`: Plantillas HTML
  - `tools/`: Herramientas y configuración
  - `data/`: Almacena videos, modelos y resultados
    - `config/`: Archivos de configuración
    - `models/`: Modelos entrenados
    - `output/`: Resultados y reportes
    - `videos/`: Videos de entrada

## Autor
[Christian Encalada]

## Licencia
MIT
