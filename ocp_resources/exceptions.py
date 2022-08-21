class PodNotRunningError(Exception):
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __str__(self):
        return f"{self.name} not running, current status: {self.status}"
