import time
from collections import OrderedDict
import threading

class CacheEntry:
    __slots__ = ("value", "timestamp")

    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp


class LRUCacheTTL:
    def __init__(self, max_size: int = 128, ttl: int = 600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key):

        with self._lock:
            entry = self._cache.get(key)
            now = time.time()
            if entry is None:
                return None
            if now - entry.timestamp > self.ttl:
                self._cache.pop(key, None)
                return None
            self._cache.move_to_end(key)
            return entry.value

    def set(self, key, value):
        with self._lock:
            if key in self._cache:
                self._cache.pop(key)
            self._cache[key] = CacheEntry(value, time.time())
            if len(self._cache) > self.max_size:
                self._cache.popitem(last=False)

    def clear(self):
        with self._lock:
            self._cache.clear()

