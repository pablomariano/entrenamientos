# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto Polar RCX5 Dashboard!

## 📋 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado ya en [Issues](https://github.com/tu-usuario/polar-rcx5-dashboard/issues)
2. Crea un nuevo issue con:
   - Título descriptivo
   - Descripción detallada del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Información del sistema (OS, Python version, etc.)

### Sugerir Mejoras

1. Abre un issue con la etiqueta `enhancement`
2. Describe claramente la funcionalidad propuesta
3. Explica por qué sería útil

### Contribuir Código

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/polar-rcx5-dashboard.git
   cd polar-rcx5-dashboard
   ```

2. **Crea una rama**
   ```bash
   git checkout -b feature/mi-nueva-funcionalidad
   ```

3. **Haz tus cambios**
   - Sigue las convenciones de código existentes
   - Añade comentarios donde sea necesario
   - Actualiza documentación si es necesario

4. **Commit tus cambios**
   ```bash
   git add .
   git commit -m "feat: añadir nueva funcionalidad X"
   ```

5. **Push y crea Pull Request**
   ```bash
   git push origin feature/mi-nueva-funcionalidad
   ```

## 📝 Convenciones

### Commits

Usa mensajes de commit descriptivos siguiendo [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, punto y coma faltante, etc.
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Cambios en build, dependencias, etc.

### Código Python

- Seguir PEP 8
- Máximo 100 caracteres por línea
- Usar type hints donde sea posible
- Documentar funciones con docstrings

### Código JavaScript

- Usar ESLint
- Seguir estilo consistente (preferiblemente Prettier)
- Comentar código complejo

## 🧪 Testing

Antes de hacer PR, asegúrate de:

- [ ] El código funciona correctamente
- [ ] No rompe funcionalidades existentes
- [ ] Los tests pasan (si existen)
- [ ] La documentación está actualizada

## 📚 Áreas donde se Necesita Ayuda

- Mejora del parser para sesiones problemáticas
- Nuevas visualizaciones para el dashboard
- Soporte para otros modelos de relojes Polar
- Traducciones a otros idiomas
- Mejoras de rendimiento
- Tests unitarios e integración

## ❓ Preguntas

Si tienes preguntas, abre un issue con la etiqueta `question` o contacta a los mantenedores.

¡Gracias por contribuir! 🎉
