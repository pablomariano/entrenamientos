# 📁 Estructura del Proyecto Landing

```
landing/
│
├── 📄 Archivos de Configuración
│   ├── package.json              # Dependencias y scripts npm
│   ├── tsconfig.json             # Configuración TypeScript
│   ├── next.config.js            # Configuración Next.js
│   ├── tailwind.config.ts        # Configuración Tailwind CSS
│   ├── postcss.config.js         # Configuración PostCSS
│   ├── vercel.json               # Configuración Vercel
│   ├── .gitignore                # Archivos ignorados por Git
│   ├── .npmrc                    # Configuración npm
│   └── .env.example              # Variables de entorno de ejemplo
│
├── 📚 Documentación
│   ├── README.md                 # Documentación principal
│   ├── QUICKSTART.md             # Guía de inicio rápido
│   ├── INSTALACION.md            # Instrucciones de instalación
│   ├── VERCEL_DEPLOY.md          # Guía de deploy en Vercel
│   ├── RESUMEN.md                # Resumen del proyecto
│   └── ESTRUCTURA.md             # Este archivo
│
├── app/                          # Next.js App Router
│   ├── layout.tsx                # Layout principal de la app
│   ├── page.tsx                  # Landing page (/)
│   ├── globals.css               # Estilos globales + Tailwind
│   └── dashboard/
│       └── page.tsx              # Página del dashboard (/dashboard)
│
├── components/                   # Componentes React
│   │
│   ├── ui/                       # Componentes shadcn/ui
│   │   ├── card.tsx              # Componente Card
│   │   ├── button.tsx            # Componente Button
│   │   └── badge.tsx             # Componente Badge
│   │
│   ├── charts/                   # Componentes de gráficos
│   │   ├── monthly-sessions-chart.tsx    # Gráfico de sesiones por mes
│   │   ├── hr-chart.tsx                   # Gráfico de frecuencia cardíaca
│   │   └── duration-chart.tsx             # Gráfico de duración por mes
│   │
│   ├── file-uploader.tsx         # Componente de upload con drag & drop
│   ├── stats-cards.tsx           # Tarjetas de estadísticas
│   └── sessions-list.tsx         # Lista de entrenamientos
│
└── lib/                          # Lógica de negocio y utilidades
    ├── utils.ts                  # Utilidades generales (cn, etc.)
    └── data-processor.ts         # Procesamiento de datos de entrenamientos
```

## 📊 Desglose por Tipo

### Configuración (9 archivos)
- package.json
- tsconfig.json
- next.config.js
- tailwind.config.ts
- postcss.config.js
- vercel.json
- .gitignore
- .npmrc
- .env.example

### Documentación (6 archivos)
- README.md
- QUICKSTART.md
- INSTALACION.md
- VERCEL_DEPLOY.md
- RESUMEN.md
- ESTRUCTURA.md

### Aplicación Next.js (3 archivos)
- app/layout.tsx
- app/page.tsx
- app/dashboard/page.tsx
- app/globals.css

### Componentes UI (3 archivos)
- components/ui/card.tsx
- components/ui/button.tsx
- components/ui/badge.tsx

### Componentes Personalizados (6 archivos)
- components/file-uploader.tsx
- components/stats-cards.tsx
- components/sessions-list.tsx
- components/charts/monthly-sessions-chart.tsx
- components/charts/hr-chart.tsx
- components/charts/duration-chart.tsx

### Lógica (2 archivos)
- lib/utils.ts
- lib/data-processor.ts

## 📈 Total de Archivos Creados

**29 archivos** en total:
- 9 de configuración
- 6 de documentación
- 4 de aplicación Next.js
- 3 componentes shadcn/ui
- 6 componentes personalizados
- 1 lógica de datos

## 🎯 Archivos Principales

Los archivos más importantes para entender el proyecto:

1. **app/page.tsx** → Landing page con instrucciones
2. **app/dashboard/page.tsx** → Dashboard con gráficos
3. **components/file-uploader.tsx** → Upload de JSON
4. **lib/data-processor.ts** → Procesamiento de datos
5. **package.json** → Dependencias

## 📦 Generados Automáticamente (No incluidos)

Estos se generarán al ejecutar `npm install`:

```
landing/
├── node_modules/          # Dependencias (ignorado por git)
├── .next/                 # Build de Next.js (ignorado por git)
├── next-env.d.ts          # Types de Next.js (auto-generado)
└── package-lock.json      # Lockfile de npm
```

## 🚀 Flujo de Datos

```
1. Landing Page (app/page.tsx)
   ↓
2. File Upload (components/file-uploader.tsx)
   ↓
3. Validación del JSON
   ↓
4. Guardar en LocalStorage
   ↓
5. Redirección al Dashboard
   ↓
6. Dashboard (app/dashboard/page.tsx)
   ↓
7. Procesamiento (lib/data-processor.ts)
   ↓
8. Renderizado de:
   - Stats Cards
   - Charts (Recharts)
   - Sessions List
```

## 🎨 Jerarquía de Componentes

```
App Layout (layout.tsx)
│
├── Landing Page (page.tsx)
│   └── FileUploader
│       └── Card, Button (shadcn/ui)
│
└── Dashboard Page (dashboard/page.tsx)
    ├── StatsCards
    │   └── Card (shadcn/ui)
    │
    ├── MonthlySessionsChart
    │   ├── Card (shadcn/ui)
    │   └── BarChart (Recharts)
    │
    ├── HRChart
    │   ├── Card (shadcn/ui)
    │   └── LineChart (Recharts)
    │
    ├── DurationChart
    │   ├── Card (shadcn/ui)
    │   └── AreaChart (Recharts)
    │
    └── SessionsList
        ├── Card (shadcn/ui)
        └── Badge (shadcn/ui)
```

## 📝 Convenciones

- **Componentes UI**: PascalCase con sufijo del tipo (Card, Button)
- **Hooks**: camelCase con prefijo `use`
- **Utilidades**: camelCase
- **Tipos**: PascalCase con prefijo `interface` o `type`
- **Archivos**: kebab-case.tsx/ts

## 🔍 Búsqueda Rápida

**¿Quieres cambiar...?**

- Colores → `app/globals.css` (variables CSS)
- Gráficos → `components/charts/`
- Estadísticas → `lib/data-processor.ts`
- Diseño landing → `app/page.tsx`
- Diseño dashboard → `app/dashboard/page.tsx`
- Upload → `components/file-uploader.tsx`
