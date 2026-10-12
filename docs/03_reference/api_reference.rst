API 参考（Runtime / Driver / Math，曦望 Sunrise 软件栈示例）
====================================================================

.. note::
   本文为 **曦望 Sunrise AI 推理 GPU 软件栈 Runtime API 参考** 的框架样例，
   覆盖统一错误码、handle/context 模型、stream 异步模型、函数签名与参数说明；
   函数名采用 ``sunrise*`` 前缀作为软件栈代称（语义对齐公开 Runtime API 形状），不含任何真实源码。

通用约定
----------------------------
- **错误模型** ：所有 API 返回统一状态码（如 ``sunriseSuccess`` / ``sunriseError*``），调用方必须检查；
- **Context / Handle** ：有状态资源通过 handle 管理，创建后复用、用完销毁；
- **Stream** ：异步 API 绑定 stream，传输与计算可重叠；
- **线程安全** ：同一 handle 跨流调用需调用方保证同步。

Runtime API
-------------------------------
设备与上下文
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - API
     - 说明
   * - ``sunriseGetDeviceCount``
     - 查询可用设备数量
   * - ``sunriseDeviceGetAttribute``
     - 查询设备属性（算力、内存等）
   * - ``sunriseSetDevice``
     - 设置当前设备

内存管理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - API
     - 说明
   * - ``sunriseMalloc``
     - 设备内存分配
   * - ``sunriseFree``
     - 设备内存释放
   * - ``sunriseMemcpy``
     - 主机/设备间同步拷贝
   * - ``sunriseMemcpyAsync``
     - 基于 stream 的异步拷贝

执行与同步
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - API
     - 说明
   * - ``sunriseLaunchKernel``
     - 启动内核
   * - ``sunriseStreamSynchronize``
     - 等待 stream 上任务完成
   * - ``sunriseEventRecord`` / ``sunriseEventSynchronize``
     - 事件记录与同步

示例
^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: c
   :caption: 最小可运行调用（骨架）

   float *d;
   sunriseMalloc((void**)&d, N * sizeof(float));     // 检查返回值
   myKernel<<<grid, block>>>(d);                     // 占位启动语法
   sunriseStreamSynchronize(0);
   sunriseFree(d);

Driver API（节选）
--------------------------------------
.. list-table::
   :header-rows: 1

   * - API
     - 说明
   * - ``sunriseDriverGetVersion``
     - 查询驱动版本
   * - ``sunriseModuleLoad``
     - 加载编译产物模块
   * - ``sunriseModuleGetFunction``
     - 获取内核函数句柄

Math API
----------------------------
- 数学函数族（占位）：向量运算、矩阵运算、随机数；
- 具体条目由领域专家补全，遵循本页「通用约定」。

词汇表
--------------------------
-**Handle**：有状态资源的引用，需创建/销毁；
-**Stream**：异步任务队列，决定执行与重叠顺序；
-**Context** ：设备上的执行上下文，隔离资源。

相关
------------------------
- 编程模型：:doc:`/04_development/programming_guide`
- 工具链：:doc:`/03_reference/tools`
