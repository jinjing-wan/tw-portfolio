# API Reference · Interface Contract

The content below is rendered automatically by Breathe from Doxygen XML — zero hand-written duplication.

## Runtime (class-based)

Class `sunrise::Device` and its static methods. Note: the free function
`GetDeviceCount`, which shares a signature with `Device::GetDeviceCount`, is
not listed here to avoid a duplicate-declaration warning in the C++ domain;
it is shown separately under "Free functions" below.

:::{doxygenclass} sunrise::Device
:project: sunrise_api
:members: SetDevice, GetDeviceInfo
:::

Free-function form (same semantics as `Device::GetDeviceCount`, demonstrates
`doxygenfunction`):

:::{doxygenfunction} sunrise::GetDeviceCount
:project: sunrise_api
:::

## Memory Management (group example)

The whole `@defgroup memory` rendered at once:

:::{doxygengroup} memory
:project: sunrise_api
:members:
:::

---

## MTX Device Runtime (C-style, modelled on Moore Threads' MUSA)

Unlike the class-based `sunrise` API above, the `mtx` runtime is a **C-style,
non-class API**: opaque handles (`mtxDevice_t` / `mtxStream_t` / `mtxEvent_t`),
enumerations (`mtxError_t` / `mtxMemcpyKind` / `mtxDeviceAttr` / `mtxLimit`),
and free functions that all return a status code — exactly how vendor GPU
runtimes are typically exposed in C. It demonstrates documenting a flat,
function-oriented interface contract with Breathe.

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
