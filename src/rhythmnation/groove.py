"""Groove analysis — swing, velocity, microtiming."""

from dataclasses import dataclass
import math

@dataclass
class Groove:
    """A groove pattern with velocity and timing offsets.
    
    velocities: MIDI velocities (0-127) for each step
    offsets: timing offsets in ms from the grid (-50 to +50)
    """
    velocities: list[int]
    offsets: list[float]
    
    @property
    def length(self) -> int:
        return len(self.velocities)
    
    @property
    def average_velocity(self) -> float:
        return sum(self.velocities) / max(len(self.velocities), 1)

def swing_factor(grid: list[float], swing_amount: float = 0.0) -> list[float]:
    """Apply swing to a grid of beat positions.
    
    swing_amount: 0 = straight, 1 = full triplet swing
    """
    result = grid.copy()
    for i in range(1, len(result), 2):
        # Push off-beats later
        swing_offset = swing_amount * (result[i] - result[i-1]) * 0.33
        result[i] += swing_offset
    return result

def groove_velocity(pattern: list[int], accent_pattern: list[int] | None = None) -> list[int]:
    """Convert a binary pattern to velocity values with optional accents."""
    accent = accent_pattern or [1] * len(pattern)
    return [min(127, p * 80 * a) for p, a in zip(pattern, accent)]

def microtiming(offsets: list[float], humanize: float = 0.0) -> list[float]:
    """Add human-like microtiming to note offsets."""
    import random
    return [o + random.gauss(0, humanize) for o in offsets]
