import cv2
import os
import logging
from engine.face_engine import FaceRecognitionEngine
from utils.logger import AttendanceLogger

# Configure global logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main execution point for the Facial Attendance System."""
    # Project paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KNOWN_FACES_DIR = os.path.join(BASE_DIR, 'data/known_faces')
    LOG_DIR = os.path.join(BASE_DIR, 'data/logs')

    # Initialize Engine and Logger
    engine = FaceRecognitionEngine(KNOWN_FACES_DIR)
    engine.load_known_faces()
    attendance_logger = AttendanceLogger(LOG_DIR)

    # Start Video Capture (Webcam)
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        logger.error("Could not open video source.")
        return

    logger.info("Facial Attendance System active. Press 'q' to exit.")

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            logger.error("Failed to capture video frame.")
            break

        # Recognize faces (logic now in engine)
        face_locations, face_names = engine.recognize_faces(frame)

        # Draw results on the frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up (processing was done on 1/4 size)
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

            # Log attendance for recognized individuals
            if name != "Unknown":
                attendance_logger.log_attendance(name)

        # Display the resulting image
        cv2.imshow('Facial Attendance System - S_STAR S.B', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    logger.info("System shutting down...")

if __name__ == "__main__":
    main()
