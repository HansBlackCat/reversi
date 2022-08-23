import structlog


def main():
    log: structlog.stdlib.BoundLogger = structlog.get_logger()
    log.info("greeting", whomee="world")


if __name__ == "__main__":
    main()
