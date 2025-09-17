#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ CUBALINK23 SYSTEM BACKEND - PRODUCCIÓN
🔒 Backend dedicado para TODO el sistema excepto Duffel y Square
🌐 Deploy: cubalink23-system.onrender.com
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Importar el panel de administración
from admin_routes import admin
app.register_blueprint(admin)

# Configuración
PORT = int(os.environ.get('PORT', 10000))

# Supabase Configuration - PRODUCCIÓN
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://zgqrhzuhrwudckwesybg.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ')

print("🛠️ CUBALINK23 SYSTEM BACKEND - PRODUCCIÓN")
print(f"🔧 Puerto: {PORT}")
print(f"🗄️ Supabase URL: {'✅ Configurada' if SUPABASE_URL else '❌ No configurada'}")

# Inicializar cliente Supabase
supabase_client = None
try:
    from supabase import create_client, Client
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente Supabase inicializado correctamente")
except Exception as e:
    print(f"❌ Error inicializando Supabase: {e}")
    supabase_client = None

@app.route('/')
def home():
    """🏠 Página principal"""
    return jsonify({
        "message": "CubaLink23 System Backend - PRODUCCIÓN",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": [
            "orders", "users", "products", "vendors", 
            "delivery", "notifications", "analytics"
        ]
    })

@app.route('/api/health')
def health_check():
    """💚 Health check"""
    return jsonify({
        "status": "healthy",
        "message": "CubaLink23 System Backend PRODUCCIÓN funcionando",
        "timestamp": datetime.now().isoformat(),
        "supabase_connected": supabase_client is not None
    })

# ==================== ORDERS API ====================

@app.route('/api/orders', methods=['POST'])
def create_order():
    """📦 Crear nueva orden desde la app Flutter - PRODUCCIÓN"""
    try:
        print("🛒 ===== CREANDO NUEVA ORDEN - PRODUCCIÓN =====")
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        print(f"📋 Datos recibidos: {list(data.keys())}")
        print(f"👤 User ID: {data.get('user_id')}")
        print(f"📦 Order Number: {data.get('order_number')}")
        print(f"💰 Total: ${data.get('total', 0)}")
        
        # Validar campos requeridos
        required_fields = ['user_id', 'order_number', 'total', 'payment_method']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Campo requerido: {field}'}), 400
        
        # Extraer cart_items para crear order_items
        cart_items = data.pop('cart_items', [])
        print(f"🛒 Cart items: {len(cart_items)}")
        
        if not supabase_client:
            return jsonify({'success': False, 'error': 'Supabase no configurado'}), 500
        
        # Crear orden principal
        order_result = supabase_client.table('orders').insert(data).execute()
        
        if not order_result.data:
            print(f"❌ Error creando orden: {order_result}")
            return jsonify({'success': False, 'error': 'Error creando orden en Supabase'}), 500
        
        order_id = order_result.data[0]['id']
        print(f"✅ Orden creada: {order_id}")
        
        # Crear order_items
        items_created = 0
        for item in cart_items:
            try:
                item_data = {
                    'order_id': order_id,
                    'product_type': item.get('product_type', 'store'),
                    'name': item.get('product_name', item.get('name')),
                    'unit_price': item.get('product_price', item.get('price')),
                    'quantity': item.get('quantity', 1),
                    'total_price': (item.get('product_price', item.get('price', 0))) * (item.get('quantity', 1)),
                    'selected_size': item.get('selected_size'),
                    'selected_color': item.get('selected_color'),
                    'asin': item.get('amazon_asin'),
                    'amazon_data': item.get('amazon_data'),
                    'unit_weight_lb': item.get('weight_lb', 0.0),
                    'total_weight_lb': (item.get('weight_lb', 0.0)) * (item.get('quantity', 1)),
                    'metadata': {
                        'original_product_id': item.get('product_id'),
                        'cart_item_id': item.get('id'),
                    },
                }
                
                # Insertar order_item
                item_result = supabase_client.table('order_items').insert(item_data).execute()
                if item_result.data:
                    print(f"   ✅ Item creado: {item_data['name']}")
                    items_created += 1
                else:
                    print(f"   ❌ Error creando item: {item_data['name']}")
            except Exception as item_error:
                print(f"   ⚠️ Error procesando item: {item_error}")
                continue
        
        print(f"📦 Items creados: {items_created}/{len(cart_items)}")
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'order_number': data['order_number'],
            'items_created': items_created,
            'message': 'Orden creada exitosamente en PRODUCCIÓN'
        })
            
    except Exception as e:
        print(f"❌ Error creando orden: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders/user/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    """📋 Obtener órdenes de un usuario - PRODUCCIÓN"""
    try:
        print(f"🔍 Obteniendo órdenes para usuario: {user_id}")
        
        if not supabase_client:
            return jsonify({'success': False, 'error': 'Supabase no configurado'}), 500
        
        # Obtener órdenes del usuario
        result = supabase_client.table('orders').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        
        orders = result.data if result.data else []
        print(f"📦 Órdenes encontradas: {len(orders)}")
        
        return jsonify({
            'success': True,
            'orders': orders,
            'count': len(orders)
        })
            
    except Exception as e:
        print(f"❌ Error obteniendo órdenes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """📊 Actualizar estado de orden - PRODUCCIÓN"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'success': False, 'error': 'Status requerido'}), 400
        
        print(f"🔄 Actualizando orden {order_id} a estado: {new_status}")
        
        if not supabase_client:
            return jsonify({'success': False, 'error': 'Supabase no configurado'}), 500
        
        result = supabase_client.table('orders').update({
            'order_status': new_status,
            'updated_at': datetime.now().isoformat()
        }).eq('id', order_id).execute()
        
        if result.data:
            print(f"✅ Estado actualizado")
            return jsonify({'success': True, 'message': 'Estado actualizado'})
        else:
            return jsonify({'success': False, 'error': 'Orden no encontrada'}), 404
            
    except Exception as e:
        print(f"❌ Error actualizando estado: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== USERS API ====================

@app.route('/api/users/<user_id>/balance', methods=['PUT'])
def update_user_balance(user_id):
    """💰 Actualizar saldo de usuario - PRODUCCIÓN"""
    try:
        data = request.get_json()
        new_balance = data.get('balance')
        
        if new_balance is None:
            return jsonify({'success': False, 'error': 'Balance requerido'}), 400
        
        if not supabase_client:
            return jsonify({'success': False, 'error': 'Supabase no configurado'}), 500
        
        result = supabase_client.table('users').update({
            'balance': new_balance,
            'updated_at': datetime.now().isoformat()
        }).eq('id', user_id).execute()
        
        if result.data:
            return jsonify({'success': True, 'message': 'Saldo actualizado'})
        else:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== ACTIVITIES API ====================

@app.route('/api/activities', methods=['POST'])
def add_activity():
    """📊 Agregar actividad de usuario - PRODUCCIÓN"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'type', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Campo requerido: {field}'}), 400
        
        # Agregar timestamp si no existe
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        if not supabase_client:
            return jsonify({'success': False, 'error': 'Supabase no configurado'}), 500
        
        result = supabase_client.table('activities').insert(data).execute()
        
        if result.data:
            return jsonify({'success': True, 'activity': result.data[0]})
        else:
            return jsonify({'success': False, 'error': 'Error creando actividad'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== ADMIN ENDPOINTS ====================

@app.route('/admin/api/orders', methods=['GET'])
def admin_get_orders():
    """📋 Obtener todas las órdenes (admin) - PRODUCCIÓN"""
    try:
        if not supabase_client:
            return jsonify({'success': False, 'error': 'Supabase no configurado'}), 500
        
        result = supabase_client.table('orders').select('*').order('created_at', desc=True).limit(100).execute()
        
        orders = result.data if result.data else []
        return jsonify({'success': True, 'orders': orders, 'count': len(orders)})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/api/stats', methods=['GET'])
def admin_get_stats():
    """📊 Obtener estadísticas del sistema - PRODUCCIÓN"""
    try:
        if not supabase_client:
            return jsonify({'success': False, 'error': 'Supabase no configurado'}), 500
        
        # Contar órdenes por estado
        orders_result = supabase_client.table('orders').select('order_status').execute()
        orders = orders_result.data if orders_result.data else []
        
        # Contar usuarios activos
        users_result = supabase_client.table('users').select('id').execute()
        users_count = len(users_result.data) if users_result.data else 0
        
        # Calcular estadísticas
        stats = {
            'total_orders': len(orders),
            'total_users': users_count,
            'orders_by_status': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Agrupar por estado
        for order in orders:
            status = order.get('order_status', 'unknown')
            stats['orders_by_status'][status] = stats['orders_by_status'].get(status, 0) + 1
        
        return jsonify({'success': True, 'stats': stats})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    print(f"🚀 INICIANDO CUBALINK23 SYSTEM BACKEND EN PUERTO {PORT}")
    print("🌐 PRODUCCIÓN - Listo para Render.com")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False,
        threaded=True
    )
