import logging
import os

_LOGGER = logging.getLogger(__name__)

if os.path.isfile('test_bit') or int(os.environ.get("DEBUG", default=0)) == 1:
    os.environ["DEBUG"] = "1"
    _LOGGER.debug(f"Setting Debug env var to: {os.environ.get('DEBUG', default=0)}")
