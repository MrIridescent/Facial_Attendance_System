import cv2
import os
import logging
import time
from datetime import datetime
from engine.face_engine import FaceRecognitionEngine
from utils.logger import AttendanceLogger

# Configure global logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UIConstants:
    """UI styling constants for the revolutionary interface."""
    COLOR_PRIMARY = (255, 200, 0)      # Cyan/Blue
    COLOR_ACCENT = (0, 255, 0)       # Green for success
    COLOR_DANGER = (0, 0, 255)       # Red for unknown/error
    COLOR_TEXT = (255, 255, 255)     # White
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6
    THICKNESS = 2

def draw_overlay(frame, fps, count):
    """Draws a professional status overlay on the frame."""
    # Semi-transparent header
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Status Info
    status_text = f"FPS: {fps:.1f} | Active Faces: {count} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    cv2.putText(frame, status_text, (10, 25), UIConstants.FONT, UIConstants.FONT_SCALE, UIConstants.COLOR_TEXT, 1)

def main():
    """Main execution point for the Revolutionary Facial Attendance System."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KNOWN_FACES_DIR = os.path.join(BASE_DIR, 'data/known_faces')
    LOG_DIR = os.path.join(BASE_DIR, 'data/logs')

    # Initialize Engine and Logger
    engine = FaceRecognitionEngine(KNOWN_FACES_DIR)
    engine.load_known_faces()
    attendance_logger = AttendanceLogger(LOG_DIR)

    # Start Video Capture (Webcam) with high resolution if possible
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not video_capture.isOpened():
        logger.error("Could not open video source.")
        return

    logger.info("Renaissance 2.0 System active. Press 'q' to exit.")
    
    fps_time = time.time()
    fps = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            logger.error("Failed to capture video frame.")
            break

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - fps_time)
        fps_time = current_time

        # Recognize faces
        face_locations, face_names = engine.recognize_faces(frame)

        # Draw results on the frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up (processing was done on 1/4 size)
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            
            # Choose color based on recognition status
            color = UIConstants.COLOR_ACCENT if name != "Unknown" else UIConstants.COLOR_DANGER
            
            # Elegant Cornered Box
            length = 30
            # Top-Left
            cv2.line(frame, (left, top), (left + length, top), color, UIConstants.THICKNESS)
            cv2.line(frame, (left, top), (left, top + length), color, UIConstants.THICKNESS)
            # Top-Right
            cv2.line(frame, (right, top), (right - length, top), color, UIConstants.THICKNESS)
            cv2.line(frame, (right, top), (right, top + length), color, UIConstants.THICKNESS)
            # Bottom-Left
            cv2.line(frame, (left, bottom), (left + length, bottom), color, UIConstants.THICKNESS)
            cv2.line(frame, (left, bottom), (left, bottom - length), color, UIConstants.THICKNESS)
            # Bottom-Right
            cv2.line(frame, (right, bottom), (right - length, bottom), color, UIConstants.THICKNESS)
            cv2.line(frame, (right, bottom), (right, bottom - length), color, UIConstants.THICKNESS)

            # Modern Label
            label_y = top - 10 if top - 10 > 10 else bottom + 25
            cv2.putText(frame, name, (left, label_y), UIConstants.FONT, UIConstants.FONT_SCALE + 0.2, color, 2)

            # Log attendance for recognized individuals
            if name != "Unknown":
                attendance_logger.log_attendance(name)

        # Apply Global Overlay
        draw_overlay(frame, fps, len(face_names))

        # Display with high-quality rendering
        cv2.imshow('Renaissance 2.0 - Facial Attendance System', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    logger.info("Renaissance 2.0 safely terminated.")

if __name__ == "__main__":
    main()
