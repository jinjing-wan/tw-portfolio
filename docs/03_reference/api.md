# API Reference (Doxygen + Breathe, auto-generated)

The interface content on this page is extracted from C/C++ header files by **Doxygen**
into XML, then bridged into Sphinx by **Breathe** and rendered automatically — zero
hand-written duplication. This is a production-grade Docs-as-Code practice for API
documentation.

:::{note}
Only the **interface contract (function signatures + doc comments)** is shown here —
no `.cpp` implementation source is included. The Doxygen XML product
(`api-docs/doxyxml`) is committed with the repository, so the public site renders
exactly the same content as the local build.
:::

## MTX Runtime Library (C-style, modeled after Moore Threads MUSA)

`mtx` is a **C-style, non-class** runtime API: opaque handles (`mtxDevice_t` /
`mtxStream_t` / `mtxEvent_t`), enumerations (`mtxError_t` / `mtxMemcpyKind` /
`mtxDeviceAttr` / `mtxLimit`), and free functions that all return a status code —
exactly how a vendor GPU runtime is typically exposed in C.

### Device Management

:::{doxygengroup} mtx_device
:project: sunrise_api
:members:
:::

### Memory Management

:::{doxygengroup} mtx_memory
:project: sunrise_api
:members:
:::

### Stream Management

:::{doxygengroup} mtx_stream
:project: sunrise_api
:members:
:::

### Event & Timing

:::{doxygengroup} mtx_event
:project: sunrise_api
:members:
:::

---

## Sunrise Runtime Library (class-style, comparison example)

`sunrise` is a **class-based C++ API**, included to demonstrate how the same
pipeline simultaneously carries both API styles.

:::{doxygenclass} sunrise::Device
:project: sunrise_api
:members: SetDevice, GetDeviceInfo
:::

:::{doxygenfunction} sunrise::GetDeviceCount
:project: sunrise_api
:::

:::{doxygengroup} memory
:project: sunrise_api
:members:
:::
