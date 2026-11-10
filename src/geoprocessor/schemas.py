from typing import Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class BufferRequest(BaseModel):
    """Paramètres validés d'un traitement buffer."""

    model_config = ConfigDict(strict=True)

    distance: float = Field(
        ge=0, allow_inf_nan=False, description="Distance du buffer en mètres"
    )

    target_epsg: int = Field(default=2950, gt=0, description="Code EPSG du CRS cible")


class ReprojectionRequest(BaseModel):
    """Paramètres validés d'une opération de reprojection."""

    model_config = ConfigDict(strict=True)

    source_epsg: int = Field(
        gt=0,
        description="Code EPSG du système source",
    )

    target_epsg: int = Field(
        gt=0,
        description="Code EPSG du système cible",
    )

    output_format: Literal["GPKG", "GeoJSON"] = Field(
        default="GPKG",
        description="Format géospatial de sortie",
    )

    @model_validator(mode="after")
    def validate_epsg(self) -> Self:
        """Empêche une reprojection vers le même CRS."""

        if self.source_epsg == self.target_epsg:
            raise ValueError("Le CRS source et le CRS cible doivent être différents.")

        return self
