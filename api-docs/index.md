# Sunrise API Reference（示例）

:::{note}
本工程演示 **Doxygen + Breathe + Sphinx** 的私有源码文档化链路：

- **源码私有**：`../api/`（头文件 + 实现）已被仓库 `.gitignore` 排除，绝不进入公开仓库；
- **只公开接口契约**：Doxygen 仅解析头文件生成 XML，Breathe 渲染为签名 / 参数 / 返回值文档，**不含 `.cpp` 实现**；
- **构建在本地**：因源码不入库，CI 无法重建，文档在你本机 `scripts/build_api_docs.sh` 生成后发布。

把 `../api/include` 换成你真实的内部库头文件路径，其余流程一字不改即可复用。
:::

## 模块导航

```{toctree}
:maxdepth: 1

api_reference
```
