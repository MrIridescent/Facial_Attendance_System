import face_recognition
import cv2
import numpy as np
import os
import logging

class FaceRecognitionEngine:
    def __init__(self, known_faces_dir):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_faces_dir = known_faces_dir
        self.logger = logging.getLogger(__name__)

    def load_known_faces(self):
        """Loads and encodes faces from the specified directory."""
        if not os.path.exists(self.known_faces_dir):
            self.logger.error(f"Directory {self.known_faces_dir} not found.")
            return

        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(self.known_faces_dir, filename)
                try:
                    image = face_recognition.load_image_file(path)
                    encoding = face_recognition.face_encodings(image)[0]
                    self.known_face_encodings.append(encoding)
                    # Use filename without extension as name
                    name = os.path.splitext(filename)[0].replace('_', ' ')
                    self.known_face_names.append(name)
                    self.logger.info(f"Loaded and encoded: {name}")
                except Exception as e:
                    self.logger.error(f"Failed to load {filename}: {str(e)}")

    def recognize_faces(self, frame):
        """Detects and recognizes faces in a given frame."""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert BGR (OpenCV) to RGB (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Use face distance to find the best match
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            
            face_names.append(name)
        
        return face_locations, face_names
