# ✅ Nueva Funcionalidad: Gráfico de Evolución de Frecuencia Cardíaca

## 📋 Resumen

Se ha agregado al dashboard la capacidad de ver la evolución de la frecuencia cardíaca durante una sesión específica.

## 🎯 Funcionalidades Agregadas

### 1. Selector de Sesión
- Dropdown con todas las sesiones que tienen muestras de HR disponibles
- Muestra fecha, hora y duración de cada sesión
- Solo muestra sesiones con datos de HR parseados

### 2. Gráfico de Evolución de HR
- Muestra la frecuencia cardíaca a lo largo del tiempo durante la sesión
- Eje X: Tiempo en minutos desde el inicio
- Eje Y: Frecuencia cardíaca en bpm
- Línea de promedio: Muestra el HR promedio como referencia
- Interactivo: Hover sobre puntos para ver valores exactos

### 3. Información de Sesión
- Muestra detalles de la sesión seleccionada:
  - Fecha y hora
  - Duración
  - HR Promedio, Máximo, Mínimo
  - Número de muestras

## 🔧 Cambios Realizados

### 1. `exportar_para_dashboard.py`

**Modificaciones**:
- ✅ Ahora parsea las muestras de HR de cada sesión
- ✅ Incluye timestamps y valores de HR de cada muestra
- ✅ Calcula tiempo desde inicio para cada muestra
- ✅ Exporta array `hr_samples` con todas las muestras

**Nuevos datos exportados**:
```json
{
  "hr_samples": [
    {
      "timestamp": 1234567890,
      "time_seconds": 0,
      "time_formatted": "00:00",
      "hr": 120
    },
    {
      "timestamp": 1234567895,
      "time_seconds": 5,
      "time_formatted": "00:05",
      "hr": 125
    }
  ],
  "num_hr_samples": 168
}
```

### 2. `ejemplo_dashboard.html`

**Nuevas características**:
- ✅ Selector dropdown de sesiones
- ✅ Gráfico de evolución de HR (Chart.js)
- ✅ Panel de información de sesión seleccionada
- ✅ Manejo de casos sin muestras de HR

**Nuevo gráfico agregado**:
- Tipo: Línea (line chart)
- Datos: Muestras de HR vs tiempo
- Línea de referencia: HR promedio
- Colores: Rojo para HR, verde para promedio

## 📊 Cómo Usar

### Paso 1: Exportar Datos con Muestras de HR

```bash
python exportar_para_dashboard.py
```

Este comando ahora incluye las muestras de HR en el JSON exportado.

### Paso 2: Abrir Dashboard

```bash
python abrir_dashboard.py
```

O abre directamente `ejemplo_dashboard.html` en tu navegador.

### Paso 3: Seleccionar Sesión

1. Desplázate hasta la sección "Evolución de Frecuencia Cardíaca por Sesión"
2. Selecciona una sesión del dropdown
3. El gráfico se mostrará automáticamente con la evolución de HR

## 🎨 Características del Gráfico

### Visualización
- **Línea principal**: Evolución de HR durante la sesión
- **Línea de promedio**: HR promedio como referencia horizontal
- **Puntos interactivos**: Hover para ver valores exactos
- **Escala automática**: Se ajusta al rango de HR de la sesión

### Información Mostrada
- Tiempo transcurrido desde inicio (minutos)
- Frecuencia cardíaca en cada punto (bpm)
- HR promedio de la sesión

## ⚠️ Notas Importantes

1. **Sesiones sin muestras**: Si una sesión no tiene muestras de HR parseadas, aparecerá un mensaje indicando que no hay datos disponibles.

2. **Sesiones problemáticas**: Las sesiones que no se pueden parsear completamente pueden no tener muestras de HR. En ese caso, solo tendrán estadísticas básicas (promedio, máximo, mínimo).

3. **Rendimiento**: Si una sesión tiene muchas muestras (cientos), el gráfico puede tardar un momento en renderizarse.

## 🔄 Compatibilidad

- ✅ Compatible con sesiones anteriores (si no tienen muestras, simplemente no aparecen en el selector)
- ✅ Funciona con sesiones parseadas completamente
- ✅ Funciona con sesiones que solo tienen información básica (pero sin gráfico)

## 📝 Ejemplo de Uso

1. Exporta tus datos: `python exportar_para_dashboard.py`
2. Abre el dashboard: `python abrir_dashboard.py`
3. Selecciona una sesión del dropdown
4. Observa cómo cambió tu frecuencia cardíaca durante el entrenamiento
5. Usa el hover para ver valores exactos en puntos específicos

## 🎯 Beneficios

- ✅ Visualización clara de la evolución de HR
- ✅ Identificación de zonas de entrenamiento
- ✅ Análisis de intensidad del entrenamiento
- ✅ Comparación visual de diferentes sesiones

---

**Última actualización**: Febrero 2026
