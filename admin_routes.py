from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
import sqlite3
import base64
import uuid

# Importar sistema mejorado de upload de imágenes
try:
    from improved_image_upload import ImprovedImageUploader
    IMAGE_UPLOADER = ImprovedImageUploader()
    IMPROVED_UPLOAD_AVAILABLE = True
    print("✅ Sistema mejorado de upload de imágenes disponible")
except ImportError:
    IMAGE_UPLOADER = None
    IMPROVED_UPLOAD_AVAILABLE = False
    print("⚠️ Sistema mejorado de upload no disponible - usando método básico")

# Variable global para modo mantenimiento
MAINTENANCE_MODE = False

# Variables globales para actualizaciones forzadas
FORCE_UPDATE_MODE = False
IOS_APP_URL = ""
ANDROID_APP_URL = ""

def get_admin_user_id():
    """Obtener ID del usuario admin"""
    try:
        import requests
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': 'Bearer {}'.format(SUPABASE_KEY),
            'Content-Type': 'application/json'
        }
        
        # Buscar usuario admin existente
        response = requests.get(f'{SUPABASE_URL}/rest/v1/users?email=eq.admin@cubalink23.com&select=id', headers=headers)
        if response.status_code == 200:
            users = response.json()
            if users:
                return users[0]['id']
        
        # Si no existe, crear usuario admin
        admin_user = {
            'email': 'admin@cubalink23.com',
            'role': 'admin'
        }
        response = requests.post(f'{SUPABASE_URL}/rest/v1/users', headers=headers, json=admin_user)
        if response.status_code == 201:
            return response.json()[0]['id']
        
        return None
    except Exception as e:
        print(f"Error obteniendo admin user: {e}")
        return None

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Configuración del panel
ADMIN_CONFIG = {
    'app_name': 'Cubalink23',
    'version': '1.0.0',
    'admin_email': 'admin@cubalink23.com'
}

# Base de datos simple para estadísticas
def init_db():
    conn = sqlite3.connect('admin_stats.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                 (id INTEGER PRIMARY KEY, date TEXT, searches INTEGER, 
                  users INTEGER, errors INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, user_id TEXT, searches INTEGER,
                  last_seen TEXT, blocked INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

@admin.route('/')
def dashboard():
    """Panel principal de administración"""
    return render_template('admin/dashboard.html', config=ADMIN_CONFIG)

@admin.route('/system')
def system():
    """Gestión del sistema"""
    return render_template('admin/system.html', config=ADMIN_CONFIG)

@admin.route('/orders')
def orders():
    """Gestión de órdenes"""
    return render_template('admin/orders.html', config=ADMIN_CONFIG)

@admin.route('/users')
def users():
    """Gestión de usuarios"""
    return render_template('admin/users.html', config=ADMIN_CONFIG)

@admin.route('/products')
def products():
    """Gestión de productos"""
    return render_template('admin/products.html', config=ADMIN_CONFIG)

@admin.route('/vendors')
def vendors():
    """Gestión de vendedores"""
    return render_template('admin/vendors.html', config=ADMIN_CONFIG)

@admin.route('/drivers')
def drivers():
    """Gestión de repartidores"""
    return render_template('admin/drivers.html', config=ADMIN_CONFIG)

@admin.route('/vehicles')
def vehicles():
    """Gestión de vehículos"""
    return render_template('admin/vehicles.html', config=ADMIN_CONFIG)

@admin.route('/wallet')
def wallet():
    """Gestión de billetera"""
    return render_template('admin/wallet.html', config=ADMIN_CONFIG)

@admin.route('/phone_recharges')
def phone_recharges():
    """Gestión de recargas telefónicas"""
    return render_template('admin/phone_recharges.html', config=ADMIN_CONFIG)

@admin.route('/support_chat')
def support_chat():
    """Chat de soporte"""
    return render_template('admin/support_chat.html', config=ADMIN_CONFIG)

@admin.route('/payroll')
def payroll():
    """Gestión de nómina"""
    return render_template('admin/payroll.html', config=ADMIN_CONFIG)

@admin.route('/payment_methods')
def payment_methods():
    """Gestión de métodos de pago"""
    return render_template('admin/payment_methods.html', config=ADMIN_CONFIG)

@admin.route('/alerts')
def alerts():
    """Gestión de alertas"""
    return render_template('admin/alerts.html', config=ADMIN_CONFIG)

@admin.route('/system_rules')
def system_rules():
    """Reglas del sistema"""
    return render_template('admin/system_rules.html', config=ADMIN_CONFIG)

# ==================== API ENDPOINTS ====================

@admin.route('/api/orders', methods=['GET'])
def get_orders():
    """Obtener órdenes desde Supabase"""
    try:
        from supabase import create_client
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = supabase.table('orders').select('*').order('created_at', desc=True).execute()
        
        orders = result.data if result.data else []
        return jsonify({'success': True, 'orders': orders})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin.route('/api/users', methods=['GET'])
def get_users():
    """Obtener usuarios desde Supabase"""
    try:
        from supabase import create_client
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = supabase.table('users').select('*').order('created_at', desc=True).execute()
        
        users = result.data if result.data else []
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin.route('/api/products', methods=['GET'])
def get_products():
    """Obtener productos desde Supabase"""
    try:
        from supabase import create_client
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = supabase.table('store_products').select('*').eq('is_active', True).execute()
        
        products = result.data if result.data else []
        return jsonify({'success': True, 'products': products})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin.route('/api/products', methods=['POST'])
def create_product():
    """Crear producto en Supabase"""
    try:
        data = request.get_json()
        
        from supabase import create_client
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = supabase.table('store_products').insert(data).execute()
        
        if result.data:
            return jsonify({'success': True, 'product': result.data[0]})
        else:
            return jsonify({'success': False, 'error': 'Error creando producto'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== SISTEMA DE NOTIFICACIONES ====================

@admin.route('/api/notifications', methods=['POST', 'GET'])
def notifications():
    """Sistema de notificaciones"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title', 'Notificación')
            message = data.get('message', '')
            user_id = data.get('user_id', 'all')
            
            print(f"🔔 Enviando notificación: {title}")
            
            # Guardar en Supabase para historial
            try:
                from supabase import create_client
                SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
                SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
                
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                
                notification_data = {
                    'user_id': user_id if user_id != 'all' else None,
                    'title': title,
                    'message': message,
                    'type': 'admin_notification',
                    'data': data.get('data', {}),
                    'created_at': datetime.now().isoformat(),
                }
                
                result = supabase.table('notifications').insert(notification_data).execute()
                if result.data:
                    print(f"💾 Notificación guardada en Supabase: {title}")
                else:
                    print(f"⚠️ Error guardando en Supabase")
                    
            except Exception as e:
                print(f"⚠️ Error guardando en Supabase: {e}")
            
            return jsonify({'success': True, 'message': 'Notificación enviada'})
        
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    elif request.method == 'GET':
        # Obtener notificaciones
        try:
            from supabase import create_client
            SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
            SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
            
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            result = supabase.table('notifications').select('*').order('created_at', desc=True).limit(50).execute()
            
            notifications = result.data if result.data else []
            return jsonify({'success': True, 'notifications': notifications})
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

# ==================== SISTEMA DE BANNERS ====================

@admin.route('/api/banners', methods=['GET'])
def get_banners():
    """Obtener banners desde Supabase"""
    try:
        from supabase import create_client
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = supabase.table('banners').select('*').order('sort_order').execute()
        
        banners = result.data if result.data else []
        return jsonify({'success': True, 'banners': banners})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin.route('/api/banners', methods=['POST'])
def create_banner():
    """Crear banner en Supabase"""
    try:
        data = request.get_json()
        
        from supabase import create_client
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = supabase.table('banners').insert(data).execute()
        
        if result.data:
            return jsonify({'success': True, 'banner': result.data[0]})
        else:
            return jsonify({'success': False, 'error': 'Error creando banner'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== SISTEMA DE CONFIGURACIÓN ====================

@admin.route('/api/system/maintenance', methods=['POST'])
def toggle_maintenance():
    """Activar/desactivar modo mantenimiento"""
    global MAINTENANCE_MODE
    try:
        data = request.get_json()
        MAINTENANCE_MODE = data.get('enabled', False)
        
        return jsonify({
            'success': True, 
            'maintenance_mode': MAINTENANCE_MODE,
            'message': 'Modo mantenimiento actualizado'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin.route('/api/system/maintenance', methods=['GET'])
def get_maintenance_status():
    """Obtener estado de mantenimiento"""
    return jsonify({
        'success': True,
        'maintenance_mode': MAINTENANCE_MODE,
        'message': 'Aplicación en mantenimiento' if MAINTENANCE_MODE else 'Aplicación funcionando normalmente'
    })

@admin.route('/api/system/force-update', methods=['POST'])
def toggle_force_update():
    """Activar/desactivar actualización forzada"""
    global FORCE_UPDATE_MODE, IOS_APP_URL, ANDROID_APP_URL
    try:
        data = request.get_json()
        FORCE_UPDATE_MODE = data.get('enabled', False)
        IOS_APP_URL = data.get('ios_url', '')
        ANDROID_APP_URL = data.get('android_url', '')
        
        return jsonify({
            'success': True,
            'force_update': FORCE_UPDATE_MODE,
            'ios_url': IOS_APP_URL,
            'android_url': ANDROID_APP_URL,
            'message': 'Actualización forzada configurada'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin.route('/api/system/force-update', methods=['GET'])
def get_force_update_status():
    """Obtener estado de actualización forzada"""
    return jsonify({
        'success': True,
        'force_update': FORCE_UPDATE_MODE,
        'ios_url': IOS_APP_URL,
        'android_url': ANDROID_APP_URL,
        'message': 'Actualización requerida' if FORCE_UPDATE_MODE else 'App actualizada'
    })

# ==================== ESTADÍSTICAS ====================

@admin.route('/api/stats', methods=['GET'])
def get_admin_stats():
    """Obtener estadísticas completas del sistema"""
    try:
        from supabase import create_client
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Contar usuarios
        users_result = supabase.table('users').select('id').execute()
        total_users = len(users_result.data) if users_result.data else 0
        
        # Contar órdenes
        orders_result = supabase.table('orders').select('id, order_status, total').execute()
        orders = orders_result.data if orders_result.data else []
        total_orders = len(orders)
        
        # Calcular ventas totales
        total_sales = sum(float(order.get('total', 0)) for order in orders)
        
        # Órdenes por estado
        orders_by_status = {}
        for order in orders:
            status = order.get('order_status', 'unknown')
            orders_by_status[status] = orders_by_status.get(status, 0) + 1
        
        stats = {
            'total_users': total_users,
            'total_orders': total_orders,
            'total_sales': total_sales,
            'orders_by_status': orders_by_status,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
