from __builtin__ import xrange
from nltk.compat import izip, imap

__all__ = ['heappush', 'heappop', 'heapify', 'heapreplace', 'merge',
           'nlargest', 'nsmallest', 'heappushpop']

from itertools import islice, repeat, count, tee
from operator import itemgetter, neg
import bisect

def heappush(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown(heap, 0, len(heap)-1)

def heappop(heap):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup(heap, 0)
    else:
        returnitem = lastelt
    return returnitem

def heapreplace(heap, item):
    returnitem = heap[0]    # raises appropriate IndexError if heap is empty
    heap[0] = item
    _siftup(heap, 0)
    return returnitem

def heappushpop(heap, item):
    """Fast version of a heappush followed by a heappop."""
    if heap and heap[0] < item:
        item, heap[0] = heap[0], item
        _siftup(heap, 0)
    return item

def heapify(x):
    n = len(x)
    for i in reversed(xrange(n//2)):
        _siftup(x, i)

def nlargest(n, iterable):
    it = iter(iterable)
    result = list(islice(it, n))
    if not result:
        return result
    heapify(result)
    _heappushpop = heappushpop
    for elem in it:
        _heappushpop(result, elem)
    result.sort(reverse=True)
    return result

def nsmallest(n, iterable):
    """Find the n smallest elements in a dataset.

    Equivalent to:  sorted(iterable)[:n]
    """
    if hasattr(iterable, '__len__') and n * 10 <= len(iterable):
        # For smaller values of n, the bisect method is faster than a minheap.
        # It is also memory efficient, consuming only n elements of space.
        it = iter(iterable)
        result = sorted(islice(it, 0, n))
        if not result:
            return result
        insort = bisect.insort
        pop = result.pop
        los = result[-1]    # los --> Largest of the nsmallest
        for elem in it:
            if los <= elem:
                continue
            insort(result, elem)
            pop()
            los = result[-1]
        return result
    h = list(iterable)
    heapify(h)
    return map(heappop, repeat(h, min(n, len(h))))

def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem

def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)

# If available, use C implementation
try:
    from _heapq import heappush, heappop, heapify, heapreplace, nlargest, nsmallest, heappushpop
except ImportError:
    pass

def merge(*iterables):
    _heappop, _heapreplace, _StopIteration = heappop, heapreplace, StopIteration

    h = []
    h_append = h.append
    for itnum, it in enumerate(map(iter, iterables)):
        try:
            next = it.next
            h_append([next(), itnum, next])
        except _StopIteration:
            pass
    heapify(h)

    while 1:
        try:
            while 1:
                v, itnum, next = s = h[0]   # raises IndexError when h is empty
                yield v
                s[0] = next()               # raises StopIteration when exhausted
                _heapreplace(h, s)          # restore heap condition
        except _StopIteration:
            _heappop(h)                     # remove empty iterator
        except IndexError:
            return

# Extend the implementations of nsmallest and nlargest to use a key= argument
_nsmallest = nsmallest
def nsmallest(n, iterable, key=None):
    """Find the n smallest elements in a dataset.

    Equivalent to:  sorted(iterable, key=key)[:n]
    """
    if key is None:
        it = izip(iterable, count())                        # decorate
        result = _nsmallest(n, it)
        return map(itemgetter(0), result)                   # undecorate
    in1, in2 = tee(iterable)
    it = izip(imap(key, in1), count(), in2)                 # decorate
    result = _nsmallest(n, it)
    return map(itemgetter(2), result)                       # undecorate

_nlargest = nlargest
def nlargest(n, iterable, key=None):
    if key is None:
        it = izip(iterable, imap(neg, count()))             # decorate
        result = _nlargest(n, it)
        return map(itemgetter(0), result)                   # undecorate
    in1, in2 = tee(iterable)
    it = izip(imap(key, in1), imap(neg, count()), in2)      # decorate
    result = _nlargest(n, it)
    return map(itemgetter(2), result)                       # undecorate

if __name__ == "__main__":
    # Simple sanity test
    # heap = []
    # data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    # for item in data:
    #     heappush(heap, item)
    # sort = []
    # while heap:
    #     sort.append(heappop(heap))
    # print sort

    # import doctest
    # doctest.testmod()

    # test = [10]
    # if test < data:
    #     print "sdf"
    # test = [0.1, 0.3, 0.5, 0.7, 0.9, 0.2, 0.4, 0.6, 0.8, 0.0]
    test = [ (0.1, [1, 5, 6]), (0.6, [9, 5, 6]) ]
    # tt = [[0.1, [4, 3,10,100]], [0.3, [5,5,1,23,23]], [0.5,3], [0.7, [1,5]], [0.7, [2,5]], [0.9, 1], [0.2, 4], [0.4, 10], [0.6,9], [0.8, 1], [0.0, 124]]
    heapify(test)
    # heapify(tt)
    heappush(test, (0.0, [1, 3]))
    dist, data = heappop(test)
    # print tt
    

    # print pow(float(3), 2)


