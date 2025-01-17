from flask import Blueprint, Response, jsonify, render_template
from src.services.processor import VehicleDetector

routes = Blueprint('routes', __name__, template_folder='../templates')
detector = VehicleDetector()
detector.load_model('src/data/models/yolov8s.pt')

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/video_feed')
def video_feed():
    return Response(
        detector.process_video_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@routes.route('/play', methods=['POST'])
def play():
    detector.stream_status["active"] = True
    return jsonify({"status": "success", "playing": True})

@routes.route('/pause', methods=['POST'])
def pause():
    detector.stream_status["active"] = False
    return jsonify({"status": "success", "playing": False})

@routes.route('/replay', methods=['POST'])
def replay():
    global detector
    detector = VehicleDetector()
    detector.load_model('src/data/models/yolov8s.pt')
    detector.stream_status["active"] = True
    return jsonify({"status": "success"})

@routes.route('/video_status')
def video_status():
    return jsonify({
        "finished": detector.video_finished,
        "playing": detector.stream_status["active"]
    })
