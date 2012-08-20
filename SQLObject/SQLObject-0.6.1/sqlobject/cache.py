"""
This implements the instance caching in SQLObject.  Caching is
relatively aggressive.  All objects are retained so long as they are
in memory, by keeping weak references to objects.  We also keep other
objects in a cache that doesn't allow them to be garbage collected
(unless caching is turned off).
"""

import threading
from weakref import ref
from time import time as now

True, False = 1==1, 0==1

class CacheFactory(object):

    """
    CacheFactory caches object creation.  Each object should be
    referenced by a single hashable ID (note tuples of hashable
    values are also hashable).

    """

    def __init__(self, cullFrequency=100, cullFraction=2,
                 cache=True):
        """
        Every cullFrequency times that an item is retrieved from
        this cache, the cull method is called.

        The cull method then expires an arbitrary fraction of
        the cached objects.  The idea is at no time will the cache
        be entirely emptied, placing a potentially high load at that
        moment, but everything object will have its time to go
        eventually.  The fraction is given as an integer, and one
        in that many objects are expired (i.e., the default is 1/2
        of objects are expired).

        By setting cache to False, items won't be cached.

        However, in all cases a weak reference is kept to created
        objects, and if the object hasn't been garbage collected
        it will be returned.
        """

        self.cullFrequency = cullFrequency
        self.cullCount = cullFrequency
        self.cullOffset = 0
        self.cullFraction = cullFraction
        self.doCache = cache

        if self.doCache:
            self.cache = {}
        self.expiredCache = {}
        self.lock = threading.Lock()

    def tryGet(self, id):
        """
        This returns None, or the object in cache.
        """
        value = self.expiredCache.get(id)
        if value:
            # it's actually a weakref:
            return value()
        if not self.doCache:
            return None
        return self.cache.get(id)

    def get(self, id):
        """
        This method can cause deadlocks!  tryGet is safer

        This returns the object found in cache, or None.  If None,
        then the cache will remain locked!  This is so that the
        calling function can create the object in a threadsafe manner
        before releasing the lock.  You should use this like (note
        that ``cache`` is actually a CacheSet object in this
        example)::

          obj = cache.get(some_id, my_class)
          if obj is None:
              try:
                  obj = create_object(some_id)
                  cache.put(some_id, my_class, obj)
              finally:
                  cache.finishPut(cls)

        This method checks both the main cache (which retains
        references) and the 'expired' cache, which retains only weak
        references.
        """

        if self.doCache:
            if self.cullCount > self.cullFrequency:
                # Two threads could hit the cull in a row, but
                # that's not so bad.  At least by setting cullCount
                # back to zero right away we avoid this.  The cull
                # method has a lock, so it's threadsafe.
                self.cullCount = 0
                self.cull()

            try:
                return self.cache[id]
            except KeyError:
                pass
            self.lock.acquire()
            try:
                val = self.cache[id]
            except KeyError:
                pass
            else:
                self.lock.release()
                return val
            try:
                val = self.expiredCache[id]()
            except KeyError:
                return None
            else:
                del self.expiredCache[id]
                if val is None:
                    return None
            self.cache[id] = val
            self.lock.release()
            return val

        else:
            try:
                val = self.expiredCache[id]()
                if val is not None:
                    return val
            except KeyError:
                pass
            self.lock.acquire()
            try:
                val = self.expiredCache[id]()
            except KeyError:
                return None
            else:
                if val is None:
                    del self.expiredCache[id]
                    return None
            self.lock.release()
            return val

    def put(self, id, obj):
        """
        Puts an object into the cache.  Should only be called after
        .get(), so that duplicate objects don't end up in the cache.
        """
        if self.doCache:
            self.cache[id] = obj
        else:
            self.expiredCache[id] = ref(obj)

    def finishPut(self):
        """
        Releases the lock that is retained when .get() is called and
        returns None.
        """
        self.lock.release()

    def created(self, id, obj):
        """
        Inserts and object into the cache.  Should be used when no one
        else knows about the object yet, so there cannot be any object
        already in the cache.  After a database INSERT is an example
        of this situation.
        """
        if self.doCache:
            self.cache[id] = obj
        else:
            self.expiredCache[id] = ref(obj)

    def cull(self):
        """
        Runs through the cache and expires objects.  E.g., if
        ``cullFraction`` is 3, then every third object is moved to
        the 'expired' (aka weakref) cache.
        """
        self.lock.acquire()
        try:
            keys = self.cache.keys()
            for i in xrange(self.cullOffset, len(keys), self.cullFraction):
                id = keys[i]
                self.expiredCache[id] = ref(self.cache[id])
                del self.cache[id]
            # This offset tries to balance out which objects we
            # expire, so no object will just hang out in the cache
            # forever.
            self.cullOffset = (self.culldOffset + 1) % self.cullFraction
        finally:
            self.lock.release()

    def clear(self):
        """
        Removes everything from the cache.  Warning!  This can cause
        duplicate objects in memory.
        """
        if self.doCache:
            self.cache.clear()
        self.expiredCache.clear()

    def expire(self, id):
        """
        Expires a single object.  Typically called after a delete.
        Doesn't even keep a weakref.  (@@: bad name?)
        """
        if not self.doCache:
            return
        self.lock.acquire()
        try:
            if self.cache.has_key(id):
                del self.cache[id]
            if self.expiredCache.has_key(id):
                del self.expiredCache[id]
        finally:
            self.lock.release()

    def expireAll(self):
        """
        Expires all objects, moving them all into the expired/weakref
        cache.
        """
        if not self.doCache:
            return
        self.lock.acquire()
        try:
            for key, value in self.cache.items():
                self.expiredCache[key] = ref(obj)
            self.cache = {}
        finally:
            self.lock.release()

    def allIDs(self):
        """
        Returns the IDs of all objects in the cache.
        """
        if self.doCache:
            all = self.cache.keys()
        else:
            all = []
        for id, value in self.expiredCache.items():
            if value():
                all.append(id)
        return all

class CacheSet(object):

    """
    A CacheSet is used to collect and maintain a series of caches.  In
    SQLObject, there is one CacheSet per connection, and one Cache
    in the CacheSet for each class, since IDs are not unique across
    classes.  It contains methods similar to Cache, but that take
    a ``cls`` argument.
    """

    def __init__(self, *args, **kw):
        self.caches = {}
        self.args = args
        self.kw = kw

    def get(self, id, cls):
        try:
            return self.caches[cls.__name__].get(id)
        except KeyError:
            self.caches[cls.__name__] = CacheFactory(*self.args, **self.kw)
            return self.caches[cls.__name__].get(id)

    def put(self, id, cls, obj):
        self.caches[cls.__name__].put(id, obj)

    def finishPut(self, cls):
        self.caches[cls.__name__].finishPut()

    def created(self, id, cls, obj):
        try:
            self.caches[cls.__name__].created(id, obj)
        except KeyError:
            self.caches[cls.__name__] = CacheFactory(*self.args, **self.kw)
            self.caches[cls.__name__].created(id, obj)

    def expire(self, id, cls):
        try:
            self.caches[cls.__name__].expire(id)
        except KeyError:
            pass

    def clear(self, cls=None):
        if cls is None:
            for cache in self.caches.values():
                cache.clear()
        elif self.caches.has_key(cls.__name__):
            self.caches[cls.__name__].clear()

    def tryGet(self, id, cls):
        try:
            self.caches[cls.__name__].tryGet(id)
        except KeyError:
            return None

    def allIDs(self, cls):
        try:
            self.caches[cls.__name__].allIDs()
        except KeyError:
            return []

    def allSubCaches(self):
        return self.caches.values()
