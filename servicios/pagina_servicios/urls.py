from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('redirect/<int:usuario_id>/',views.redireccion_rol, name='redireccion_rol'),
    path('reacciones/', views.reacciones, name='reacciones'),
    path('comentarios/', views.comentarios, name='comentarios'),
    path('reproducciones/', views.reproducciones, name='reproducciones'),
    path('envivo/', views.envivo, name='envivo'),
    path('compartidas/', views.compartidas, name='compartidas'),
    path('seguidores/', views.seguidores, name='seguidores'),
    path('votos/', views.votos, name='votos'),
    path('rt/', views.rt, name='rt'),
    path('likes/', views.likes, name='likes'),
    path('perfil/', views.perfil, name='perfil'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('check-logged-in/', views.check_logged_in, name='check_logged_in'),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', views.logout_view, name='logout'),
    
    path('servicios/reacciones', views.reacciones, name='reacciones'),
    path('servicios/comentarios/', views.comentarios, name='comentarios'),
    path('servicios/compartidas/', views.compartidas, name='compartidas'),
    path('servicios/reproducciones/', views.reproducciones, name='reproducciones'),
    path('servicios/seguidores/', views.seguidores, name='seguidores'),
    path('servicios/envivo/', views.envivo, name='envivo'),

    path('servicios/votos/', views.votos, name='votos'),
    path('servicios/retwitt/', views.rt, name='retwitt'),
    path('servicios/likes/', views.likes, name='likes'),

    path('calcular-costo/', views.calcular_costo, name='calcular_costo'),
    path('user-data/', views.user_data, name='user_data'),
    path('creditos-usuario/', views.creditos_usuario, name='creditos_usuario'),
    path('backend-cliente/', views.backend_cliente, name='backend_cliente'),
    path('payInfo/', views.payInfo, name='payInfo'),
    path('validateOperation/', views.validateOperation, name='validateOperation'),
    path('agregar-transaccion/', views.agregar_transaccion, name='agregar_transaccion'),
    path('crear_pago/', views.crear_pago, name='crear_pago'),
    path('obtener_datos/', views.obtener_datos, name='obtener_datos'),
    path('obtener_pool/', views.obtener_pool, name='obtener_pool'),
    path('actualizar_registro/', views.actualizar_registro, name='actualizar_registro'),
    path('actualizar_pool/', views.actualizar_pool, name='actualizar_pool'),
    

    #path('ruta-pago/', views.pagina_pago, name='ruta_a_la_pagina_de_pago'),

    # Asumiendo que tienes vistas para 'admin_dashboard' y 'user_dashboard'
    path('create-payment/', views.create_payment, name='create_payment'),

    
    
]