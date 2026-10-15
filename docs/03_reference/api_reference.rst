API Reference (Runtime / Driver / Math — Sunrise software stack sample)
================================================================================

.. note::
   This page is a **framework sample** of the *Sunrise AI Inference GPU software
   stack Runtime API reference*. It covers the unified error model, the
   handle/context model, the stream async model, and function signatures with
   parameter descriptions. Function names use the ``sunrise*`` prefix as a
   stand-in for the software stack (shaped like a public Runtime API); no real
   source code is included.

General Conventions
----------------------------

- **Error model**: every API returns a unified status code
  (e.g. ``sunriseSuccess`` / ``sunriseError*``); the caller must check it.
- **Context / Handle**: stateful resources are managed through handles —
  create, reuse, then destroy.
- **Stream**: async APIs bind to a stream so transfer and compute can overlap.
- **Thread safety**: cross-stream calls on the same handle must be synchronized
  by the caller.

Runtime API
-------------------------------

Device and Context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - API
     - Description
   * - ``sunriseGetDeviceCount``
     - Query the number of available devices.
   * - ``sunriseDeviceGetAttribute``
     - Query device attributes (compute capability, memory, etc.).
   * - ``sunriseSetDevice``
     - Set the current device.

Memory Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - API
     - Description
   * - ``sunriseMalloc``
     - Allocate device memory.
   * - ``sunriseFree``
     - Free device memory.
   * - ``sunriseMemcpy``
     - Synchronous host/device copy.
   * - ``sunriseMemcpyAsync``
     - Stream-based asynchronous copy.

Execution and Synchronization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - API
     - Description
   * - ``sunriseLaunchKernel``
     - Launch a kernel.
   * - ``sunriseStreamSynchronize``
     - Wait for tasks on a stream to finish.
   * - ``sunriseEventRecord`` / ``sunriseEventSynchronize``
     - Event recording and synchronization.

Example
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c
   :caption: Minimal runnable call (skeleton)

   float *d;
   sunriseMalloc((void**)&d, N * sizeof(float));     // check return value
   myKernel<<<grid, block>>>(d);                     // placeholder launch syntax
   sunriseStreamSynchronize(0);
   sunriseFree(d);

Driver API (excerpt)
--------------------------------------

.. list-table::
   :header-rows: 1

   * - API
     - Description
   * - ``sunriseDriverGetVersion``
     - Query the driver version.
   * - ``sunriseModuleLoad``
     - Load a compiled module.
   * - ``sunriseModuleGetFunction``
     - Get a kernel function handle.

Math API
----------------------------

- Math function families (placeholders): vector, matrix, random number.
- Concrete entries are completed by domain experts, following the
  *General Conventions* on this page.

Glossary
--------------------------

- **Handle**: a reference to a stateful resource; must be created/destroyed.
- **Stream**: an async task queue that orders execution and overlap.
- **Context**: an execution context on the device that isolates resources.

Related
------------------------

- Programming model: :doc:`/04_development/programming_guide`
- Toolchain: :doc:`/03_reference/tools`
