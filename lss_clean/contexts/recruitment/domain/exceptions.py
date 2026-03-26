class DomainError(Exception):
    """Base exception for all domain errors."""
    ...


class ValidationError(DomainError):
    """Exception raised when validation rules are violated."""
    ...


class BusinessRuleViolation(DomainError):
    """Exception raised when business rules are violated."""
    ...


class NotFoundError(DomainError):
    """Exception raised when a resource is not found."""
    ...