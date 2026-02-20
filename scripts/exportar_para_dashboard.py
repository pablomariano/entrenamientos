"""
Script para exportar sesiones de entrenamiento en formato JSON estructurado
para usar en un dashboard. Solo incluye duración y frecuencia cardíaca.
NO incluye GPS ni distancias (el reloj no tiene estas funcionalidades).
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Agregar el path de la librería instalada
sys.path.insert(0, r'C:\Users\Pablo\AppData\Local\Programs\Python\Python314\Lib\site-packages')

from polar_rcx5_datalink.datalink import DataLink
from polar_rcx5_datalink.parser import TrainingSession
from polar_rcx5_datalink.exceptions import ParserError, SyncError
from polar_rcx5_datalink.utils import bcd_to_int
import polar_rcx5_datalink.utils as utils
import pytz
import tzlocal

# tzlocal >= 3.0 retorna ZoneInfo en lugar de un timezone de pytz,
# pero la librería llama .localize() que solo existe en pytz.
# Reemplazamos datetime_to_utc por una versión compatible.
def _datetime_to_utc_fixed(dt, timezone=None):
    if timezone is None:
        tz = pytz.timezone(str(tzlocal.get_localzone()))
    else:
        tz = pytz.timezone(timezone)
    return tz.localize(dt, is_dst=None).astimezone(pytz.utc)

utils.datetime_to_utc = _datetime_to_utc_fixed

# geopy lanza ValueError cuando lat/lon están fuera de rango (-90..90 / -180..180).
# En sesiones donde el GPS falló o los datos están corruptos esto mata el parsing
# completo, perdiendo todos los samples de HR. Parcheamos para ignorar el error.
def _safe_calculate_distance(self, coord1, coord2):
    try:
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        if (lat1 is None or lon1 is None or lat2 is None or lon2 is None
                or abs(lat1) > 90 or abs(lon1) > 180
                or abs(lat2) > 90 or abs(lon2) > 180):
            return 0.0
        import geopy.distance
        return geopy.distance.distance(coord1, coord2).meters
    except Exception:
        return 0.0

TrainingSession._calculate_distance = _safe_calculate_distance

# Rango fisiológico válido de frecuencia cardíaca (bpm)
# Valores fuera de este rango son errores de parsing o datos corruptos
HR_MIN_VALID = 30
HR_MAX_VALID = 250


def _hr_valido(hr):
    """Devuelve True si el valor de HR está en rango fisiológico válido."""
    if hr is None:
        return False
    return HR_MIN_VALID <= hr <= HR_MAX_VALID


def extraer_laps_basicos(raw_session):
    """
    Extrae información básica de laps desde los datos raw.
    Intenta detectar patrones de lap data en los bits de la sesión.
    """
    try:
        # Crear una sesión temporal para acceder a los métodos de parsing
        sess_temp = TrainingSession(raw_session)
        
        # Obtener los bits de las muestras
        samples_bits = sess_temp.tobin()[349 * 8:] if sess_temp.has_gps else sess_temp.tobin()[351 * 8:]
        
        # Buscar patrones de lap data (416 bits cada uno)
        LAP_DATA_BITS_LENGTH = 416
        laps_detectados = []
        
        # Buscar patrones que podrían indicar laps
        # Basado en el algoritmo del parser original pero simplificado
        cursor = 0
        lap_count = 0
        
        while cursor < len(samples_bits) - LAP_DATA_BITS_LENGTH:
            # Buscar patrón que podría indicar inicio de lap
            # El parser original busca patrones de longitud/latitud
            chunk = samples_bits[cursor:cursor + LAP_DATA_BITS_LENGTH]
            
            # Heurística simple: buscar secuencias que podrían ser lap data
            # Los laps suelen tener patrones repetitivos y estructurados
            if len(chunk) == LAP_DATA_BITS_LENGTH:
                # Convertir chunk a bytes para análisis
                if len(chunk) % 8 == 0:
                    try:
                        bytes_chunk = []
                        for i in range(0, len(chunk), 8):
                            byte_str = chunk[i:i+8]
                            if len(byte_str) == 8:
                                bytes_chunk.append(int(byte_str, 2))
                        
                        # Heurística: si hay suficiente variación en los datos,
                        # podría ser un lap (no solo padding o datos vacíos)
                        if len(bytes_chunk) >= 10:
                            variacion = max(bytes_chunk[:10]) - min(bytes_chunk[:10])
                            if variacion > 10:  # Umbral arbitrario
                                lap_count += 1
                                
                                # Intentar extraer información básica
                                # Esto es experimental y puede no ser 100% preciso
                                lap_info = {
                                    'lap_number': lap_count,
                                    'bit_position': cursor,
                                    'data_length': LAP_DATA_BITS_LENGTH,
                                    'detected_pattern': True,
                                    # Información estimada (puede no ser precisa)
                                    'raw_data_summary': {
                                        'first_bytes': bytes_chunk[:5],
                                        'data_variation': variacion,
                                        'non_zero_bytes': sum(1 for b in bytes_chunk if b != 0)
                                    }
                                }
                                laps_detectados.append(lap_info)
                                
                                # Saltar los datos del lap
                                cursor += LAP_DATA_BITS_LENGTH
                                continue
                    except:
                        pass
            
            cursor += 100  # Avanzar en chunks más pequeños
        
        return laps_detectados
        
    except Exception as e:
        return {
            'error': f'Error extrayendo laps: {str(e)}',
            'laps': []
        }


def extraer_laps_alternativos(sess):
    """
    Método alternativo para detectar laps usando el parser existente.
    Intenta parsear samples y detectar cuando se encuentran laps.
    """
    laps_info = []
    
    if not sess.has_hr:
        return laps_info
    
    try:
        # Crear una versión modificada del parser para detectar laps
        original_cursor = 0
        lap_count = 0
        
        # Simular el proceso de parsing para detectar laps
        sess_copy = TrainingSession(sess.raw)
        samples_bits = sess_copy._get_samples_bits()
        
        # Usar el método _has_lap_data del parser original
        cursor = 0
        sample_count = 0
        
        # Parsear samples hasta encontrar laps
        while cursor < len(samples_bits) - 500:  # Margen de seguridad
            try:
                # Simular posición del cursor
                sess_copy._cursor = cursor
                
                # Verificar si hay lap data en esta posición
                if hasattr(sess_copy, '_has_lap_data'):
                    if sess_copy._has_lap_data():
                        lap_count += 1
                        
                        # Calcular tiempo aproximado del lap
                        sample_rate = sess.info.get('sample_rate', 5)
                        tiempo_aproximado = sample_count * sample_rate
                        
                        lap_info = {
                            'lap_number': lap_count,
                            'approximate_time_seconds': tiempo_aproximado,
                            'approximate_time_formatted': f"{tiempo_aproximado // 60:02d}:{tiempo_aproximado % 60:02d}",
                            'sample_position': sample_count,
                            'detected_by_parser': True
                        }
                        laps_info.append(lap_info)
                        
                        # Saltar los datos del lap
                        cursor += 416  # LAP_DATA_BITS_LENGTH
                
                # Avanzar al siguiente sample
                cursor += 50  # Estimación del tamaño promedio de un sample
                sample_count += 1
                
            except:
                cursor += 10
                
        return laps_info
        
    except Exception as e:
        return [{
            'error': f'Error en detección alternativa: {str(e)}',
            'method': 'alternative'
        }]


def extraer_info_basica(raw_session):
    """Extrae información básica de una sesión sin parsear las muestras."""
    try:
        first_packet = raw_session[0]
        
        # Extraer información básica del header (similar a _parse_info)
        year = first_packet[44] + 1920
        month = first_packet[43]
        day = first_packet[42]
        hour = bcd_to_int(first_packet[41])
        minute = bcd_to_int(first_packet[40])
        second = bcd_to_int(first_packet[39])
        
        duration_hours = bcd_to_int(first_packet[38])
        duration_minutes = bcd_to_int(first_packet[37])
        duration_seconds = bcd_to_int(first_packet[36])
        
        has_hr = bool(first_packet[165])
        has_gps = bool(first_packet[166])
        
        # HR stats (si están disponibles)
        hr_avg = first_packet[201] if has_hr else None
        hr_max = first_packet[205] if has_hr else None
        hr_min = first_packet[203] if has_hr else None
        
        start_time = datetime(year, month, day, hour, minute, second)
        duration_total = duration_hours * 3600 + duration_minutes * 60 + duration_seconds
        
        return {
            'start_time': start_time.isoformat(),
            'duration_seconds': duration_total,
            'duration_formatted': f"{duration_hours:02d}:{duration_minutes:02d}:{duration_seconds:02d}",
            'has_hr': has_hr,
            'hr_avg': hr_avg,
            'hr_max': hr_max,
            'hr_min': hr_min,
        }
    except Exception as e:
        return {
            'error': str(e),
            'parseable': False
        }


def parsear_sesion_completa(raw_session):
    """Extrae solo información de duración y frecuencia cardíaca, incluyendo muestras de HR."""
    try:
        sess = TrainingSession(raw_session)

        # El byte 166 del protocolo queda en True aunque el reloj no tenga GPS.
        # El parser GPS intenta leer coordenadas/velocidad/satélites donde solo
        # hay datos de HR, produciendo crashes o samples truncados. Forzamos
        # modo no-GPS y recalculamos el inicio del stream de bits (351 vs 349).
        if sess.has_gps:
            sess.has_gps = False
            sess._samples_bits = sess._get_samples_bits()

        # Intentar parsear muestras de HR (solo si tiene HR, sin necesidad de GPS)
        muestras_hr = []
        muestras_parseadas = False
        
        if sess.has_hr:
            try:
                sess.parse_samples()
                muestras_parseadas = True
                
                # Extraer muestras de HR con sus timestamps
                sample_rate = sess.info.get('sample_rate', 5)  # Default 5 segundos
                start_time = sess.start_time
                
                for i, sample in enumerate(sess.samples):
                    if sample.hr is not None and _hr_valido(sample.hr):
                        # Calcular timestamp de esta muestra
                        seconds_from_start = i * sample_rate
                        timestamp = start_time.timestamp() + seconds_from_start
                        
                        muestras_hr.append({
                            'timestamp': timestamp,
                            'time_seconds': seconds_from_start,
                            'time_formatted': f"{seconds_from_start // 60:02d}:{seconds_from_start % 60:02d}",
                            'hr': sample.hr
                        })
            except Exception as e:
                # Si falla el parsing de muestras, continuar con solo estadísticas
                muestras_parseadas = False
                pass
        
        # Construir datos estructurados - SOLO HR y duración
        datos = {
            'id': sess.id,
            'start_time': sess.start_time.isoformat(),
            'start_utctime': sess.start_utctime.isoformat() if sess.start_utctime else None,
            'duration_seconds': sess.duration,
            'duration_formatted': f"{sess.duration // 3600:02d}:{(sess.duration % 3600) // 60:02d}:{sess.duration % 60:02d}",
            'has_hr': sess.has_hr,
        }
        
        # Información de HR (estadísticas) - solo valores en rango válido 30-250 bpm
        if sess.has_hr:
            hr_avg = sess.info.get('hr_avg')
            hr_max = sess.info.get('hr_max')
            hr_min = sess.info.get('hr_min')
            datos['hr_avg'] = hr_avg if _hr_valido(hr_avg) else None
            datos['hr_max'] = hr_max if _hr_valido(hr_max) else None
            datos['hr_min'] = hr_min if _hr_valido(hr_min) else None
            datos['sample_rate_seconds'] = sess.info.get('sample_rate', 5)
        else:
            datos['hr_avg'] = None
            datos['hr_max'] = None
            datos['hr_min'] = None
            datos['sample_rate_seconds'] = None
        
        # Incluir muestras de HR para gráficos de evolución
        if muestras_parseadas and muestras_hr:
            datos['hr_samples'] = muestras_hr
            datos['num_hr_samples'] = len(muestras_hr)
        else:
            datos['hr_samples'] = []
            datos['num_hr_samples'] = 0

        # Intentar extraer información de laps
        laps_info = []
        try:
            # Método directo: usar sess.laps si la librería lo expone
            if hasattr(sess, 'laps') and sess.laps:
                for i, lap in enumerate(sess.laps, 1):
                    lap_data = {'lap_number': i}
                    if hasattr(lap, 'duration'):
                        lap_data['duration_seconds'] = lap.duration
                        lap_data['duration_formatted'] = f"{lap.duration // 60:02d}:{lap.duration % 60:02d}"
                    if hasattr(lap, 'hr_avg') and _hr_valido(lap.hr_avg):
                        lap_data['hr_avg'] = lap.hr_avg
                    if hasattr(lap, 'hr_max') and _hr_valido(lap.hr_max):
                        lap_data['hr_max'] = lap.hr_max
                    if hasattr(lap, 'hr_min') and _hr_valido(lap.hr_min):
                        lap_data['hr_min'] = lap.hr_min
                    laps_info.append(lap_data)

            # Fallback: métodos alternativos si lo anterior no produjo laps
            if not laps_info:
                laps_basicos = extraer_laps_basicos(raw_session)
                if isinstance(laps_basicos, list) and laps_basicos:
                    laps_info = laps_basicos

            if not laps_info:
                laps_alternativos = extraer_laps_alternativos(sess)
                if isinstance(laps_alternativos, list) and laps_alternativos:
                    laps_info = laps_alternativos

        except Exception:
            laps_info = []
        
        # Agregar información de laps a los datos
        datos['laps'] = laps_info
        datos['num_laps'] = len([lap for lap in laps_info if not lap.get('error')])
        datos['has_laps'] = datos['num_laps'] > 0
        
        return datos
        
    except Exception:
        # Si falla el parsing, devolver solo la información básica del header
        datos_basicos = extraer_info_basica(raw_session)
        datos_basicos['laps'] = []
        datos_basicos['num_laps'] = 0
        datos_basicos['has_laps'] = False
        return datos_basicos


def pedir_filtro_meses():
    """Pregunta al usuario cuántos meses hacia atrás exportar. Retorna None para todo."""
    print("\nFiltro de fecha:")
    print("  0  = Exportar TODAS las sesiones")
    print("  N  = Exportar solo los últimos N meses (ej: 2, 6, 12)")
    while True:
        respuesta = input("¿Cuántos meses? [0 para todas]: ").strip()
        if respuesta == '' or respuesta == '0':
            return None
        try:
            meses = int(respuesta)
            if meses > 0:
                return meses
            print("  Ingresá un número mayor a 0, o 0 para todas.")
        except ValueError:
            print("  Valor inválido. Ingresá un número entero.")


def fecha_limite(meses):
    """Retorna el primer día del mes que resulta de restar N meses a hoy."""
    hoy = datetime.now()
    total_meses = hoy.year * 12 + (hoy.month - 1) - meses
    anio_destino = total_meses // 12
    mes_destino = total_meses % 12 + 1
    return hoy.replace(year=anio_destino, month=mes_destino, day=1,
                       hour=0, minute=0, second=0, microsecond=0)


def sesion_dentro_del_filtro(datos, limite):
    """Retorna True si la sesión está dentro del período a exportar."""
    if limite is None:
        return True
    start_str = datos.get('start_time')
    if not start_str:
        return True
    try:
        start = datetime.fromisoformat(start_str)
        return start >= limite
    except ValueError:
        return True


def main():
    print("="*80)
    print("EXPORTADOR PARA DASHBOARD - Polar RCX5")
    print("="*80)
    print("\nEste script exporta sesiones de entrenamiento en formato JSON estructurado.\n")

    filtro_meses = pedir_filtro_meses()
    limite_fecha = fecha_limite(filtro_meses) if filtro_meses else None

    if limite_fecha:
        print(f"\n  → Exportando sesiones desde {limite_fecha.strftime('%d/%m/%Y')} en adelante")
    else:
        print("\n  → Exportando TODAS las sesiones")

    input("\nPresiona ENTER cuando hayas seleccionado 'Connect > Start synchronizing' en tu reloj...")
    
    output_dir = Path(r'C:\Users\Pablo\Desktop\entrenamientos_dashboard')
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Sincronizar con el reloj
        print("\n[1/3] Sincronizando con el reloj...")
        with DataLink() as dl:
            dl.synchronize()
            raw_sessions = dl.sessions
        
        print(f"✓ Sincronización completada: {len(raw_sessions)} sesiones encontradas")
        
        # Procesar cada sesión
        print(f"\n[2/3] Procesando sesiones...")
        todas_las_sesiones = []
        sesiones_omitidas = 0
        
        for i, raw_session in enumerate(raw_sessions, 1):
            print(f"  Procesando sesión {i}/{len(raw_sessions)}...", end=' ')
            
            datos = parsear_sesion_completa(raw_session)

            if not sesion_dentro_del_filtro(datos, limite_fecha):
                sesiones_omitidas += 1
                fecha = datos.get('start_time', '?')[:10]
                print(f"omitida (fuera del período: {fecha})")
                continue

            todas_las_sesiones.append(datos)
            print("✓")
        
        # Guardar en archivo JSON
        print(f"\n[3/3] Guardando datos...")
        output_file = output_dir / 'entrenamientos.json'

        resultado = {
            'export_date': datetime.now().isoformat(),
            'filter_months': filtro_meses,
            'filter_from': limite_fecha.isoformat() if limite_fecha else None,
            'total_sessions': len(todas_las_sesiones),
            'sessions': todas_las_sesiones
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Datos guardados en: {output_file}")
        
        # Resumen
        print(f"\n{'='*80}")
        print("RESUMEN")
        print(f"{'='*80}")
        if filtro_meses:
            print(f"Período:           últimos {filtro_meses} mes(es) (desde {limite_fecha.strftime('%d/%m/%Y')})")
        else:
            print(f"Período:           todas las sesiones")
        print(f"Sesiones incluidas:{len(todas_las_sesiones)}")
        if sesiones_omitidas:
            print(f"Sesiones omitidas: {sesiones_omitidas} (fuera del período)")
        print(f"\nArchivo JSON: {output_file}")
        
        # Mostrar estadísticas de laps
        sesiones_con_laps = sum(1 for s in todas_las_sesiones if s.get('has_laps', False))
        total_laps = sum(s.get('num_laps', 0) for s in todas_las_sesiones)
        
        if sesiones_con_laps > 0:
            print(f"\n📊 INFORMACIÓN DE LAPS:")
            print(f"  - Sesiones con laps detectados: {sesiones_con_laps}")
            print(f"  - Total de laps encontrados: {total_laps}")
            print(f"  - Promedio de laps por sesión: {total_laps/sesiones_con_laps:.1f}")
        else:
            print(f"\n⚠️ No se detectaron laps en las sesiones procesadas.")
            print(f"   Esto puede deberse a:")
            print(f"   - Las sesiones no tienen laps configurados")
            print(f"   - Los datos de laps están en un formato no reconocido")
            print(f"   - Limitaciones en el algoritmo de detección")
        
    except SyncError as e:
        print(f"\n✗ Error de sincronización: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
