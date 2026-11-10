import logging

from geoprocessor.exceptions import GeoProcessorError
from geoprocessor.logger import setup_logging
from geoprocessor.processor import GeoProcessor
from geoprocessor.schemas import BufferRequest


def main() -> None:
    setup_logging()

    logger = logging.getLogger("geoprocessor.main")

    try:
        config = BufferRequest(
            distance=100.0,
            target_epsg=2950,
        )

        processor = GeoProcessor(
            "D:/geodeveloppement/geoprocessor-project/data/bornes-recharge-publiques.shp"
        )

        processor.load()

        processor.process_buffer(config)

        processor.add_area()

        processor.export("data/points_buffer.gpkg")

        logger.info("Traitement terminé avec succès.")

    except GeoProcessorError as exc:
        logger.error(
            "Erreur géospatiale : %s",
            exc,
        )
        raise

    except Exception:
        logger.exception("Erreur inattendue pendant le traitement.")
        raise


if __name__ == "__main__":
    main()
