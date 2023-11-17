import logging


class LRUCache:

    def __init__(self, limit=42):
        if not isinstance(limit, int):
            logging.error("__init__: Bad type for limit= `%s`", limit)
            raise TypeError("int required")
        if limit <= 0:
            logging.error("__init__: Bad value for limit= `%s`", limit)

        self.limit = limit
        logging.info("__init__: Set limit= `%s`", limit)

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
            logging.error("get: Not found value for `%s`. cache = `%s`", key, self.cache)
            return None

        logging.info("get: Found value for `%s`", key)

        self.calls_count += 1
        self.queue_for_delete[self.calls_count] = key
        self.last_call_for_keys[key] = self.calls_count

        logging.debug("get: `%s` is used in `%s`th cache call", key, self.calls_count)
        return value

    def _find_last_used_cache_item(self):
        while self.queue_for_delete:
            self.deleted_call += 1
            current_key = self.queue_for_delete[self.deleted_call]
            del self.queue_for_delete[self.deleted_call]
            logging.debug("_find_last_used_cache_item: "
                          "`%s`'s call has deleted from queue_for_delete. Delete call is `%s`th",
                          current_key, self.deleted_call)

            if self.last_call_for_keys[current_key] == self.deleted_call:
                return current_key

        logging.critical("_find_last_used_cache_item: Not found last used cache item. cache = `%s`",
                         self.cache)

    def _free_cache_item(self, key):
        del self.cache[key]
        del self.last_call_for_keys[key]

        logging.debug("_free_cache_item: `%s` has deleted from cache. Delete call is `%s`th",
                      key, self.deleted_call)

    def set(self, key, value):
        if not self.cache.get(key) is None:
            logging.info("set: '`%s`': '`%s`' has already been in cache", key, value)
        else:
            if len(self.cache) >= self.limit:
                last_cached_key = self._find_last_used_cache_item()
                self._free_cache_item(last_cached_key)
                logging.info("set: set `%s`: `%s` in crowded cache", key, value)
            else:
                logging.info("set: set `%s`: `%s` in not crowded cache", key, value)

            self.cache[key] = value

        self.calls_count += 1
        self.queue_for_delete[self.calls_count] = key
        self.last_call_for_keys[key] = self.calls_count
        logging.debug("set: `%s` is used in `%s`th cache call", key, self.calls_count)


class CustomFilter(logging.Filter):
    def filter(self, record):
        return len(record.funcName) % 2 == 0


def use_cache():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")

    cache.get("k1")
    cache.get("k2")
    cache.get("k3")

    cache.set("k3", "val3")

    cache.get("k1")
    cache.get("k2")
    cache.get("k3")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stdout_logging', action="store_true")
    parser.add_argument('-f', '--filter_logging', action="store_true")
    args = parser.parse_args()

    # configurate FileHandler
    formatter1 = logging.Formatter(
        "\t%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
    )

    file_handler = logging.FileHandler(filename='cache.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter1)

    if args.filter_logging:
        file_handler.addFilter(CustomFilter())

    # if stdout_logging configurate StreamHandler
    if args.stdout_logging:
        formatter2 = logging.Formatter(
            "-s\t%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter2)

    # configurate root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    root.addHandler(file_handler)
    if args.stdout_logging:
        root.addHandler(stream_handler)

    use_cache()
