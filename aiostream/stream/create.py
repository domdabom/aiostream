
import asyncio
import builtins
import itertools
from collections import Iterable, AsyncIterable

from ..core import operator
from ..stream import time

__all__ = ['from_iterable', 'from_aiterable', 'iterate',
           'just', 'throw', 'empty', 'never', 'range', 'count']


# Convert regular iterables

@operator
async def from_iterable(it):
    for item in it:
        yield item


@operator
def from_aiterable(ait):
    return ait


@operator
def iterate(it):
    if isinstance(it, AsyncIterable):
        return from_aiterable.raw(it)
    if isinstance(it, Iterable):
        return from_iterable.raw(it)
    raise TypeError("Not (async) iterable")


# Simple operators

@operator
async def just(value):
    yield value


@operator
async def throw(exc):
    if False:
        yield
    raise exc


@operator
async def empty():
    if False:
        yield


@operator
async def never():
    if False:
        yield
    future = asyncio.Future()
    await future


# Counting operators

@operator
def range(*args, interval=0):
    stream = from_iterable.raw(builtins.range(*args))
    return time.space_out.raw(stream, interval) if interval else stream


@operator
def count(start=0, step=1, *, interval=0):
    stream = from_iterable.raw(itertools.count(start, step))
    return time.space_out.raw(stream, interval) if interval else stream
