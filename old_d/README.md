# 🎨 Antiguo Dashboard Web

Dashboard interactivo para visualizar entrenamientos del Polar RCX5.

## 📄 Archivos

### `index.html`
Dashboard web completo con visualizaciones interactivas.

## 🚀 Cómo Usar

### Opción 1: Servidor Local (Recomendado)

Desde la raíz del proyecto:
```bash
python scripts/abrir_dashboard.py
```

Esto abrirá automáticamente el dashboard en tu navegador.

### Opción 2: Abrir Directamente

1. Asegúrate de haber exportado los datos primero:
   ```bash
   python scripts/exportar_para_dashboard.py
   ```

2. Abre `dashboard/index.html` en tu navegador

3. Si aparece error, usa el selector de archivo para cargar `entrenamientos_dashboard/entrenamientos.json`

## 📊 Características

### Estadísticas Generales
- Total de entrenamientos
- Tiempo total acumulado
- HR promedio, máximo y mínimo

### Gráficos
1. **Entrenamientos por Mes**: Gráfico de barras mostrando cuántos entrenamientos por mes
2. **Frecuencia Cardíaca Promedio**: Evolución del HR promedio en los últimos 20 entrenamientos
3. **Duración por Mes**: Tiempo total de entrenamiento por mes
4. **Evolución de HR por Sesión**: Selector para ver cómo cambió tu HR durante una sesión específica

### Lista de Entrenamientos
- Todas las sesiones ordenadas por fecha
- Información de duración y HR
- Indicador de disponibilidad de datos

## 🎨 Personalización

El dashboard usa:
- **Chart.js** para gráficos
- **CSS personalizado** para estilos
- **JavaScript vanilla** (sin frameworks)

Para personalizar:
1. Abre `index.html` en un editor
2. Modifica los estilos en la sección `<style>`
3. Ajusta los colores en las configuraciones de Chart.js
4. Agrega nuevas visualizaciones según necesites

## 🌐 Para Despliegue Web

Ver `../DEPLOY.md` para instrucciones de despliegue en producción.

Opciones recomendadas:
- **Frontend**: Vercel o Netlify (hosting estático)
- **Backend**: Railway o Render (API Python)
- **Base de datos**: PostgreSQL

## 📝 Estructura de Datos Esperada

El dashboard espera un archivo JSON con esta estructura:

```json
{
  "export_date": "2026-02-13T10:30:00",
  "total_sessions": 34,
  "sessions": [
    {
      "id": "2026-02-10T14:44:53Z",
      "start_time": "2026-02-10T11:44:53",
      "duration_seconds": 8172,
      "duration_formatted": "02:16:12",
      "has_hr": true,
      "hr_avg": 141,
      "hr_max": 192,
      "hr_min": 96,
      "hr_samples": [
        {
          "timestamp": 1234567890,
          "time_seconds": 0,
          "time_formatted": "00:00",
          "hr": 145
        }
      ]
    }
  ]
}
```

---

**Última actualización**: Febrero 2026
