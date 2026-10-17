
"""Main entry point for race simulation."""
 
from engine.core.horse import Horse
from engine.core.race import Race
from engine.core.track import Track
 
RACE_DISTANCE_M = 1600.0
 
# ค่าเริ่มต้นที่ม้าทุกตัวใช้ร่วมกัน (ตัวไหนต่างค่อย override ตอนสร้าง)
HORSE_DEFAULTS = dict(
    distance=RACE_DISTANCE_M,
    v_gen_target=1.0,
    v_gen_current=1.0,
    accel_ref=18.0,
    theta_base=1.0,
    cr3_base=1.0,
    eta_wt=0.08,
    alpha=0.05,
)
 
 
def make_horse(**overrides) -> Horse:
    """สร้าง Horse โดยรวมค่า default กับค่าที่ระบุเฉพาะตัว"""
    return Horse(**{**HORSE_DEFAULTS, **overrides})
 
 
def create_horses() -> list[Horse]:
    # Horse 1: Speed-focused
    thunderstorm = make_horse(
        # --- identity ---
        name="Thunderstorm", country="USA", age=4, sex="G", weight=500.0,
        # --- speed / acceleration ---
        time_norm=1.45, v_limit=85.0, burst_accel=22.0,
        time_3f=34.5, time_3f_best=34.0, gamma_drag=0.1,
        # --- energy ---
        energy_consumed=38.0, glycogen=65.0, energy_capacity=100.0,
        # --- duel ---
        duel_strength=0.85, duel_force=0.90, cr3=0.82,
        # --- rank / position ---
        sigma_rank=0.55, beta=0.12, avg_abs_delta_wb=2.0,
        w_pos=0.75, lamda=0.18, position_gain_sum=8.0, m_total=20.0,
        # --- tactics ---
        w_tact=0.65, tactical_value=0.82,
        # --- ground condition ---
        avg_v_heavy=1.05, avg_v_firm=1.20, alpha_water=0.15, water_index=0.15,
        # --- distance aptitude ---
        distance_target=1600.0, distance_opt=1600.0, sigma_d=180.0,
        # --- weight ---
        weight_carried=51.0, weight_base=52.0,
        # --- G1 / jockey ---
        w_g1=0.82, s_g1=0.75, w_jock=0.80, cr3_pair=0.75,
    )
 
    # Horse 2: Stamina-focused (ถนัดระยะ 2000 m จึงเสียเปรียบในระยะ 1600 m)
    endurance_queen = make_horse(
        name="Endurance Queen", country="UK", age=5, sex="F", weight=480.0,
        time_norm=1.55, v_limit=80.0, burst_accel=18.0,
        time_3f=36.0, time_3f_best=35.0, gamma_drag=0.12,
        energy_consumed=35.0, glycogen=75.0, energy_capacity=110.0,
        duel_strength=0.72, duel_force=0.78, cr3=0.88,
        alpha=0.04, sigma_rank=0.45, beta=0.10, avg_abs_delta_wb=1.5,
        w_pos=0.68, lamda=0.20, position_gain_sum=5.0, m_total=18.0,
        w_tact=0.58, tactical_value=0.70,
        avg_v_heavy=0.98, avg_v_firm=1.15, alpha_water=0.20, water_index=0.10,
        distance_target=2000.0, distance_opt=2000.0, sigma_d=220.0,
        weight_carried=50.0, weight_base=50.0,
        w_g1=0.75, s_g1=0.68, w_jock=0.78, cr3_pair=0.70,
    )
 
    # Horse 3: Balanced
    perfect_balance = make_horse(
        name="Perfect Balance", country="USA", age=4, sex="G", weight=495.0,
        time_norm=1.50, v_limit=82.0, burst_accel=20.0,
        time_3f=35.2, time_3f_best=34.5, gamma_drag=0.11,
        energy_consumed=40.0, glycogen=65.0, energy_capacity=105.0,
        duel_strength=0.78, duel_force=0.84, cr3=0.80,
        sigma_rank=0.50, beta=0.11, avg_abs_delta_wb=2.2,
        w_pos=0.70, lamda=0.19, position_gain_sum=7.0, m_total=19.0,
        w_tact=0.62, tactical_value=0.76,
        avg_v_heavy=1.00, avg_v_firm=1.18, alpha_water=0.18, water_index=0.12,
        distance_target=1600.0, distance_opt=1600.0, sigma_d=200.0,
        weight_carried=51.5, weight_base=52.0, eta_wt=0.09,
        w_g1=0.78, s_g1=0.71, w_jock=0.79, cr3_pair=0.72,
    )
 
    return [thunderstorm, endurance_queen, perfect_balance]
 
 
def create_track() -> Track:
    """Firm turf, slight wind."""
    return Track(
        name="Belmont Park",
        country="USA",
        altitude=20.0,  # meters
        surface="TURF",
        specialty_distance="middle",
        track_layout="oval",
        temperature_c=22.0,
        humidity_pct=55.0,
        wind_speed_kph=8.0,
        precipitation_mm=1.0,
        soil_moisture=0.15,
        track_rating=0.75,
    )
 
 
def create_sample_race() -> Race:
    """Create a sample race with test horses and track."""
    return Race(
        name="Belmont Middle-Distance Championship",
        track=create_track(),
        horses=create_horses(),
    )
 
 
def print_top_breakdown(results) -> None:
    """แสดงรายละเอียดคะแนนของม้าอันดับ 1"""
    if not results:
        print("No results.")
        return
 
    top = results[0]
    print(f"TOP HORSE BREAKDOWN: {top.horse.name}")
    print(f"  Final Score: {top.final_score:.4f}")
    print(f"  Base Score: {top.base_score:.4f}")
    print(f"  R Scores: {[f'{r:.3f}' for r in top.r_scores]}")
    print("  Omega Factors:")
    for key, val in top.omega_factors.items():
        print(f"    {key}: {val:.4f}")
 
 
def main() -> None:
    """Run the sample race and display results."""
    print("\n" + "=" * 80)
    print("FUKU-CHAN THOROUGHBRED RACE SIMULATOR")
    print("=" * 80)
 
    race = create_sample_race()
    race.print_results()
 
    # หมายเหตุ: ถ้า score_all_horses() มีการสุ่ม ผลอาจไม่ตรงกับที่ print_results() แสดง
    # แนะนำให้ปรับ print_results() ให้รับ results เข้ามา จะได้คำนวณครั้งเดียว
    print_top_breakdown(race.score_all_horses())
 
 
if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
