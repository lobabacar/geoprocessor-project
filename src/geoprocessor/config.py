import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BufferConfig:
    input_path: Path
    output_path: Path
    distance: float
    target_epsg: int = 2950

    def __post_init__(self) -> None:

        if (
            isinstance(self.distance, bool)
            or not isinstance(self.distance, (int, float))
            or not math.isfinite(self.distance)
            or self.distance < 0
        ):
            raise ValueError("La distance doit être un nombre fini positif ou nul.")

        if (
            isinstance(self.target_epsg, bool)
            or not isinstance(self.target_epsg, int)
            or self.target_epsg <= 0
        ):
            raise ValueError("Le code EPSG doit être un entier positif.")
