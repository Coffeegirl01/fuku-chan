"""Deterministic score calculation for Fuku-chan.

This module combines already-calculated R1-R10 dimensions with a surface-specific
weight profile and Omega multipliers. It intentionally does not fetch data or
make claims about race outcomes; callers are responsible for preparing and
validating the input data.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import prod
from typing import Mapping, Sequence


DIMENSION_COUNT = 10
MIN_SCORE = 0.0
MAX_SCORE = 1.0

# The values follow the weight matrix documented in README.md.
SURFACE_WEIGHTS: dict[str, tuple[float, ...]] = {
    "TURF": (0.15, 0.25, 0.15, 0.05, 0.05, 0.15, 0.15, 0.15, 0.05, 0.05),
    "DIRT": (0.25, 0.15, 0.20, 0.05, 0.05, 0.10, 0.20, 0.10, 0.05, 0.05),
}


@dataclass(frozen=True)
class CalculationResult:
    """A reproducible calculation result with inspectable intermediate values."""

    surface: str
    dimensions: tuple[float, ...]
    weights: tuple[float, ...]
    multipliers: tuple[float, ...]
    base_score: float
    final_score: float


def clamp(value: float, minimum: float = MIN_SCORE, maximum: float = MAX_SCORE) -> float:
    """Limit *value* to the inclusive interval [minimum, maximum]."""
    if minimum > maximum:
        raise ValueError("minimum must not be greater than maximum")
    return min(maximum, max(minimum, float(value)))


def validate_vector(values: Sequence[float], name: str) -> tuple[float, ...]:
    """Validate and clamp a ten-item dimension or multiplier vector."""
    if len(values) != DIMENSION_COUNT:
        raise ValueError(f"{name} must contain exactly {DIMENSION_COUNT} values")

    result = tuple(float(value) for value in values)
    if any(not 0.0 <= value <= 1.0 for value in result):
        raise ValueError(f"{name} values must be between 0 and 1")
    return result


def validate_weights(weights: Sequence[float], tolerance: float = 1e-9) -> tuple[float, ...]:
    """Validate a ten-item weight vector whose values sum to one."""
    result = tuple(float(weight) for weight in weights)
    if len(result) != DIMENSION_COUNT:
        raise ValueError(f"weights must contain exactly {DIMENSION_COUNT} values")
    if any(weight < 0.0 for weight in result):
        raise ValueError("weights cannot be negative")
    if abs(sum(result) - 1.0) > tolerance:
        raise ValueError("weights must sum to 1.0")
    return result


def get_surface_weights(surface: str) -> tuple[float, ...]:
    """Return the validated weight profile for TURF or DIRT."""
    key = surface.strip().upper()
    try:
        return validate_weights(SURFACE_WEIGHTS[key], name="surface weights")
    except KeyError as exc:
        raise ValueError("surface must be either 'TURF' or 'DIRT'") from exc


def calculate_score(
    dimensions: Sequence[float],
    *,
    surface: str = "TURF",
    multipliers: Sequence[float] = (1.0, 1.0, 1.0, 1.0, 1.0),
    weights: Sequence[float] | None = None,
) -> CalculationResult:
    """Calculate P from R1-R10 and the Omega multipliers.

    ``dimensions`` and ``multipliers`` must already be normalized to [0, 1].
    Passing invalid values raises an error instead of silently hiding bad data.
    """
    normalized_dimensions = validate_vector(dimensions, "dimensions")
    normalized_multipliers = tuple(float(value) for value in multipliers)
    if not normalized_multipliers:
        raise ValueError("multipliers must contain at least one value")
    if any(not 0.0 <= value <= 1.0 for value in normalized_multipliers):
        raise ValueError("multipliers values must be between 0 and 1")

    normalized_weights = validate_weights(
        weights if weights is not None else get_surface_weights(surface),
        name="weights",
    )
    normalized_surface = surface.strip().upper()
    base_score = sum(dimension * weight for dimension, weight in zip(normalized_dimensions, normalized_weights))
    final_score = clamp(base_score * prod(normalized_multipliers))

    return CalculationResult(
        surface=normalized_surface,
        dimensions=normalized_dimensions,
        weights=normalized_weights,
        multipliers=normalized_multipliers,
        base_score=base_score,
        final_score=final_score,
    )
