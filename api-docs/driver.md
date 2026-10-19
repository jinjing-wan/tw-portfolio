# Driver Layer (`gxDrv*`)

The Driver layer is the lowest abstraction. It talks directly to the GPU and
the host OS: driver initialization, device enumeration, context and module
management, and device-memory allocation. Application code normally goes
through the [Runtime layer](runtime.md), which wraps these calls.

:::{cpp:function} gxDrvError_t gxDrvInit(void)
Initialize the 示例 driver. Must be called once before any other driver
or runtime API. Returns `GX_DRV_SUCCESS` on success.
:::

:::{cpp:function} gxDrvError_t gxDrvDeviceGetCount(int *count)
Query the number of GPUs available on the host.
:::

:::{cpp:function} gxDrvError_t gxDrvDeviceGet(gxDrvDevice_t *device, int ordinal)
Acquire a handle to the GPU at the given `ordinal` (0-based).
:::

:::{cpp:function} gxDrvError_t gxDrvCtxCreate(gxDrvCtx_t *ctx, gxDrvDevice_t device)
Create a driver context bound to `device`. A context isolates resources
(streams, allocations) for a host thread or process.
:::

:::{cpp:function} gxDrvError_t gxDrvModuleLoad(gxDrvModule_t *module, const char *fname)
Load a compiled device module (e.g. a PTX / cubin-equivalent image) from
disk into the given context.
:::

:::{cpp:function} gxDrvError_t gxDrvMemAlloc(void **ptr, size_t size)
Allocate `size` bytes of device memory. The returned `ptr` is used by the
Runtime layer's `gxMalloc` callers indirectly.
:::

:::{cpp:function} gxDrvError_t gxDrvMemFree(void *ptr)
Free device memory previously allocated with `gxDrvMemAlloc`.
:::
