常见问题（FAQ，曦望 Sunrise 软件栈示例）
==============================================

.. note::
   本文为 **曦望 Sunrise AI 推理 GPU 软件栈 FAQ 样例** ：把高频问题结构化，降低支持成本。
   条目为示意口径，答案需可验证、不臆测。

安装类
--------------------------
**Q：安装后设备查不到？**
A：检查驱动版本与 SDK 版本匹配（见 :doc:`../01_getting_started/installation` 验证步骤）；
确认用户权限与设备可见性（``<命令占位>``）。

**Q：环境变量配了仍无效？**
A：确认 shell 类型与配置文件（bash/zsh），重开终端或 ``source`` 配置。

编译类
--------------------------
**Q：编译报 API 未定义？**
A：确认头文件路径与链接库（见 :doc:`../03_reference/tools` 编译器选项）；
核对 API 名称映射（见 :doc:`../04_development/porting_guide` 映射表）。

**Q：从 CUDA 迁移后编译失败？**
A：按 :doc:`../04_development/porting_guide` 检查清单逐项核对语义差异。

运行时类
----------------------------
**Q：内核启动后无结果 / 报错？**
A：检查返回值（见 :doc:`../03_reference/api` 错误模型）；
确认内存拷贝方向与同步（``sunriseStreamSynchronize``）。

**Q：性能远低于预期？**
A：按 :doc:`../04_development/performance_tuning` 排查 occupancy / 合并访存 / 流重叠。

API 类
--------------------------
**Q：统一错误码如何排查？**
A：每个 API 返回状态码必须检查，错误码含义见 :doc:`../03_reference/api` 词汇表。

**Q：异步 API 什么时候生效？**
A：绑定 stream，需 ``sunriseStreamSynchronize`` 或事件等待确认完成。

提交问题
----------------------------
- 文档缺陷请提 PR（见 :doc:`../07_about/methodology` 三方评审）；
- 技术问题请附环境、版本、复现步骤。
