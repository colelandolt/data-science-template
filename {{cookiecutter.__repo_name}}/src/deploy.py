import logging
import logging.config

from utils import Arguments, FileReader


def main():
    # Configure logger
    log_config = FileReader("conf/logger.yaml").read()
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    args = Arguments("name", "target")
    name = args.name
    target = args.target


if __name__ == "__main__":
    main()
    