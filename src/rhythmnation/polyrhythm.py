"""Polyrhythm mathematics."""

from dataclasses import dataclass
from math import gcd
from functools import reduce

def lcm(a: int, b: int) -> int:
    """Least common multiple."""
    return abs(a * b) // gcd(a, b)

@dataclass
class Polyrhythm:
    """A polyrhythm defined by multiple pulse rates.
    
    Example: Polyrhythm([3, 2]) is a 3:2 polyrhythm (hemiola).
    """
    rates: list[int]
    
    @property
    def cycle_length(self) -> int:
        """Length of the full cycle in subdivisions."""
        return reduce(lcm, self.rates)
    
    @property
    def pattern(self) -> list[list[int]]:
        """Generate the full pattern for each voice."""
        cycle = self.cycle_length
        return [[1 if i % (cycle // r) == 0 else 0 for i in range(cycle)] for r in self.rates]
    
    @property
    def density(self) -> float:
        """Average density (hits per subdivision)."""
        total_hits = sum(self.rates)
        return total_hits / self.cycle_length
    
    @property
    def complexity(self) -> float:
        """Complexity score based on LCM relative to sum."""
        return self.cycle_length / sum(self.rates)

def lcm_polyrhythm(rates: list[int]) -> int:
    """Compute LCM of a set of rates."""
    return reduce(lcm, rates)

def polyrhythm_cycle(rates: list[int]) -> list[int]:
    """Compute the combined rhythm pattern (any voice hits)."""
    cycle = lcm_polyrhythm(rates)
    combined = [0] * cycle
    for r in rates:
        step = cycle // r
        for i in range(r):
            combined[i * step] = 1
    return combined
