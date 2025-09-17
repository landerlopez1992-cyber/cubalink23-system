# 🛠️ CubaLink23 System Backend

## 📋 Descripción
Backend dedicado para el sistema principal de CubaLink23, maneja todas las funcionalidades excepto vuelos Duffel y pagos Square.

## 🎯 Funcionalidades
- 📦 **Órdenes y pedidos** - Creación, seguimiento, estados
- 👥 **Usuarios y perfiles** - Gestión de usuarios y saldos  
- 🛒 **Productos y carrito** - Catálogo y carrito de compras
- 🚚 **Vendedores y repartidores** - Sistema de delivery
- 🔔 **Notificaciones** - Sistema de alertas
- 📊 **Reportes y analytics** - Estadísticas del sistema

## 🌐 Endpoints Principales

### Órdenes
- `POST /api/orders` - Crear nueva orden
- `GET /api/orders/user/<user_id>` - Obtener órdenes de usuario
- `PUT /api/orders/<order_id>/status` - Actualizar estado

### Usuarios  
- `PUT /api/users/<user_id>/balance` - Actualizar saldo

### Actividades
- `POST /api/activities` - Agregar actividad
- `GET /api/activities/user/<user_id>` - Obtener actividades

### Administración
- `GET /admin/api/orders` - Todas las órdenes
- `GET /admin/api/stats` - Estadísticas

### Health Check
- `GET /api/health` - Estado del servidor

## 🗄️ Base de Datos
- **Supabase**: PostgreSQL con todas las tablas del sistema
- **Tablas principales**: orders, order_items, users, activities

## 🚀 Deploy en Render
- **URL**: https://cubalink23-system.onrender.com
- **Variables de entorno**: SUPABASE_URL, SUPABASE_KEY
- **Deploy automático**: Desde GitHub

## 🏗️ Arquitectura
Parte del ecosistema de 3 backends especializados:
- `cubalink23-backend` → Vuelos Duffel + Banners
- `cubalink23-payments` → Square API
- `cubalink23-system` → Sistema principal (este)
