# Dashboard de Entrenamientos - Landing Page

Landing page moderna con React, Next.js y shadcn/ui para visualizar entrenamientos del Polar RCX5.

## 🚀 Características

- ✅ **Landing page con instrucciones** claras para obtener el archivo JSON
- ✅ **Upload de archivo JSON** desde el navegador (procesamiento 100% local)
- ✅ **Dashboard interactivo** con gráficos usando Recharts
- ✅ **Estadísticas detalladas** (HR, duración, distancia, etc.)
- ✅ **Diseño responsive** y moderno con Tailwind CSS
- ✅ **Compatible con Vercel** para deploy instantáneo

## 📦 Stack Tecnológico

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **shadcn/ui** (componentes UI)
- **Recharts** (gráficos)
- **Tailwind CSS** (estilos)
- **Lucide React** (iconos)

## 🛠️ Instalación Local

1. Instalar dependencias:

```bash
npm install
```

2. Ejecutar en modo desarrollo:

```bash
npm run dev
```

3. Abrir [http://localhost:3000](http://localhost:3000) en tu navegador

## 📤 Deploy en Vercel

### Opción 1: Deploy desde el repositorio

1. Ve a [vercel.com](https://vercel.com)
2. Conecta tu repositorio de GitHub
3. Selecciona la carpeta `landing` como directorio raíz
4. Vercel detectará automáticamente Next.js y configurará todo
5. ¡Deploy listo!

### Opción 2: Deploy con Vercel CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Desde la carpeta landing/
cd landing
vercel

# Para producción
vercel --prod
```

## 📋 Cómo usar

### 1. Obtener tu archivo de entrenamientos

Ejecuta el script de exportación desde la raíz del proyecto:

```bash
python scripts/exportar_para_dashboard.py
```

Esto generará el archivo `entrenamientos_dashboard/entrenamientos.json`

### 2. Cargar el archivo en la web

1. Abre la landing page (local o desplegada en Vercel)
2. Sigue las instrucciones en pantalla
3. Arrastra o selecciona tu archivo `entrenamientos.json`
4. ¡Visualiza tus datos!

## 🎨 Personalización

### Colores

Los colores principales se pueden modificar en `app/globals.css`:

```css
:root {
  --primary: 262 83% 58%; /* Color principal (púrpura) */
  /* ... más colores */
}
```

### Gráficos

Los componentes de gráficos están en `components/charts/`:

- `monthly-sessions-chart.tsx` - Entrenamientos por mes
- `hr-chart.tsx` - Frecuencia cardíaca
- `duration-chart.tsx` - Duración por mes

## 🏗️ Estructura del Proyecto

```
landing/
├── app/
│   ├── layout.tsx              # Layout principal
│   ├── page.tsx                # Landing page
│   ├── dashboard/
│   │   └── page.tsx            # Dashboard
│   └── globals.css             # Estilos globales
├── components/
│   ├── ui/                     # Componentes shadcn
│   ├── charts/                 # Gráficos
│   ├── file-uploader.tsx       # Upload de JSON
│   ├── stats-cards.tsx         # Tarjetas de estadísticas
│   └── sessions-list.tsx       # Lista de sesiones
├── lib/
│   ├── utils.ts                # Utilidades
│   └── data-processor.ts       # Procesamiento de datos
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## 🔒 Privacidad

Todos los datos se procesan **localmente en tu navegador**. No se envían a ningún servidor. El archivo JSON se almacena temporalmente en `localStorage` mientras navegas por el dashboard.

## 📝 Notas

- El proyecto está optimizado para Vercel pero funciona en cualquier plataforma que soporte Next.js
- Los gráficos son responsivos y se adaptan a cualquier tamaño de pantalla
- Compatible con navegadores modernos (Chrome, Firefox, Safari, Edge)

## 🤝 Contribuir

Para contribuir al proyecto:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto hereda la licencia MIT del proyecto principal.
