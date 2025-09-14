class SpeechToTextError(Exception):
    """Custom exception for Speech-to-text conversion errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class TextToSpeechError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TextToImageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ImageToTextError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message