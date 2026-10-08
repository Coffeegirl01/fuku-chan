"""Main entry point for race simulation."""

from engine.core.horse import Horse
from engine.core.race import Race
from engine.core.track import Track


def create_sample_race() -> Race:
    """Create a sample race with test horses and track."""

    # Horse 1: Speed-focused
    horse1 = Horse(
        name="Thunderstorm",
        country="USA",
        age=4,
        sex="G",
        weight=500.0,
        distance=1600.0,
        time_norm=1.45,
        v_limit=85.0,
        v_gen_target=1.0,
        v_gen_current=1.0,
        burst_accel=22.0,
        accel_ref=18.0,
        time_3f=34.5,
        time_3f_best=34.0,
        gamma_drag=0.1,
        energy_consumed=38.0,
        glycogen=65.0,
        energy_capacity=100.0,
        duel_strength=0.85,
        duel_force=0.90,
        cr3=0.82,
        alpha=0.05,
        sigma_rank=0.55,
        beta=0.12,
        avg_abs_delta_wb=2.0,
        w_pos=0.75,
        lamda=0.18,
        position_gain_sum=8.0,
        m_total=20.0,
        w_tact=0.65,
        tactical_value=0.82,
        avg_v_heavy=1.05,
        avg_v_firm=1.20,
        alpha_water=0.15,
        water_index=0.15,
        distance_target=1600.0,
        distance_opt=1600.0,
        sigma_d=180.0,
        weight_carried=51.0,
        weight_base=52.0,
        theta_base=1.0,
        eta_wt=0.08,
        w_g1=0.82,
        s_g1=0.75,
        w_jock=0.80,
        cr3_pair=0.75,
        cr3_base=1.0,
    )

    # Horse 2: Stamina-focused
    horse2 = Horse(
        name="Endurance Queen",
        country="UK",
        age=5,
        sex="F",
        weight=480.0,
        distance=1600.0,
        time_norm=1.55,
        v_limit=80.0,
        v_gen_target=1.0,
        v_gen_current=1.0,
        burst_accel=18.0,
        accel_ref=18.0,
        time_3f=36.0,
        time_3f_best=35.0,
        gamma_drag=0.12,
        energy_consumed=35.0,
        glycogen=75.0,
        energy_capacity=110.0,
        duel_strength=0.72,
        duel_force=0.78,
        cr3=0.88,
        alpha=0.04,
        sigma_rank=0.45,
        beta=0.10,
        avg_abs_delta_wb=1.5,
        w_pos=0.68,
        lamda=0.20,
        position_gain_sum=5.0,
        m_total=18.0,
        w_tact=0.58,
        tactical_value=0.70,
        avg_v_heavy=0.98,
        avg_v_firm=1.15,
        alpha_water=0.20,
        water_index=0.10,
        distance_target=2000.0,
        distance_opt=2000.0,
        sigma_d=220.0,
        weight_carried=50.0,
        weight_base=50.0,
        theta_base=1.0,
        eta_wt=0.08,
        w_g1=0.75,
        s_g1=0.68,
        w_jock=0.78,
        cr3_pair=0.70,
        cr3_base=1.0,
    )

    # Horse 3: Balanced
    horse3 = Horse(
        name="Perfect Balance",
        country="USA",
        age=4,
        sex="G",
        weight=495.0,
        distance=1600.0,
        time_norm=1.50,
        v_limit=82.0,
        v_gen_target=1.0,
        v_gen_current=1.0,
        burst_accel=20.0,
        accel_ref=18.0,
        time_3f=35.2,
        time_3f_best=34.5,
        gamma_drag=0.11,
        energy_consumed=40.0,
        glycogen=65.0,
        energy_capacity=105.0,
        duel_strength=0.78,
        duel_force=0.84,
        cr3=0.80,
        alpha=0.05,
        sigma_rank=0.50,
        beta=0.11,
        avg_abs_delta_wb=2.2,
        w_pos=0.70,
        lamda=0.19,
        position_gain_sum=7.0,
        m_total=19.0,
        w_tact=0.62,
        tactical_value=0.76,
        avg_v_heavy=1.00,
        avg_v_firm=1.18,
        alpha_water=0.18,
        water_index=0.12,
        distance_target=1600.0,
        distance_opt=1600.0,
        sigma_d=200.0,
        weight_carried=51.5,
        weight_base=52.0,
        theta_base=1.0,
        eta_wt=0.09,
        w_g1=0.78,
        s_g1=0.71,
        w_jock=0.79,
        cr3_pair=0.72,
        cr3_base=1.0,
    )

    # Track: firm turf, slight wind
    track = Track(
        name="Belmont Park",
        country="USA",
        altitude=20,
        surface="TURF",
        specialty_distance="middle",
        track_layout="oval",
        temperature_c=22.0,
        humidity_pct=55.0,
        wind_speed_kph=8.0,
        precipitation_mm=1.0,
        soil_moisture=0.15,
        track_rating=0.75,
        course_bias=0.60,
    )

    # Create race
    race = Race(
        name="Belmont Middle-Distance Championship",
        track=track,
        horses=[horse1, horse2, horse3],
    )

    return race


def main():
    """Run the sample race and display results."""
    print("\n" + "=" * 80)
    print("FUKU-CHAN THOROUGHBRED RACE SIMULATOR")
    print("=" * 80)

    race = create_sample_race()
    race.print_results()

    # Also show detailed breakdown for top horse
    results = race.score_all_horses()
    if results:
        top = results[0]
        print(f"TOP HORSE BREAKDOWN: {top.horse.name}")
        print(f"  Final Score: {top.final_score:.4f}")
        print(f"  Base Score: {top.base_score:.4f}")
        print(f"  R Scores: {[f'{r:.3f}' for r in top.r_scores]}")
        print(f"  Omega Factors:")
        for key, val in top.omega_factors.items():
            print(f"    {key}: {val:.4f}")


if __name__ == "__main__":
    main()
