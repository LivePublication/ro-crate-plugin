import logging

class Logger():
    def __init__(self, name, log_file="app.log", level=logging.DEBUG):
        # Logger to help keep a trace of any events that occur.
        self.logger = logging.getLogger(name)
        logging.basicConfig(level=logging.DEBUG)

        # Remove all handlers associated with the root logger (which could output to the terminal)
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Create a file handler to write logs to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter and set it for the file handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        return self.logger
