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
    """R1: Adjusted Speed."""
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
    """R2: Burst Acceleration."""
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
    """R3: Base Stamina."""
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
    """R4: Guts / Resilience."""
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
    """R5: Conditioning."""
    if cr3 < 0:
        return 0.0
    if alpha < 0:
        alpha = 0.0

    adjustment = cr3 / (1.0 + alpha * sigma_rank)
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
    """R6: Race IQ and Positioning."""
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
    """R7: Track Adaptability."""
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
    """R8: Distance Fit."""
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
    """R9: Weight Tolerance."""
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
    """R10: Clutch / Synergy."""
    if cr3_base <= 0:
        return 0.0

    pair_ratio = cr3_pair / cr3_base
    result = (w_g1 * s_g1) + (w_jock * pair_ratio)
    return clamp(result, 0.0, 1.0)
