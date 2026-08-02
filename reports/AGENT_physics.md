# Quantitative audit — Černohajev Works 3, 5, 6, 8, 9, 10, 11, 12

Source: extracted text of the CARI "Critical Editions" (ed. E. Sticco) at
`/tmp/claude-1001/-home-user-new-skinny-bob/0a8dd3d2-3fd5-4e22-b0d7-a55e36ce5c1c/scratchpad/ei/txt/`.
Every number below was recomputed independently with `python3.12`. Works 1, 2, 7 and the two 2026
preprints were audited separately and are used here only as context.

Throughout I separate three failure modes, as requested:

- **(a) arithmetic error** — the manuscript's own numbers do not follow from its own inputs;
- **(b) correct arithmetic on an unphysical premise** — the sum is right, the premise is not;
- **(c) correct standard physics restated** — no error, no novelty.

A fourth category appears often enough to deserve a label:

- **(d) editorial-apparatus error** — a mistake in the CARI editor's commentary, not in the
  manuscript. These matter because the commentary is what an external reader will quote.

---

## 1. Work No. 3 — "What is electric current from the standpoint of spherical-Bohr rather than planetary-Rutherford atomic structure"

### 1.1 What it claims

Four claims, in order of load-bearing weight:

1. Classical electrodynamics is "built on" the Rutherford planetary atom and therefore mis-describes
   conduction. Under the Bohr-spherical atom plus GCD excess negative charge, no positive "hole" ever
   forms when a conduction electron leaves an atom, because the GCD-derived surplus electron
   population refills it instantly. Hole conduction therefore does not exist.
2. Direct and alternating current *of the same magnitude* produce magnetic fields of **different
   strength** around the same conductor.
3. The drift-velocity waveform out of a frame rotating in a magnetic field is a sequence of
   **half-circles, not a sine**, "because the frame rotates circularly, not sinusoidally."
4. Engineering payload: a two-frame synchronised rotor on one shaft converts AC to DC mechanically,
   is lossless relative to diode rectifiers, and scales current arbitrarily by raising rpm at fixed
   magnet mass. This is the constant-current source that Work 2 forwards to (10³–10⁵ A into
   3.39·10⁸ solenoid turns).

### 1.2 Every quantitative claim

Work 3 is almost entirely qualitative. The complete numerical inventory:

| Quantity | Manuscript value | My recomputation | Verdict |
|---|---|---|---|
| `I = Q/t` | definition of current | exact SI definition (1 A = 1 C/s) | **(c)** correct, restated |
| Atomic size `r_Bohr.orbit` | ≈ 10⁻¹⁰ m | Bohr radius 5.29·10⁻¹¹ m; atomic radii 0.3–3 Å | **(c)** correct to order |
| "Classical" electron size `r_e` | ≈ 10⁻¹⁵ m | classical electron radius 2.818·10⁻¹⁵ m | value correct, *interpretation* wrong (below) |
| Nuclear size | ≈ 10⁻¹⁵ m | 1.2 fm × A^(1/3): 1.2·10⁻¹⁵ m (H) to 7.4·10⁻¹⁵ m (U) | **(c)** correct to order |
| Size ratio | "100 000 times" | 10⁻¹⁰/10⁻¹⁵ = 10⁵ ✓ — but with the *actual* values 5.29·10⁻¹¹/2.818·10⁻¹⁵ = **1.88·10⁴** | **(a)** minor: the analogy is 5.3× off if his own cited constants are used rather than the rounded powers of ten |
| "1 cm electron ⇒ 1 km atom" | — | geometrically exact given 10⁵ | **(c)** |
| Solenoid current forwarded | 10³–10⁵ A | see cross-work table §7 | inconsistent across corpus |

### 1.3 Independent assessment

**Claim 2 (AC vs DC field strength) — (b), with a real phenomenon underneath.**
Ampère's law gives H = I/(2πr) outside a long straight conductor for *any* enclosed current, constant
or instantaneous. The peak field of I₀·sin(ωt) equals the steady field of a DC current I₀. The
manuscript's assertion is not what electrodynamics says.

*In fairness*, there are two real effects that would produce exactly the observation he reports if you
measured naively:

- **Meter artefact.** An AC ammeter reads RMS; a DC-responding magnetometer (compass, Hall probe on
  DC range) time-averages the AC field to ~zero. "Same current I, much weaker field" is precisely
  what that instrument pair reports. This is almost certainly the origin of Aspect 2.
- **Skin effect.** At 50 Hz the skin depth in copper is **9.2 mm** (my calculation), so in a thick bar
  the current redistributes to the surface at AC. This genuinely changes the field *inside* the
  conductor. It does not change the field *outside*, which is all Ampère's law needs.

He identifies a real measurement asymmetry and then draws the wrong conclusion from it. That is worth
recording as the only place in Work 3 where an empirical observation is plausibly behind a claim.

**Claim 3 (half-circular drift profile) — (b), and the argument is a category error.**
Faraday's law on a frame of area A, N turns, angular frequency ω in uniform B:
Φ = N·B·A·cos(ωt), ε = −dΦ/dt = N·B·A·ω·sin(ωt). Sinusoidal. The manuscript never invokes Faraday's
law; the inference is "the frame moves in a circle, therefore the output traces circles," which
confuses the trajectory of the conductor with the time-derivative of the flux through it.

There *is* a regime where the waveform departs from sinusoidal — a spatially non-uniform field across
the frame, which is exactly what the two close permanent magnets in his own figure would produce.
That distortion is harmonic content, not half-discs, and he does not compute it.

**Claim 1 (no hole conduction) — (b).** Hole conduction is a band-structure result, not an
atomic-model result. It is the operating principle of every p-type semiconductor. The proposed
replacement mechanism would forbid the diode.

Note also that the manuscript's microscopic picture is quantitatively wrong in a way the editor did
not check: it has each drift electron knocking a new one out of *the very next atom*, a cascade with
mean free path ≈ one lattice spacing. Measured mean free path in copper at 300 K is ~39 nm, i.e.
**~110 lattice spacings** (0.36 nm), and the actual drift velocity at 1 A/mm² is
**7.3·10⁻⁵ m/s** — about 2·10¹⁰ times slower than the Fermi velocity (1.57·10⁶ m/s) that actually
sets the electron kinematics. The "drift electron" of the manuscript is not a physically identifiable
object at any speed scale.

**Claim 4 (two-frame mechanical rectifier) — (c) restated, plus (b) on losslessness.**
Scheme 1 / Scheme 2 is a correct identification of the split-ring commutator vs slip-ring
distinction — this is a real engineering distinction, correctly drawn, and it is the one genuinely
sound piece of engineering in the paper. The claim of *no losses* is wrong: brush contact drop,
friction, and commutation arcing are why high-current DC moved to solid-state rectification. The
scaling claim ("more rpm ⇒ more current at fixed magnet mass") is true only into a fixed load
impedance and ignores that EMF ∝ ω raises the required insulation voltage and the commutation
duty simultaneously.

**Electron-size claim — (b).** Treating the classical electron radius as a physical extent that
*changes* between the bound and conducting state has no counterpart in QM. Collider bounds put the
electron's structure below ~10⁻²² m; the classical radius is an energy bookkeeping quantity.

### 1.4 Genuine content in Work 3

- The commutator/slip-ring distinction (Schemes 1 and 2) is correct.
- `I = Q/t` is exactly right.
- The atom/electron/nucleus size scales are right to order of magnitude, and the 1 cm : 1 km analogy
  is a legitimate pedagogical device.
- The AC/DC field observation is probably a real instrument artefact, honestly reported.

Nothing in Work 3 supplies the constant-current source Work 2 needs. No power, mass, voltage, or
commutation-rating number appears anywhere in the paper.

---

## 2. Works No. 5, 9, 12 — "Refinement of the absolute dimensional and motional characteristics for the Solar System inside our Galaxy"

### 2.1 How the three works differ

They are one derivation revised three times, and they are **mutually consistent on every number
except two** (Jupiter's orbital velocity, and the retrograde-planet list). The progression:

| | **Work 5** (9 pp.) | **Work 9** (5 pp.) | **Work 12** (8 pp.) |
|---|---|---|---|
| Core result | 7150 km/s, 60 pc, 8.5 kpc, 15 kpc, 26 000 yr | identical | identical |
| 29.78 factor | asserted, no derivation shown | derived as 461.58 mm / 15.5 mm | same, **and the source figure is supplied** as p. 4 "Приложение I" |
| Retrograde planets | table marks Venus + Uranus; **p. 8 text says Venus + Saturn** | "Venus/Uranus" only | "Venus and Uranus" only |
| Jupiter V_orb | 13 km/s | 13 km/s | **13.4 km/s** |
| Spin cancellation argument | absent | present | present |
| Laplace | **rejected outright** (prominence-ejection origin of planets) | omitted | **accommodated** — "averaged position" between Laplacian circles and GCD spirals |
| Big Bang | rejected ("whipping of massless space by Time") | omitted | omitted |
| Galaxy evolution | 4-stage globular→elliptical→barred spiral→spiral | omitted | omitted |

So the sequence is 5 → 9 → 12, with each revision *removing* the falsifiable astrophysical
extensions and *adding* documentary support for the one number the chain rests on. Work 12 is the
mature version and reverses Work 5's central cosmological position.

### 2.2 Every quantitative claim, with recomputation

| Claim | Manuscript | My recomputation | Verdict |
|---|---|---|---|
| Arm rotation about Galactic Centre | 240 km/s | modern 229–240 km/s | **(c)** taken from source, correct |
| Precession period | 26 000 yr | 25 772 yr | **(c)** correct |
| 29.78 multiplier | 461.58 / 15.5 | 3.14 × 147 = 461.58 ✓; 461.58/15.5 = **29.7794** ✓ | arithmetic exact; see §2.3 |
| Intra-arm solar velocity | 240 × 29.78 = 7150 km/s | 240 × 29.78 = **7147.2** ✓ | **(b)** |
| Orion Arm diameter | (V·T)/π = 1.87·10¹⁵ km ≈ 60 pc | V·T/π = **1.866·10¹⁵ km**; ÷ 3.0857·10¹³ = **60.48 pc** ✓ | **(b)** |
| 1 pc | 30.84·10¹² km | 3.0857·10¹³ km ✓ | **(c)** |
| Sun–Galactic-Centre | 8.5 kpc | modern 8.12–8.3 kpc | **(c)** ~4% high, matches 1966 source |
| Galactic radius | 15 kpc | modern disc 25–30 kpc | 1966-era value, honestly labelled "на 1966 год" |
| Sun above galactic plane | 25 pc | modern 17–25 pc | **(c)** correct |
| Sun: R = 696 000 km, M = 2·10³³ g, ρ = 1.4 g/cm³ | — | ρ = M/(4πR³/3) = **1.416 g/cm³** ✓ | **(c)** |
| Sun V_rot = 1.99 km/s | — | 2πR/(25.4 d) = **1.993 km/s** ✓ | **(c)** |
| Planetary orbital velocities (9 rows) | Pluto 4.7 … Mercury 48 | recomputed 2πa/P for all nine: **agree to 0.2–0.8%** | **(c)** all correct |
| Planetary equatorial rotation speeds | Mercury 3 … Jupiter 12 700 m/s | recomputed 2πR/P: Mercury 3.0, Venus 1.7, Earth 465.1, Mars 241.1, Jupiter 12 673, Saturn 10 301, Uranus 3 840 — all within 2% **except Neptune: he gives 2300, correct is 2592 (−11%)** | **(c)** with one **(a)** |
| Solar-system point count on arm circle | 8 points (I–VIII) | 26 000/8 = 3250 yr/point, which is exactly the "3250 years" of Work 10 | internally consistent |

**The planetary table is genuinely good work.** Nine orbital velocities and eight equatorial rotation
speeds, all hand-computed from semi-major axes and periods, all correct to sub-percent except one.
This is real, careful arithmetic.

**Editorial-apparatus error (d):** the Work 5 critical edition, Translator's Note to p. 3, states that
the rotation-velocity column is "in m/sec for Earth and km/h elsewhere; the units are not consistent
across the column." That is not true. I recomputed every row: the whole column is in **m/s** and is
correct. The commentary invents an inconsistency that is not in the manuscript.

### 2.3 The 29.78 factor — the load-bearing number

Everything downstream (7150 km/s, 60 pc, and by forwarding the B-field values of Work 1 p. 21) hangs
on this one dimensionless multiplier. Work 12 p. 4 finally shows where it comes from: two lengths
**measured with a ruler off a hand-drawn star chart** of the 26 000-year precession circle overlaid on
Cygnus / Cepheus / Ursa Minor / Draco.

- 147 mm = drawn diameter of the precession circle, relabelled "diameter of the internal orbit of the
  Orion Arm where the Solar System is located";
- 15.5 mm = drawn "shift over 26 000 years at 240 km/s".

Four independent problems, in ascending severity:

1. **Spurious precision.** A ruler reading of a hand-drawn 15.5 mm segment carries at best ±0.5 mm.
   I propagated it: 15.0 mm → 30.77 → **7385 km/s**; 16.0 mm → 28.85 → **6924 km/s**. The quoted
   four-significant-figure "29.78" is not supportable from the measurement it is drawn from.

2. **Dimensional mismatch.** The chart is a map of *directions on the celestial sphere* (its own scale
   bar reads 10°, 15°, 20°, 25°). The precession circle has angular radius equal to the obliquity,
   23.44°, so 147 mm ↔ 46.9° and 1 mm ↔ 0.319°. The "shift", by contrast, is meant to represent a
   *linear translation* of 240 km/s × 26 000 yr = **1.968·10¹⁴ km = 6.38 pc**. A ratio of an angle to
   a length is being used as a ratio of two speeds.

3. **The construction is circular.** At the scale implied by the answer (147 mm ↔ 60.5 pc, i.e.
   2.43 mm/pc), 6.38 pc plots as **15.50 mm** — I get 15.502 mm. The "measured" shift is exactly the
   value the 60-pc answer requires. The figure therefore carries no information the conclusion did not
   already contain. (I cannot rule out that the figure was drawn first and the agreement is genuine;
   but the two are numerically indistinguishable, so the figure cannot discriminate.)

4. **The number coincides with a dimensioned constant.** Earth's mean orbital speed is
   **29.7847 km/s** — the standard figure in the very textbook cited (Bakulin et al. 1966), and the
   quantity whose rounded form "30" appears in his own p. 3 table. His 461.58/15.5 = 29.7794 agrees
   with it to **0.018%**. I cannot establish intent, and I record this as an observation rather than a
   conclusion: the dimensionless multiplier that converts 240 km/s into 7150 km/s is numerically
   Earth's orbital speed in km/s to four figures.

**Verdict: (b) — the arithmetic is exact, the premise is a ruler measurement on a diagram whose
physical scale is undefined.**

### 2.4 The premise: precession period ≠ galactic orbital period

The 26 000-year identification is the physics failure. Earth's axial precession is a lunisolar torque
on the equatorial bulge; the Sun's galactic orbit is set by the enclosed galactic mass. My numbers:

- Galactic year, from his own inputs: 2π × 8.5 kpc / 240 km/s = **218 Myr** (modern: 225–250 Myr).
- Ratio to 26 000 yr: **~8 400–9 600×**.

His derivation therefore replaces the galactic year with a period 9 000 times too short.

### 2.5 Independent tests of the 7150 km/s claim

Three quantitative checks, none of which appear in the corpus or in the CARI commentary:

**(i) Self-gravity of the claimed orbit.** A circular orbit of radius 30 pc (= 9.257·10¹⁷ m) at
7150 km/s requires centripetal acceleration a = v²/r = **5.52·10⁻⁵ m/s²**. The enclosed mass needed is
M = v²r/G = **7.09·10⁴¹ kg = 3.6·10¹¹ M☉** — roughly a quarter of the entire Milky Way, concentrated
within 30 pc of the Sun. For comparison, the Sun's actual galactic acceleration is
v²/R = (230 km/s)²/8.2 kpc = **2.09·10⁻¹⁰ m/s²**, i.e. **2.6·10⁵ times smaller**. The claimed orbit is
not dynamically closeable by anything.

**(ii) The absolute-velocity claim is directly measured.** Work 5/9/12 explicitly frame 7150 km/s as
the Sun's *absolute* speed, arguing that the textbook 20 km/s apex velocity is merely relative. But
the Sun's velocity relative to the CMB rest frame is measured from the CMB dipole:
**369.8 ± 0.1 km/s**. The claimed absolute speed exceeds the measured one by **19×**, and exceeds even
the Local Group's motion (~620 km/s) by 12×. Also, 7150 km/s = **2.4% of c**, which would put a
measurable ~0.03% second-order Doppler asymmetry on the sky.

**(iii) The arm diameter.** 60 pc vs the Orion Spur's ~1 100 pc width: **18× short**. The manuscript's
own cross-check ("fully corresponds… since the Solar System is 25 pc from the galactic plane") does not
work: 25 pc out of a 30 pc radius puts the Sun at 83% of the way to the wall of its own orbit.

### 2.6 Are the "refinements" derived or asserted?

**Asserted, then decorated with a derivation.**

- 240 km/s: taken from the source. Not refined.
- 26 000 yr: taken from the source, then *reassigned* to a different physical quantity. Not derived.
- 8.5 kpc, 15 kpc, 25 pc: taken from the source verbatim, explicitly labelled "на 1966 год". Not refined.
- 29.78: measured off a drawing whose scale is set by the answer. Not derived.
- 7150 km/s and 60 pc: arithmetically exact consequences of the above. Derived from asserted inputs.

Not one accepted value is displaced by an independent measurement or an independent calculation. The
word "уточнение" (refinement) in the title describes a re-labelling.

### 2.7 Genuine content in Works 5/9/12

- The full planetary table (§2.2) is careful, correct arithmetic.
- The **Keplerian observation** — orbital speed rises toward the centre and is independent of the
  planet's own mass — is correct standard physics (v = √(GM/r), the test mass cancels), correctly
  stated, and correctly attributed to the data.
- The reading of §165 of Bakulin (aspect b) is **substantially right**: the 20 km/s apex velocity *is*
  a velocity relative to the local standard of rest, not an absolute velocity. He identifies a genuine
  interpretive subtlety in the source.
- The non-coplanarity of the planetary orbits with the solar equator (7°15′) is a real, correctly
  cited observation.
- Work 9/12's correction of Work 5's Saturn-retrograde error is a real self-correction — one of the
  few places in the corpus where a later work fixes an earlier one.
- Work 12's retreat from "Laplace is wrong" to "Laplace and GCD are both partly right" is
  intellectually honest movement, whatever one makes of the synthesis.

### 2.8 Errors specific to Work 5's philosophical section (pp. 7–9)

- **Saturn retrograde (a).** Saturn's rotation is prograde, period 10.7 h. The manuscript's own p. 3
  table does *not* mark Saturn; the p. 8 argument does. Since the prominence-ejection argument rests
  on exactly two data points, removing Saturn removes half of it.
- **Hubble sequence inverted (b).** Globular cluster → elliptical → barred spiral → spiral as a literal
  evolutionary path runs opposite to the observed direction (spirals merge into ellipticals), and
  globular clusters are components of galaxies, not precursors to them.
- **Prominence-ejection planet formation (b).** A typical CME/prominence carries ~10¹³ kg. Jupiter is
  1.9·10²⁷ kg — **14 orders of magnitude** larger. There is no mass budget.
- **The ice-age/human-evolution digression** is not a physical claim and is not assessable.

---

## 3. Work No. 8 — thermonuclear synthesis via d+d

### 3.1 What it claims

An impulse-type d+d reactor: deuterium at >2000 atm, ignited by an electrical breakdown ("пробой")
that simultaneously supplies temperature and an excess negative charge density >0.12·10¹³ e⁻/m³, with
Laval nozzle, MHD generator and piston compressor in a closed loop. The operating point is derived
**by analogy with the Sun's surface**, not from plasma physics. A 9-page addendum ("К работам
№№ 7, 8, 2") then derives the corpus's headline numbers: B_Sun = 16.65 T, 32 solenoids, I = 1.65 kA.

### 3.2 Every quantitative claim, with recomputation

| Claim | Manuscript | My recomputation | Verdict |
|---|---|---|---|
| M☉, R☉ | 2·10³⁰ kg, 7·10⁸ m | ✓ | (c) |
| ρ̄☉ = M/(πr³) | ≈ 2·10³ kg/m³ | **his own formula gives 1856**, not 2000; and the formula omits the 4/3: correct ρ̄ = **1392 kg/m³** (true 1410) | **(a)** double: 4/3 missing (+33%), then rounded up a further 8% |
| "2·10³ kg/m³ ~ 2000 atm" | — | mass density is not pressure. 2000 atm = 2.03·10⁸ Pa | **(a)** dimensional category error |
| N_protons/m³ | ρ/(2m_p) = 0.6·10³⁰ | 2000/(2×1.67·10⁻²⁷) = **5.99·10²⁹** ✓ | (b) — arithmetic ✓, but see below |
| N_excess e⁻ | 0.6·10³⁰/5·10¹⁷ = 0.12·10¹³ | **1.198·10¹²** ✓ | (b) |
| q_excess | ×1.6·10⁻¹⁹ = 0.2·10⁻⁶ C/m³ | **1.916·10⁻⁷** ✓ | (b) |
| Literature values cited | "15 mln K and hydrogen pressure 100 g/cm³" | T_core 1.57·10⁷ K ✓; ρ_core = **150 g/cm³**, and it is a *density*, not a pressure | **(a)** value 33% low, unit wrong |
| 1 Oe → A/m | 79.6 | 1000/4π = **79.5775** ✓ | (c) |
| q☉/q⊕ | 1.9·10²⁰/5.72·10¹⁴ | **3.3217·10⁵** ✓ | (c) arithmetic |
| H☉ = (q☉/q⊕)·0.5 Oe | 1.66·10⁵ Oe | **1.6608·10⁵** ✓ | (b) |
| B☉ = μ₀·79.6·H | 1.26·10⁻⁶ × 79.6 × 1.66·10⁵ = 16.65 T | **16.658 T** ✓ (with exact μ₀ and 1000/4π: 16.608 T) | (b) |
| Turns per metre | 2 mm wire + 2 mm gap ⇒ 250/m | 1/0.004 = **250** ✓ | (c) |
| N/L for 32 solenoids | 250 × 32 = 8000 /m | 8000 ✓ arithmetically | **(a)** physics — see §3.4 |
| I = B/(μμ₀·N/L) | 16.65/(1.26·10⁻⁶ × 8000) = 1.65·10³ A | **1651.8 A** ✓ (exact μ₀: 1656.2) | (b) |
| Reaction on p. 6 | "{d+d → d+t+p}" | LHS A = 4, Z = 2; RHS A = **6**, Z = **3** | **(a)** nucleon and charge number not conserved as written |

**Every arithmetic step in the 16.65 T / 32 / 1.65 kA chain checks out to <0.5%.** It is the most
computationally clean derivation in the corpus. Its inputs are the problem, not its sums.

### 3.3 The nuclear data — branching ratios and Q-values (requested specifically)

I computed the Q-values from atomic masses (electron counts balance in all three channels), with
u = 931.49410242 MeV:

| Branch | My Q (MeV) | Accepted Q | Real branching at ~10–100 keV | Product energies |
|---|---|---|---|---|
| d + d → t + p | **4.0327** | 4.03 | **~50%** | t 1.010, p 3.023 MeV |
| d + d → ³He + n | **3.2689** | 3.27 | **~50%** | ³He 0.819, n 2.450 MeV |
| d + d → ⁴He + γ | **23.8465** | 23.85 | **~10⁻⁷** | γ 23.8 MeV |

**Does he treat the γ branch as comparable to the other two?** Yes — the title, the page-1 header, the
schema box and the addendum all list the three branches in parallel with no weighting and no
statement of any branching ratio. No branching ratio appears anywhere in Work 8.

Quantifying the consequence, if a reader takes the three branches as co-equal (as the presentation
invites):

- equal-weight mean Q = **10.383 MeV**;
- true branch-weighted Q = 0.5(4.0327) + 0.5(3.2689) + 10⁻⁷(23.8465) = **3.651 MeV**;
- **energy-yield overestimate = 2.84×**.

Worse for the design logic: on an equal-weight reading the γ branch supplies **76.6%** of the energy;
in reality it supplies **6.5·10⁻⁷** of it. The reactor's radiation environment is therefore
mischaracterised in both directions at once — the 23.8 MeV γ he implicitly budgets for essentially
never happens, while the 2.45 MeV neutron he does not budget for happens in **half of all events**.

This collides directly with Work 2 p. 7, which selects d + ⁶Li → 2 ⁴He *specifically* because it is
aneutronic (no shielding mass on the saucer). d+d is not aneutronic. Work 8 does not address this.

### 3.4 Ignition temperature, Lawson criterion, energy yield

**None of the three appears in Work 8.** This is the paper's largest omission. The ignition condition
is specified purely as a *charge* condition (">0.12·10¹³ e⁻/m³") plus "temperature — maximally
possible (achieved via electrical discharges)".

What the standard criteria actually require, for comparison:

| | D–T | **D–D** | Work 8 |
|---|---|---|---|
| Ignition ion temperature | ~10–15 keV (1.2–1.7·10⁸ K) | **~40–50 keV (4.6–5.8·10⁸ K)** | not stated |
| Lawson nτ_E | ~1.5·10²⁰ s/m³ | **~10²² s/m³** | not stated |
| Triple product nTτ_E | ~3·10²¹ keV·s/m³ | **~10²⁴ keV·s/m³** (~300× harder) | not stated |

A gas-discharge breakdown, the ignition mechanism the manuscript specifies, produces electron
temperatures of order 1–5 eV, i.e. **~10⁴–6·10⁴ K**. The shortfall to d+d ignition is
**~4 orders of magnitude in temperature**, and d+d is the *hardest* of the practical fuels, roughly
300× worse than D–T on triple product. Selecting d+d and then specifying discharge ignition is the
least favourable combination available.

**The excess-charge ignition condition is quantitatively negligible.** His 1.92·10⁻⁷ C/m³, in a fusion
plasma of n ≈ 10³⁰ m⁻³, is a net charge imbalance of
1.92·10⁻⁷/(1.602·10⁻¹⁹ × 10³⁰) = **1.2·10⁻¹⁸**. That is *far below* ordinary plasma quasi-neutrality
departures and does nothing to confinement or ignition. The associated field at the surface of a 1 m
sphere is E = ρr/3ε₀ = **7.2 kV/m** — a laboratory triviality. The specification is not a confinement
criterion in any sense.

### 3.5 The solar-analogy premise

The whole operating point comes from "the Sun's surface." Three problems:

1. **He uses the *mean* density as the *surface* density.** The solar photosphere has
   ρ ≈ 2·10⁻⁴ kg/m³. His 2·10³ kg/m³ is **10⁷ times too large** for the location he assigns it to.
2. **There is no fusion at the solar surface.** T_photosphere ≈ 5772 K. Hydrogen burning is confined
   to the inner ~25% by radius.
3. **The "periphery makes light elements, centre makes heavy elements" picture is inverted.** In the
   standard model the *centre* is where hydrogen burns; heavy elements are not synthesised in the Sun
   at all (it will not reach carbon burning).

### 3.6 The 16.65 T result against measurement

| | Value | Ratio |
|---|---|---|
| GCD prediction, solar surface | **16.65 T** | — |
| Measured general photospheric field | ~1 G = 10⁻⁴ T | **1.7·10⁵×** high |
| Strongest sunspot umbral fields | ~0.3–0.6 T | **28–56×** high |

The **(b)** classification is exact here: flawless arithmetic on q☉ and q⊕ that are themselves fixed by
the "1 e⁻ per 5·10¹⁷ protons" constant, which (per your Work 7 audit) is 1.11 × √(G/k) and produces an
Earth surface field of 1.3·10¹¹ V/m against a measured ~100 V/m.

### 3.7 The 32-solenoid step is a physics error, not just an unjustified choice

The CARI commentary treats "32" as a round-number engineering choice. It is worse than that.

`N/L = 250 turns/m × 32 solenoids = 8000 turns/m` then fed into `B = μμ₀(N/L)I`.

But the on-axis field of a solenoid is B = μ₀nI where **n is the turns per unit length of that
solenoid**. Placing 32 separate 2-cm-diameter solenoids side by side does **not** multiply the field
inside any one of them by 32; each still produces μ₀ × 250 × I. Multiplying the turn density by the
solenoid count is not a valid application of the formula, and it under-states the required current by
exactly the factor 32 (correct single-solenoid current for 16.65 T: **I = 16.65/(μ₀ × 250) = 53.0 kA**).

Second, geometrically: the manuscript's own diagram shows the 32 solenoids as **spokes radiating from
a central axis**. Thirty-two solenoid axes pointing radially inward with 11.25° spacing produce fields
that cancel by symmetry at the centre — the vector sum of 32 equal radial vectors is zero. The
configuration as drawn cannot produce a 16.65 T axial field at all.

Third, at 16.65 T the magnetic pressure on the winding is B²/2μ₀ = **1.10·10⁸ Pa ≈ 1100 atm**, which
is a structural problem the paper does not mention.

### 3.8 Genuine content in Work 8

- The CGS↔SI conversion (1 Oe = 79.6 A/m) is right.
- B = μμ₀H with μ<1 diamagnetic, μ>1 ferromagnetic is right.
- 250 turns/m from 2 mm wire + 2 mm gap is right.
- The three d+d channels are the correct three channels, and the two dominant ones are correctly
  identified as the primary reactions. The reaction set is real nuclear physics.
- Recognising that a UFO platform cannot use rotating turbines and therefore needs a piston + MHD
  topology is a coherent engineering constraint, honestly propagated.
- The addendum is the most derivationally transparent page in the corpus: every headline number is
  traceable to a stated input. That transparency is what makes it auditable, and is a real virtue.

---

## 4. Work No. 11 — "Methodology of determination of the magnetic field H in the centre of Mass-Charge Objects"

### 4.1 What it claims

A two-step recipe for the field at the *centre* of any star, planet, galactic nucleus, UFO or rocket
engine:

1. `I_centre = H_surface × r_body` — invert the surface field to get a fictitious central current;
2. `H_centre = I_centre / (2π × 1 m)` — evaluate that current's field at a 1-metre "plasma core".

Applied to ten Solar System bodies in a table. Plus two side claims: that fusion runs in planetary
cores (Note 2), and that UFOs and rockets are the same kind of object (Note 1).

### 4.2 Recomputation of the entire page-3 table

I recomputed both derived columns from the manuscript's own H_surface and r for all ten rows.

| Body | q (C) | H_surf (Oe) | r (m) | I his | **I calc** | Δ | H_c his | **H_c calc** | Δ |
|---|---|---|---|---|---|---|---|---|---|
| Sun | 1.9·10²⁰ | 1.66·10⁵ | 6.9·10⁸ | 9.1·10¹⁵ | 9.117·10¹⁵ | −0.2% | 1.4·10¹⁵ | 1.451·10¹⁵ | −3.5% |
| Mercury | 0.03·10¹⁴ | 0.0026 | 2.4·10⁶ | 5·10⁵ | 4.967·10⁵ | +0.7% | 7.9·10⁴ | 7.905·10⁴ | −0.1% |
| Venus | 4.66·10¹⁴ | 0.4 | 6.2·10⁶ | 1.97·10⁸ | 1.974·10⁸ | −0.2% | 3.14·10⁷ | 3.142·10⁷ | −0.1% |
| Earth | 5.72·10¹⁴ | 0.5 | 6.37·10⁶ | 2.53·10⁸ | 2.535·10⁸ | −0.2% | 4·10⁷ | 4.035·10⁷ | −0.9% |
| Mars | 0.6·10¹⁴ | 0.05 | 3.4·10⁶ | 1.35·10⁷ | 1.353·10⁷ | −0.2% | 2·10⁶ | 2.154·10⁶ | −7.1% |
| Jupiter | 1.82·10¹⁷ | 159 | 71·10⁶ | 9·10¹¹ | 8.986·10¹¹ | +0.2% | 1.4·10¹¹ | 1.430·10¹¹ | −2.1% |
| **Saturn** | 5.44·10¹⁶ | 47 | 60·10⁶ | **1.39·10¹⁰** | **2.245·10¹¹** | **−93.8%** | 3.5·10¹⁰ | 3.573·10¹⁰ | −2.0% |
| **Uranus** | 8.32·10¹⁵ | 7.37 | 23.8·10⁶ | **2.2·10¹¹** | **1.396·10¹⁰** | **+1476%** | 2.2·10⁹ | 2.222·10⁹ | −1.0% |
| Neptune | 9.85·10¹⁵ | 8.6 | 22.3·10⁶ | 1.5·10¹⁰ | 1.527·10¹⁰ | −1.7% | 2.4·10⁹ | 2.430·10⁹ | −1.2% |
| Pluto | 5.15·10¹⁴ | 0.045 | 7.2·10⁶ | 2.58·10⁷ | 2.579·10⁷ | 0.0% | 4.1·10⁶ | 4.105·10⁶ | −0.1% |

**Three arithmetic faults, all previously unreported:**

**(a) Saturn and Uranus have their I_centre entries transposed.** Saturn's correct I is 2.245·10¹¹
(printed under Uranus); Uranus's correct I is 1.396·10¹⁰ (printed under Saturn). The H_centre column
for both rows is *correct*, so within the table column 5 and column 6 contradict each other for
exactly these two rows — H_c(Saturn) = 3.5·10¹⁰ cannot be obtained from I(Saturn) = 1.39·10¹⁰ by
dividing by 2π.

**(a) Mercury's charge is a factor 10 low.** The corpus's own constant is q/M = 9.568·10⁻¹¹ C/kg. I
computed q/M for every row: nine rows give 9.46–10.0 ·10⁻¹¹, and **Mercury gives 1.00·10⁻¹¹**.
With Work 7's own Mercury mass (0.3167·10²⁴ kg) the charge should be **0.303·10¹⁴ C**, not
0.03·10¹⁴ C. The slip is inherited from Work 7 p. 4 and propagates into Work 11.

**(a) Pluto's surface field is a factor 10 low.** I tested the rule H ∝ q against Earth for all ten
rows: nine give (H/H⊕)/(q/q⊕) = 0.98–1.01, and **Pluto gives 0.100**. Its H should be 0.45 Oe on the
corpus's own rule, not 0.045.

### 4.3 The "methodology" is one asserted proportionality

The H ∝ q normalisation above is exact to ±2% for nine of ten rows. Since q ∝ M by construction
(q/M = const), Work 11 and Work 7 are not deriving planetary fields from anything — they are
**asserting H ∝ M, calibrated on Earth**. There is no dynamo model, no rotation rate, no core
conductivity, no radius dependence. A one-parameter fit through one point.

That is testable in one line. Against measured equatorial surface dipole fields:

| Body | H his (Oe) | measured (G) | his/measured |
|---|---|---|---|
| Mercury | 0.0026 | 0.00195 | **1.3** |
| Venus | 0.4 | <10⁻⁵ | **>4·10⁴** |
| Earth | 0.5 | 0.31 | 1.6 |
| Mars | 0.05 | <5·10⁻⁵ | **>10³** |
| Jupiter | 159 | 4.17 | **38** |
| Saturn | 47 | 0.21 | **224** |
| Uranus | 7.37 | 0.23 | **32** |
| Neptune | 8.6 | 0.14 | **61** |
| Pluto | 0.045 | ~0 | **≫10⁴** |
| Sun (photosphere) | 1.66·10⁵ | ~1 | **1.7·10⁵** |

**Venus is the decisive case.** It has 0.815 of Earth's mass, so H ∝ M predicts 0.8 of Earth's field.
It has no measurable intrinsic dipole — the observed upper limit is below 10⁻⁵ of Earth's. Mars is the
same story at 10³. A mass-proportional field cannot accommodate two bodies of ordinary planetary mass
with no field at all, and the standard explanation (dynamo action requires a *convecting, rotating,
conducting* core, which Venus lacks) is exactly the physics the framework discards.

**Note (d):** the Work 7 commentary says "H_Jupiter = 159 Oersted (15.9 mT) is broadly consistent with
Jupiter's actual surface field… within an order of magnitude." 159 G / 4.17 G = **38**. That is not
within an order of magnitude, and the editor's own text elsewhere gives the measured value as ~0.4 mT
against his 16 mT, which is the same factor 40. The claim of consistency is not supported by the
numbers in the same paragraph.

**Note:** the corpus's single best planetary agreement — Mercury at 1.3× — rests on the factor-10
charge slip identified in §4.2. Corrected, the GCD value is 0.0265 Oe against a measured ~0.00195 Oe,
i.e. **13.6× high**, in line with the other planets. The agreement is an artefact of the error.

### 4.4 The two-step formula is internally inconsistent

Step 1 uses `H = I/r`. Step 2 uses `H = I/(2πr)`. **These are different formulas for the same
geometry, applied in consecutive lines.** Neither matches a physical configuration exactly:

- infinite straight wire: H = I/(2πr);
- single loop, at centre: H = I/(2r).

Used consistently with H = I/(2πr) at both ends, the answer would be
H_centre = H_surface × r_body/r_core = 39.8 × 6.37·10⁶ = **2.535·10⁸ A/m**, i.e. **2π = 6.28× larger**
than his 4·10⁷. The internal inconsistency is worth exactly a factor 2π; the physical inconsistency is
much larger, because a **dipole** field (which is what a planetary field is) falls as 1/r³, not 1/r. A
naive 1/r³ back-extrapolation from Earth's surface to r = 1 m gives 0.5 × (6.37·10⁶)³ =
**1.29·10²⁰ Oe** — which demonstrates that the extrapolation is meaningless in either form, since the
external multipole expansion does not describe the field *inside* the source region at all.

### 4.5 The H_centre values against physics

H_centre(Sun) = 1.4·10¹⁵ A/m. Converting: 1.4·10¹⁵/79.577 = **1.759·10¹³ Oe**, and
B = μ₀H = **1.759·10⁹ T**.

- **Magnetic energy density** u = B²/2μ₀ = **1.23·10²⁴ J/m³**.
- **Mass-equivalent density** u/c² = **1.37·10⁷ kg/m³** — about **90× the actual solar core density**
  (1.5·10⁵ kg/m³). The field's own inertia would exceed the plasma's.
- **QED context:** the Schwinger critical field is B_crit = m²c³/(eℏ) = 4.41·10⁹ T. His value is
  **0.40 B_crit** — magnetar territory (magnetar surface fields 10¹⁰–10¹¹ T), not stellar-interior
  territory. Helioseismic and standard-solar-model constraints put radiative-zone fields below ~10 T.
  The prediction is high by **~8 orders of magnitude**.

### 4.6 Note 2 — fusion in planetary cores

Two independent failures:

- **Conditions.** Earth's outer core is ~5000–6000 K at ~10⁴ kg/m³. Fusion needs ≳10⁷ K. Short by
  **~3–4 orders of magnitude in temperature**.
- **Premise.** The stated evidence is "deposits of heavy elements above the Uranium group in Earth's
  depths." There are no natural deposits of transuranic elements. Terrestrial ore deposits are U (Z=92)
  and Th (Z=90) — both *at or below* the uranium threshold, both primordial (²³⁸U t½ = 4.47 Gyr,
  ²³²Th t½ = 14.05 Gyr, comparable to Earth's age). The trace ²⁴⁴Pu and ²³⁹Pu that exist are from
  primordial residue and from neutron capture on ²³⁸U (the Oklo natural reactor), not fusion.
  Additionally, fusion does not produce actinides in any case — the r-process in supernovae and
  neutron-star mergers does.

**Verdict: (b) — no arithmetic to check, an unphysical premise resting on a factual error about ores.**

### 4.7 A transcription caveat

The free-particle set is written throughout as `{e⁻ e⁺ p⁻ n²}`. As transcribed this reads
"electron, positron, **antiproton**, and n-squared". Almost certainly p⁺ and n⁰ in the original. I flag
it because any quantitative reading of the "quasi-neutrality" argument depends on the signs, and the
extracted text as it stands does not define them.

### 4.8 Genuine content in Work 11

- The 79.6 A/m per Oersted conversion is applied correctly in all ten rows.
- The four comparative field strengths quoted from the ФЭС (0.5 Oe at Earth's surface, ~50 Oe at
  atomic distances, 5·10⁵ Oe at ferromagnetic ion cores, 8·10⁶ Oe for ¹⁶⁶Dy) are approximately right
  and correctly sourced — hyperfine fields at rare-earth nuclei genuinely do reach 10⁶–10⁷ Oe.
- The underlying observation in the p. 2 footnote — that fields at the individual-particle scale are
  vastly larger than bulk macroscopic fields because bulk motion self-cancels — is correct standard
  physics **(c)**, described in unusual language.
- Eight of the ten table rows are internally arithmetically clean to ≤2%.

---

## 5. Work No. 6 — 18-year planetary and 12-year constellational cycles (characterisation only)

Four pages applying GCD to political economy. A society passes four stages: formation 18 yr, stable
development **36 yr** (twice the unit, no derivation offered), decline 18 yr, dissolution 18 yr. USSR
markers at 1917 / 1935 / 1953 / 1971 / 1989 / 2007. A parallel 12-year "constellational" cycle
(1917, 1929, 1941, 1953, 1965, 1977, 1989, 2001) is invoked without derivation; the zodiacal 12-year
period is not attributed. Comparative 18-year plots for USSR/Russia, PRC, USA, EU and Japan converge
on a marker at 2024.

The single testable claim: on **21 June 2024 (summer solstice)** the Solar System passes **point 6** of
the Orion Arm and civilisation undergoes a "fifty-percent transition" from Intellectual to Spiritual.
Point 6 is one of the eight markers I–VIII on the Work 5 p. 5 orbital diagram, so the spacing is
26 000/8 = **3250 years per point** — internally consistent with the "3250 years" period of Work 10,
and the only respect in which the astrology is coupled to the astronomy. Neither the 18-year nor the
12-year period is derivable from 3250. The date has passed.

Cites Kant (*Critique of Practical Reason*, the starry-heavens/moral-law passage) and the author's own
1991–1997 КПРФ Duma submissions, which dates composition to the late 1990s / early 2000s.

Not audited. There is nothing quantitative to audit: no cycle period is derived from any physical
quantity in the corpus.

---

## 6. Work No. 10 — philosophical theses (characterisation only)

Four pages of synthetic doctrine: time-flow rate as a function of gravitational-charge energy density;
personality and civilisation as a triad Spirituality / Intellect / Material Code; a 2000-year cycle of
dominance among the three; a **412-year** Pythagorean reincarnation period for the
"Energy-Information Field"; a mapping of the 10 planets onto 10 generations of a human genetic cycle;
and a **6500-year** civilisational flood cycle with Atlantis as the previous exemplar and a forecast
flood at the close of the present period. Restates the 21 June 2024 "point 6" prediction of Work 6 in
two places.

Citations: Plato, Pythagoras, Aristotle, Kant, Darwin, Marx, the Old Testament, and unspecified
Tibetan manuscripts — all by tradition or author only, no page references.

The numerology is internally arranged around 26 000/8 = 3250 (half of 6500) but no period is derived
from a physical quantity. Not audited.

---

## 7. Cross-work inconsistency table

Quantities given one value in one place and a different value elsewhere. Rows 1–2 are the two you
already had; rows 3–16 are new from this pass. "W" = Work.

| # | Quantity | Value A | Value B | Ratio | Notes |
|---|---|---|---|---|---|
| 1 | Excess-charge ratio | 1 e⁻ per **5·10¹⁷** p (W1 p.5, W3 p.2, W7 p.4, W8 p.4) | **5·10¹⁸** (per your W7 audit / preprints) | 10× | Corpus text is uniformly 5·10¹⁷; the 5·10¹⁸ appears only in the 2026 restatement. The corpus's own q/M = 9.568·10⁻¹¹ C/kg requires 5·10¹⁷ (I verified: 0.2989·10²⁷/5·10¹⁷ × 1.6·10⁻¹⁹ = 9.57·10⁻¹¹). **The 5·10¹⁸ version is the one that breaks the corpus's own q values.** |
| 2 | Solenoid current | **1.65·10³ A** (W8 addendum p.12, ball-lightning sheet) | **10⁴–10⁵ A** (W2 p.6) | 6–60× | W8 note calls 1.65 kA "bare" and W2's uplift an ad-hoc "Si interstitial permeability" factor. W3's editorial note quotes the range three different ways: "10³–10⁵" (p.41), "10⁴–10⁵" (p.859), "10³–10⁵" (p.1264). |
| 3 | **Solar radius** | **7·10⁸ m** (W8 p.3, density calc) | **6.9·10⁸ m** (W11 p.2 + table) and **696 000 km = 6.96·10⁸ m** (W5/W9/W12 tables) | 1.4% | Three different R☉ in the same corpus, one of them cubed. Using 6.96·10⁸ instead of 7·10⁸ changes his ρ̄ by 1.7%. |
| 4 | **Jupiter orbital velocity** | **13 km/s** (W5 p.3+p.4, W9 p.2+p.3) | **13.4 km/s** (W12 p.3) | 3% | True value 13.06 km/s, so W5/W9 are right and W12 "refined" it in the wrong direction. |
| 5 | **Retrograde planets** | Venus + **Saturn** (W5 p.8 text) | Venus + **Uranus** (W5 p.3 table, W9 p.2, W12 p.2) | — | Self-contradictory *within Work 5*. Saturn is prograde (10.7 h). Removes one of the two data points supporting the prominence-ejection origin. |
| 6 | **Laplacian nebular hypothesis** | rejected outright; planets formed by prominence ejection (W5 p.7–8) | accommodated as complementary; solar rotation plane at "averaged position" between Laplacian circles and GCD spirals (W12 p.6) | — | A reversal of position, not a numerical conflict, but it means W5 and W12 cannot both be cited as the corpus's cosmology. |
| 7 | **q_Mercury** | **0.03·10¹⁴ C** (W7 p.4, W11 p.3) | corpus rule q = 9.568·10⁻¹¹ × M requires **0.303·10¹⁴ C** | 10× | I verified q/M for all ten bodies: nine give 9.46–10.0·10⁻¹¹, Mercury alone gives 1.00·10⁻¹¹. The corpus's best planetary field agreement (Mercury 1.3× vs measurement) is produced by this slip. |
| 8 | **H_surface Pluto** | **0.045 Oe** (W11 p.3) | corpus rule H = (q/q⊕)·0.5 requires **0.45 Oe** | 10× | Same test: nine rows normalise to 0.98–1.01, Pluto to 0.100. |
| 9 | **I_centre Saturn / Uranus** | Saturn 1.39·10¹⁰, Uranus 2.2·10¹¹ (W11 p.3 col. 5) | his own H×r gives Saturn 2.245·10¹¹, Uranus 1.396·10¹⁰ | 16× each, swapped | The H_centre column (col. 6) is correct for both, so cols. 5 and 6 of the same table contradict each other on these two rows. |
| 10 | **Solar mean density** | ρ̄ = 2·10³ kg/m³ (W8 p.3) | ρ = 1.4 g/cm³ = 1.4·10³ kg/m³ (W5/W9/W12 planetary tables, Sun header) | 1.43× | **The corpus contains the correct solar density in three places and the wrong one in the place where it is used.** W8's formula drops the 4/3 (I get 1856 from his own formula, and 1392 with the 4/3 restored). |
| 11 | **Solar core density from the literature** | "hydrogen pressure **100 g/cm³**" (W8 p.4 note) | accepted 150 g/cm³, and it is a density not a pressure | 1.5× + unit | Two errors in one citation. |
| 12 | **B☉ = 16.65 T identified as** | the Sun's **surface** field (W8 addendum p.9: B_Sun_Max = μ₀·H_surface) | the Sun's **core** field ("Rosetta Stone" doc, lines 950, 1122: "Bsun_core = 16.65 Tesla") | — | The corpus's own core-field value is W11's **1.76·10⁹ T**, i.e. **10⁸× larger**. The "16.65 T vs WHAM 17 T, 2.1% gap" argument built on this in the Rosetta Stone compares a *surface* field to a *device* field. |
| 13 | **16.65 T "independently derived"** | Rosetta Stone: "Works №7 and №11 **independently** derive 16.65 T" | W8 addendum p.9 is the single derivation; W7's appendix and W11's table both take H☉ = 1.66·10⁵ Oe as an **input** | — | The three appearances are one chain: q☉/q⊕ × 0.5 Oe. Not independent confirmation. |
| 14 | **Reactor fuel** | d + ⁶Li → 2 ⁴He, chosen **because aneutronic** (W2 p.7) | d + d, which is ~50% neutron-producing (W8 title and throughout) | — | W8 does not address the conflict. Its own p. 6 also writes the reaction as "{d+d → d+t+p}", which does not balance (A: 4→6, Z: 2→3). |
| 15 | **Ignition condition** | charge density >0.12·10¹³ e⁻/m³ (W8 p.4 box) | Lawson/triple product; never mentioned anywhere in the corpus | — | Not a conflict between works but a conflict between the corpus and the field. His condition corresponds to a net charge fraction of 1.2·10⁻¹⁸ in a fusion-density plasma. |
| 16 | **H formula for a Mass-Charge Object** | H = I/r (W11 p.1, step 1) | H = I/(2πr) (W11 p.2, step 2; also W8 addendum p.7³ "H = I·const/r") | 2π | Two formulas for one geometry, consecutive lines, same worked example. |

### Editorial-apparatus errors found (category d)

Recorded separately because they are in the CARI commentary, not the manuscripts, and an external
reader is more likely to quote the commentary:

| Where | Claim | What I find |
|---|---|---|
| W5 crit. ed., Translator's Note to p. 3 | rotation-velocity column "in m/sec for Earth and km/h elsewhere; units not consistent" | All eight entries are m/s and all are correct to ≤2% except Neptune (−11%). No unit inconsistency exists. |
| W7 crit. ed., pp. 879 and 946–947 | "H_Jupiter = 159 Oe (15.9 mT) is broadly consistent with Jupiter's actual surface field… within an order of magnitude" | 159 G / 4.17 G = **38**; 15.9 mT / 0.4 mT = **40**. Not within an order of magnitude. |
| W5/W9 crit. ed. | the 29.78/Earth-orbital-speed agreement is "a coincidence of the arithmetic" | Stated as settled. It is 0.018% agreement with a dimensioned constant in the cited textbook, on a factor whose stated derivation is a ruler reading; the commentary asserts a conclusion it does not test. |
| W8 crit. ed., Critical Point 5 | "32 solenoids" is a "round-number engineering choice"; a different count scales the current proportionally | The scaling claim is only true within an invalid formula. N/L = 250 × 32 is not a valid solenoid turn density, and 32 radial solenoids cancel at the centre. |
| W9 crit. ed., Critical Point 2 | the appendix figure is "not in the present collection", so the 147/15.5 inputs are "not independently verifiable" | Correct at the time, superseded by W12 p. 4. But the deeper point survives: even with the figure, the inputs are ruler readings on a celestial-sphere chart. |

---

## 8. Summary of what is actually right

Being fair, across the five audited works:

1. **The Work 5/9/12 planetary table.** Nine orbital velocities and eight equatorial rotation speeds,
   hand-computed from a/P and R/P, all correct to sub-percent bar one. Solar density and rotation
   velocity likewise. This is careful, competent arithmetic.
2. **The Keplerian insight** — orbital speed rises inward and is independent of the orbiting mass —
   is correct, correctly derived from his own table, and correctly stated.
3. **The reading of the apex velocity** (Bakulin §165): the 20 km/s figure genuinely *is* relative to
   the local standard of rest, not absolute. A real interpretive point, correctly spotted in a
   textbook.
4. **The commutator vs slip-ring distinction** in Work 3 Schemes 1/2 is real engineering, correctly
   identified without the standard vocabulary.
5. **The AC/DC field discrepancy** he reports is almost certainly a real instrument artefact
   (RMS vs peak, DC-responding magnetometer time-averaging), honestly recorded even though the
   inference drawn from it is wrong.
6. **The d+d reaction set** in Work 8 is the correct set of three channels, with the two dominant ones
   correctly named; Q-values are not stated but the reactions are real.
7. **All unit conversions** I checked are right: 1 Oe = 79.6 A/m, 1 pc = 3.084·10¹³ km, B = μμ₀H,
   250 turns/m from 4 mm pitch, I = Q/t.
8. **The "hyperfine fields exceed bulk fields because bulk motion self-cancels"** argument in
   Work 11 p. 2 is correct standard physics.
9. **Self-correction across revisions.** Work 9/12 fix Work 5's Saturn error; Work 12 retreats from
   Work 5's rejection of Laplace. The corpus revises itself, which is more than many such bodies of
   work do.
10. **Derivational transparency.** Work 8's addendum states every input of its headline number. That is
    precisely why the chain could be audited at all, and it is a genuine methodological virtue.

## 9. Summary of the structural pattern

Across all five works the same shape recurs, and it is worth stating plainly because it determines
how the corpus should be cited:

**The arithmetic is almost always right. The dimensional bookkeeping is almost always wrong.**

- mass density used as pressure (W8: "2·10³ kg/m³ ~ 2000 atm");
- a length ratio on a celestial-sphere chart used as a velocity ratio (W5/9/12: 461.58/15.5);
- a dimensioned constant (Earth's orbital speed in km/s) appearing as a dimensionless multiplier;
- turns-per-metre multiplied by a solenoid *count* (W8: 250 × 32);
- two different H-vs-I formulas in consecutive lines (W11);
- a 1/r extrapolation applied to a dipole field, and applied inside the source region (W11).

Of the ~60 discrete arithmetic operations I recomputed, **five are wrong** (W8's 4/3 factor, W5's
Neptune rotation speed, W11's Saturn/Uranus transposition, W7/W11's Mercury charge, W11's Pluto
field) — an error rate of about 8%, which for hand calculation is respectable. Of the ~12 distinct
physical premises, **none survives comparison with measurement**, and three (Venus's absent magnetic
field, the CMB dipole, the mass budget of solar prominences) fail by four or more orders of magnitude
against data that were available when the works were written.
