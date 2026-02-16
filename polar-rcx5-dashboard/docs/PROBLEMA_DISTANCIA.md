# 🔍 Análisis del Problema: Cálculo de Distancia en Sesiones GPS

## 📋 Resumen del Problema

Se detectó que el cálculo de distancia en sesiones con GPS puede ser **incorrecto o no confiable** cuando:
1. El GPS no estaba funcionando correctamente durante el entrenamiento
2. Las coordenadas GPS están fijas (mismo punto) indicando falta de señal
3. El entrenamiento fue en interiores sin señal GPS válida

## 🔬 Cómo Funciona Actualmente

### Proceso Actual del Parser

1. **Detección de GPS**: El parser lee el byte 166 del primer paquete para determinar si `has_gps = True`
2. **Si tiene GPS**: 
   - Parsea coordenadas GPS (latitud/longitud) de cada muestra
   - Calcula distancia entre muestras consecutivas usando fórmula de Haversine
   - Suma todas las distancias para obtener distancia total
3. **Si NO tiene GPS**: No calcula distancia (correcto)

### Problema Identificado

El código **NO valida** si las coordenadas GPS son realmente válidas antes de calcular distancia:

```python
# Código actual (línea 141-142 de parser.py)
prev = self._prev_sample()
distance = self._calculate_distance((prev.lat, prev.lon), (lat, lon))
self.distance += distance
```

**Problemas potenciales**:
- ✅ Si `has_gps = True` pero el GPS no tenía señal → coordenadas pueden ser inválidas o fijas
- ✅ Si todas las coordenadas son iguales → distancia = 0, pero el código no lo detecta explícitamente
- ✅ Si hay ruido GPS mínimo → puede calcular distancias pequeñas incorrectas
- ✅ No hay validación de que las coordenadas estén en rangos válidos (-90 a 90 para lat, -180 a 180 para lon)

## 🎯 Caso Específico: Sesión del 10/2/2026

### Pregunta del Usuario
> "De dónde saca la información de la distancia recorrida? Me parece que las nuevas sesiones de entrenamiento no tienen información de distancias o no deberían tenerla porque no tengo un dispositivo que mida las distancias"

### Respuesta

**La distancia NO viene de un sensor de distancia**, sino que se **calcula usando coordenadas GPS**:

1. El reloj Polar RCX5 tiene GPS integrado (o puede usar GPS externo)
2. Durante el entrenamiento, guarda coordenadas GPS cada X segundos (sample rate)
3. El parser calcula la distancia en línea recta entre coordenadas consecutivas
4. Suma todas esas distancias para obtener la distancia total

### Verificación Necesaria

Para la sesión del 10/2/2026, necesitamos verificar:

1. **¿Realmente tiene GPS activado?**
   - Verificar `has_gps = True/False` en los datos

2. **¿Las coordenadas GPS son válidas?**
   - ¿Están en rangos válidos?
   - ¿Varían entre muestras o están fijas?

3. **¿La distancia calculada es coherente?**
   - Comparar distancia total vs distancia en línea recta primera-última muestra
   - Verificar si las coordenadas están todas en el mismo punto

## 🛠️ Solución Propuesta

### Script de Análisis

Se creó `analizar_sesion.py` que:
- ✅ Analiza una sesión específica
- ✅ Verifica si tiene GPS
- ✅ Valida que las coordenadas sean válidas
- ✅ Detecta si las coordenadas están fijas
- ✅ Muestra información detallada sobre el cálculo de distancia

### Mejoras al Parser (Futuro)

Se propone mejorar el parser para:

1. **Validar coordenadas antes de calcular distancia**:
   ```python
   # Validar rangos
   if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
       distance = 0  # Coordenadas inválidas
   
   # Validar cambio significativo
   if abs(lat - prev_lat) < 0.0001 and abs(lon - prev_lon) < 0.0001:
       distance = 0  # Coordenadas fijas (GPS no funcionaba)
   ```

2. **Marcar distancia como "no confiable"** cuando:
   - Todas las coordenadas están en el mismo punto
   - Las coordenadas no varían significativamente
   - Hay errores en el parsing de coordenadas

3. **Incluir metadatos de confiabilidad** en los datos exportados:
   ```json
   {
     "distance_meters": 1234.56,
     "distance_reliable": false,
     "gps_quality": "poor",
     "coordinates_fixed": true
   }
   ```

## 📊 Cómo Verificar tu Sesión

### Paso 1: Ejecutar Script de Análisis

```bash
python analizar_sesion.py
```

Este script:
- Sincroniza con tu reloj
- Busca la sesión del 10/2/2026
- Analiza las coordenadas GPS
- Muestra si la distancia es confiable

### Paso 2: Interpretar Resultados

**Si ves**:
- ✅ "Las coordenadas GPS varían" → La distancia es probablemente confiable
- ⚠️ "Las coordenadas GPS están fijas" → La distancia NO es confiable (debería ser 0)
- ⚠️ "Coordenadas fuera de rango" → Error en los datos

### Paso 3: Verificar Manualmente

Si quieres verificar manualmente los datos exportados:

```bash
python exportar_para_dashboard.py
```

Luego revisa `entrenamientos_dashboard/entrenamientos.json` y busca la sesión del 10/2/2026:
- Verifica `has_gps`: ¿es `true` o `false`?
- Si `has_gps = false` pero hay distancia → ERROR
- Si `has_gps = true`, revisa las coordenadas en `first_sample` y `last_sample`

## 🎓 Explicación Técnica

### ¿Por qué el reloj marca `has_gps = True` si no hay GPS?

El reloj marca `has_gps = True` cuando:
- El GPS está **activado** en la configuración del reloj
- El reloj **intentó** obtener señal GPS durante el entrenamiento

Pero esto NO garantiza que:
- El GPS tuvo señal válida
- Las coordenadas son correctas
- El GPS funcionó durante todo el entrenamiento

### ¿Cómo se calcula la distancia?

1. **Fórmula de Haversine**: Calcula distancia en línea recta entre dos puntos GPS
2. **Suma acumulativa**: Suma todas las distancias entre muestras consecutivas
3. **Limitaciones**:
   - Es distancia en línea recta, no la ruta real recorrida
   - Si el GPS tiene errores, la distancia será incorrecta
   - Si las coordenadas están fijas, distancia = 0

## ✅ Recomendaciones

1. **Para sesiones futuras**:
   - Si entrenas en interiores → Desactiva GPS en el reloj
   - Si entrenas al aire libre → Asegúrate de tener señal GPS antes de empezar
   - Verifica que las coordenadas varíen durante el entrenamiento

2. **Para datos históricos**:
   - Usa el script `analizar_sesion.py` para verificar cada sesión
   - Si la distancia no es confiable, marca como "no disponible" en tu dashboard
   - Considera usar solo sesiones con GPS válido para estadísticas de distancia

3. **Para el dashboard**:
   - Mostrar advertencia cuando `distance_reliable = false`
   - Permitir filtrar sesiones por calidad de GPS
   - Mostrar "Distancia no disponible" en lugar de 0 cuando no es confiable

## 📝 Conclusión

**La distancia se calcula desde coordenadas GPS, NO desde un sensor de distancia.**

Si tu sesión del 10/2/2026 muestra distancia pero no debería tenerla:
1. Verifica si realmente tiene GPS activado (`has_gps`)
2. Verifica si las coordenadas son válidas y varían
3. Si las coordenadas están fijas → La distancia NO es confiable

**Ejecuta `analizar_sesion.py` para obtener un análisis detallado de tu sesión específica.**

---

**Última actualización**: Febrero 2026
