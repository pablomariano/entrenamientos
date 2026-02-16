# 🚀 Guía de Inicio Rápido

## Instalación y Ejecución Local

### 1. Instalar dependencias

```bash
cd landing
npm install
```

Si usas yarn:
```bash
yarn install
```

### 2. Ejecutar en modo desarrollo

```bash
npm run dev
```

O con yarn:
```bash
yarn dev
```

### 3. Abrir en el navegador

Abre [http://localhost:3000](http://localhost:3000)

## Deploy en Vercel

### Método más simple (recomendado)

1. Haz fork/clone del repositorio en GitHub
2. Ve a [vercel.com/new](https://vercel.com/new)
3. Importa tu repositorio
4. En la configuración:
   - **Root Directory**: selecciona `landing`
   - Vercel detectará automáticamente Next.js
5. Click en "Deploy"

¡Listo! Tu sitio estará en línea en menos de 2 minutos.

### Método alternativo con CLI

```bash
# Instalar Vercel CLI (solo una vez)
npm i -g vercel

# Desde la carpeta landing/
cd landing

# Login (solo la primera vez)
vercel login

# Deploy a preview
vercel

# Deploy a producción
vercel --prod
```

## Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno en el futuro:

1. Copia `.env.example` a `.env.local`
2. Configura tus variables
3. En Vercel: Settings > Environment Variables

## Comandos Disponibles

```bash
npm run dev      # Modo desarrollo
npm run build    # Compilar para producción
npm start        # Iniciar servidor de producción
npm run lint     # Ejecutar linter
```

## Verificación Post-Deploy

1. Abre tu URL de Vercel
2. Verifica que la landing page carga correctamente
3. Prueba subir un archivo JSON de ejemplo
4. Confirma que el dashboard muestra los gráficos

## Problemas Comunes

### Error: Module not found

```bash
# Eliminar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Error de compilación en Vercel

- Verifica que el directorio raíz sea `landing`
- Asegúrate de que todas las dependencias estén en `package.json`

### El archivo JSON no se carga

- Verifica que el archivo tenga la estructura correcta
- Abre la consola del navegador para ver errores
- El archivo debe tener al menos la propiedad `sessions` como array

## Soporte

Para problemas o preguntas, abre un issue en GitHub.
