# Driver Layer (`mtxDrv*`)

The Driver layer is the lowest abstraction. It talks directly to the GPU and
the host OS: driver initialization, device enumeration, context and module
management, and device-memory allocation. Application code normally goes
through the [Runtime layer](runtime.md), which wraps these calls.

:::{cpp:function} mtxDrvError_t mtxDrvInit(void)
Initialize the Sunrise driver. Must be called once before any other driver
or runtime API. Returns `MTX_DRV_SUCCESS` on success.
:::

:::{cpp:function} mtxDrvError_t mtxDrvDeviceGetCount(int *count)
Query the number of GPUs available on the host.
:::

:::{cpp:function} mtxDrvError_t mtxDrvDeviceGet(mtxDrvDevice_t *device, int ordinal)
Acquire a handle to the GPU at the given `ordinal` (0-based).
:::

:::{cpp:function} mtxDrvError_t mtxDrvCtxCreate(mtxDrvCtx_t *ctx, mtxDrvDevice_t device)
Create a driver context bound to `device`. A context isolates resources
(streams, allocations) for a host thread or process.
:::

:::{cpp:function} mtxDrvError_t mtxDrvModuleLoad(mtxDrvModule_t *module, const char *fname)
Load a compiled device module (e.g. a PTX / cubin-equivalent image) from
disk into the given context.
:::

:::{cpp:function} mtxDrvError_t mtxDrvMemAlloc(void **ptr, size_t size)
Allocate `size` bytes of device memory. The returned `ptr` is used by the
Runtime layer's `mtxMalloc` callers indirectly.
:::

:::{cpp:function} mtxDrvError_t mtxDrvMemFree(void *ptr)
Free device memory previously allocated with `mtxDrvMemAlloc`.
:::
