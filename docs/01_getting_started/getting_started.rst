快速开始（Quick Start，示例 软件栈示例）
=====================================================

.. note::
   本页为 **文档体系骨架** ：结构与评审流程由本文档体系负责；
   命令、路径、输出为占位，具体内容由领域专家填充。

目标
------------------------
5 分钟内完成环境准备并运行第一个示例程序。

前置条件
----------------------------
- 已安装驱动与 SDK（步骤见 :doc:`/01_getting_started/installation`）
- 操作系统：Linux x86_64（占位）
- 可用 GPU 设备一台（占位）

步骤
------------------------
1. 验证驱动与设备可见：

   .. code-block:: bash

      <命令占位：如 gx-device-query>
      # 期望输出：检测到 1 台设备，型号 <占位>

2. 编译示例：

   .. code-block:: bash

      <命令占位：如 gxcc hello.gx -o hello>

3. 运行：

   .. code-block:: bash

      ./hello
      # 期望输出：Hello, GXPU / GPGPU

下一步
--------------------------
- 阅读 :doc:`/04_development/programming_guide` 了解编程模型（线程层次、内存层次、同步）；
- 查阅 :doc:`/03_reference/api` 了解 Runtime / Driver / Math API 契约；
- 遇到问题先看 :doc:`/05_release_support/faq`。
