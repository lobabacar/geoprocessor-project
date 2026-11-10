import logging
import math
from pathlib import Path

import geopandas as gpd

from geoprocessor.exceptions import (
    GeoCRSError,
    GeoDataLoadError,
    GeoExportError,
    GeoGeometryError,
)
from geoprocessor.geometry import calculate_area
from geoprocessor.projection import reproject_layer
from geoprocessor.schemas import BufferRequest

logger = logging.getLogger("geoprocessor.processor")


class GeoProcessor:
    """Classe pour le traitement géospatial des couches géographiques."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.gdf: gpd.geodataframe | None = None

    def load(self) -> None:
        """Charge les données géospatiales."""

        logger.info(
            "Chargement du fichier : %s",
            self.file_path,
        )

        if not self.file_path.is_file():
            logger.error(
                "Fichier introuvable : %s",
                self.file_path,
            )
            raise GeoDataLoadError(f"Fichier introuvable : {self.file_path}")

        try:
            gdf = gpd.read_file(self.file_path)

        except Exception as exc:
            logger.exception(
                "Erreur de lecture : %s",
                self.file_path,
            )
            raise GeoDataLoadError(f"Impossible de charger {self.file_path}") from exc

        self.gdf = gdf

        logger.info(
            "Chargement réussi : %s entités",
            len(self.gdf),
        )

    def validate_geometry(self) -> int:
        """
        Vérifie la validité des géométries de la couche.

        Returns
        -------
        int
            Nombre de géométries valides.

        Raises
        ------
        RuntimeError
            Si aucune donnée n'est chargée.
        GeoGeometryError
            Si des géométries invalides sont détectées.
        """

        # 1. Vérifier que les données sont chargées
        if self.gdf is None:
            raise RuntimeError("Aucune donnée chargée. Exécutez load().")

        # 2. Vérifier la validité des géométries
        valid_mask = (
            self.gdf.geometry.notna()
            & ~self.gdf.geometry.is_empty
            & self.gdf.geometry.is_valid
        )

        # 3. Compter les géométries
        total = len(self.gdf)
        valid_count = int(valid_mask.sum())
        invalid_count = total - valid_count

        # 4. Journaliser les résultats
        if invalid_count == 0:
            logger.info(
                "Validation réussie : %s géométries valides.",
                valid_count,
            )

            return valid_count

        # 5. Journaliser les anomalies
        logger.warning(
            "%s géométries invalides sur %s entités.",
            invalid_count,
            total,
        )

        # 6. Déclencher une exception personnalisée
        raise GeoGeometryError(
            f"{invalid_count} géométries invalides détectées sur {total} entités."
        )

    def reproject(self, target_epsg: int) -> None:
        """Reprojette la couche vers le CRS cible."""

        if self.gdf is None:
            raise RuntimeError("Chargez les données avant la reprojection.")

        logger.info(
            "Début de la reprojection vers EPSG:%s",
            target_epsg,
        )

        try:
            result = reproject_layer(
                self.gdf,
                target_epsg,
            )

        except (ValueError, TypeError) as exc:
            logger.exception("Échec de la validation du CRS")
            raise GeoCRSError(
                f"Reprojection impossible vers EPSG:{target_epsg}"
            ) from exc

        except Exception as exc:
            logger.exception("Erreur technique pendant la reprojection")
            raise GeoCRSError("Échec de la reprojection géospatiale.") from exc

        self.gdf = result

        logger.info(
            "Reprojection terminée : %s",
            self.gdf.crs,
        )

    def add_area(self) -> None:
        """Calcule les superficies en hectares et en km²."""
        if self.gdf is None:
            raise RuntimeError(
                "La couche géographique n'est pas chargée. Veuillez appeler la méthode 'load' avant de calculer les superficies."
            )
        self.gdf = calculate_area(self.gdf)

    def export(self, output_path: str | Path) -> None:
        """Exporte les données géospatiales."""

        if self.gdf is None:
            raise RuntimeError("Aucune donnée à exporter.")

        output_path = Path(output_path)

        logger.info(
            "Début de l'export : %s",
            output_path,
        )

        try:
            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.gdf.to_file(output_path)

        except Exception as exc:
            logger.exception(
                "Échec de l'export : %s",
                output_path,
            )
            raise GeoExportError(f"Impossible d'exporter vers {output_path}") from exc

        logger.info(
            "Export terminé : %s",
            output_path,
        )

    @property
    def feature_count(self) -> int:
        """Retourne le nombre d'entités dans la couche géographique."""
        if self.gdf is None:
            raise RuntimeError(
                "La couche géographique n'est pas chargée. Veuillez appeler la méthode 'load' avant de vérifier le nombre d'entités."
            )
        return len(self.gdf)

    @property
    def crs(self) -> str | None:
        """Retourne le système de coordonnées de la couche géographique."""
        if self.gdf is None:
            raise RuntimeError(
                "La couche géographique n'est pas chargée. Veuillez appeler la méthode 'load' avant de vérifier le CRS."
            )
        return str(self.gdf.crs)

    def buffer(self, distance: float) -> None:
        """
        Crée un buffer autour des géométries.

        Parameters
        ----------
        distance : float
            Distance du buffer en mètres.

        Raises
        ------
        RuntimeError
            Si aucune couche n'est chargée.
        ValueError
            Si la distance ou le CRS est invalide.
        """
        # 1. Vérifier la distance
        if (
            isinstance(distance, bool)
            or not isinstance(distance, (int, float))
            or not math.isfinite(distance)
            or distance < 0
        ):
            raise ValueError("La distance doit être un nombre fini positif ou nul.")
        # 2. Vérifier que les données sont chargées
        if self.gdf is None:
            raise RuntimeError("Aucune donnée chargée. Exécutez load() avant buffer().")

        # 3. Vérifier la présence du CRS
        if self.gdf.crs is None:
            raise ValueError("Le système de coordonnées est absent.")
        # 4. Vérifier que le CRS est projeté
        if not self.gdf.crs.is_projected:
            raise ValueError("Le CRS doit être projeté.")

        # 5. Vérifier que les axes sont en mètres
        axes = self.gdf.crs.axis_info

        if len(axes) < 2 or any(
            not math.isclose(axis.unit_conversion_factor, 1.0, rel_tol=0, abs_tol=1e-9)
            for axis in axes[:2]
        ):
            raise ValueError("Les unités horizontales du CRS doivent être des mètres.")
        # 6. Calculer les buffers
        result = self.gdf.copy()
        result["geometry"] = result.geometry.buffer(distance)

        # 7. Mettre à jour l'objet
        self.gdf = result

    def process_buffer(self, config: BufferRequest) -> None:
        """
        Exécute un buffer à partir d'une configuration
        Pydantic préalablement validée.
        """

        if not isinstance(config, BufferRequest):
            raise TypeError("config doit être une instance de BufferRequest.")

        if self.gdf is None:
            raise RuntimeError("Chargez les données avant le traitement.")

        # Reprojeter vers le CRS cible
        self.reproject(config.target_epsg)

        # Calculer le buffer
        self.buffer(config.distance)
