# API Reference

The 示例 AI inference GPU software stack is exposed through **three
layered APIs**. The full API reference is maintained as a **separate Sphinx
project** (`api-docs/`) and published under `/api`. This site cross-references
its symbols by name through **Intersphinx**: write a function name such as
{cpp:func}`gxMalloc` and Sphinx resolves it to the API reference page
automatically — no hand-written URLs, and the link follows renames.

```{mermaid}
flowchart TD
    APP[User Application]
    OP[Operator Library<br/>gxGemm / gxConv2dForward / ...]
    RT[Runtime Layer<br/>gx* C API]
    DR[Driver Layer<br/>gxDrv* low-level]
    HW[示例 AI GPU]
    APP --> OP --> RT --> DR --> HW
```

## Driver Layer — `gxDrv*`

The lowest layer: driver initialization, device enumeration, context /
module management, device-memory allocation. Rarely called directly by
applications; the Runtime layer wraps it. Example entry point:
{cpp:func}`gxDrvInit`. Full list → <a href="../api/driver.html">Driver API</a>.

## Runtime Layer — `gx*`

The primary surface most applications use: a C-style, handle-based API for
device management, memory, streams, and events. Example symbols:
{cpp:func}`gxGetDeviceCount`, {cpp:func}`gxMalloc`, {cpp:func}`gxMemcpy`,
{cpp:func}`gxStreamCreate`, {cpp:func}`gxEventRecord`. These are rendered
from Doxygen XML by Breathe in the API reference project — zero hand-written
duplication. Full list → <a href="../api/runtime.html">Runtime API</a>.

## Operator Library — `gxGemm` / `gxConv2dForward` / …

The highest layer: performance-critical NN primitives (matrix multiply,
convolution, normalization, activation, pooling) built on the Runtime layer.
Example: {cpp:func}`gxGemm`, {cpp:func}`gxConv2dForward`,
{cpp:func}`gxBatchNormForward`, {cpp:func}`gxSoftmaxForward`. Each is a
first-class, cross-referenceable symbol. Full list →
<a href="../api/operator.html">Operator Library</a>.

:::{admonition} Why a separate API-reference project?
:class: note

Splitting the API reference into its own Sphinx project lets the two sites
share a **single source of truth** for symbols. A rename in the API project
ripples to every cross-reference here automatically via `objects.inv` —
exactly the symbol-level, cross-project linking that template-based static
site generators (e.g. Docusaurus) lack out of the box.
:::
