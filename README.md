# BytesFIFO

## Introduction

This module contains exactly one class, ``BytesFIFO``.  The purpose of ``BytesFIFO`` is to 
provide a stream-like interface to a fixed-size byte-oriented FIFO in Python.  This should
be significantly faster than using a deque, list, or manually manipulating 
``str``/``bytearray``/``bytes``.

The API only accepts ``bytes`` and ``bytearray``, and will read data back as ``bytes``.
It is a non-blocking stream.

## Performance

Preliminary performance analysis shows that Python 2.7 is about
25% faster than Python 3.4 when reading and writing large chunks of data to the FIFO. 

## Examples

### Creating a FIFO

A FIFO is created with a fixed size.  The internal buffer is completely pre-allocated.

```python
# Create a 5 kB FIFO
f = fifo.BytesFIFO(5*1024)
```

### Filling the FIFO

```python
f.write(b"Here's some data")
f.write(b"More data!")
# Consume all data
d = f.read(len(f))
```

### Querying the FIFO state

```python
f.full()     # Is the FIFO completely filled?
f.empty()    # Is the FIFO completely empty?
f.free()     # How much data is left in the FIFO?
f.capacity() # How much data can the FIFO hold?
len(f)       # How much data is filled in the FIFO?
bool(f)      # Is the FIFO non-empty?
```

### Resizing

The FIFO may be expanded or contracted.  All data is retained after the resize operation, 
but a copy operation may be occur.  ``ValueError`` is raised if the resize operation would
cause data loss.

```python
f = fifo.BytesFIFO(10)
f.write(b"Testing")
f.resize(20)
# returns b"Testing"
f.read(len(f))

### Writing more data than allocated

```python
f = fifo.BytesFIFO(5)
# Only b"Lorem" is written, since the FIFO depth is 5 bytes.
bytes_written = f.write(b"Lorem ipsum dolor sit amet, consectetur adipiscing elit")
data = f.read(5)
```
 
