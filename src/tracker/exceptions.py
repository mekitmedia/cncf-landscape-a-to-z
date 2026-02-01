"""Custom exceptions for the tracker package."""


class TrackerError(Exception):
    """Base exception for tracker-related errors."""
    pass


class DependencyNotMetError(TrackerError):
    """Raised when task dependencies are not satisfied."""
    pass


class InvalidTaskTypeError(TrackerError):
    """Raised when an invalid task type is referenced."""
    pass


class ItemNotFoundError(TrackerError):
    """Raised when an item is not found in the tracker."""
    pass


class WeekNotFoundError(TrackerError):
    """Raised when a week's tracker data is not found."""
    pass
