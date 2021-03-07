from redis import Redis
from src.constants import Constants
from src.main_logger import set_up_logging
from json import loads, dumps
from time import time


constants = Constants
logger = set_up_logging()


class RedisConnector:
    __slots__ = ["redis", "mapping_dict"]

    def __init__(self):
        try:
            self.redis = Redis(**constants.get_config('redis_docker'))
            logger.info("Redis initialized.")
            self.mapping_dict = {
                "locality": [],
                "home": {},
                "products": {}
            }
        except Exception as ex:
            self.redis = None
            logger.exception(f"Redis failed to connect: {ex}")

    def set_metadata(self, domain_type, metadata: dict) -> dict:

        logger.info(f"Populating metadata for {domain_type}")

        try:
            start_time = time()

            for key, value in metadata.items():
                self.redis.hset(domain_type, key, dumps(value))

            logger.info(f"Total Time taken to populate Redis : {time() - start_time:.2f} seconds.")
            return {
                "redis": {
                    "success": True,
                    "error": None
                }
            }

        except Exception as ex:
            logger.exception("Exception in populate metadata", exc_info=1)
            return {
                "redis": {
                    "success": False,
                    "error": {
                        "set": {
                            "type": ex,
                            "message": ex
                        }
                    }
                }
            }

    def get_metadata(self, domain_type, key) -> dict:
        logger.info(f"Getting metadata for {domain_type}")
        if self.redis is None:
            logger.info("Redis is not initialized.")
            return self.mapping_dict.get(key, {})
        try:
            value = loads(self.redis.hget(domain_type, key))
            return value
        except Exception as ex:
            logger.info(f"Error in get_metadata : {ex}")
            return self.mapping_dict.get(key, {})
