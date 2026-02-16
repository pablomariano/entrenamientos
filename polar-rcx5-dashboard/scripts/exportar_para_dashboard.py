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

# Rango fisiológico válido de frecuencia cardíaca (bpm)
# Valores fuera de este rango son errores de parsing o datos corruptos
HR_MIN_VALID = 30
HR_MAX_VALID = 250


def _hr_valido(hr):
    """Devuelve True si el valor de HR está en rango fisiológico válido."""
    if hr is None:
        return False
    return HR_MIN_VALID <= hr <= HR_MAX_VALID


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
        
        return datos
        
    except Exception as e:
        # Si falla el parsing, intentar extraer info básica
        datos_basicos = extraer_info_basica(raw_session)
        datos_basicos['error_parsing'] = str(e)
        datos_basicos['error_type'] = type(e).__name__
        datos_basicos['hr_samples'] = []
        datos_basicos['num_hr_samples'] = 0
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
        print(f"\nNOTA: No se incluye información de GPS ni distancias")
        print(f"      porque tu reloj no tiene estas funcionalidades.")
        
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
