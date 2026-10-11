"""Race orchestration and scoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from engine.core.calculator import calculate_score
from engine.core.horse import Horse
from engine.core.track import Track


@dataclass
class RaceResult:
    """Result for one horse in a race."""

    horse: Horse
    r_scores: tuple[float, ...]
    omega_factors: Dict[str, float]
    base_score: float
    final_score: float


@dataclass
class Race:
    """A race with a track and multiple horses."""

    name: str
    track: Track
    horses: List[Horse] = field(default_factory=list)

    def score_all_horses(self) -> List[RaceResult]:
        """Score each horse and return ranked results."""
        results = []

        # Get track environment multipliers once
        omegas = self.track.omega_factors()
        multipliers = (
            omegas.get("Omega_stamina", 1.0),
            omegas.get("Omega_traffic", 1.0),
            omegas.get("Omega_soil", 1.0),
            omegas.get("Omega_corner", 1.0),
            omegas.get("Omega_pace", 1.0),
        )

        # Score each horse
        for horse in self.horses:
            r_scores = horse.calculate_r_scores()

            score_result = calculate_score(
                dimensions=r_scores,
                surface=self.track.surface,
                multipliers=multipliers,
            )

            result = RaceResult(
                horse=horse,
                r_scores=r_scores,
                omega_factors=omegas,
                base_score=score_result.base_score,
                final_score=score_result.final_score,
            )
            results.append(result)

        # Sort by final score descending
        return sorted(results, key=lambda x: x.final_score, reverse=True)

    def print_results(self, top_n: int = None) -> None:
        """Print race results in a formatted table."""
        results = self.score_all_horses()
        if top_n:
            results = results[:top_n]

        print(f"\n{'='*80}")
        print(f"Race: {self.name}")
        print(f"Track: {self.track.name} ({self.track.country}, {self.track.surface})")
        print(f"{'='*80}")
        print(f"{'Position':<10} {'Horse':<20} {'Final Score':<15} {'Base Score':<15}")
        print(f"{'-'*80}")

        for i, result in enumerate(results, 1):
            print(
                f"{i:<10} {result.horse.name:<20} {result.final_score:<15.4f} {result.base_score:<15.4f}"
            )

        print(f"{'='*80}\n")


__all__ = ["Race", "RaceResult"]
