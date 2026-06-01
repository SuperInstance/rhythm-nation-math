# rhythm-nation-math

> Rhythm mathematics for Python — polyrhythms, syncopation, groove, meter, and tempo as formal math.

## What This Does

`rhythm-nation-math` provides pure mathematics for musical rhythm. It models time signatures, polyrhythms, syncopation scores, groove patterns with velocity and microtiming, and tempo curves. No audio output — just the math. Use it for music information retrieval, generative music systems, rhythm analysis, or building sequencers and drum machines.

## The Cultural Root

Polyrhythms are central to West African, Afro-Cuban, and Brazilian musical traditions. A 3:2 polyrhythm (hemiola) creates tension by playing three against two. The mathematical insight: **polyrhythms are least common multiple problems** — a 3:2 polyrhythm repeats every LCM(3,2) = 6 subdivisions. Syncopation measures the tension between expected and actual accents, quantified by the Longuet-Higgins/Lee model from music theory.

## Install

```bash
pip install rhythm-nation-math
```

## Quick Start

```python
from rhythmmath.polyrhythm import Polyrhythm
from rhythmmath.syncopation import syncopation_score, offbeat_density, rhythmic_entropy
from rhythmmath.groove import Groove, swing_factor, groove_velocity, microtiming
from rhythmmath.meter import Meter
from rhythmmath.tempo import Tempo, tempo_curve

# Polyrhythms
pr = Polyrhythm([3, 2])  # 3:2 hemiola
print(f"Cycle length: {pr.cycle_length()}")  # 6
print(f"Pattern: {pr.pattern()}")            # [[1,0,0,1,0,0], [1,0,1,0,1,0]]
print(f"Density: {pr.density():.2f}")        # 0.58
print(f"Complexity: {pr.complexity():.2f}")  # 0.33

# Syncopation
pattern = [1, 0, 0, 1, 0, 0, 1, 0]  # beats in 4/4
score = syncopation_score(pattern, meter_numerator=4)
density = offbeat_density(pattern, meter_numerator=4)
entropy = rhythmic_entropy(pattern)

# Meter classification
m = Meter(numerator=7, denominator=8)
print(f"Odd meter: {m.is_odd()}")       # True
print(f"Beats: {m.beat_count()}")        # 7
print(f"Subdivisions: {m.subdivision()}") # 2

# Tempo
t = Tempo(bpm=120)
print(f"ms/beat: {t.ms_per_beat()}")  # 500.0
print(f"Hz: {t.hz():.2f}")            # 2.0

# Tempo curve (ritardando)
curve = tempo_curve(start_bpm=120, end_bpm=60, steps=8)
# [120, 111.4, 102.9, 94.3, 85.7, 77.1, 68.6, 60]

# Groove with velocity and timing
g = Groove(velocities=[100, 80, 90, 70], offsets=[0, 5, 0, -3])
swung = swing_factor(g.offsets, amount=0.5)
humanized = microtiming(g.offsets, amount=3.0)
```

## API Reference

### `polyrhythm` module

#### `Polyrhythm(rates: list[int])`
```python
class Polyrhythm:
    def cycle_length(self) → int        # LCM of all rates
    def pattern(self) → list[list[int]] # Binary pattern per voice
    def density(self) → float           # Average hits per subdivision
    def complexity(self) → float        # LCM / sum of rates
```

#### `lcm_polyrhythm(rates) → int`
LCM of a set of integer rates.

#### `polyrhythm_cycle(rates) → list[int]`
Combined binary pattern (any voice hits).

### `syncopation` module

#### `syncopation_score(pattern, meter_numerator=4) → float`
Longuet-Higgins/Lee syncopation measure. Higher = more syncopated.

#### `offbeat_density(pattern, meter_numerator=4) → float`
Fraction of hits falling on off-beats. 0 = all on-beat, 1 = all off-beat.

#### `rhythmic_entropy(pattern) → float`
Shannon entropy of the interval distribution between onsets.

### `groove` module

#### `Groove(velocities, offsets)`
```python
@dataclass
class Groove:
    velocities: list[int]  # MIDI velocities 0-127
    offsets: list[float]   # Timing offsets in ms
```

#### `swing_factor(grid, amount=0) → list[float]`
Apply swing. 0 = straight, 1 = full triplet swing.

#### `groove_velocity(pattern, accent_pattern=None) → list[int]`
Convert binary pattern to velocity values with optional accents.

#### `microtiming(offsets, amount=1.0, seed=None) → list[float]`
Add human-like microtiming jitter.

### `meter` module

#### `Meter(numerator, denominator)`
```python
@dataclass
class Meter:
    numerator: int    # Beats per measure
    denominator: int  # Beat unit (4 = quarter note)

    def is_simple(self) → bool     # 2, 3, or 4
    def is_compound(self) → bool   # Grouped in 3s
    def is_odd(self) → bool        # 5, 7, 11, etc.
    def beat_count(self) → int
    def subdivision(self) → int    # Subdivisions per beat
```

#### `downbeats(measures, meter) → list[int]`
Positions of downbeats across multiple measures.

#### `time_signature_change(meters, repeats=1) → list[Meter]`
Generate a sequence of time signature changes.

### `tempo` module

#### `Tempo(bpm)`
```python
@dataclass
class Tempo:
    bpm: float

    def ms_per_beat(self) → float
    def hz(self) → float           # Frequency
    def period(self) → float       # Period in seconds
```

#### `bpm_to_ms(bpm) → float`
#### `ms_to_bpm(ms) → float`
#### `tempo_curve(start_bpm, end_bpm, steps, curve="linear") → list[float]`
Generate a tempo curve. Curve types: `"linear"`, `"exponential"`, `"logarithmic"`.

## How It Works

**Polyrhythms:** For rates [r₁, r₂, ...], the cycle length is LCM(r₁, r₂, ...). Each voice vᵢ has a hit at position k if k mod rᵢ == 0. Complexity = LCM / Σ(rᵢ).

**Syncopation (Longuet-Higgins/Lee):** Each beat position has a "weight" based on its metrical position. Syncopation = Σ (weight of rest − weight of preceding onset) for every syncopated pair.

**Shannon Entropy:** H = −Σ p(i) log₂ p(i) where p(i) is the frequency of interval length i between consecutive onsets.

**Swing:** Off-beat positions (even indices in a grid) are delayed by `amount × grid_spacing / 3`.

## The Math

**LCM of Polyrhythms:** L = lcm(r₁, r₂, ..., rₙ). The pattern repeats every L subdivisions.

**Longuet-Higgins/Lee Syncopation:** For each onset at position j, if the following rest position j+1 has higher metrical weight, syncopation += w(j+1) − w(j).

**Shannon Entropy of Rhythm:** H = −Σₖ p(Δₖ) log₂ p(Δₖ) where Δₖ are inter-onset intervals.

**Tempo Conversion:** ms/beat = 60000 / BPM. Hz = BPM / 60.

## License

MIT
