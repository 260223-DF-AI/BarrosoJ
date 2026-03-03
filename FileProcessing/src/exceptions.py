class FileProcessingError(Exception):
    """Base exception for file processing errors."""
    pass

class InvalidDataError(FileProcessingError):
    """Raised when data validation fails."""
    pass

class MissingFieldError(FileProcessingError):
    """Raised when a required field is missing."""
    pass