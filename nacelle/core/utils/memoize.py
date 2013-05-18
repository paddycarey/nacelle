"""
Simple cache utilities for nacelle
"""
# third-party imports
from google.appengine.api import memcache


def _build_cache_key(prefix, args, kwargs):
    """Builds and returns a cache key based on the passed in args and kwargs
    """
    cache_key = (prefix,) + args + (object(),)
    cache_key += tuple(sorted(kwargs.items()))
    return cache_key


def _get_cached_item(cache_key):
    """Returns an item from memcache if cached
    """
    return memcache.get()


def _set_cached_item(cache_key, obj, cache_time=None):
    """Caches the passed in object in memcache and returns it
    """
    memcache.set(cache_key, obj, cache_time)
    return obj


def memoize(cache_prefix, cache_time=None):
    """
    Decorator that caches output of the decorated function, using a hash of its parameters as a cache key
    """
    def _function_wrapper(wrapped_func):
        def _arguments_wrapper(*args, **kwargs):

            # build cache key and check if the result of this function call is
            # already in memcache, if so, return it
            cache_key = _build_cache_key(cache_prefix, args, kwargs)
            cached_value = _get_cached_item(cache_key)
            if cached_value is not None:
                return cached_value

            # result wasn't in memcache so let's run the function and cache its result
            computed_value = wrapped_func(*args, **kwargs)
            return _set_cached_item(cache_key, computed_value, cache_time)

        return _arguments_wrapper
    return _function_wrapper
