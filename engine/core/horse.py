"""Horse data model and R-score calculation.

This module defines the Horse dataclass and methods to compute R1–R10 scores
from raw horse performance data. Horses are populated from race history or
external data sources, then passed to the score calculator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from engine.core.dimensions import (
    calculate_r1_speed,
    calculate_r2_burst,
    calculate_r3_stamina,
    calculate_r4_guts,
    calculate_r5_conditioning,
    calculate_r6_race_iq,
    calculate_r7_track_adaptability,
    calculate_r8_distance_fit,
    calculate_r9_weight_tolerance,
    calculate_r10_clutch,
)


@dataclass
class Horse:
    """A horse with calculated performance metrics for racing."""

    # Basic identification
    name: str
    country: str
    age: int
    sex: str
    weight: float

    # R1: Speed factors
    distance: float = 0.0
    time_norm: float = 0.0
    v_limit: float = 1.0
    v_gen_target: float = 1.0
    v_gen_current: float = 1.0
    same_era: bool = True

    # R2: Burst acceleration
    burst_accel: float = 0.0
    accel_ref: float = 1.0
    time_3f: float = 0.0
    time_3f_best: float = 1.0
    gamma_drag: float = 0.1

    # R3: Stamina
    energy_consumed: float = 0.0
    glycogen: float = 100.0
    energy_capacity: float = 100.0

    # R4: Guts / Resilience
    duel_strength: float = 0.5
    duel_force: float = 0.5

    # R5: Conditioning
    cr3: float = 0.5
    alpha: float = 0.1
    sigma_rank: float = 0.5
    beta: float = 0.05
    avg_abs_delta_wb: float = 0.0

    # R6: Race IQ and positioning
    w_pos: float = 0.5
    lamda: float = 0.1
    position_gain_sum: float = 0.0
    m_total: float = 1.0
    w_tact: float = 0.5
    tactical_value: float = 0.5

    # R7: Track adaptability
    avg_v_heavy: float = 1.0
    avg_v_firm: float = 1.0
    alpha_water: float = 0.1
    water_index: float = 0.0

    # R8: Distance fit
    distance_target: float = 0.0
    distance_opt: float = 2000.0
    sigma_d: float = 500.0

    # R9: Weight tolerance
    weight_carried: float = 0.0
    weight_base: float = 1.0
    theta_base: float = 1.0
    eta_wt: float = 0.1

    # R10: Clutch / Synergy
    w_g1: float = 0.5
    s_g1: float = 0.5
    w_jock: float = 0.5
    cr3_pair: float = 0.5
    cr3_base: float = 1.0

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_r_scores(self) -> tuple[float, ...]:
        """Calculate R1–R10 from this horse's raw race data."""
        r1 = calculate_r1_speed(
            distance=self.distance,
            time_norm=self.time_norm,
            v_limit=self.v_limit,
            v_gen_target=self.v_gen_target,
            v_gen_current=self.v_gen_current,
            same_era=self.same_era,
        )

        r2 = calculate_r2_burst(
            burst_accel=self.burst_accel,
            accel_ref=self.accel_ref,
            time_3f=self.time_3f,
            time_3f_best=self.time_3f_best,
            gamma_drag=self.gamma_drag,
        )

        r3 = calculate_r3_stamina(
            energy_consumed=self.energy_consumed,
            glycogen=self.glycogen,
            energy_capacity=self.energy_capacity,
        )

        r4 = calculate_r4_guts(
            duel_strength=self.duel_strength,
            duel_force=self.duel_force,
        )

        r5 = calculate_r5_conditioning(
            cr3=self.cr3,
            alpha=self.alpha,
            sigma_rank=self.sigma_rank,
            beta=self.beta,
            avg_abs_delta_wb=self.avg_abs_delta_wb,
        )

        r6 = calculate_r6_race_iq(
            w_pos=self.w_pos,
            lamda=self.lamda,
            position_gain_sum=self.position_gain_sum,
            m_total=self.m_total,
            w_tact=self.w_tact,
            tactical_value=self.tactical_value,
        )

        r7 = calculate_r7_track_adaptability(
            avg_v_heavy=self.avg_v_heavy,
            avg_v_firm=self.avg_v_firm,
            alpha_water=self.alpha_water,
            water_index=self.water_index,
        )

        r8 = calculate_r8_distance_fit(
            distance_target=self.distance_target,
            distance_opt=self.distance_opt,
            sigma_d=self.sigma_d,
        )

        r9 = calculate_r9_weight_tolerance(
            weight_carried=self.weight_carried,
            weight_base=self.weight_base,
            theta_base=self.theta_base,
            eta_wt=self.eta_wt,
        )

        r10 = calculate_r10_clutch(
            w_g1=self.w_g1,
            s_g1=self.s_g1,
            w_jock=self.w_jock,
            cr3_pair=self.cr3_pair,
            cr3_base=self.cr3_base,
        )

        return (r1, r2, r3, r4, r5, r6, r7, r8, r9, r10)

    def to_dict(self) -> Dict[str, Any]:
        """Return basic horse info as a dictionary."""
        return {
            "name": self.name,
            "country": self.country,
            "age": self.age,
            "sex": self.sex,
            "weight": self.weight,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return f"Horse(name={self.name!r}, country={self.country!r}, age={self.age})"


__all__ = ["Horse"]
