# 📁 Estructura del Proyecto

```
polar-rcx5-dashboard/
│
├── 📄 README.md                      # Documentación principal del proyecto
├── 📄 LICENSE                        # Licencia MIT
├── 📄 .gitignore                     # Archivos a ignorar en Git
├── 📄 ROADMAP.md                     # Plan de desarrollo futuro
├── 📄 DEPLOY.md                      # Guía de despliegue web
├── 📄 CONTRIBUTING.md                # Guía para contribuidores
├── 📄 ESTRUCTURA.md                  # Este archivo
│
├── 📁 scripts/                       # Scripts Python
│   ├── 📄 README.md                  # Documentación de scripts
│   ├── 🐍 exportar_para_dashboard.py    # ⭐ Script principal de exportación
│   ├── 🐍 abrir_dashboard.py            # Servidor local para dashboard
│   ├── 🐍 diagnostico_sesiones.py       # Diagnóstico general
│   ├── 🐍 diagnosticar_hr.py            # Diagnóstico de HR
│   ├── 🐍 encontrar_offset_hr.py        # Encuentra offset correcto
│   ├── 🐍 verificar_correccion.py       # Verifica que patches funcionan
│   ├── 🐍 revisar_sesion_json.py        # Analiza sesión desde JSON
│   └── 🐍 analizar_sesion.py            # Analiza sesión desde reloj
│
├── 📁 dashboard/                     # Dashboard web
│   ├── 📄 README.md                  # Documentación del dashboard
│   └── 🌐 index.html                 # ⭐ Dashboard interactivo
│
├── 📁 docs/                          # Documentación adicional
│   ├── 📄 explicacion_formatos.md    # Explica formatos RAW/TCX/BIN
│   ├── 📄 PROBLEMA_DISTANCIA.md      # Documentación problema GPS
│   ├── 📄 CAMBIOS_REALIZADOS.md      # Resumen de cambios
│   ├── 📄 NUEVA_FUNCIONALIDAD_HR.md  # Doc de gráfico de evolución
│   └── 📄 RESUMEN_PROYECTO.md        # Resumen completo del proyecto
│
└── 📁 patches/                       # Patches para librería instalada
    └── 📄 README.md                  # ⭐ Instrucciones de parcheo

📁 entrenamientos_dashboard/          # (Generado) Datos exportados
    └── 📄 entrenamientos.json        # JSON con todas las sesiones
```

## 📌 Archivos Clave

### Para Empezar
1. **README.md** - Lee esto primero
2. **patches/README.md** - Aplica estos cambios a la librería
3. **scripts/exportar_para_dashboard.py** - Ejecuta esto para exportar datos
4. **dashboard/index.html** - Abre esto (o usa abrir_dashboard.py)

### Para Desarrollo
- **ROADMAP.md** - Plan de futuras mejoras
- **DEPLOY.md** - Cómo desplegar a producción
- **CONTRIBUTING.md** - Cómo contribuir al proyecto

### Para Diagnóstico
- **scripts/diagnostico_sesiones.py** - Problemas generales
- **scripts/diagnosticar_hr.py** - Problemas específicos de HR
- **scripts/encontrar_offset_hr.py** - Encontrar offset correcto

## 🎯 Flujo de Trabajo

### Configuración Inicial
```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/polar-rcx5-dashboard.git
cd polar-rcx5-dashboard

# 2. Instalar dependencias
pip install polar-rcx5-datalink

# 3. Aplicar patches
# Ver patches/README.md

# 4. Verificar
python scripts/verificar_correccion.py

# 5. Exportar datos
python scripts/exportar_para_dashboard.py

# 6. Ver dashboard
python scripts/abrir_dashboard.py
```

### Uso Regular
```bash
# Exportar nuevos datos
python scripts/exportar_para_dashboard.py

# Ver dashboard
python scripts/abrir_dashboard.py
```

## 📦 Dependencias

### Python
- `polar-rcx5-datalink` - Comunicación con el reloj
- `click` - Interfaz de línea de comandos
- `pytz` - Manejo de zonas horarias
- `geopy` - Cálculos geográficos (solo si se usa GPS)

### Web
- `Chart.js` (CDN) - Gráficos interactivos

## 🔒 Archivos Ignorados (.gitignore)

No se suben a Git:
- `entrenamientos_dashboard/` - Datos personales
- `*.json` - Archivos de datos
- `*.tcx` - Archivos de entrenamiento
- `__pycache__/` - Cache de Python
- `.venv/` - Entornos virtuales

## 📝 Notas

- Los scripts asumen que se ejecutan desde la raíz del proyecto o desde `scripts/`
- Los datos se exportan a `entrenamientos_dashboard/` relativo al directorio actual
- El dashboard busca datos en `entrenamientos_dashboard/entrenamientos.json`

---

**Última actualización**: Febrero 2026
