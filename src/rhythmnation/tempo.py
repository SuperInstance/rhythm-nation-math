"""Tempo and timing mathematics."""

from dataclasses import dataclass
from typing import Callable

@dataclass
class Tempo:
    """Tempo in BPM with conversion utilities."""
    bpm: float
    
    @property
    def ms_per_beat(self) -> float:
        """Milliseconds per beat."""
        return 60000.0 / self.bpm
    
    @property
    def hz(self) -> float:
        """Frequency in Hz."""
        return self.bpm / 60.0
    
    @property
    def period(self) -> float:
        """Period in seconds."""
        return 60.0 / self.bpm

def bpm_to_ms(bpm: float) -> float:
    """Convert BPM to milliseconds per beat."""
    return 60000.0 / bpm

def ms_to_bpm(ms: float) -> float:
    """Convert milliseconds per beat to BPM."""
    return 60000.0 / ms

def tempo_curve(start_bpm: float, end_bpm: float, steps: int,
                curve: str = "linear") -> list[float]:
    """Generate a tempo curve from start to end BPM.
    
    Args:
        start_bpm: Starting tempo
        end_bpm: Ending tempo
        steps: Number of steps
        curve: "linear", "exponential", or "logarithmic"
    
    Returns:
        List of BPM values
    """
    if curve == "linear":
        return [start_bpm + (end_bpm - start_bpm) * i / max(steps - 1, 1) for i in range(steps)]
    elif curve == "exponential":
        ratio = end_bpm / max(start_bpm, 0.1)
        return [start_bpm * ratio ** (i / max(steps - 1, 1)) for i in range(steps)]
    elif curve == "logarithmic":
        import math
        log_start = math.log(max(start_bpm, 0.1))
        log_end = math.log(max(end_bpm, 0.1))
        return [math.exp(log_start + (log_end - log_start) * i / max(steps - 1, 1)) for i in range(steps)]
    else:
        raise ValueError(f"Unknown curve type: {curve}")
