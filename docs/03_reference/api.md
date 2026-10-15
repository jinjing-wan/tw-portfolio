# API 参考（Doxygen + Breathe 自动生成）

本页的接口内容由 **Doxygen** 从 C/C++ 头文件抽取 XML，经 **Breathe** 桥接进 Sphinx 自动渲染，
零手写重复——这是 Docs-as-Code 在 API 文档场景的实战落地。

:::{note}
以下仅展示**接口契约（函数签名 + 文档注释）**，不含任何 `.cpp` 实现源码。
接口产物 `api-docs/doxyxml` 随仓库提交，公开站与本地渲染完全一致。
:::

## MTX 运行库（C 风格，仿摩尔线程 MUSA）

`mtx` 是一套 **C 风格、非类式** 的运行时 API：不透明句柄（`mtxDevice_t` /
`mtxStream_t` / `mtxEvent_t`）、枚举（`mtxError_t` / `mtxMemcpyKind` /
`mtxDeviceAttr` / `mtxLimit`），以及全部返回状态码的自由函数——这正是厂商 GPU
运行时在 C 语言中的典型暴露方式。

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

## Sunrise 运行库（类式，对照示例）

`sunrise` 是**类式 C++ API**，用于对照展示同一份管线如何同时承载两种风格。

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
