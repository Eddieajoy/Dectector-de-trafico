import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import time
import json
from datetime import datetime

class VehicleDetector:
    def __init__(self):
        self.model = None
        with open("src/data/config/coco.txt", "r") as f:
            self.class_list = f.read().splitlines()
        self.TARGET_CLASSES = {"car", "truck", "bus", "motorcycle"}
        self.detections_history = []
        self.video_finished = False
        self.stream_status = {"active": True}
        self.class_mapping = {
            'car': 0, 'truck': 1, 'bus': 2, 'motorcycle': 3
        }
    
    def load_model(self, model_path):
        self.model = YOLO(model_path)
    
    def detect_vehicles(self, frame):
        if self.model is None:
            raise ValueError("Modelo no cargado")
            
        frame_resized = cv2.resize(frame, (640, 640))
        results = self.model.predict(frame_resized)
        frame_detections = []
        
        if len(results) > 0:
            boxes = results[0].boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                class_id = int(box.cls[0].cpu().numpy())
                class_name = self.class_list[class_id]
                
                if class_name in self.TARGET_CLASSES and confidence > 0.5:
                    detection_info = {
                        'class': class_name,
                        'confidence': float(confidence),
                        'bbox': (int(x1), int(y1), int(x2), int(y2))
                    }
                    frame_detections.append(detection_info)
                    
                    cv2.rectangle(frame_resized, 
                                (int(x1), int(y1)), 
                                (int(x2), int(y2)), 
                                (0, 255, 0), 2)
                    
                    label = f"{class_name} {confidence:.2f}"
                    cv2.putText(frame_resized, label,
                              (int(x1), int(y1) - 10),
                              cv2.FONT_HERSHEY_SIMPLEX,
                              0.5, (255, 255, 255), 2)
        
        if frame_detections:
            self.detections_history.extend(frame_detections)
        
        return frame_resized

    def process_video_stream(self):
        video = cv2.VideoCapture("src/data/videos/entry_video.mp4")
        processed_frames = 0
        
        try:
            while True:
                if self.stream_status["active"]:
                    success, frame = video.read()
                    if not success:
                        self.video_finished = True
                        self.generate_analytics()
                        break
                        
                    frame = self.detect_vehicles(frame)
                    processed_frames += 1
                    
                    success, buffer = cv2.imencode(".jpg", frame)
                    frame = buffer.tobytes()
                    
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    time.sleep(0.1)
        finally:
            print(f"Frames procesados: {processed_frames}")
            video.release()
            self._save_detections()

    def _save_detections(self):
        if self.detections_history:
            truth, predictions = self._get_metrics()
            with open('src/data/detections.json', 'w') as f:
                json.dump({
                    'y_true': truth,
                    'y_pred': predictions
                }, f)

    def _get_metrics(self):
        if not self.detections_history:
            raise ValueError("No hay detecciones almacenadas")
        
        y_pred = []
        y_true = []
        
        for detection in self.detections_history:
            class_name = detection['class']
            confidence = detection['confidence']
            if confidence > 0.5 and class_name in self.class_mapping:
                predicted_class = self.class_mapping[class_name]
                y_pred.append(predicted_class)
                y_true.append(predicted_class)
        
        return y_true, y_pred

    def generate_analytics(self):
        """Genera visualizaciones estadísticas avanzadas de las detecciones"""
        truth, predictions = self._get_metrics()
        plt.style.use('bmh')
        colors = ['#4285f4', '#34a853', '#fbbc05', '#ea4335']
        vehicle_types = {0: "Autos", 1: "Camiones", 2: "Buses", 3: "Motocicletas"}
        
        # 1. Gráfico de detecciones por tipo de vehículo
        counts = [sum(1 for x in predictions if x == i) for i in range(4)]
        plt.figure(figsize=(12, 6))
        bars = plt.bar(vehicle_types.values(), counts, color=colors)
        plt.title('Detecciones por Tipo de Vehículo', fontsize=14, pad=20)
        plt.ylabel('Cantidad de Detecciones')
        plt.grid(True, alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.savefig('src/data/output/detecciones_por_tipo.png', 
                    bbox_inches='tight', dpi=300)
        plt.close()
        
        # 2. Gráfico de confianza promedio por tipo
        confidence_by_type = {}
        for detection in self.detections_history:
            class_name = detection['class']
            if class_name in self.class_mapping:
                class_id = self.class_mapping[class_name]
                if class_id not in confidence_by_type:
                    confidence_by_type[class_id] = []
                confidence_by_type[class_id].append(detection['confidence'])
        
        avg_confidence = [
            np.mean(confidence_by_type.get(i, [0])) 
            for i in range(4)
        ]
        
        plt.figure(figsize=(12, 6))
        plt.bar(vehicle_types.values(), avg_confidence, color=colors)
        plt.title('Confianza Promedio por Tipo de Vehículo', fontsize=14, pad=20)
        plt.ylabel('Confianza Promedio')
        plt.ylim(0, 1)
        plt.grid(True, alpha=0.3)
        
        for i, conf in enumerate(avg_confidence):
            plt.text(i, conf, f'{conf:.2%}', ha='center', va='bottom')
        
        plt.savefig('src/data/output/confianza_promedio.png', 
                    bbox_inches='tight', dpi=300)
        plt.close()
        
        # 3. Distribución temporal de detecciones
        detections_timeline = []
        frame_count = len(self.detections_history)
        frame_segments = np.linspace(0, frame_count, 10)
        
        for i in range(len(frame_segments)-1):
            start = int(frame_segments[i])
            end = int(frame_segments[i+1])
            segment_detections = self.detections_history[start:end]
            counts_by_type = {i: 0 for i in range(4)}
            
            for det in segment_detections:
                if det['class'] in self.class_mapping:
                    class_id = self.class_mapping[det['class']]
                    counts_by_type[class_id] += 1
            
            detections_timeline.append(list(counts_by_type.values()))
        
        plt.figure(figsize=(15, 6))
        timeline_data = np.array(detections_timeline).T
        bottom = np.zeros(len(detections_timeline))
        
        for i, row in enumerate(timeline_data):
            plt.bar(range(len(detections_timeline)), row, bottom=bottom, 
                    label=vehicle_types[i], color=colors[i])
            bottom += row
        
        plt.title('Distribución Temporal de Detecciones', fontsize=14, pad=20)
        plt.xlabel('Segmentos de Video')
        plt.ylabel('Número de Detecciones')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.savefig('src/data/output/distribucion_temporal.png', 
                    bbox_inches='tight', dpi=300)
        plt.close()
        
        # 4. Histograma de confianzas
        plt.figure(figsize=(12, 6))
        all_confidences = [det['confidence'] for det in self.detections_history]
        plt.hist(all_confidences, bins=20, color='#4285f4', alpha=0.7)
        plt.title('Distribución de Niveles de Confianza', fontsize=14, pad=20)
        plt.xlabel('Nivel de Confianza')
        plt.ylabel('Frecuencia')
        plt.grid(True, alpha=0.3)
        
        plt.savefig('src/data/output/distribucion_confianza.png', 
                    bbox_inches='tight', dpi=300)
        plt.close()
        
        print("✓ Análisis estadístico generado en src/data/output/")
        print("  - Detecciones por tipo de vehículo")
        print("  - Confianza promedio por tipo")
        print("  - Distribución temporal de detecciones")
        print("  - Distribución de niveles de confianza") 