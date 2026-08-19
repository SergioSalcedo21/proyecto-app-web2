from django.contrib import admin
from .models import Producto, Pedido

admin.site.site_header = "ADMINISTRACIÓN CAFETERÍA SERGIO"
admin.site.site_title = "Panel cafe Sergio"
admin.site.index_title = "Control de operaciones"

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'estado', 'total', 'fecha')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente_nombre',)
