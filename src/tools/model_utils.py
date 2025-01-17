from ultralytics import YOLO
import os

def setup_model():
    """Configura el modelo YOLOv8 para detección de vehículos"""
    print("Iniciando configuración del modelo...")
    
    # Crear directorios necesarios
    os.makedirs('src/data/models', exist_ok=True)
    os.makedirs('src/data/videos', exist_ok=True)
    os.makedirs('src/data/output', exist_ok=True)
    
    try:
        print("Descargando modelo YOLOv8...")
        model = YOLO('yolov8s.pt')
        model_path = 'src/data/models/yolov8s.pt'
        model.save(model_path)
        print(f"✓ Modelo guardado en: {model_path}")
        return True
    except Exception as e:
        print(f"❌ Error al configurar el modelo: {e}")
        return False

def train_model():
    """Entrena el modelo con dataset personalizado"""
    try:
        model = YOLO('yolov8s.pt')
        results = model.train(
            data='src/data/config/data.yaml',
            epochs=100,
            imgsz=640,
            batch=16,
            name='vehicle_detection'
        )
        model.save('src/data/models/best.pt')
        print("✓ Modelo entrenado y guardado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al entrenar el modelo: {e}")
        return False

if __name__ == "__main__":
    action = input("¿Qué deseas hacer? (setup/train): ").lower()
    if action == 'setup':
        setup_model()
    elif action == 'train':
        train_model()
    else:
        print("Opción no válida. Usa 'setup' o 'train'") 