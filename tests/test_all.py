"""Tests for rhythm-nation-math."""
import sys
sys.path.insert(0, "src")

from rhythmnation.tempo import Tempo, bpm_to_ms, ms_to_bpm, tempo_curve
from rhythmnation.polyrhythm import Polyrhythm, lcm_polyrhythm, polyrhythm_cycle
from rhythmnation.groove import Groove, swing_factor, groove_velocity
from rhythmnation.syncopation import syncopation_score, offbeat_density, rhythmic_entropy
from rhythmnation.meter import Meter, downbeats, subdivisions, time_signature_change

import math

def test_tempo_basic():
    t = Tempo(120)
    assert abs(t.ms_per_beat - 500.0) < 0.01
    assert abs(t.hz - 2.0) < 0.01
    assert abs(t.period - 0.5) < 0.01

def test_bpm_to_ms():
    assert abs(bpm_to_ms(120) - 500.0) < 0.01
    assert abs(bpm_to_ms(60) - 1000.0) < 0.01

def test_ms_to_bpm():
    assert abs(ms_to_bpm(500) - 120.0) < 0.01

def test_tempo_curve_linear():
    curve = tempo_curve(100, 200, 5, "linear")
    assert len(curve) == 5
    assert abs(curve[0] - 100) < 0.01
    assert abs(curve[-1] - 200) < 0.01

def test_tempo_curve_exponential():
    curve = tempo_curve(100, 200, 5, "exponential")
    assert len(curve) == 5
    assert curve[0] < curve[-1]

def test_tempo_curve_logarithmic():
    curve = tempo_curve(100, 200, 5, "logarithmic")
    assert len(curve) == 5

def test_polyrhythm_hemiola():
    p = Polyrhythm([3, 2])
    assert p.cycle_length == 6
    assert abs(p.density - 5/6) < 0.01

def test_polyrhythm_complexity():
    p = Polyrhythm([3, 2])
    assert p.complexity == 6/5

def test_polyrhythm_pattern():
    p = Polyrhythm([3, 2])
    patterns = p.pattern
    assert len(patterns) == 2
    assert len(patterns[0]) == 6

def test_lcm_polyrhythm():
    assert lcm_polyrhythm([3, 4]) == 12
    assert lcm_polyrhythm([2, 3, 5]) == 30

def test_polyrhythm_cycle():
    cycle = polyrhythm_cycle([3, 2])
    assert len(cycle) == 6
    assert sum(cycle) == 4  # 3 + 2 - 1 overlap at 0

def test_groove_basic():
    g = Groove([100, 80, 90, 70], [0, 5, -3, 10])
    assert g.length == 4
    assert abs(g.average_velocity - 85.0) < 0.01

def test_swing_factor():
    grid = [0.0, 0.5, 1.0, 1.5]
    swung = swing_factor(grid, 0.5)
    assert len(swung) == 4
    assert swung[0] == 0.0  # On-beats don't move

def test_groove_velocity():
    pattern = [1, 0, 1, 0]
    vel = groove_velocity(pattern)
    assert len(vel) == 4
    assert vel[1] == 0
    assert vel[0] > 0

def test_groove_velocity_accent():
    pattern = [1, 1, 1, 1]
    accent = [2, 1, 2, 1]
    vel = groove_velocity(pattern, accent)
    assert vel[0] > vel[1]

def test_syncopation_basic():
    # All on downbeats = no syncopation
    pattern = [1, 0, 1, 0, 1, 0, 1, 0]
    score = syncopation_score(pattern, 4)
    assert score == 0.0

def test_syncopation_offbeat():
    # All on offbeats = high syncopation
    pattern = [0, 1, 0, 1, 0, 1, 0, 1]
    score = syncopation_score(pattern, 4)
    assert score > 0

def test_offbeat_density_all_on():
    pattern = [1, 0, 1, 0]
    assert abs(offbeat_density(pattern, 4) - 0.0) < 0.01

def test_offbeat_density_mixed():
    pattern = [1, 1, 1, 1]
    density = offbeat_density(pattern, 4)
    assert density > 0

def test_rhythmic_entropy_solid():
    pattern = [1, 1, 1, 1]
    entropy = rhythmic_entropy(pattern)
    assert entropy == 0.0  # All same interval

def test_rhythmic_entropy_varied():
    pattern = [1, 0, 1, 0, 0, 1, 0, 1]
    entropy = rhythmic_entropy(pattern)
    assert entropy > 0

def test_meter_basic():
    m = Meter(4, 4)
    assert m.is_simple
    assert not m.is_compound
    assert not m.is_odd
    assert m.beat_count == 4
    assert m.subdivision == 2

def test_meter_compound():
    m = Meter(6, 8)
    assert m.is_compound
    assert m.beat_count == 2
    assert m.subdivision == 3

def test_meter_odd():
    m = Meter(7, 8)
    assert m.is_odd
    assert m.beat_count == 7

def test_downbeats():
    m = Meter(4, 4)
    beats = downbeats(3, m)
    assert beats == [0, 4, 8]

def test_subdivisions():
    m = Meter(4, 4)
    subs = subdivisions(m, 2)
    assert len(subs) == 8

def test_time_signature_change():
    changes = time_signature_change([Meter(4, 4), Meter(3, 4)], [2, 1])
    assert len(changes) == 3
    assert changes[0].numerator == 4
    assert changes[2].numerator == 3

def test_tempo_60():
    t = Tempo(60)
    assert abs(t.ms_per_beat - 1000.0) < 0.01

def test_polyrhythm_single():
    p = Polyrhythm([4])
    assert p.cycle_length == 4
    assert p.complexity == 1.0

def test_syncopation_empty():
    assert syncopation_score([], 4) == 0.0

def test_offbeat_empty():
    assert offbeat_density([], 4) == 0.0

def test_entropy_single():
    assert rhythmic_entropy([1]) == 0.0

def test_entropy_two():
    assert rhythmic_entropy([1, 1]) == 0.0

def test_polyrhythm_4_3():
    p = Polyrhythm([4, 3])
    assert p.cycle_length == 12

def test_groove_empty():
    g = Groove([], [])
    assert g.length == 0
    assert g.average_velocity == 0.0

def test_meter_3_4():
    m = Meter(3, 4)
    assert m.is_simple
    assert m.beat_count == 3

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"FAIL: {t.__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed")
    exit(1 if failed else 0)
