# 🚀 Guía de Deploy en Vercel

## Método 1: Deploy desde la Web (Más Fácil)

### Paso 1: Preparar el repositorio

Tu código debe estar en GitHub, GitLab o Bitbucket.

### Paso 2: Importar en Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Haz clic en **"New Project"** o **"Add New..."** → **"Project"**
3. Conecta tu cuenta de GitHub/GitLab/Bitbucket
4. Selecciona el repositorio `entrenamientos`

### Paso 3: Configurar el proyecto

En la configuración de deploy:

- **Framework Preset**: Next.js (detectado automáticamente)
- **Root Directory**: Haz clic en "Edit" y selecciona `landing`
- **Build Command**: `npm run build` (por defecto)
- **Output Directory**: `.next` (por defecto)
- **Install Command**: `npm install` (por defecto)

### Paso 4: Deploy

1. Haz clic en **"Deploy"**
2. Espera 1-2 minutos
3. ¡Tu sitio está en línea!

Vercel te dará una URL como: `https://tu-proyecto.vercel.app`

## Método 2: Deploy desde la Terminal

### Requisitos previos

```bash
# Instalar Vercel CLI globalmente
npm install -g vercel
```

### Paso 1: Login

```bash
vercel login
```

Sigue las instrucciones para autenticarte.

### Paso 2: Deploy

```bash
# Ir a la carpeta landing
cd landing

# Deploy a preview (desarrollo)
vercel

# Deploy a producción
vercel --prod
```

### Configuración inicial (solo la primera vez)

Cuando ejecutes `vercel` por primera vez, te preguntará:

```
? Set up and deploy "~/path/to/landing"? [Y/n] Y
? Which scope do you want to deploy to? [Tu cuenta]
? Link to existing project? [y/N] N
? What's your project's name? entrenamientos-dashboard
? In which directory is your code located? ./
```

## Configuración Automática

El proyecto incluye `vercel.json` que configura:
- Framework: Next.js
- Región: `iad1` (USA Este)
- Comandos de build y desarrollo

## Variables de Entorno (Si las necesitas)

### En Vercel Web

1. Ve a tu proyecto en Vercel
2. Settings → Environment Variables
3. Añade tus variables

### Desde CLI

```bash
vercel env add NOMBRE_VARIABLE
```

## URLs Generadas

Vercel genera automáticamente:

- **URL de Preview**: Para cada commit/branch (ej: `https://tu-proyecto-git-main.vercel.app`)
- **URL de Producción**: URL principal (ej: `https://tu-proyecto.vercel.app`)

## Dominio Personalizado (Opcional)

### Añadir dominio propio

1. Ve a tu proyecto en Vercel
2. Settings → Domains
3. Añade tu dominio (ej: `entrenamientos.tudominio.com`)
4. Sigue las instrucciones para configurar DNS

## Actualizaciones Automáticas

Una vez configurado, Vercel desplegará automáticamente:

- **Producción**: Cada push a la rama `main` o `master`
- **Preview**: Cada push a otras ramas

## Verificar el Deploy

1. Visita tu URL de Vercel
2. Verifica que la landing page carga
3. Prueba subir un JSON de ejemplo
4. Revisa que el dashboard funcione correctamente

## Comandos Útiles

```bash
# Ver lista de deploys
vercel list

# Ver logs del último deploy
vercel logs

# Eliminar un proyecto
vercel remove [nombre-proyecto]

# Abrir el proyecto en el navegador
vercel open
```

## Rollback (Revertir Deploy)

Si algo sale mal:

1. Ve a tu proyecto en Vercel
2. Deployments
3. Encuentra el deploy anterior que funcionaba
4. Click en "⋯" → "Promote to Production"

## Optimizaciones

Vercel optimiza automáticamente:

- ✅ Compresión de assets
- ✅ Cache de imágenes
- ✅ CDN global
- ✅ SSL/HTTPS automático
- ✅ Edge Network

## Límites del Plan Gratuito

- ✅ Deploys ilimitados
- ✅ 100GB de ancho de banda/mes
- ✅ Funciones serverless
- ✅ Dominio personalizado

Más que suficiente para este proyecto.

## Problemas Comunes

### "Error: No Output Directory"

- Asegúrate de seleccionar `landing` como Root Directory
- Verifica que `next.config.js` está en la carpeta

### "Module not found"

- Verifica que todas las dependencias están en `package.json`
- Intenta: `rm -rf node_modules && npm install`

### Build falla

- Revisa los logs en Vercel
- Verifica que el build funciona localmente: `npm run build`

## Soporte

- [Documentación de Vercel](https://vercel.com/docs)
- [Soporte de Vercel](https://vercel.com/support)
- [Issues del proyecto](https://github.com/tu-usuario/entrenamientos/issues)
