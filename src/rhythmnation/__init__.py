"""Rhythm Nation Mathematics — The mathematics of rhythm and groove."""

from .tempo import Tempo, bpm_to_ms, ms_to_bpm, tempo_curve
from .polyrhythm import Polyrhythm, lcm_polyrhythm, polyrhythm_cycle
from .groove import Groove, swing_factor, groove_velocity, microtiming
from .syncopation import syncopation_score, offbeat_density, rhythmic_entropy
from .meter import Meter, downbeats, subdivisions, time_signature_change

__all__ = [
    "Tempo", "bpm_to_ms", "ms_to_bpm", "tempo_curve",
    "Polyrhythm", "lcm_polyrhythm", "polyrhythm_cycle",
    "Groove", "swing_factor", "groove_velocity", "microtiming",
    "syncopation_score", "offbeat_density", "rhythmic_entropy",
    "Meter", "downbeats", "subdivisions", "time_signature_change",
]
