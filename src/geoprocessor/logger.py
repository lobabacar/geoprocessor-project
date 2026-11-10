import logging
from pathlib import Path


def setup_logging(
    log_file: str | Path = "logs/geoprocessor.log",
    level: int = logging.INFO,
) -> None:
    """Configure les journaux de l'application."""

    log_file = Path(log_file)

    # Créer le dossier de logs si nécessaire
    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Journalisation dans un fichier
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    # Affichage dans la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configurer le logger de notre application
    logger = logging.getLogger("geoprocessor")
    logger.setLevel(level)
    logger.propagate = False

    # Éviter les handlers en double
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
