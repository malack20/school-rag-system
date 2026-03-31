# MASTER DOCKERFILE FOR MONOREPO DEPLOYMENT
# This Dockerfile can build either the backend or the frontend based on the BUILD_TARGET argument.

# The BUILD_TARGET arg must be declared BEFORE the first FROM to be used in FROM statements later.
ARG BUILD_TARGET=backend-final

# --- FRONTEND BUILD STAGE ---
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .

# Accept build-time environment variables
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# --- FRONTEND SERVE STAGE ---
FROM nginx:alpine AS frontend-final
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# --- BACKEND STAGE ---
FROM python:3.11-slim AS backend-final
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ /app
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# --- FINAL SELECTOR ---
FROM ${BUILD_TARGET}
