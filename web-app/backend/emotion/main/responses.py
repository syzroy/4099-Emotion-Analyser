from .config import OK


# The class for error responses
class Error:
    def __init__(self, status, message):
        self.status = status
        self.message = message


# The class for success upload responses
class Success:
    def __init__(self, job_id):
        self.status = OK
        self.id = job_id


# The class for frame paths
class Frames:
    def __init__(self, csv_path, frames):
        self.status = OK
        self.csv_path = csv_path
        self.frames = frames
