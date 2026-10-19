# Runtime Layer (`gx*`)

The Runtime layer is a **C-style, non-class API**: opaque handles
(`gxDevice_t` / `gxStream_t` / `gxEvent_t`), enumerations
(`gxError_t` / `gxMemcpyKind` / `gxDeviceAttr` / `gxLimit`), and free
functions that all return a status code — exactly how a vendor GPU runtime
is typically exposed in C.

The content below is rendered automatically by **Breathe** from Doxygen
XML — only the interface contract (signatures + doc comments) is shown, no
`.cpp` implementation. Zero hand-written duplication.

## Device Management

:::{doxygengroup} gx_device
:project: gx_api
:members:
:::

## Memory Management

:::{doxygengroup} gx_memory
:project: gx_api
:members:
:::

## Stream Management

:::{doxygengroup} gx_stream
:project: gx_api
:members:
:::

## Event & Timing

:::{doxygengroup} gx_event
:project: gx_api
:members:
:::

---

## 示例 Runtime (class-style, comparison example)

`gx` is a **class-based C++ API**, included to demonstrate how the same
pipeline simultaneously carries both API styles.

:::{doxygenclass} gx::Device
:project: gx_api
:members: SetDevice, GetDeviceInfo
:::

:::{doxygenfunction} gx::GetDeviceCount
:project: gx_api
:::

:::{doxygengroup} memory
:project: gx_api
:members:
:::
