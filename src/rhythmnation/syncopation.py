"""Syncopation metrics."""

import math
from collections import Counter

def syncopation_score(pattern: list[int], meter_numerator: int = 4) -> float:
    """Compute syncopation score for a rhythm pattern.
    
    Uses the Longuet-Higgins/Lee syncopation measure:
    syncopation = sum of (metric_weight - note_weight) for all syncopated notes.
    """
    n = len(pattern)
    if n == 0:
        return 0.0
    
    # Metric weights: strong beats have higher weight
    weights = []
    for i in range(n):
        beat_in_measure = i % meter_numerator
        if beat_in_measure == 0:
            weights.append(4.0)  # Downbeat
        elif beat_in_measure == meter_numerator // 2:
            weights.append(3.0)  # Middle beat
        elif beat_in_measure % 2 == 0:
            weights.append(2.0)  # Even beat
        else:
            weights.append(1.0)  # Off-beat
    
    syncopation = 0.0
    for i in range(n):
        if pattern[i] == 1:
            # Check if this note is syncopated (followed by a rest on a stronger beat)
            next_i = (i + 1) % n
            if pattern[next_i] == 0 and weights[next_i] > weights[i]:
                syncopation += weights[next_i] - weights[i]
    
    return syncopation

def offbeat_density(pattern: list[int], meter_numerator: int = 4) -> float:
    """Fraction of hits that fall on off-beats."""
    hits = sum(pattern)
    if hits == 0:
        return 0.0
    
    offbeat_hits = sum(1 for i, v in enumerate(pattern) if v == 1 and i % meter_numerator not in (0, meter_numerator // 2))
    return offbeat_hits / hits

def rhythmic_entropy(pattern: list[int]) -> float:
    """Shannon entropy of the interval distribution in the pattern."""
    # Find intervals between hits
    hit_positions = [i for i, v in enumerate(pattern) if v == 1]
    if len(hit_positions) < 2:
        return 0.0
    
    intervals = [hit_positions[i+1] - hit_positions[i] for i in range(len(hit_positions) - 1)]
    # Wrap around
    intervals.append(len(pattern) - hit_positions[-1] + hit_positions[0])
    
    # Compute entropy
    counts = Counter(intervals)
    total = len(intervals)
    entropy = -sum((c/total) * math.log2(c/total) for c in counts.values())
    return entropy
