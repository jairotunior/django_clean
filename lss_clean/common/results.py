from dataclasses import dataclass, field
from typing import Generic, TypeVar, Optional

from lss_clean.common.enums import ErrorCode


T = TypeVar('T')


@dataclass
class Error:
    message: str
    code: str
    details: dict[str, any] = field(default_factory=dict)

    @classmethod
    def not_found(cls, message: str) -> 'Error':
        return cls(message=message, code=ErrorCode.NOT_FOUND)

    @classmethod
    def validation_error(cls, message: str) -> 'Error':
        return cls(message=message, code=ErrorCode.VALIDATION_ERROR)

    @classmethod
    def business_rule_violation(cls, message: str) -> 'Error':
        return cls(message=message, code=ErrorCode.BUSINESS_RULE_VIOLATION)


@dataclass(frozen=True)
class Result(Generic[T]):

    _value: Optional[T] = None
    _error: Optional[Error] = None

    def __post_init__(self):
        if (self._value is None and self._error is None) or (self._value is not None and self._error is not None):
            raise ValueError("Value and error cannot be set at the same time")

    @property
    def is_success(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> T:
        if self._value is None:
            raise ValueError("Value is not set")
        return self._value

    @property
    def error(self) -> Error:
        if self._error is None:
            raise ValueError("Error is not set")
        return self._error

    @classmethod
    def success(cls, value: T) -> 'Result[T]':
        return cls(_value=value)

    @classmethod
    def failure(cls, error: Error) -> 'Result[T]':
        return cls(_error=error)