"""Meter and time signature mathematics."""

from dataclasses import dataclass

@dataclass
class Meter:
    """A time signature.
    
    numerator: beats per measure
    denominator: beat unit (4 = quarter note, 8 = eighth note)
    """
    numerator: int
    denominator: int
    
    @property
    def is_simple(self) -> bool:
        """Simple meter (2, 3, 4)."""
        return self.numerator in (2, 3, 4)
    
    @property
    def is_compound(self) -> bool:
        """Compound meter (grouped in 3s)."""
        return self.numerator % 3 == 0 and self.numerator > 3
    
    @property
    def is_odd(self) -> bool:
        """Odd meter (5, 7, 11, etc)."""
        return self.numerator not in (2, 3, 4, 6, 9, 12)
    
    @property
    def beat_count(self) -> int:
        """Number of main beats per measure."""
        if self.is_compound:
            return self.numerator // 3
        return self.numerator
    
    @property
    def subdivision(self) -> int:
        """Subdivisions per beat."""
        if self.is_compound:
            return 3
        return 2

def downbeats(measures: int, meter: Meter) -> list[int]:
    """Positions of downbeats across multiple measures."""
    return [i * meter.numerator for i in range(measures)]

def subdivisions(meter: Meter, subdivision_level: int = 2) -> list[int]:
    """Generate subdivision grid for one measure."""
    total = meter.numerator * subdivision_level
    return list(range(total))

def time_signature_change(meters: list[Meter], repeats: list[int] | None = None) -> list[Meter]:
    """Generate a sequence of time signature changes.
    
    Args:
        meters: List of meters to cycle through
        repeats: How many times to repeat each meter (default: 1 each)
    """
    reps = repeats or [1] * len(meters)
    result = []
    for meter, rep in zip(meters, reps):
        result.extend([meter] * rep)
    return result
