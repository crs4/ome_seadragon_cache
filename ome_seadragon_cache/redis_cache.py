import logging
import redis
from io import BytesIO
from PIL import Image

from .cache_interface import CacheInterface


class RedisCache(CacheInterface):

    def __init__(self, host, port, database, default_expire):
        self.client = redis.StrictRedis(host=host, port=port, db=database)
        self.default_expire_time = default_expire
        self.logger = logging.getLogger(__name__)

    def _get_tile_key(self, image_id, level, column, row, tile_size, image_format,
                      image_quality=None, rendering_engine='UNKNOWN'):
        return super(RedisCache, self)._get_tile_key(image_id, level, column, row,
                                                     tile_size, image_format,
                                                     image_quality, rendering_engine)

    def _get_thumbnail_key(self, image_id, thumbnail_size, image_format, rendering_engine='UNKNOWN'):
        return super(RedisCache, self)._get_thumbnail_key(image_id, thumbnail_size, image_format,
                                                          rendering_engine)

    def tile_to_cache(self, image_id, image_obj, level, column, row, tile_size, image_format,
                      image_quality=None, rendering_engine='UNKNOWN'):
        out_buffer = BytesIO()
        image_obj.save(out_buffer, image_format)
        tile_key = self._get_tile_key(image_id, level, column, row, tile_size,
                                      image_format.upper(), image_quality, rendering_engine)
        self.client.set(tile_key, out_buffer.getvalue())
        self._set_expire_time(tile_key)

    def tile_from_cache(self, image_id, level, column, row, tile_size, image_format,
                        image_quality=None, rendering_engine='UNKNOWN'):
        tile_key = self._get_tile_key(image_id, level, column, row, tile_size,
                                      image_format.upper(), image_quality, rendering_engine)
        self.logger.info('Tile from cache: %s' % tile_key)
        tile_str = self.client.get(tile_key)
        if tile_str:
            self.logger.info('Tile retrieved')
            img_buffer = BytesIO(tile_str)
            image = Image.open(img_buffer)
            # reset expire time for this image
            self._set_expire_time(tile_key)
            return image
        else:
            self.logger.info('No tile')
            return None

    def thumbnail_to_cache(self, image_id, image_obj, thumbnail_size, image_format,
                           rendering_engine='UNKNOWN'):
        out_buffer = BytesIO()
        image_obj.save(out_buffer, image_format)
        th_key = self._get_thumbnail_key(image_id, thumbnail_size, image_format, rendering_engine)
        self.client.set(th_key, out_buffer.getvalue())
        self._set_expire_time(th_key)

    def thumbnail_from_cache(self, image_id, thumbnail_size, image_format, rendering_engine='UNKNOWN'):
        th_key = self._get_thumbnail_key(image_id, thumbnail_size, image_format, rendering_engine)
        self.logger.info('Thumbnail from cache: %s' % th_key)
        img_str = self.client.get(th_key)
        if img_str:
            self.logger.info('Thumbnail retrieved')
            img_buffer = BytesIO(img_str)
            image = Image.open(img_buffer)
            # reset expire time for this image
            self._set_expire_time(th_key)
            return image
        else:
            self.logger.info('No Thumbnail')
            return None

    def _set_expire_time(self, key):
        self.client.expire(key, self.default_expire_time)
