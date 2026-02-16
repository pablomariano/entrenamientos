# 🚀 Guía Rápida de Inicio

Guía para empezar a usar el proyecto en 5 minutos.

## 📋 Requisitos Previos

- Python 3.7 o superior
- Dongle Polar DataLink USB
- Reloj Polar RCX5

## ⚡ Inicio Rápido (3 pasos)

### 1. Instalar dependencias

```bash
pip install polar-rcx5-datalink
```

### 2. Aplicar correcciones

Lee y aplica los cambios en: **`patches/README.md`**

Estos son cambios manuales en 3 archivos de la librería instalada:
- `datalink.py` - Fix de timeout en Windows
- `utils.py` - Fix de StopIteration
- `parser.py` - Fix para relojes sin GPS

**⚠️ Importante**: Sin estos cambios, el proyecto no funcionará correctamente.

### 3. Exportar y visualizar

```bash
# Exportar datos del reloj
python scripts/exportar_para_dashboard.py

# Ver dashboard
python scripts/abrir_dashboard.py
```

¡Listo! El dashboard se abrirá en tu navegador.

---

## 🔍 Si Algo Falla

### Verificar que los patches funcionan
```bash
python scripts/verificar_correccion.py
```

### Diagnosticar problemas
```bash
python scripts/diagnostico_sesiones.py
```

### Problemas con HR
```bash
python scripts/diagnosticar_hr.py
```

---

## 📊 Características del Dashboard

- ✅ Estadísticas generales (total entrenamientos, tiempo, HR)
- ✅ Gráfico de entrenamientos por mes
- ✅ Evolución de HR promedio
- ✅ Duración por mes
- ✅ **Evolución de HR por sesión** (selector + gráfico)
- ✅ Lista completa de entrenamientos

---

## 💡 Consejos

1. **Primera vez**: Ejecuta `encontrar_offset_hr.py` si tienes problemas con HR
2. **Sin reloj a mano**: Usa `revisar_sesion_json.py` para analizar datos ya exportados
3. **Desarrollo**: Abre `dashboard/index.html` directamente en tu editor favorito

---

## 📚 Documentación Completa

- **README.md** - Documentación principal
- **ROADMAP.md** - Plan de desarrollo
- **DEPLOY.md** - Despliegue web
- **ESTRUCTURA.md** - Estructura del proyecto
- **docs/** - Documentación adicional

---

**Tiempo estimado de configuración**: 10-15 minutos

**Última actualización**: Febrero 2026
