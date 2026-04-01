from typing import Generic, TypeVar, Optional
from dataclasses import dataclass


T = TypeVar('T')


@dataclass(frozen=True)
class ErrorViewModel:

    message: str
    code: str


@dataclass
class OperationResult(Generic[T]):
    
    _success: Optional[T] = None
    _error: Optional[ErrorViewModel] = None

    def __init__(self, success: Optional[T] = None, error: Optional[ErrorViewModel] = None):
        if (success is not None and error is not None) or (success is None and error is None):
            raise ValueError("Success and error cannot be set at the same time")
        self._success = success
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._success is not None
    
    @property
    def success(self) -> T:
        if self._success is None:
            raise ValueError("Cannot access success value if operation failed")
        return self._success
    
    @property
    def error(self) -> ErrorViewModel:
        if self._error is None:
            raise ValueError("Cannot access error value if operation succeeded")
        return self._error
    
    @classmethod
    def success(cls, value: T) -> 'OperationResult[T]':
        return cls(success=value)
    
    @classmethod
    def failure(cls, message: str, code: str) -> 'OperationResult[T]':
        return cls(error=ErrorViewModel(message=message, code=code))