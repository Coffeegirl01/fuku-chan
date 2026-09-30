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
"""Dimension calculation functions for Fuku-chan.

Each function implements one R_i equation from README.md.
All functions return values clamped to [0, 1].
"""

from engine.core.calculator import clamp


def calculate_r1_speed(
    distance: float,
    time_norm: float,
    v_limit: float,
    v_gen_target: float,
    v_gen_current: float,
    same_era: bool = True,
) -> float:
    """
    R1: Adjusted Speed
    Formula from README.md:
        R1 = clamp((D / (T_norm * V_limit)) * [delta + (1-delta) * V_gen(Y_t) / V_gen(Y_c)], 0, 1)
    """
    if distance <= 0 or time_norm <= 0 or v_limit <= 0:
        return 0.0
    if v_gen_current <= 0 or v_gen_target < 0:
        return 0.0

    delta = 1.0 if same_era else 0.0
    era_factor = delta + (1.0 - delta) * (v_gen_target / v_gen_current)

    result = (distance / (time_norm * v_limit)) * era_factor
    return clamp(result, 0.0, 1.0)


def calculate_r2_burst(
    burst_accel: float,
    accel_ref: float,
    time_3f: float,
    time_3f_best: float,
    gamma_drag: float = 0.1,
) -> float:
    """
    R2: Burst Acceleration
    Formula from README.md:
        R2 = clamp((a_burst / a_ref) * [1 - gamma_drag * ((T_3F - T_3F_best) / T_3F_best)], 0, 1)
    """
    if accel_ref <= 0 or time_3f_best <= 0:
        return 0.0
    if burst_accel < 0:
        return 0.0

    drag_penalty = 1.0 - gamma_drag * ((time_3f - time_3f_best) / time_3f_best)
    result = (burst_accel / accel_ref) * drag_penalty
    return clamp(result, 0.0, 1.0)


def calculate_r3_stamina(
    energy_consumed: float,
    glycogen: float,
    energy_capacity: float,
) -> float:
    """
    R3: Base Stamina — Quadratic Pace Tax
    Formula from README.md:
        R3 = clamp(1 - max(0, E_consumed - E_glycogen) / E_capacity, 0, 1)
    """
    if energy_capacity <= 0:
        return 0.0
    if glycogen < 0:
        glycogen = 0.0

    excess = max(0.0, energy_consumed - glycogen)
    result = 1.0 - (excess / energy_capacity)
    return clamp(result, 0.0, 1.0)


def calculate_r4_guts(
    duel_strength: float,
    duel_force: float,
) -> float:
    """
    R4: Guts / Resilience
    Formula from README.md:
        R4 = clamp(S_duel * sqrt(F_duel), 0, 1)
    """
    if duel_force < 0 or duel_strength < 0:
        return 0.0

    result = duel_strength * (duel_force ** 0.5)
    return clamp(result, 0.0, 1.0)


def calculate_r5_conditioning(
    cr3: float,
    alpha: float,
    sigma_rank: float,
    beta: float,
    avg_abs_delta_wb: float,
) -> float:
    """
    R5: Conditioning
    Formula from README.md:
        R5 = clamp((CR3 / (1 + alpha * sigma_rank)) * exp[-beta * max(0, abs_delta_WB - 6)], 0, 1)
    """
    if cr3 < 0:
        return 0.0
    if alpha < 0:
        alpha = 0.0

    adjustment = (cr3 / (1.0 + alpha * sigma_rank))
    penalty = (-beta) * max(0.0, abs(avg_abs_delta_wb) - 6.0)
    result = adjustment * (2.718281828459045 ** penalty)
    return clamp(result, 0.0, 1.0)


def calculate_r6_race_iq(
    w_pos: float,
    lamda: float,
    position_gain_sum: float,
    m_total: float,
    w_tact: float,
    tactical_value: float,
) -> float:
    """
    R6: Race IQ and Positioning
    Formula from README.md:
        R6 = clamp(w_pos * [1 - lambda * (sum(max(0, C_{k+1} - C_k)) / M)] + w_tact * V_tactical, 0, 1)
    """
    if m_total <= 0:
        return 0.0

    positioning_term = 1.0 - lamda * (position_gain_sum / m_total)
    result = (w_pos * positioning_term) + (w_tact * tactical_value)
    return clamp(result, 0.0, 1.0)


def calculate_r7_track_adaptability(
    avg_v_heavy: float,
    avg_v_firm: float,
    alpha_water: float,
    water_index: float,
) -> float:
    """
    R7: Track Adaptability
    Formula from README.md:
        R7 = clamp(min(1, avg_v_heavy / avg_v_firm) * [1 - alpha_water * M_water], 0, 1)
    """
    if avg_v_firm <= 0:
        return 0.0

    ground_term = min(1.0, avg_v_heavy / avg_v_firm)
    result = ground_term * (1.0 - alpha_water * water_index)
    return clamp(result, 0.0, 1.0)


def calculate_r8_distance_fit(
    distance_target: float,
    distance_opt: float,
    sigma_d: float,
) -> float:
    """
    R8: Distance Fit
    Formula from README.md:
        R8 = exp(-((D_target - D_opt)^2) / (2 * sigma_D^2))
    """
    if sigma_d <= 0:
        return 0.0

    diff = (distance_target - distance_opt) ** 2
    result = (2.718281828459045 ** (-(diff / (2.0 * sigma_d ** 2))))
    return clamp(result, 0.0, 1.0)


def calculate_r9_weight_tolerance(
    weight_carried: float,
    weight_base: float,
    theta_base: float,
    eta_wt: float,
) -> float:
    """
    R9: Weight Tolerance
    Formula from README.md:
        R9 = clamp(1 - eta_wt * ((W_carried / WB) - theta_base), 0, 1)
    """
    if weight_base <= 0:
        return 0.0

    ratio = weight_carried / weight_base
    result = 1.0 - eta_wt * (ratio - theta_base)
    return clamp(result, 0.0, 1.0)


def calculate_r10_clutch(
    w_g1: float,
    s_g1: float,
    w_jock: float,
    cr3_pair: float,
    cr3_base: float,
) -> float:
    """
    R10: Clutch / Synergy
    Formula from README.md:
        R10 = clamp(w_G1 * S_G1 + w_jock * (CR3_pair / CR3_base), 0, 1)
    """
    if cr3_base <= 0:
        return 0.0

    pair_ratio = cr3_pair / cr3_base
    result = (w_g1 * s_g1) + (w_jock * pair_ratio)
    return clamp(result, 0.0, 1.0)
