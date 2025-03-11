#!/bin/bash
set -e

# This script is not used with systemd as the entrypoint,
# but is included for reference or for use with non-systemd containers

# Start services based on server role
case "$SERVER_ROLE" in
  database)
    echo "Starting database role services..."
    # Start PostgreSQL
    service postgresql start
    
    # Create database and user if they don't exist
    su - postgres -c "psql -c \"SELECT 1 FROM pg_roles WHERE rolname='crown_user'\" | grep -q 1 || \
      psql -c \"CREATE USER crown_user WITH PASSWORD 'crown_password';\""
    
    su - postgres -c "psql -c \"SELECT 1 FROM pg_database WHERE datname='crown_nexus'\" | grep -q 1 || \
      psql -c \"CREATE DATABASE crown_nexus OWNER crown_user;\""
    
    # Start Redis
    service redis-server start
    ;;
    
  backend)
    echo "Starting backend role services..."
    # Start Elasticsearch
    service elasticsearch start
    
    # Create Python virtual environment and install dependencies if needed
    if [ -d "/app/backend" ]; then
      cd /app/backend
      if [ ! -d "venv" ]; then
        python3 -m venv venv
        ./venv/bin/pip install --upgrade pip
        if [ -f "requirements.txt" ]; then
          ./venv/bin/pip install -r requirements.txt
        else
          # Install minimum required packages
          ./venv/bin/pip install fastapi uvicorn[standard] sqlalchemy[asyncio] alembic pydantic elasticsearch redis
        fi
      fi
      
      # Run migrations if Alembic is configured
      if [ -d "alembic" ]; then
        ./venv/bin/alembic upgrade head
      fi
      
      # Start the API server
      # If main.py doesn't exist, create a minimal one
      if [ ! -f "main.py" ]; then
        echo "Creating minimal FastAPI application..."
        cat > main.py << 'EOF'
from fastapi import FastAPI
import os
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Crown Nexus API")

@app.get("/")
async def root():
    return {"message": "Crown Nexus API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/env")
async def environment():
    # Return environment variables (excluding sensitive ones)
    env_vars = {k: v for k, v in os.environ.items() 
                if not any(secret in k.lower() for secret in ["password", "secret", "key"])}
    return env_vars

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
EOF
      fi
      
      # Start the FastAPI server
      nohup ./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 > /app/backend/api.log 2>&1 &
      echo "FastAPI server started on port 8000"
    else
      # Start a simple Python HTTP server for testing
      python3 -m http.server 8000 &
    fi
    ;;
    
  frontend)
    echo "Starting frontend role services..."
    
    # Configure Nginx for Vue.js SPA
    if [ ! -f "/etc/nginx/sites-available/crown-nexus" ]; then
      cat > /etc/nginx/sites-available/crown-nexus << 'EOF'
server {
    listen 80;
    server_name _;

    root /app/frontend/dist;
    index index.html;

    # Handle SPA routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to the backend
    location /api {
        proxy_pass http://server2:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
      ln -sf /etc/nginx/sites-available/crown-nexus /etc/nginx/sites-enabled/
      rm -f /etc/nginx/sites-enabled/default
    fi
    
    # Set up Vue.js project if not exists
    if [ -d "/app/frontend" ]; then
      cd /app/frontend
      
      # Create minimal Vue 3 project if not exists
      if [ ! -f "package.json" ]; then
        echo "Creating minimal Vue 3 project..."
        
        # Create package.json
        cat > package.json << 'EOF'
{
  "name": "crown-nexus-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc --noEmit && vite build",
    "preview": "vite preview",
    "test": "vitest"
  },
  "dependencies": {
    "axios": "^1.5.0",
    "pinia": "^2.1.6",
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "vuetify": "^3.3.15"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.3.4",
    "typescript": "^5.2.2",
    "vite": "^4.4.9",
    "vitest": "^0.34.3",
    "vue-tsc": "^1.8.11"
  }
}
EOF
        
        # Create minimal Vue app
        mkdir -p src public
        
        # Create index.html
        cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Crown Nexus</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
EOF
        
        # Create vite.config.ts
        cat > vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://server2:8000',
        changeOrigin: true
      }
    }
  }
})
EOF
        
        # Create tsconfig.json
        cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ESNext",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "strict": true,
    "jsx": "preserve",
    "sourceMap": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "lib": ["ESNext", "DOM"],
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOF

        cat > tsconfig.node.json << 'EOF'
{
  "compilerOptions": {
    "composite": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
EOF
        
        # Create main.ts
        cat > src/main.ts << 'EOF'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

const app = createApp(App)

app.use(createPinia())
   .use(router)
   .use(vuetify)
   .mount('#app')
EOF
        
        # Create App.vue
        cat > src/App.vue << 'EOF'
<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title>Crown Nexus</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn to="/">Home</v-btn>
      <v-btn to="/about">About</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} Crown Nexus</span>
    </v-footer>
  </v-app>
</template>

<script lang="ts" setup>
// Component setup
</script>
EOF
        
        # Create router
        mkdir -p src/router
        cat > src/router/index.ts << 'EOF'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
EOF
        
        # Create views
        mkdir -p src/views
        cat > src/views/HomeView.vue << 'EOF'
<template>
  <div class="home">
    <h1>Welcome to Crown Nexus</h1>
    <p>Status: {{ status }}</p>
    <v-btn color="primary" @click="checkHealth">Check Health</v-btn>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

const status = ref('Unknown')

const checkHealth = async () => {
  try {
    const response = await axios.get('/api/health')
    status.value = response.data.status
  } catch (error) {
    status.value = 'Error connecting to API'
    console.error(error)
  }
}
</script>
EOF

        cat > src/views/AboutView.vue << 'EOF'
<template>
  <div class="about">
    <h1>About Crown Nexus</h1>
    <p>Crown Nexus is a comprehensive deployment system.</p>
  </div>
</template>
EOF
        
        # Create store with Pinia
        mkdir -p src/stores
        cat > src/stores/counter.ts << 'EOF'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  
  function increment() {
    count.value++
  }

  return { count, increment }
})
EOF
        
        # Install dependencies
        npm install
        
        # Build the app
        npm run build
      fi
    fi
    
    # Start Nginx
    service nginx start
    ;;
    
  *)
    echo "No specific role set, starting SSH only"
    ;;
esac

# Start SSH server
echo "Starting SSH server..."
/usr/sbin/sshd -D
