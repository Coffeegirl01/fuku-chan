"""Omega multipliers for the Fuku-chan master score equation.

These functions convert raw environmental and contextual inputs into bounded
multipliers in the range [0, 1]. They are used in the final integration step:

    P = (sum(R_i * W_i)) * Omega_stamina * Omega_traffic * Omega_soil * Omega_corner * Omega_pace + epsilon
"""


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a value into the inclusive range [minimum, maximum]."""
    return max(minimum, min(maximum, float(value)))


def omega_stamina(stamina_score: float, wet_track_penalty: float = 0.0) -> float:
    """Wet-track stamina multiplier.

    Formula pattern:
        Omega_stamina = clamp(stamina_score - wet_track_penalty, 0.0, 1.0)
    """
    raw = stamina_score - wet_track_penalty
    return clamp(raw, 0.0, 1.0)


def omega_traffic(traffic_score: float, congestion_penalty: float = 0.0) -> float:
    """Traffic / raceflow multiplier.

    Formula pattern:
        Omega_traffic = clamp(traffic_score - congestion_penalty, 0.0, 1.0)
    """
    raw = traffic_score - congestion_penalty
    return clamp(raw, 0.0, 1.0)


def omega_soil(soil_score: float, mud_penalty: float = 0.0) -> float:
    """Ground / soil suitability multiplier.

    Formula pattern:
        Omega_soil = clamp(soil_score - mud_penalty, 0.0, 1.0)
    """
    raw = soil_score - mud_penalty
    return clamp(raw, 0.0, 1.0)


def omega_corner(corner_score: float, rail_penalty: float = 0.0) -> float:
    """Cornering / turning efficiency multiplier.

    Formula pattern:
        Omega_corner = clamp(corner_score - rail_penalty, 0.0, 1.0)
    """
    raw = corner_score - rail_penalty
    return clamp(raw, 0.0, 1.0)


def omega_pace(pace_score: float, pace_penalty: float = 0.0) -> float:
    """Pace control / rhythm multiplier.

    Formula pattern:
        Omega_pace = clamp(pace_score - pace_penalty, 0.0, 1.0)
    """
    raw = pace_score - pace_penalty
    return clamp(raw, 0.0, 1.0)


def combine_omega(
    stamina: float,
    traffic: float,
    soil: float,
    corner: float,
    pace: float,
) -> float:
    """Multiply all omega factors together as a single scalar coefficient."""
    return (
        omega_stamina(stamina)
        * omega_traffic(traffic)
        * omega_soil(soil)
        * omega_corner(corner)
        * omega_pace(pace)
    )


__all__ = [
    "clamp",
    "omega_stamina",
    "omega_traffic",
    "omega_soil",
    "omega_corner",
    "omega_pace",
    "combine_omega",
]
