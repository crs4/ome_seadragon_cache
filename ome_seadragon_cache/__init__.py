from utils import time_dict_to_seconds


class UnknownCacheDriver(Exception):
    pass


class CacheDriverFactory(object):

    def __init__(self, cache_driver=None):
        self.cache_driver = cache_driver

    def _get_fake_cache(self):
        from fake_cache import FakeCache

        return FakeCache()

    def _get_redis_driver(self, host, port, db, expire_time):
        from redis_cache import RedisCache

        expire_time = time_dict_to_seconds(expire_time)
        return RedisCache(host, port, db, expire_time)

    def get_cache(self, host=None, port=None, db=None, expire_time=None):
        if self.cache_driver is None:
            return self._get_fake_cache()
        else:
            if self.cache_driver == 'redis':
                return self._get_redis_driver(host, port, db, expire_time)
            else:
                raise UnknownCacheDriver('There is no driver for %s' % self.cache_driver)
