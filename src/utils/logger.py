import csv
import os
from datetime import datetime
import logging

class AttendanceLogger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.logger = logging.getLogger(__name__)

    def log_attendance(self, name):
        """Logs attendance for a person on current date if not already logged today."""
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_dir, f"{current_date}.csv")
        current_time = now.strftime("%H:%M:%S")

        # Check if already logged today
        if self._is_already_logged(log_file, name):
            self.logger.info(f"{name} already logged for today.")
            return False

        try:
            with open(log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, current_time])
            self.logger.info(f"Attendance logged: {name} at {current_time}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to log attendance: {str(e)}")
            return False

    def _is_already_logged(self, log_file, name):
        """Helper to check for duplicate logs in the daily CSV."""
        if not os.path.exists(log_file):
            return False
        
        try:
            with open(log_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) > 0 and row[0] == name:
                        return True
        except Exception as e:
            self.logger.error(f"Failed to check log file: {str(e)}")
        return False
