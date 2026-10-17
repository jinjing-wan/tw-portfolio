# Sunrise API Reference

This is the **API reference** for the Sunrise AI inference GPU software stack.
It is a separate Sphinx project from the main documentation site
(`docs/`), and the two are linked through **Intersphinx** — the main site
references the API symbols defined here by name, and Sphinx resolves them
automatically.

The stack is exposed through three layered APIs. Higher layers are built on
top of lower ones:

- **Operator Library** (`mtxGemm`, `mtxConv2dForward`, …) — top, NN primitives
- **Runtime Layer** (`mtx*` C API) — middle, device / memory / stream / event
- **Driver Layer** (`mtxDrv*`) — bottom, direct GPU + OS access

## Layers

```{toctree}
:maxdepth: 2

runtime
operator
driver
```

### Driver Layer — `mtxDrv*`

The lowest layer. Talks directly to the GPU and the OS: driver
initialization, device enumeration, context / module management, and
device-memory allocation. Application code rarely calls it directly; the
Runtime layer wraps it.

### Runtime Layer — `mtx*`

A C-style, handle-based runtime API (opaque handles, enumerations, status
codes). This is the primary surface most applications use: device
management, memory, streams, and events. It is rendered automatically from
Doxygen XML via Breathe — **zero hand-written duplication**.

### Operator Library — `mtx*Forward` / `mtxGemm`

The highest layer. Performance-critical neural-network primitives
(matrix multiply, convolution, normalization, activation, pooling) built on
top of the Runtime layer. Documented with the Sphinx C++ domain so each
operator is a first-class, cross-referenceable symbol.
