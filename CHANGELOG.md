# 📝 Changelog

Historial de cambios del proyecto.

## [1.0.0] - 2026-02-13

### ✨ Características Iniciales

#### Exportación de Datos
- Exportación de sesiones en formato JSON estructurado
- Extracción de duración y frecuencia cardíaca
- Inclusión de muestras detalladas de HR
- Soporte para sesiones con y sin GPS
- Manejo robusto de sesiones problemáticas

#### Dashboard Web
- Dashboard interactivo con Chart.js
- Estadísticas generales (total sesiones, tiempo, HR)
- Gráfico de entrenamientos por mes
- Gráfico de HR promedio (últimos 20 entrenamientos)
- Gráfico de duración por mes
- **Gráfico de evolución de HR por sesión** (selector + visualización detallada)
- Lista completa de entrenamientos ordenada por fecha
- Servidor local integrado

#### Scripts de Diagnóstico
- Diagnóstico general de sesiones
- Diagnóstico específico de HR
- Búsqueda automática de offset correcto
- Verificación de correcciones aplicadas
- Análisis de sesiones desde JSON

### 🐛 Bugs Corregidos

#### Fix 1: USBTimeoutError en Windows
- **Problema**: Código de error de timeout incorrecto (110 en lugar de 10060)
- **Solución**: Cambio en `datalink.py` para usar código correcto en Windows
- **Archivo**: `polar_rcx5_datalink/datalink.py` línea ~35

#### Fix 2: StopIteration en Python 3.7+
- **Problema**: `pop_zeroes()` lanzaba StopIteration cuando todos los elementos eran cero
- **Solución**: Uso de valor por defecto en `next()` para manejar caso edge
- **Archivo**: `polar_rcx5_datalink/utils.py` línea ~48-51

#### Fix 3: HR Incorrecto en Relojes sin GPS
- **Problema**: Parser intentaba leer GPS inexistente, desincronizando la lectura de HR
- **Solución**: Forzar `has_gps = False` para relojes sin GPS funcional
- **Archivo**: `polar_rcx5_datalink/parser.py` línea ~48-52
- **Resultado**: HR promedio ahora coincide con el header (diferencia <5 bpm)

#### Fix 4: Valores de HR Imposibles (>500 bpm)
- **Problema**: Parser generaba valores fisiológicamente imposibles
- **Causa**: Lectura de GPS inexistente causaba desincronización
- **Solución**: Fix 3 + validación de rango 30-250 bpm
- **Resultado**: 96-99% de datos ahora en rango válido

#### Fix 5: Eje X Agrupado en Gráfico de Evolución
- **Problema**: Datos se mostraban agrupados al inicio del gráfico
- **Solución**: Configurar eje X como escala lineal (`type: 'linear'`)
- **Archivo**: `dashboard/index.html`

### 📊 Estadísticas

- **Líneas de código**: ~3,500+
- **Archivos**: 24
- **Scripts Python**: 8
- **Documentación**: 15 archivos markdown
- **Sesiones testeadas**: 34
- **Tasa de éxito de parsing**: 100% (con patches aplicados)

### 🎯 Cobertura de Funcionalidades

- ✅ Exportación de todas las sesiones (34/34)
- ✅ Extracción de información básica incluso de sesiones problemáticas
- ✅ Valores de HR correctos (diferencia <5 bpm con header)
- ✅ Filtrado de valores anómalos (0 bpm, >250 bpm)
- ✅ Dashboard completamente funcional
- ✅ Gráfico de evolución por sesión

---

## [Unreleased] - Próximas Versiones

Ver **ROADMAP.md** para plan detallado.

### Planificado para v1.1.0
- [ ] Dashboard web en línea (hosting)
- [ ] Backend API con FastAPI
- [ ] Base de datos PostgreSQL
- [ ] Autenticación de usuarios

### Planificado para v1.2.0
- [ ] Sincronización automática programada
- [ ] Exportación a Strava
- [ ] Análisis avanzado de zonas de HR
- [ ] Comparación de entrenamientos

### Planificado para v2.0.0
- [ ] Soporte para otros modelos Polar
- [ ] Aplicación móvil
- [ ] Funcionalidades sociales

---

## 📌 Tipos de Cambios

- ✨ `Feature` - Nueva funcionalidad
- 🐛 `Fix` - Corrección de bug
- 📝 `Docs` - Cambios en documentación
- 🎨 `Style` - Formato, estilos
- ♻️ `Refactor` - Refactorización de código
- ⚡ `Perf` - Mejoras de rendimiento
- 🧪 `Test` - Tests

---

**Última actualización**: Febrero 2026
