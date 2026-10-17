# Runtime Layer (`mtx*`)

The Runtime layer is a **C-style, non-class API**: opaque handles
(`mtxDevice_t` / `mtxStream_t` / `mtxEvent_t`), enumerations
(`mtxError_t` / `mtxMemcpyKind` / `mtxDeviceAttr` / `mtxLimit`), and free
functions that all return a status code — exactly how a vendor GPU runtime
is typically exposed in C.

The content below is rendered automatically by **Breathe** from Doxygen
XML — only the interface contract (signatures + doc comments) is shown, no
`.cpp` implementation. Zero hand-written duplication.

## Device Management

:::{doxygengroup} mtx_device
:project: sunrise_api
:members:
:::

## Memory Management

:::{doxygengroup} mtx_memory
:project: sunrise_api
:members:
:::

## Stream Management

:::{doxygengroup} mtx_stream
:project: sunrise_api
:members:
:::

## Event & Timing

:::{doxygengroup} mtx_event
:project: sunrise_api
:members:
:::

---

## Sunrise Runtime (class-style, comparison example)

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
