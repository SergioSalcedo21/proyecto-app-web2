import io
import csv

from django.contrib import admin, messages
from django import forms
from django.shortcuts import render, redirect
from django.urls import path

from .models import Producto, Pedido


admin.site.site_header = "ADMINISTRACIÓN CAFETERÍA SERGIO"
admin.site.site_title = "Panel cafe Sergio"
admin.site.index_title = "Control de operaciones"


# Formulario para importar archivos CSV
class CsvImportForm(forms.Form):
    csv_file = forms.FileField(label="Selecciona un archivo CSV")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = ('id', 'nombre', 'precio', 'categoria', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)

    change_list_template = "admin/productos_list.html"

    # IMPORTANTE: este método está DENTRO de ProductoAdmin
    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                'importar-csv/',
                self.admin_site.admin_view(self.importar_csv),
                name='pedidos_producto_importar_csv',
            ),
        ]

        return custom_urls + urls

    # IMPORTANTE: este método también está DENTRO de ProductoAdmin
    def importar_csv(self, request):
        """Vista para realizar la importación masiva de productos."""

        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)

            if form.is_valid():
                csv_file = request.FILES['csv_file']

                if not csv_file.name.endswith('.csv'):
                    messages.error(
                        request,
                        'El archivo debe tener extensión .csv'
                    )
                    return redirect('.')

                contenido = csv_file.read()

                try:
                    data_set = contenido.decode('utf-8-sig')
                except UnicodeDecodeError:
                    data_set = contenido.decode('cp1252')

                io_string = io.StringIO(data_set)
                next(io_string, None)  # Omitir encabezados

                contador = 0

                for row in csv.reader(io_string, delimiter=','):
                    if row:
                        Producto.objects.create(
                            nombre=row[0].strip(),
                            precio=row[1].strip(),
                            categoria=row[2].strip().upper(),
                        )
                        contador += 1

                messages.success(
                    request,
                    f'¡Se cargaron {contador} productos correctamente!'
                )

                return redirect('..')

        else:
            form = CsvImportForm()

        context = {
            'form': form,
            'title': 'Cargue Masivo de Productos (CSV)',
            'site_header': admin.site.site_header,
            'opts': self.model._meta,
            'add': True,
            'change': False,
        }

        return render(
            request,
            "admin/csv_form.html",
            context
        )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'cliente_nombre',
        'estado',
        'total',
        'fecha',
    )

    list_filter = ('estado', 'fecha')
    search_fields = ('cliente_nombre',)
