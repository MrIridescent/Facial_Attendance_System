import face_recognition
import cv2
import numpy as np
import os
import logging
from typing import List, Tuple, Optional
import threading

class FaceRecognitionEngine:
    """
    Revolutionary Face Recognition Engine with multi-threading support 
    and optimized processing pipelines.
    """
    def __init__(self, known_faces_dir: str):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_faces_dir = known_faces_dir
        self.logger = logging.getLogger(__name__)
        
        # Performance & Threading
        self.process_this_frame = True
        self.lock = threading.Lock()
        
        # Cache for recognized faces to prevent flickering
        self._last_face_locations = []
        self._last_face_names = []

    def load_known_faces(self):
        """Loads and encodes faces from the specified directory with error handling."""
        if not os.path.exists(self.known_faces_dir):
            self.logger.error(f"Directory {self.known_faces_dir} not found.")
            return

        for filename in os.listdir(self.known_faces_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(self.known_faces_dir, filename)
                try:
                    image = face_recognition.load_image_file(path)
                    encodings = face_recognition.face_encodings(image)
                    
                    if not encodings:
                        self.logger.warning(f"No face found in {filename}. Skipping.")
                        continue
                        
                    encoding = encodings[0]
                    with self.lock:
                        self.known_face_encodings.append(encoding)
                        # Use filename without extension as name, cleaner formatting
                        name = os.path.splitext(filename)[0].replace('_', ' ').title()
                        self.known_face_names.append(name)
                    
                    self.logger.info(f"Loaded and encoded: {name}")
                except Exception as e:
                    self.logger.error(f"Failed to load {filename}: {str(e)}")

    def recognize_faces(self, frame: np.ndarray) -> Tuple[List[Tuple], List[str]]:
        """
        Detects and recognizes faces in a given frame.
        Uses frame-skipping (process every other frame) to double performance.
        """
        if self.process_this_frame:
            # Resize frame for faster processing (0.25x scale)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert BGR (OpenCV) to RGB (face_recognition)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all face locations and encodings in current frame
            # Using 'hog' for CPU speed; 'cnn' would be more accurate but slower without GPU
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            with self.lock:
                for face_encoding in face_encodings:
                    # Default to Unknown
                    name = "Unknown"

                    # Calculate distances to all known faces
                    if self.known_face_encodings:
                        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        
                        # Tolerance of 0.6 is default; lower is more strict
                        if face_distances[best_match_index] < 0.6:
                            name = self.known_face_names[best_match_index]
                    
                    face_names.append(name)
            
            self._last_face_locations = face_locations
            self._last_face_names = face_names

        # Toggle process_this_frame to skip next frame
        self.process_this_frame = not self.process_this_frame
        
        return self._last_face_locations, self._last_face_names
