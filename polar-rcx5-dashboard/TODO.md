# ✅ TODO - Antes de Subir a GitHub

## 🔍 Checklist de Verificación

### Pre-commit
- [ ] Verificar que no hay datos personales
  ```bash
  # Buscar archivos .json que no deben subirse
  cd C:\Users\Pablo\Desktop\polar-rcx5-dashboard
  Get-ChildItem -Recurse -Filter "*.json"
  ```
  **Resultado esperado**: Ningún archivo (todos están en .gitignore)

- [ ] Verificar que no hay paths absolutos con información personal
  ```bash
  # Buscar "C:\Users\Pablo" en archivos
  rg "C:\\Users\\Pablo" -t py -t md
  ```
  **Acción**: Reemplazar con paths relativos si encuentra alguno

- [ ] Verificar que .gitignore funciona correctamente
  ```bash
  # Ver qué archivos Git rastreará
  git status --short
  ```

### Pruebas Finales
- [ ] Ejecutar script principal desde carpeta scripts/
  ```bash
  cd C:\Users\Pablo\Desktop\polar-rcx5-dashboard
  python scripts/exportar_para_dashboard.py
  ```

- [ ] Verificar que dashboard carga correctamente
  ```bash
  python scripts/abrir_dashboard.py
  ```

- [ ] Probar scripts de diagnóstico
  ```bash
  python scripts/verificar_correccion.py
  ```

### Documentación
- [ ] README.md está actualizado
- [ ] Todos los links internos funcionan
- [ ] No hay referencias a archivos que no existen
- [ ] Instrucciones de instalación son claras

### GitHub
- [ ] Crear cuenta de GitHub (si no tienes)
- [ ] Instalar Git en Windows
  - Descargar desde: https://git-scm.com/download/win
  - Configurar usuario:
    ```bash
    git config --global user.name "Tu Nombre"
    git config --global user.email "tu@email.com"
    ```

---

## 🚀 Comandos de Git (Orden de Ejecución)

### 1. Inicializar repositorio
```bash
cd C:\Users\Pablo\Desktop\polar-rcx5-dashboard
git init
```

### 2. Añadir todos los archivos
```bash
git add .
```

### 3. Ver qué se va a commitear
```bash
git status
```

### 4. Primer commit
```bash
git commit -m "Initial commit: Polar RCX5 Dashboard v1.0.0"
```

### 5. Crear repositorio en GitHub
- Ir a: https://github.com/new
- Nombre: `polar-rcx5-dashboard`
- Público o Privado (tu elección)
- **NO** marcar "Add README"

### 6. Conectar con GitHub
```bash
git remote add origin https://github.com/TU-USUARIO/polar-rcx5-dashboard.git
git branch -M main
git push -u origin main
```

---

## ⚠️ Posibles Problemas y Soluciones

### "Git no es reconocido como comando"
**Solución**: Instalar Git desde https://git-scm.com/download/win

### "Failed to push"
**Solución**: Verificar URL del repositorio
```bash
git remote -v
```

### "Archivos muy grandes"
**Solución**: Verificar .gitignore, no debería incluir archivos de datos
```bash
git rm --cached archivo-grande.json
```

### "Conflictos con README"
**Solución**: No inicializar el repo con README en GitHub

---

## 📋 Después de Subir

### Configurar Repositorio
1. Añadir descripción
2. Añadir topics/tags
3. Configurar GitHub Pages (opcional)
4. Añadir badge de licencia al README

### Compartir
1. Reddit: r/running, r/fitness, r/python
2. Twitter/X con hashtags: #Polar #RCX5 #Python
3. Comunidades de Polar

---

## 🎯 Próximas Tareas (Post-GitHub)

Ver **ROADMAP.md** para plan completo.

### Corto plazo
- [ ] Crear issues para bugs conocidos
- [ ] Documentar sesiones problemáticas en wiki
- [ ] Añadir screenshots al README

### Medio plazo
- [ ] Implementar backend API (FastAPI)
- [ ] Desplegar dashboard en Vercel
- [ ] Crear base de datos PostgreSQL

### Largo plazo
- [ ] Soporte multi-usuario
- [ ] App móvil
- [ ] Integración con Strava

---

**Última actualización**: Febrero 2026
