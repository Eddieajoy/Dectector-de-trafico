from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import tempfile
import os

class PDFReport:
    def __init__(self, filename):
        self.pdf = FPDF()
        self.filename = filename
        self.colors = ['#4a90e2', '#27ae60', '#e74c3c', '#f39c12']
        
    def add_bar_chart(self, data, labels):
        plt.figure(figsize=(10, 5))
        bars = plt.bar(labels, data, color=self.colors)
        
        # Añadir valores sobre las barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.title('Detecciones por Tipo de Vehículo')
        plt.ylabel('Cantidad')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Guardar gráfico temporalmente
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            plt.savefig(tmp.name, format='png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Agregar al PDF
            self.pdf.image(tmp.name, x=10, w=190)
            
        os.unlink(tmp.name)
        
    def generate(self, y_true, y_pred):
        # Iniciar PDF
        self.pdf.add_page()
        
        # Título
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.cell(0, 20, 'Reporte de Detección de Vehículos', ln=True, align='C')
        
        # Fecha
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 10, f'Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True)
        
        # Separador
        self.pdf.ln(10)
        
        # Resumen de detecciones
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, 'Resumen de Detecciones:', ln=True)
        
        # Contar detecciones por tipo
        vehicles = {
            0: "Autos",
            1: "Camiones",
            2: "Buses",
            3: "Motocicletas"
        }
        
        self.pdf.set_font('Arial', '', 12)
        total_detections = len(y_pred)
        self.pdf.cell(0, 10, f'Total de detecciones: {total_detections}', ln=True)
        
        # Recolectar datos para el gráfico
        counts = []
        labels = []
        for vehicle_id, vehicle_name in vehicles.items():
            count = sum(1 for x in y_pred if x == vehicle_id)
            percentage = (count / total_detections * 100) if total_detections > 0 else 0
            self.pdf.cell(0, 10, f'{vehicle_name}: {count} ({percentage:.1f}%)', ln=True)
            counts.append(count)
            labels.append(vehicle_name)
        
        # Agregar espacio antes del gráfico
        self.pdf.ln(10)
        
        # Agregar gráfico
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, 'Gráfico de Detecciones:', ln=True)
        self.add_bar_chart(counts, labels)
        
        # Guardar PDF
        self.pdf.output(self.filename)
        print(f"Reporte generado: {self.filename}")