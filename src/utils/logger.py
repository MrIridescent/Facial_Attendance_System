import csv
import os
from datetime import datetime, timedelta
import logging
from typing import Dict, Optional

class AttendanceLogger:
    """
    Revolutionary Attendance Logger with cooldown management, 
    session persistence, and enhanced integrity.
    """
    def __init__(self, log_dir: str, cooldown_minutes: int = 30):
        self.log_dir = log_dir
        self.cooldown_minutes = cooldown_minutes
        self.logger = logging.getLogger(__name__)
        
        # In-memory cache for recent logs to handle cooldowns efficiently
        # Format: {name: last_log_datetime}
        self._recent_logs: Dict[str, datetime] = {}
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            self.logger.info(f"Created log directory: {self.log_dir}")

    def log_attendance(self, name: str) -> bool:
        """
        Logs attendance for a person with smart cooldown management.
        Prevents multiple logs for the same person within the cooldown period.
        """
        now = datetime.now()
        
        # 1. Check in-memory cooldown cache first (High Performance)
        if name in self._recent_logs:
            last_log_time = self._recent_logs[name]
            if now - last_log_time < timedelta(minutes=self.cooldown_minutes):
                # Still in cooldown
                return False

        # 2. Check file-based log (Persistence/Crash Recovery)
        current_date = now.strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_dir, f"{current_date}.csv")
        
        if self._is_already_logged_recently(log_file, name, now):
            # Update cache if it was missing but exists in file
            self._recent_logs[name] = now # Approximate
            return False

        # 3. Perform the log
        current_time = now.strftime("%H:%M:%S")
        try:
            file_exists = os.path.isfile(log_file)
            with open(log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                # Add headers for a new file
                if not file_exists:
                    writer.writerow(["Name", "Timestamp", "Status"])
                
                writer.writerow([name, current_time, "Present"])
            
            # Update cache
            self._recent_logs[name] = now
            self.logger.info(f"Attendance Verified: {name} at {current_time}")
            return True
        except Exception as e:
            self.logger.error(f"Integrity Error - Failed to log attendance for {name}: {str(e)}")
            return False

    def _is_already_logged_recently(self, log_file: str, name: str, now: datetime) -> bool:
        """Helper to check for recent logs in the daily CSV with timestamp awareness."""
        if not os.path.exists(log_file):
            return False
        
        try:
            with open(log_file, 'r') as f:
                reader = csv.DictReader(f)
                # Scan from end or check all for now (files are small/daily)
                for row in reader:
                    if row.get("Name") == name:
                        # Parse time to check if it's within the cooldown (revolutionary logic)
                        try:
                            log_time_str = row.get("Timestamp")
                            log_time = datetime.strptime(log_time_str, "%H:%M:%S")
                            # Combine with current date for comparison
                            full_log_dt = datetime.combine(now.date(), log_time.time())
                            
                            if now - full_log_dt < timedelta(minutes=self.cooldown_minutes):
                                return True
                        except (ValueError, TypeError):
                            # Fallback to simple name check if time parsing fails
                            return True
        except Exception as e:
            self.logger.error(f"File System Error - Failed to check log integrity: {str(e)}")
        return False

    def clear_cache(self):
        """Manually clear the cooldown cache."""
        self._recent_logs.clear()
        self.logger.info("Cooldown cache cleared.")
