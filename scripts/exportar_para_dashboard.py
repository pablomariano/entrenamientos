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
            'parseable': False,  # Marcamos que no se pudo parsear completamente
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
        
        # Intentar parsear muestras de HR (solo si tiene HR, sin necesidad de GPS)
        muestras_hr = []
        muestras_parseadas = False
        
        if sess.has_hr:
            try:
                # Intentar parsear muestras - funciona incluso sin GPS
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
            datos['hr_max'] = min(hr_max, HR_MAX_VALID) if hr_max is not None else None
            datos['hr_min'] = max(hr_min, HR_MIN_VALID) if hr_min is not None else None
            if datos['hr_max'] is not None and datos['hr_max'] > HR_MAX_VALID:
                datos['hr_max'] = HR_MAX_VALID
            if datos['hr_min'] is not None and datos['hr_min'] < HR_MIN_VALID:
                datos['hr_min'] = HR_MIN_VALID
            datos['sample_rate_seconds'] = sess.info.get('sample_rate', 5)
        else:
            datos['hr_avg'] = None
            datos['hr_max'] = None
            datos['hr_min'] = None
            datos['sample_rate_seconds'] = None
        
        # Incluir muestras de HR si se pudieron parsear
        if muestras_parseadas and len(muestras_hr) > 0:
            datos['hr_samples'] = muestras_hr
            datos['num_hr_samples'] = len(muestras_hr)
        else:
            datos['hr_samples'] = []
            datos['num_hr_samples'] = 0
        
        # Intentar extraer información de laps
        laps_info = []
        try:
            # Método 1: Extracción básica desde datos raw
            laps_basicos = extraer_laps_basicos(raw_session)
            if isinstance(laps_basicos, list) and len(laps_basicos) > 0:
                laps_info = laps_basicos
            
            # Método 2: Si el primer método no funcionó, intentar método alternativo
            if len(laps_info) == 0:
                laps_alternativos = extraer_laps_alternativos(sess)
                if isinstance(laps_alternativos, list) and len(laps_alternativos) > 0:
                    laps_info = laps_alternativos
            
        except Exception as e:
            # Si hay error en la extracción de laps, continuar sin ellos
            laps_info = [{
                'error': f'Error extrayendo laps: {str(e)}',
                'method': 'error_fallback'
            }]
        
        # Agregar información de laps a los datos
        datos['laps'] = laps_info
        datos['num_laps'] = len([lap for lap in laps_info if not lap.get('error')])
        datos['has_laps'] = datos['num_laps'] > 0
        
        return datos
        
    except Exception as e:
        # Si falla el parsing, intentar extraer info básica
        datos_basicos = extraer_info_basica(raw_session)
        datos_basicos['error_parsing'] = str(e)
        datos_basicos['error_type'] = type(e).__name__
        datos_basicos['hr_samples'] = []
        datos_basicos['num_hr_samples'] = 0
        
        # Intentar extraer laps incluso si falla el parsing principal
        try:
            laps_basicos = extraer_laps_basicos(raw_session)
            if isinstance(laps_basicos, list):
                datos_basicos['laps'] = laps_basicos
                datos_basicos['num_laps'] = len([lap for lap in laps_basicos if not lap.get('error')])
                datos_basicos['has_laps'] = datos_basicos['num_laps'] > 0
            else:
                datos_basicos['laps'] = []
                datos_basicos['num_laps'] = 0
                datos_basicos['has_laps'] = False
        except:
            datos_basicos['laps'] = []
            datos_basicos['num_laps'] = 0
            datos_basicos['has_laps'] = False
        
        return datos_basicos


def main():
    print("="*80)
    print("EXPORTADOR PARA DASHBOARD - Polar RCX5")
    print("="*80)
    print("\nEste script exporta todas las sesiones en formato JSON estructurado")
    print("para usar en tu dashboard, incluyendo información básica de sesiones")
    print("que no se pueden parsear completamente.\n")
    
    input("Presiona ENTER cuando hayas seleccionado 'Connect > Start synchronizing' en tu reloj...")
    
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
        sesiones_exitosas = 0
        sesiones_basicas = 0
        
        for i, raw_session in enumerate(raw_sessions, 1):
            print(f"  Procesando sesión {i}/{len(raw_sessions)}...", end=' ')
            
            datos = parsear_sesion_completa(raw_session)
            
            if datos.get('parseable'):
                sesiones_exitosas += 1
                print("✓ Parseada completamente")
            else:
                sesiones_basicas += 1
                print("⚠ Solo información básica")
            
            todas_las_sesiones.append(datos)
        
        # Guardar en archivo JSON
        print(f"\n[3/3] Guardando datos...")
        output_file = output_dir / 'entrenamientos.json'
        
        resultado = {
            'export_date': datetime.now().isoformat(),
            'total_sessions': len(todas_las_sesiones),
            'sessions_fully_parseable': sesiones_exitosas,
            'sessions_basic_info_only': sesiones_basicas,
            'sessions': todas_las_sesiones
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Datos guardados en: {output_file}")
        
        # Resumen
        print(f"\n{'='*80}")
        print("RESUMEN")
        print(f"{'='*80}")
        print(f"Total de sesiones: {len(todas_las_sesiones)}")
        print(f"✓ Sesiones completamente parseadas: {sesiones_exitosas}")
        print(f"⚠ Sesiones con solo información básica: {sesiones_basicas}")
        print(f"\nArchivo JSON creado: {output_file}")
        print(f"\nEste archivo contiene todos los datos estructurados que necesitas")
        print(f"para crear tu dashboard, incluyendo:")
        print(f"  - Fechas y duraciones")
        print(f"  - Estadísticas de frecuencia cardíaca (promedio, máximo, mínimo)")
        print(f"  - Información de laps (vueltas) cuando estén disponibles")
        print(f"\nNOTA: No se incluye información de GPS ni distancias")
        print(f"      porque tu reloj no tiene estas funcionalidades.")
        
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
