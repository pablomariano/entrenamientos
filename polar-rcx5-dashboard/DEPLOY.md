# 🚀 Guía de Despliegue - Dashboard en Línea

Guía paso a paso para desplegar el dashboard web en producción.

## 📋 Prerequisitos

- Cuenta en plataforma de hosting (Vercel, Netlify, Railway, etc.)
- Repositorio Git configurado
- Dominio (opcional pero recomendado)

---

## 🎯 Opción 1: Despliegue con Vercel + Railway (Recomendado)

### Frontend (Vercel)

1. **Preparar el frontend**
   ```bash
   # Crear estructura básica
   mkdir frontend
   cd frontend
   
   # Inicializar proyecto React/Vue
   npm create vite@latest . -- --template react
   # o
   npm create vite@latest . -- --template vue
   ```

2. **Configurar Vercel**
   - Conectar repositorio GitHub con Vercel
   - Configurar build command: `npm run build`
   - Output directory: `dist`
   - Framework preset: Vite/React o Vite/Vue

3. **Variables de entorno**
   ```
   VITE_API_URL=https://tu-backend.railway.app
   ```

### Backend (Railway)

1. **Crear estructura del backend**
   ```bash
   mkdir backend
   cd backend
   
   # Crear requirements.txt
   pip freeze > requirements.txt
   ```

2. **Crear `main.py` (FastAPI)**
   ```python
   from fastapi import FastAPI, File, UploadFile
   from fastapi.middleware.cors import CORSMiddleware
   import json
   import os
   
   app = FastAPI()
   
   # CORS
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # En producción, especificar dominio
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   
   @app.get("/api/sessions")
   async def get_sessions():
       # Leer archivo JSON
       with open("entrenamientos.json", "r") as f:
           data = json.load(f)
       return data
   
   @app.post("/api/upload")
   async def upload_file(file: UploadFile = File(...)):
       # Guardar archivo subido
       content = await file.read()
       data = json.loads(content)
       # Procesar y guardar
       return {"status": "ok", "sessions": len(data.get("sessions", []))}
   ```

3. **Crear `Procfile`**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Desplegar en Railway**
   - Conectar repositorio
   - Railway detectará automáticamente Python
   - Configurar variables de entorno si es necesario

---

## 🎯 Opción 2: Despliegue Todo-en-Uno con Render

1. **Estructura del proyecto**
   ```
   proyecto/
   ├── frontend/          # Frontend estático
   ├── backend/          # API Python
   ├── render.yaml       # Configuración Render
   └── README.md
   ```

2. **Crear `render.yaml`**
   ```yaml
   services:
     - type: web
       name: polar-dashboard-api
       env: python
       buildCommand: pip install -r backend/requirements.txt
       startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: DATABASE_URL
           value: postgresql://...
   
     - type: web
       name: polar-dashboard-frontend
       env: static
       buildCommand: cd frontend && npm install && npm run build
       staticPublishPath: frontend/dist
   ```

3. **Desplegar**
   - Conectar repositorio con Render
   - Render leerá `render.yaml` automáticamente

---

## 🎯 Opción 3: Despliegue Manual (VPS/Droplet)

### Requisitos del servidor
- Ubuntu 20.04+
- Python 3.8+
- Nginx
- PostgreSQL (opcional)

### Pasos

1. **Configurar servidor**
   ```bash
   # Actualizar sistema
   sudo apt update && sudo apt upgrade -y
   
   # Instalar Python y dependencias
   sudo apt install python3-pip python3-venv nginx postgresql -y
   ```

2. **Clonar repositorio**
   ```bash
   git clone https://github.com/tu-usuario/polar-rcx5-dashboard.git
   cd polar-rcx5-dashboard
   ```

3. **Configurar backend**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configurar Nginx**
   ```nginx
   server {
       listen 80;
       server_name tu-dominio.com;
       
       # Frontend
       location / {
           root /var/www/polar-dashboard/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
       
       # Backend API
       location /api {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Configurar servicio systemd**
   ```ini
   # /etc/systemd/system/polar-api.service
   [Unit]
   Description=Polar Dashboard API
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/var/www/polar-dashboard/backend
   Environment="PATH=/var/www/polar-dashboard/backend/venv/bin"
   ExecStart=/var/www/polar-dashboard/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Iniciar servicios**
   ```bash
   sudo systemctl enable polar-api
   sudo systemctl start polar-api
   sudo systemctl restart nginx
   ```

---

## 🔒 Seguridad

### Variables de Entorno

Crear archivo `.env` (NO subir a Git):
```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=tu-clave-secreta-muy-segura
ALLOWED_ORIGINS=https://tu-dominio.com
```

### HTTPS

1. **Certbot (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d tu-dominio.com
   ```

2. **Actualizar Nginx para HTTPS**
   ```nginx
   server {
       listen 443 ssl;
       ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
       # ... resto de configuración
   }
   ```

---

## 📊 Monitoreo

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected"
    }
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🔄 CI/CD con GitHub Actions

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          # Comandos de despliegue
          
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          # Comandos de despliegue
```

---

## 🧪 Testing Local

Antes de desplegar, probar localmente:

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

---

## 📝 Checklist de Despliegue

- [ ] Código en repositorio Git
- [ ] Variables de entorno configuradas
- [ ] Base de datos configurada (si aplica)
- [ ] HTTPS configurado
- [ ] Dominio apuntando correctamente
- [ ] Health check funcionando
- [ ] Logs configurados
- [ ] Backup de datos configurado
- [ ] Documentación actualizada

---

## 🆘 Troubleshooting

### Error: CORS
- Verificar configuración CORS en backend
- Asegurar que `ALLOWED_ORIGINS` incluye el dominio frontend

### Error: Base de datos
- Verificar conexión a base de datos
- Revisar credenciales en variables de entorno

### Error: Build falla
- Verificar logs de build
- Asegurar que todas las dependencias están en `requirements.txt`

---

**Última actualización**: Febrero 2026
