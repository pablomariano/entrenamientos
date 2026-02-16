# Polar RCX5 Dashboard - Exportador y Visualizador de Entrenamientos

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Herramienta completa para exportar y visualizar sesiones de entrenamiento del reloj Polar RCX5, incluyendo soluciones para sesiones problemáticas y un dashboard interactivo.

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Problemas Resueltos](#problemas-resueltos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Roadmap](#roadmap)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## 🎯 Descripción

Este proyecto permite exportar sesiones de entrenamiento del reloj Polar RCX5 en formato estructurado JSON para su visualización en un dashboard interactivo. Incluye soluciones para problemas comunes de parsing y manejo de sesiones con datos incompletos o corruptos.

### ¿Por qué este proyecto?

El reloj Polar RCX5 es un dispositivo antiguo pero funcional que almacena datos de entrenamiento. Sin embargo:
- El software oficial de Polar ya no está disponible o es difícil de usar
- Las herramientas de línea de comandos existentes tienen problemas con sesiones antiguas
- No existe una solución moderna para visualizar todos los datos históricos

Este proyecto resuelve estos problemas proporcionando:
- ✅ Exportación confiable de todas las sesiones (incluso problemáticas)
- ✅ Dashboard interactivo para visualización
- ✅ Formato JSON estructurado para integración con otras herramientas

## ✨ Características

### Exportación de Datos
- **Exportación completa**: Extrae todas las sesiones del reloj, incluyendo las problemáticas
- **Múltiples formatos**: Soporta exportación en formato raw (JSON), bin y TCX
- **Información básica garantizada**: Incluso las sesiones que no se pueden parsear completamente incluyen fecha, duración y estadísticas de frecuencia cardíaca
- **Datos estructurados**: Formato JSON limpio y fácil de procesar

### Dashboard Interactivo
- 📊 Gráficos de entrenamientos por mes
- ❤️ Visualización de frecuencia cardíaca promedio
- 📏 Estadísticas de distancia total
- 📋 Lista completa de entrenamientos con filtros
- 🎨 Interfaz moderna y responsive

### Soluciones Técnicas
- Corrección de bugs en la librería `polar-rcx5-datalink`
- Manejo robusto de errores con información detallada
- Parser mejorado con mejor diagnóstico de problemas

## 🐛 Problemas Resueltos

### 1. USBTimeoutError en Windows
**Problema**: El código original solo manejaba el código de error de timeout de Linux (110), causando fallos en Windows (10060).

**Solución**: Modificación de `datalink.py` para reconocer el código de error correcto en Windows.

**Archivo modificado**: 
```
C:\Users\Pablo\AppData\Local\Programs\Python\Python314\Lib\site-packages\polar_rcx5_datalink\datalink.py
```

**Cambio**:
```python
# Antes
_ERROR_TIMEOUT_CODE = 110

# Después  
_ERROR_TIMEOUT_CODE = 10060  # Código correcto para Windows
```

### 2. StopIteration en Python 3.7+
**Problema**: La función `pop_zeroes()` lanzaba `StopIteration` cuando todos los elementos eran cero, causando `RuntimeError` en Python 3.7+.

**Solución**: Uso de valor por defecto en `next()` para manejar el caso cuando todos los elementos son cero.

**Archivo modificado**: 
```
C:\Users\Pablo\AppData\Local\Programs\Python\Python314\Lib\site-packages\polar_rcx5_datalink\utils.py
```

**Cambio**:
```python
# Antes
index = next(i for i, v in enumerate(reversed(items)) if v != 0)

# Después
index = next((i for i, v in enumerate(reversed(items)) if v != 0), len(items))
```

### 3. Sesiones Problemáticas
**Problema**: 25 de 34 sesiones no se podían parsear completamente debido a cambios en el firmware o datos corruptos.

**Solución**: 
- Parser mejorado con mejor manejo de errores
- Extracción de información básica incluso cuando el parsing completo falla
- Script de diagnóstico para identificar problemas específicos

## 📦 Instalación

### Requisitos Previos

1. **Python 3.7 o superior**
   ```bash
   python --version
   ```

2. **libusb** (requerido por pyusb)
   - **Windows**: Descargar desde [libusb.info](https://libusb.info/) o usar [Zadig](https://zadig.akeo.ie/) para instalar el driver WinUSB
   - **Linux**: Generalmente incluido en la distribución
   - **macOS**: `brew install libusb`

3. **Polar DataLink USB Dongle**
   - Conectado al ordenador
   - Driver instalado correctamente

### Instalación de Dependencias

```bash
pip install polar-rcx5-datalink
```

### Aplicar Correcciones

Las correcciones de bugs deben aplicarse manualmente a los archivos instalados:

1. **Corregir timeout en Windows** (`datalink.py`):
   ```python
   # Cambiar línea ~47
   _ERROR_TIMEOUT_CODE = 10060
   ```

2. **Corregir StopIteration** (`utils.py`):
   ```python
   # Cambiar función pop_zeroes() línea ~50
   index = next((i for i, v in enumerate(reversed(items)) if v != 0), len(items))
   ```

## 🚀 Uso

Ver **QUICKSTART.md** para inicio rápido.

### 1. Exportar Datos para Dashboard

```bash
python scripts/exportar_para_dashboard.py
```

Este script:
- Sincroniza con el reloj Polar RCX5
- Exporta todas las sesiones en formato JSON estructurado
- Guarda el resultado en `entrenamientos_dashboard/entrenamientos.json`

**Proceso**:
1. Ejecuta el comando
2. Cuando se te indique, selecciona `Connect > Start synchronizing` en tu reloj
3. Coloca el reloj cerca del dongle DataLink
4. Espera a que termine la sincronización

### 2. Visualizar Dashboard Local

**Opción A: Servidor Local (Recomendado)**
```bash
python scripts/abrir_dashboard.py
```
Abre automáticamente el dashboard en tu navegador con un servidor HTTP local.

**Opción B: Abrir HTML Directamente**
1. Abre `dashboard/index.html` en tu navegador
2. Si aparece un error, selecciona manualmente el archivo `entrenamientos_dashboard/entrenamientos.json`

### 3. Exportar en Otros Formatos

```bash
# Formato TCX (solo sesiones parseables)
rcx5 export --format tcx --out ./entrenamientos

# Formato RAW (todas las sesiones)
rcx5 export --format raw --out ./entrenamientos_raw

# Formato BIN
rcx5 export --format bin --out ./entrenamientos_bin
```

### 4. Diagnóstico de Sesiones Problemáticas

```bash
python scripts/diagnostico_sesiones.py
```

Analiza cada sesión individualmente y muestra información detallada sobre errores de parsing.

## 📁 Estructura del Proyecto

Ver **ESTRUCTURA.md** para detalles completos.

```
polar-rcx5-dashboard/
├── README.md                          # Este archivo
├── QUICKSTART.md                      # Guía rápida de inicio
├── LICENSE                            # Licencia MIT
├── .gitignore                         # Archivos a ignorar
├── ROADMAP.md                         # Plan de desarrollo
├── DEPLOY.md                          # Guía de despliegue
├── CONTRIBUTING.md                    # Guía para contribuidores
├── CHANGELOG.md                       # Historial de cambios
├── ESTRUCTURA.md                      # Estructura detallada
│
├── scripts/                           # Scripts Python
│   ├── exportar_para_dashboard.py   # ⭐ Script principal
│   ├── abrir_dashboard.py           # Servidor local
│   └── ... (8 scripts en total)
│
├── dashboard/                         # Dashboard web
│   └── index.html                    # ⭐ Dashboard interactivo
│
├── docs/                              # Documentación adicional
│   └── ... (5 archivos markdown)
│
└── patches/                           # Patches necesarios
    └── README.md                     # ⭐ Instrucciones de parcheo
```

## 📊 Formato de Datos JSON

El archivo `entrenamientos.json` tiene la siguiente estructura:

```json
{
  "export_date": "2026-02-13T10:30:00",
  "total_sessions": 34,
  "sessions_fully_parseable": 9,
  "sessions_basic_info_only": 25,
  "sessions": [
    {
      "id": "2026-02-10T14:44:53Z",
      "start_time": "2026-02-10T11:44:53",
      "start_utctime": "2026-02-10T14:44:53Z",
      "duration_seconds": 8172,
      "duration_formatted": "02:16:12",
      "has_hr": true,
      "has_gps": true,
      "parseable": true,
      "muestras_parseadas": true,
      "num_muestras": 168,
      "hr_avg": 150,
      "hr_max": 180,
      "hr_min": 120,
      "distance_meters": 12345.67,
      "max_speed_ms": 5.2,
      "max_speed_kmh": 18.7,
      "sample_rate_seconds": 5,
      "first_sample": {
        "lat": 39.9149567,
        "lon": 148.3754800,
        "hr": 150
      },
      "last_sample": {
        "lat": 39.9250000,
        "lon": 148.3800000,
        "hr": 145
      }
    }
  ]
}
```

### Sesiones No Parseables

Las sesiones que no se pueden parsear completamente incluyen al menos:

```json
{
  "start_time": "2020-11-15T14:17:31",
  "duration_seconds": 3600,
  "duration_formatted": "01:00:00",
  "has_hr": true,
  "has_gps": true,
  "parseable": false,
  "hr_avg": 140,
  "hr_max": 170,
  "hr_min": 110,
  "error_parsing": "Error description",
  "error_type": "ParserError"
}
```

## 🗺️ Roadmap

Ver [ROADMAP.md](ROADMAP.md) para detalles completos del plan de desarrollo.

### Próximas Mejoras

- [ ] Dashboard web en línea (hosting)
- [ ] Autenticación y multi-usuario
- [ ] Sincronización automática programada
- [ ] Exportación a Strava/Garmin Connect
- [ ] Análisis avanzado de rendimiento
- [ ] Visualización de rutas en mapas
- [ ] Comparación de entrenamientos
- [ ] API REST para integraciones

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Áreas donde se necesita ayuda

- Mejora del parser para sesiones problemáticas
- Nuevas visualizaciones para el dashboard
- Soporte para otros modelos de relojes Polar
- Documentación y ejemplos

## 📝 Notas Técnicas

### Limitaciones Conocidas

1. **Sesiones Antiguas**: Algunas sesiones antiguas (2020-2023) no se pueden parsear completamente debido a cambios en el firmware del reloj o datos corruptos.

2. **Dependencia de libusb**: Requiere configuración específica del sistema operativo.

3. **Modificaciones Manuales**: Las correcciones de bugs requieren modificación manual de archivos instalados por pip.

### Compatibilidad

- ✅ Windows 10/11
- ✅ Linux (distribuciones con libusb)
- ✅ macOS (con libusb instalado)
- ✅ Python 3.7 - 3.14

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [polar-rcx5-datalink](https://github.com/purpledot/polar-rcx5-datalink) - Librería base para comunicación con el reloj
- [Chart.js](https://www.chartjs.org/) - Librería de gráficos para el dashboard

## 📧 Contacto

Para preguntas, problemas o sugerencias, por favor abre un issue en GitHub.

---

**Última actualización**: Febrero 2026
