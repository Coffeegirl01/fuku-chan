# Fuku-chan

A transparent thoroughbred racing analysis platform for race prediction, cross-era comparison, pedigree research, and Bruce Lowe sire-line analysis.

> **Project philosophy:** AI should be combined with human reasoning—not blindly trusted. The equation engine is the source of calculated scores; AI may explain results, but must not replace validation or domain judgment.

## Master Integration Equation 2.0

The final performance score is calculated as:

$$
P = \left( \sum_{i=1}^{10} \Big( R_i \cdot W_i(\text{Surface}) \Big) \right)
\cdot \Omega_{\text{stamina}}
\cdot \Omega_{\text{traffic}}
\cdot \Omega_{\text{soil}}
\cdot \Omega_{\text{corner}}
\cdot \Omega_{\text{pace}}
+ \epsilon
$$

The model is designed to be explainable: every dimension, weight, multiplier, calibration step, and environmental assumption should be inspectable.

---

## 1. Bounded Dimension Equations ($R_1$–$R_{10}$)

**Global constraint:** every dimension must be clamped to:

$$0.00 \le R_i \le 1.00$$

In code, use a common clamp function:

$$
\text{clamp}(x,0,1)=\min(1,\max(0,x))
$$

### $R_1$: Adjusted Speed

$$
R_1 = \text{clamp}\left(
\frac{D}{T_{\text{norm}} \cdot V_{\text{limit}}}
\left[
\delta_{Y_c,Y_t} + (1-\delta_{Y_c,Y_t})
\frac{V_{\text{gen}}(Y_t)}{V_{\text{gen}}(Y_c)}
\right],0,1\right)
$$

### $R_2$: Burst Acceleration

$$
R_2 = \text{clamp}\left(
\frac{a_{\text{burst}}}{a_{\text{ref}}}
\left[
1-\gamma_{\text{drag}}
\left(\frac{T_{3F}-T_{3F,\text{best}}}{T_{3F,\text{best}}}\right)
\right],0,1\right)
$$

### $R_3$: Base Stamina — Quadratic Pace Tax

$$
R_3 = \text{clamp}\left(
1-\frac{\max\left(0,E_{\text{consumed}}(D)-E_{\text{glycogen}}\right)}{E_{\text{capacity}}},0,1\right)
$$

Accumulated energy consumption is modeled by:

$$
E_{\text{consumed}}
=\int_0^T\left(
V(t)+\alpha_{\text{surface}}
\cdot\max\left(0,V(t)-V_{\text{critical}}\right)^2
\right)\,dt
$$

### $R_4$: Guts / Resilience

$$
R_4 = \text{clamp}\left(
\bar{S}_{\text{duel}}\sqrt{F_{\text{duel}}},0,1\right)
$$

### $R_5$: Conditioning

$$
R_5 = \text{clamp}\left(
\frac{CR_3}{1+\alpha\sigma_{\text{rank}}}
\exp\left[-\beta\max\left(0,\overline{|\Delta WB|}-6\right)\right],0,1\right)
$$

### $R_6$: Race IQ and Positioning

$$
R_6 = \text{clamp}\left(
 w_{\text{pos}}\left[1-\lambda\frac{\sum\max(0,C_{k+1}-C_k)}{M}\right]
 +w_{\text{tact}}V_{\text{tactical}},0,1\right)
$$

### $R_7$: Track Adaptability

$$
R_7 = \text{clamp}\left(
\min\left(1,\frac{\bar V_{\text{heavy}}}{\bar V_{\text{firm}}}\right)
\left[1-\alpha_{\text{water}}M_{\text{water}}\right],0,1\right)
$$

### $R_8$: Distance Fit

$$
R_8 = \exp\left(
-\frac{(D_{\text{target}}-D_{\text{opt}})^2}{2\sigma_D^2}
\right)
$$

This Gaussian form naturally produces $0 < R_8 \le 1$ when $\sigma_D>0$.

### $R_9$: Weight Tolerance

$$
R_9 = \text{clamp}\left(
1-\eta_{\text{wt}}\left(\frac{W_{\text{carried}}}{WB}-\theta_{\text{base}}\right),0,1\right)
$$

### $R_{10}$: Clutch / Synergy

$$
R_{10} = \text{clamp}\left(
 w_{G1}S_{G1}
 +w_{\text{jock}}\frac{CR_{3\_\text{pair}}}{CR_{3\_\text{base}}},0,1\right)
$$

Implementation should define behavior for zero denominators such as $CR_{3\_\text{base}}=0$ rather than silently producing an invalid value.

---

## 2. Surface-Specific Conditional Protocol

### Weight Allocation Matrix

The active surface profile must satisfy:

$$
\sum_{i=1}^{10}W_i(\text{Surface})=1.00
$$

| Dimension | Turf | Dirt | Biomechanical emphasis |
| --- | ---: | ---: | --- |
| $R_1$ — Base Speed | 0.15 | 0.25 | Sustained speed, especially on dirt |
| $R_2$ — Burst Acceleration | 0.25 | 0.15 | Closing sprint on turf |
| $R_3$ — Base Stamina | 0.15 | 0.20 | Greater resistance from dirt footing |
| $R_4$ — Guts / Resilience | 0.05 | 0.05 | Fighting through the straight |
| $R_5$ — Conditioning | 0.05 | 0.05 | Physical readiness |
| $R_6$ — Race IQ / Position | 0.15 | 0.10 | Lane control and corner efficiency |
| $R_7$ — Track Adaptability | 0.15 | 0.20 | Grip and dirt-track adaptation |
| $R_8$ — Distance Fit | 0.15 | 0.10 | Distance specialization |
| $R_9$ — Weight Tolerance | 0.05 | 0.05 | Carrying weight |
| $R_{10}$ — Clutch / Synergy | 0.05 | 0.05 | Jockey synergy and experience |
| **Total** | **1.00** | **1.00** | |

### Time Calibration Protocol

**Turf standard:**

$$
T_{\text{norm}}=T_{\text{raw}}
$$

**Dirt variant (US/EU):**

$$
T_{\text{norm}}
=T_{\text{raw}}-T_{\text{runup}}\pm\Delta T_{\text{variant}}
$$

This accounts for run-up distance and daily track sensitivity. Calibration parameters must be versioned so that historical comparisons remain reproducible.

---

## 3. Non-linear Penalty Multipliers ($\Omega$)

**Global constraint:** every multiplier must be clamped to:

$$0.00\le\Omega\le1.00$$

### Stamina Crash

$$
\Omega_{\text{stamina}}=
\begin{cases}
1, & E_{\text{consumed}}\le E_{\text{glycogen}}\\
\exp\left[-\lambda_{\text{stam}}(E_{\text{consumed}}-E_{\text{glycogen}})\right], & E_{\text{consumed}}>E_{\text{glycogen}}
\end{cases}
$$

### Traffic Drag

$$
\Omega_{\text{traffic}}
=\text{clamp}(1-\delta_{\text{block}}T_{\text{blocked}},0,1)
$$

### Soil Resistance — Bifurcated Model

$$
\Omega_{\text{soil}}=
\begin{cases}
\text{clamp}\left(
1-\kappa_{\text{turf}}\max(0,P_{\text{depth}}-P_{\text{base}})(1-R_7),0,1\right), & \text{TURF}\\
\text{clamp}(\Omega_{\text{cushion}}\Omega_{\text{kickback}},0,1), & \text{DIRT}
\end{cases}
$$

For dirt:

$$
\Omega_{\text{cushion}}
=\text{clamp}\left(1-\kappa_{\text{dirt}}d_{\text{cushion}}(1-R_7),0,1\right)
$$

$$
\Omega_{\text{kickback}}
=\text{clamp}\left(
1-\lambda_{\text{kb}}
\left(\frac{\text{Position}-1}{N_{\text{total}}-1}\right)
(1-M_{\text{water}}),0,1\right)
$$

A front-running position of 1 gives $\Omega_{\text{kickback}}=1$ before clamping. The implementation must define behavior when $N_{\text{total}}=1$.

### Centripetal and Corner Drag

$$
\Omega_{\text{corner}}
=\text{clamp}\left(
1-\gamma_{\text{corner}}\frac{V_{\text{entry}}^2}{r_{\text{turn}}}
-\eta_{\text{wide}}\Delta D_{\text{wide}},0,1\right)
$$

### Pace Bias Adjustment

Because the raw pace-bias expression can exceed 1 or become negative, apply the global constraint explicitly:

$$
\Omega_{\text{pace}}
=\text{clamp}\left(
1+\mu_{\text{pace}}
\left(\frac{\text{Pace}_{\text{actual}}-\text{Pace}_{\text{par}}}{\text{Pace}_{\text{par}}}\right)
\mathbb{I}_{\text{lead}},0,1\right)
$$

The implementation must define behavior when $\text{Pace}_{\text{par}}=0$.

---

## 4. Core System Rules and Pipeline

1. **Strict clamping:** clamp every $R_1$–$R_{10}$ and every $\Omega$ to $[0,1]$ before the next stage.
2. **Weight constraint:** select the `TURF` or `DIRT` profile and verify that its weights sum to 1.00.
3. **No silent missing data:** missing or imputed inputs must be reported in the output.
4. **Reproducibility:** record calibration version, parameters, source data, and model version for every prediction.
5. **No certainty claims:** a score is a model output, not a guarantee of race outcome.

### Execution Pipeline

```text
Raw Data
  -> Time Calibration
  -> R1 ... R10
  -> Surface Weight Profile
  -> Weighted Base Score
  -> Apply Omega Multipliers
  -> P (Final Score)
```

$$
\text{Raw Data}
\xrightarrow{\text{Time Calibration}}
R_1\ldots R_{10}
\xrightarrow{\text{Surface Profile}}
\sum_{i=1}^{10}(R_iW_i)
\xrightarrow{\text{Penalty Multipliers}}
\prod\Omega
\longrightarrow P
$$

---

## 5. Search and Environmental Lookup Protocol

### 5.1 Mode-based search control

- **Blind Evaluation Mode:** do not search for any information. Calculate only from the raw inputs supplied to the evaluation.
- **Environmental Dynamic Mode:** environmental lookup is allowed only for race-day weather and track-surface conditions described below.

### 5.2 Permitted environmental search

Only the following physical conditions may be retrieved in Environmental Dynamic Mode:

- Weather
- Accumulated rainfall in millimetres
- Temperature
- Official track-condition rating, such as `良`, `稍重`, `重`, `不良`, `Firm`, `Good`, `Yielding`, `Soft`, or `Heavy`

These values may be mapped to physical coefficients such as:

- $\kappa_{\text{turf}}$ — turf resistance coefficient
- $P_{\text{depth}}$ — hoof-sinkage/depth index derived from rainfall and track condition

The mapping must be documented, versioned, and applied forward from the environmental input.

### 5.3 Absolute result-leakage ban

In Blind Evaluation Mode, do not search for or retrieve race results, finishing order, top-three results, winning time, or equivalent outcome data. If an outcome is accidentally encountered, it must not be used for backward reasoning or parameter tuning.

### 5.4 Forward-only physics deduction

The intended direction is:

$$
\text{Weather / Track Condition}
\longrightarrow \text{Physical Coefficients}
\longrightarrow \Omega_{\text{soil}}
\longrightarrow P
\longrightarrow \text{Ranking}
$$

Do not adjust multipliers merely to force agreement with the known winner. Evaluation data must remain separate from calibration data.

---

## 6. Validation and Limitations

A single exact-order blind test is encouraging but is not sufficient to establish general predictive accuracy. The project should report results over many genuinely out-of-sample races using metrics such as:

- Winner accuracy
- Top-3 inclusion rate
- Rank correlation
- Mean absolute rank error
- Exact-order rate
- Calibration of confidence estimates
- Performance by surface, distance, era, and track condition

The model cannot reliably anticipate every unexpected event, including injury or medical collapse, voluntary stopping, equipment failure, or an abrupt tactical change. Those should be represented as uncertainty and limitations—not retroactively explained as certain predictions.

## Status

The equation specification is being refined for implementation. The next engineering step is a deterministic calculation engine with unit tests for clamping, weight validation, denominator edge cases, and reproducible pipeline outputs.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
