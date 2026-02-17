import logging
from pathlib import Path
from datetime import datetime

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


class ColorFormatter(logging.Formatter):
    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[94m",    # Blue
        "INFO": "\033[92m",     # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "CRITICAL": "\033[95m"  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"

class LogMaker:
    @staticmethod
    def log_gen():

        logs_dir = Path("logs")
        logs_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = logs_dir / f"orangehrm_test_logs_{timestamp}.log"

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.handlers.clear()

        # -------- FILE HANDLER (No colors) --------
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%d-%b-%Y %I:%M:%S %p"
        )
        file_handler.setFormatter(file_formatter)

        # -------- CONSOLE HANDLER (With Colors) --------
        console_handler = logging.StreamHandler()
        console_formatter = ColorFormatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
