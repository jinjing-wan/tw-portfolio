# API Reference

The Sunrise AI inference GPU software stack is exposed through **three
layered APIs**. The full API reference is maintained as a **separate Sphinx
project** (`api-docs/`) and published under `/api`. This site cross-references
its symbols by name through **Intersphinx**: write a function name such as
{cpp:func}`mtxMalloc` and Sphinx resolves it to the API reference page
automatically — no hand-written URLs, and the link follows renames.

```{mermaid}
flowchart TD
    APP[User Application]
    OP[Operator Library<br/>mtxGemm / mtxConv2dForward / ...]
    RT[Runtime Layer<br/>mtx* C API]
    DR[Driver Layer<br/>mtxDrv* low-level]
    HW[Sunrise AI GPU]
    APP --> OP --> RT --> DR --> HW
```

## Driver Layer — `mtxDrv*`

The lowest layer: driver initialization, device enumeration, context /
module management, device-memory allocation. Rarely called directly by
applications; the Runtime layer wraps it. Example entry point:
{cpp:func}`mtxDrvInit`. Full list → <a href="../api/driver.html">Driver API</a>.

## Runtime Layer — `mtx*`

The primary surface most applications use: a C-style, handle-based API for
device management, memory, streams, and events. Example symbols:
{cpp:func}`mtxGetDeviceCount`, {cpp:func}`mtxMalloc`, {cpp:func}`mtxMemcpy`,
{cpp:func}`mtxStreamCreate`, {cpp:func}`mtxEventRecord`. These are rendered
from Doxygen XML by Breathe in the API reference project — zero hand-written
duplication. Full list → <a href="../api/runtime.html">Runtime API</a>.

## Operator Library — `mtxGemm` / `mtxConv2dForward` / …

The highest layer: performance-critical NN primitives (matrix multiply,
convolution, normalization, activation, pooling) built on the Runtime layer.
Example: {cpp:func}`mtxGemm`, {cpp:func}`mtxConv2dForward`,
{cpp:func}`mtxBatchNormForward`, {cpp:func}`mtxSoftmaxForward`. Each is a
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
