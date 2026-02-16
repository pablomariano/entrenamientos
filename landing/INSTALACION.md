# ⚡ Instalación Inmediata

## 🚀 Opción 1: Ejecución Local (5 minutos)

### Paso 1: Instalar dependencias

```bash
cd landing
npm install
```

Si no tienes npm instalado, [descarga Node.js](https://nodejs.org/) primero.

### Paso 2: Iniciar servidor de desarrollo

```bash
npm run dev
```

### Paso 3: Abrir en el navegador

Abre [http://localhost:3000](http://localhost:3000)

¡Listo! Ya puedes probar la aplicación.

### Prueba rápida

1. En la landing page, verás las instrucciones
2. Si tienes un archivo `entrenamientos.json`, arrástralo al área de upload
3. Automáticamente te redirigirá al dashboard

---

## 🌐 Opción 2: Deploy en Vercel (2 minutos)

### Método A: Desde la interfaz web (MÁS FÁCIL)

1. **Push tu código a GitHub** (si no lo has hecho):
   ```bash
   git add .
   git commit -m "Add landing page"
   git push
   ```

2. **Ir a Vercel**:
   - Abre [vercel.com/new](https://vercel.com/new)
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio `entrenamientos`

3. **Configurar**:
   - Click en "Edit" en **Root Directory**
   - Selecciona `landing`
   - Todo lo demás se detecta automáticamente

4. **Deploy**:
   - Click en "Deploy"
   - Espera 1-2 minutos
   - ¡Ya está en línea!

### Método B: Desde la terminal

```bash
# Instalar Vercel CLI (solo una vez)
npm install -g vercel

# Ir a la carpeta
cd landing

# Login (solo la primera vez)
vercel login

# Deploy
vercel --prod
```

---

## ✅ Verificación

### En local:
- [ ] La landing page carga en http://localhost:3000
- [ ] El área de upload acepta archivos JSON
- [ ] El dashboard muestra los gráficos correctamente

### En Vercel:
- [ ] La URL de Vercel carga correctamente
- [ ] Se puede subir un archivo JSON
- [ ] Los gráficos son interactivos

---

## 🐛 Problemas Comunes

### `npm: command not found`

Necesitas instalar Node.js:
- Windows: [nodejs.org/download](https://nodejs.org/download)
- Mac: `brew install node`
- Linux: `sudo apt install nodejs npm`

### `Error: Cannot find module`

```bash
rm -rf node_modules package-lock.json
npm install
```

### El puerto 3000 está ocupado

```bash
# Usar otro puerto
npm run dev -- -p 3001
```

### Build falla en Vercel

1. Verifica que seleccionaste `landing` como Root Directory
2. Revisa que el build funciona localmente: `npm run build`
3. Mira los logs en Vercel para detalles

---

## 📦 Dependencias Principales

Se instalarán automáticamente con `npm install`:

- next (14.2.18)
- react (18.3.1)
- recharts (2.12.7) - Gráficos
- lucide-react (0.451.0) - Iconos
- tailwindcss (3.4.1) - Estilos
- typescript (5.x)

---

## 🎯 ¿Qué sigue?

Una vez que tengas la aplicación corriendo:

1. **Exporta tus datos**:
   ```bash
   python scripts/exportar_para_dashboard.py
   ```

2. **Carga el JSON** en la aplicación

3. **Explora el dashboard** con tus datos

---

## 📚 Más Información

- **README.md**: Documentación completa
- **QUICKSTART.md**: Guía rápida
- **VERCEL_DEPLOY.md**: Deploy detallado
- **RESUMEN.md**: Resumen del proyecto

---

## 💡 Tips

- **Desarrollo**: Los cambios se reflejan automáticamente (hot reload)
- **Producción**: Ejecuta `npm run build` antes de desplegar
- **Deploy**: Vercel detecta cambios en GitHub y redeploy automáticamente
- **Gratis**: El plan gratuito de Vercel es más que suficiente

---

## 🆘 Soporte

¿Problemas? Abre un issue en GitHub con:
- Mensaje de error completo
- Sistema operativo
- Versión de Node.js (`node --version`)
- Pasos para reproducir el problema
