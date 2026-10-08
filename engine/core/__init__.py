"""Core engine modules for Fuku-chan."""

from engine.core.calculator import calculate_score
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
from engine.core.horse import Horse
from engine.core.multipier import combine_omega
from engine.core.race import Race, RaceResult
from engine.core.track import Track

__all__ = [
    "calculate_score",
    "calculate_r1_speed",
    "calculate_r2_burst",
    "calculate_r3_stamina",
    "calculate_r4_guts",
    "calculate_r5_conditioning",
    "calculate_r6_race_iq",
    "calculate_r7_track_adaptability",
    "calculate_r8_distance_fit",
    "calculate_r9_weight_tolerance",
    "calculate_r10_clutch",
    "Horse",
    "Track",
    "Race",
    "RaceResult",
    "combine_omega",
]
