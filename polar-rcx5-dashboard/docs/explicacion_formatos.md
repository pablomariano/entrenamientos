# Formatos de Exportación - Polar RCX5

## 1. Formato RAW (JSON) - `--format raw`
**Contenido:** Arrays de bytes crudos tal como vienen del reloj
**Ejemplo:**
```json
[[4, 66, 192, 1, 64, 179, 0, 0, ...], [4, 66, 192, 1, ...], ...]
```
**Ventajas:**
- ✅ Contiene TODOS los datos (incluso sesiones problemáticas)
- ✅ No pierde información

**Desventajas:**
- ❌ Son bytes crudos, NO están parseados
- ❌ Necesitas parsearlos manualmente para obtener valores legibles
- ❌ Requiere entender el formato binario del reloj

## 2. Formato TCX (XML) - `--format tcx`
**Contenido:** Datos completamente parseados y estructurados
**Ejemplo:**
```xml
<TrainingCenterDatabase>
  <Activities>
    <Activity Sport="Other">
      <Id>2026-02-10T14:44:53Z</Id>
      <Lap StartTime="2026-02-10T14:44:53Z">
        <TotalTimeSeconds>8172</TotalTimeSeconds>
        <DistanceMeters>12345.67</DistanceMeters>
        <Track>
          <Trackpoint>
            <Time>2026-02-10T14:44:53Z</Time>
            <Position>
              <LatitudeDegrees>39.9149567</LatitudeDegrees>
              <LongitudeDegrees>148.3754800</LongitudeDegrees>
            </Position>
            <HeartRateBpm><Value>150</Value></HeartRateBpm>
            <DistanceMeters>0.0</DistanceMeters>
          </Trackpoint>
          ...
        </Track>
      </Lap>
    </Activity>
  </Activities>
</TrainingCenterDatabase>
```
**Ventajas:**
- ✅ Datos completamente parseados y legibles
- ✅ Formato estándar (TCX es usado por Garmin, Strava, etc.)
- ✅ Fácil de procesar para dashboards
- ✅ Incluye: fechas, HR, GPS, velocidad, distancia, etc.

**Desventajas:**
- ❌ Solo funciona para sesiones que se pueden parsear correctamente
- ❌ Las 25 sesiones problemáticas NO se exportan

## 3. Formato BIN - `--format bin`
**Contenido:** Representación binaria de los datos
**Ventajas:** Similar a raw pero en formato binario
**Desventajas:** Aún menos útil para dashboards

---

## ¿Qué necesitas para tu Dashboard?

Para crear un dashboard necesitas datos **estructurados y parseados**:
- ✅ Fecha/hora de cada entrenamiento
- ✅ Duración
- ✅ Distancia total
- ✅ Frecuencia cardíaca (promedio, máxima, mínima)
- ✅ Coordenadas GPS (para mapas)
- ✅ Velocidad
- ✅ Muestras individuales (cada X segundos)

**Conclusión:** Necesitas el formato **TCX** (o parsear manualmente el RAW), pero el problema es que 25 sesiones no se pueden parsear.

## Solución Recomendada

1. **Exportar las sesiones exitosas en TCX** (9 sesiones)
2. **Exportar TODAS las sesiones en RAW** (34 sesiones) como respaldo
3. **Crear un parser personalizado** que extraiga al menos la información básica (fecha, duración, HR promedio) de las sesiones RAW problemáticas, aunque no pueda parsear todas las muestras GPS
