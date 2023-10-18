class LRUCache:

    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError("int required")
        if limit <= 0:
            raise ValueError("limit must be positive number")

        self.limit = limit
        self.cache = {}

        # счетчик вызовов LRUCache, каждое использование (set, get) увеличивает счетчик на 1
        self.calls_count = 0

        # хранит очередь, в которой использовались хранимые в cache ключи
        # ключами словаря являются номера вызовов LRUCache
        self.queue_for_delete = {}

        # хранит для хранимых в cache ключей, какой номер вызова был последним
        self.last_call_for_keys = {}

        # счетчик, который показывает последний проверенный вызов, хранящийся в queue_for_delete
        self.deleted_call = 0

    def get(self, key):
        value = self.cache.get(key)
        if not value:
            return None

        self.calls_count += 1
        self.queue_for_delete[self.calls_count] = key
        self.last_call_for_keys[key] = self.calls_count
        return value

    def _find_last_used_cache_item(self):
        while True:
            self.deleted_call += 1
            current_key = self.queue_for_delete[self.deleted_call]
            del self.queue_for_delete[self.deleted_call]

            if self.last_call_for_keys[current_key] == self.deleted_call:
                return current_key

    def _free_cache_item(self, key):
        del self.cache[key]
        del self.last_call_for_keys[key]

    def set(self, key, value):
        if self.cache.get(key) is None:
            if len(self.cache) >= self.limit:
                last_cached_key = self._find_last_used_cache_item()
                self._free_cache_item(last_cached_key)
            self.cache[key] = value

        self.calls_count += 1
        self.queue_for_delete[self.calls_count] = key
        self.last_call_for_keys[key] = self.calls_count
