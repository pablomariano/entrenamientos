# 🔧 Patches para polar-rcx5-datalink

Esta carpeta contiene las instrucciones para aplicar correcciones necesarias a la librería `polar-rcx5-datalink` instalada.

## ⚠️ Importante

Estos cambios deben aplicarse **manualmente** a los archivos instalados por pip en tu sistema.

La ubicación típica en Windows es:
```
C:\Users\TU_USUARIO\AppData\Local\Programs\Python\PythonXXX\Lib\site-packages\polar_rcx5_datalink\
```

## 📝 Correcciones Necesarias

### 1. Fix de Timeout en Windows (`datalink.py`)

**Problema**: El código solo maneja el código de error de timeout de Linux (110), causando fallos en Windows (10060).

**Archivo**: `polar_rcx5_datalink/datalink.py`

**Ubicación**: Línea ~35

**Cambio**:
```python
# ANTES
_ERROR_TIMEOUT_CODE = 110

# DESPUÉS
_ERROR_TIMEOUT_CODE = 10060  # Código correcto para Windows
```

---

### 2. Fix de StopIteration (`utils.py`)

**Problema**: La función `pop_zeroes()` lanza `StopIteration` cuando todos los elementos son cero, causando `RuntimeError` en Python 3.7+.

**Archivo**: `polar_rcx5_datalink/utils.py`

**Ubicación**: Línea ~48-51

**Cambio**:
```python
# ANTES
def pop_zeroes(items):
    """Removes trailing zeros from a list"""
    index = next(i for i, v in enumerate(reversed(items)) if v != 0)
    return items[:-index]

# DESPUÉS
def pop_zeroes(items):
    """Removes trailing zeros from a list"""
    # If all items are zero, return empty list
    # Use default value len(items) so that items[:-len(items)] returns []
    index = next((i for i, v in enumerate(reversed(items)) if v != 0), len(items))
    return items[:-index]
```

---

### 3. Fix de GPS para Relojes sin GPS (`parser.py`)

**Problema**: El parser detecta `has_gps = True` aunque el reloj no tenga GPS funcional, causando lectura incorrecta de HR.

**Archivo**: `polar_rcx5_datalink/parser.py`

**Ubicación**: Línea ~48-52

**Cambio**:
```python
# ANTES
def __init__(self, raw_session):
    self.raw = raw_session
    self.info = self._parse_info()
    self.has_hr = self.info['has_hr']
    self.has_gps = self.info['has_gps']

# DESPUÉS
def __init__(self, raw_session):
    self.raw = raw_session
    self.info = self._parse_info()
    self.has_hr = self.info['has_hr']
    # CORRECCIÓN: Para relojes sin GPS funcional, forzar a False
    # Esto evita que el parser intente leer coordenadas inexistentes
    # y lea correctamente el HR sin GPS
    self.has_gps = False  # Forzado a False para relojes sin GPS
```

**⚠️ NOTA**: Solo aplica este cambio si tu reloj **NO tiene GPS funcional**. Si tu reloj sí tiene GPS y quieres exportar coordenadas, NO apliques este cambio.

---

### 4. Fix de Manejo de Errores Mejorado (`parser.py`) - Opcional

**Archivo**: `polar_rcx5_datalink/parser.py`

**Ubicación**: Línea ~150-151

**Cambio**:
```python
# ANTES
        except Exception as e:
            raise ParserError(e)

# DESPUÉS
        except Exception as e:
            # Incluir información contextual sobre el error
            error_info = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'session_id': self.id,
                'samples_parsed': len(self.samples),
                'cursor_position': self._cursor,
                'total_bits': len(self._samples_bits),
                'has_hr': self.has_hr,
                'has_gps': self.has_gps,
            }
            error_msg = (
                f"Error parsing samples: {error_info['error_type']}: {error_info['error_message']}. "
                f"Session: {error_info['session_id']}, "
                f"Samples parsed: {error_info['samples_parsed']}, "
                f"Cursor: {error_info['cursor_position']}/{error_info['total_bits']}"
            )
            enhanced_error = ParserError(error_msg)
            enhanced_error.error_info = error_info
            enhanced_error.original_exception = e
            raise enhanced_error
```

---

## 🚀 Cómo Aplicar los Patches

### Opción 1: Manual

1. Localiza la carpeta de instalación:
   ```bash
   python -c "import polar_rcx5_datalink; print(polar_rcx5_datalink.__file__)"
   ```

2. Abre cada archivo con un editor de texto

3. Busca las líneas indicadas y aplica los cambios

4. Guarda los archivos

### Opción 2: Reinstalar desde Fork (Futuro)

Cuando se cree un fork del proyecto original con estos fixes:
```bash
pip uninstall polar-rcx5-datalink
pip install git+https://github.com/tu-usuario/polar-rcx5-datalink.git
```

---

## ✅ Verificar que los Patches Funcionan

Después de aplicar los patches, ejecuta:

```bash
python scripts/verificar_correccion.py
```

Deberías ver:
- ✅ Sin errores de timeout
- ✅ Sin errores de StopIteration
- ✅ Valores de HR en rango válido (30-250 bpm)
- ✅ Promedios coinciden con el header

---

## 📋 Checklist de Patches

- [ ] Fix 1: Timeout en Windows (`datalink.py`)
- [ ] Fix 2: StopIteration (`utils.py`)
- [ ] Fix 3: GPS forzado a False (`parser.py`)
- [ ] Fix 4: Manejo de errores mejorado (`parser.py`) - Opcional
- [ ] Verificación exitosa

---

**Última actualización**: Febrero 2026
