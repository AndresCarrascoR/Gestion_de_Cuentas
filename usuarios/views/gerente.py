from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from usuarios.permissions import IsManager, IsAdmin
from facturas.models import FacturaCliente, FacturaProveedor
from django.db.models import Sum
from datetime import datetime, timedelta
import pandas as pd
from django.http import HttpResponse
import openpyxl
from io import BytesIO
from xhtml2pdf import pisa

class DashboardView(APIView):
    """
    Vista para obtener las métricas del dashboard contable.
    Accesible para gerentes y administradores.
    """
    permission_classes = [IsAuthenticated, IsAdmin | IsManager]

    def get(self, request):
        total_por_cobrar = FacturaCliente.objects.filter(estado='pendiente').aggregate(Sum('monto_total'))['monto_total__sum'] or 0
        total_por_pagar = FacturaProveedor.objects.filter(estado='pendiente').aggregate(Sum('monto_total'))['monto_total__sum'] or 0

        facturas_vencidas = {
            "clientes": FacturaCliente.objects.filter(estado='vencida').count(),
            "proveedores": FacturaProveedor.objects.filter(estado='vencida').count(),
        }

        proyecciones_flujo_caja = self.get_proyeccion_flujo_caja()

        return Response({
            "total_por_cobrar": total_por_cobrar,
            "total_por_pagar": total_por_pagar,
            "facturas_vencidas": facturas_vencidas,
            "proyecciones_flujo_caja": proyecciones_flujo_caja,
        })

    def get_proyeccion_flujo_caja(self):
        hoy = datetime.now().date()
        proyecciones = {}
        for i in range(1, 4):  # Proyección a 3 meses
            inicio_mes = (hoy + timedelta(days=(i * 30))).replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=30)) - timedelta(days=1)

            total_mes = FacturaCliente.objects.filter(
                fecha_vencimiento__range=[inicio_mes, fin_mes]
            ).aggregate(Sum('monto_total'))['monto_total__sum'] or 0

            proyecciones[f"{inicio_mes.strftime('%B %Y')}"] = total_mes

        return proyecciones


class ExportarDatosView(APIView):
    """
    Exporta los datos a Excel o PDF.
    Accesible para gerentes y administradores.
    """
    permission_classes = [IsAuthenticated, IsAdmin | IsManager]

    def get(self, request, formato):
        facturas = FacturaCliente.objects.all().values(
            'numero_factura', 'cliente__nombre', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'estado'
        )

        if formato == 'excel':
            return self.exportar_excel(facturas)
        elif formato == 'pdf':
            return self.exportar_pdf(facturas)
        else:
            return Response({"error": "Formato no válido"}, status=400)

    def exportar_excel(self, facturas):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Facturas"

        # Encabezados
        headers = ['Número', 'Cliente', 'Fecha Emisión', 'Fecha Vencimiento', 'Monto', 'Estado']
        ws.append(headers)

        # Datos
        for factura in facturas:
            ws.append(list(factura.values()))

        # Guardar el archivo en memoria
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        # Respuesta HTTP
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="facturas.xlsx"'
        return response

    def exportar_pdf(self, facturas):
        html = "<h1>Facturas</h1><table border='1'><tr><th>Número</th><th>Cliente</th><th>Fecha Emisión</th><th>Fecha Vencimiento</th><th>Monto</th><th>Estado</th></tr>"
        for factura in facturas:
            html += f"<tr><td>{factura['numero_factura']}</td><td>{factura['cliente__nombre']}</td><td>{factura['fecha_emision']}</td><td>{factura['fecha_vencimiento']}</td><td>{factura['monto_total']}</td><td>{factura['estado']}</td></tr>"
        html += "</table>"

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="facturas.pdf"'
        pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=response)

        if pisa_status.err:
            return Response({"error": "Error generando PDF"}, status=500)
        return response


class ImportarFacturasView(APIView):
    """
    Importa facturas desde un archivo CSV o Excel.
    Accesible para gerentes y administradores.
    """
    permission_classes = [IsAuthenticated, IsAdmin | IsManager]

    def post(self, request):
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({"error": "No se ha enviado un archivo"}, status=400)

        try:
            if archivo.name.endswith('.csv'):
                df = pd.read_csv(archivo)
            elif archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo)
            else:
                return Response({"error": "Formato de archivo no válido"}, status=400)

            for _, row in df.iterrows():
                FacturaCliente.objects.create(
                    numero_factura=row['numero_factura'],
                    cliente_id=row['cliente_id'],
                    fecha_emision=row['fecha_emision'],
                    fecha_vencimiento=row['fecha_vencimiento'],
                    monto_total=row['monto_total'],
                    estado=row['estado']
                )
            return Response({"mensaje": "Facturas importadas correctamente"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
