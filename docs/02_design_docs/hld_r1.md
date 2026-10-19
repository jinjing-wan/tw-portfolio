# HLD Release 1.0 — 示例 AI 推理 GPU 软件栈 · 基础软件栈

:::{note}
本文为 **示例 AI 推理 GPU 软件栈（基础软件栈层）HLD 框架样例（Release 1.0）**：
给出分层边界、层间接口契约与设计基线。
分层职责与接口契约由本文档体系定义；**各层内部具体技术机制由领域专家贡献，本文不展开 GPU 底层实现**。
后续版本见 [R2.0](hld_r2.md) / [R3.0](hld_r3.md)。
:::

---

## 1. 文档信息

| 项 | 内容 |
| --- | --- |
| **项目** | 示例 AI 推理 GPU 软件栈 |
| **文档类型** | High Level Design (HLD) |
| **版本** | v1.0（草稿，待三方评审） |
| **评审人** | 领域技术主管 / 集成测试主管 / 关联模块 Owner |

## 2. 概述

### 2.1 背景

AI 推理 GPU 软件栈为上层框架（PyTorch / TensorFlow 等）与底层硬件之间提供统一抽象：
驱动加载、资源管理、算子执行、内存搬运与同步。缺乏统一分层将导致框架适配成本高、问题定位难。

### 2.2 目的

本文定义基础软件栈的：四层职责边界与层间接口；统一资源（Context/Handle/Stream）模型；
错误模型与版本兼容基线。

### 2.3 范围（Scope）

- **包含**：软件栈分层、层间 API 契约、资源管理模型、统一错误模型；
- **不包含**：具体 GPU 微架构、算子 kernels 内部实现、编译器后端（由领域专家贡献）。

## 3. 软件栈分层架构

- **驱动层（Driver）**：设备管理、模块加载、与硬件交互的底层入口；
- **运行时层（Runtime）**：Context/Stream/内存与执行管理，面向开发者的核心 API 面；
- **算子编译层（Operator / Compiler）**：算子库与图编译，向下对接 Runtime，向上暴露算子接口；
- **框架接口层（Framework Binding）**：PyTorch / TensorFlow 等前端适配，屏蔽底层差异。

```text
框架接口层 (PyTorch / TF 适配)
      │
      ▼
算子编译层 (算子库 / 图编译)
      │
      ▼
运行时层 (Runtime: Context/Stream/内存/执行)   ← 本文重点契约
      │
      ▼
驱动层 (Driver: 设备管理 / 模块加载)
```

## 4. 层间接口契约（Runtime 层视角）

**统一约定（由本文档体系定义，全栈遵循）：**

- **错误模型**：所有 API 返回统一状态码，调用方必须检查；
- **Context / Handle**：有状态资源通过 handle 管理，创建后复用、用完销毁；
- **Stream**：异步任务队列，决定执行与重叠顺序；
- **线程安全**：同一 handle 跨流调用由调用方保证同步。

详细函数签名见 [API 参考](../03_reference/api.md)；层间契约变更走 Phase Gate 评审（见 [文档体系方法论](../07_about/methodology.rst)）。

## 5. 资源管理模型（框架示意）

Runtime 层对「管理操作」采用 **生产者-消费者任务模型** 解耦（示意，非真实源码）：
生产者线程接收上层调用请求封装为任务入队，消费者线程按 stream 顺序派发执行。

**任务队列与锁的核心约束（范式示意）**

```cpp
std::queue<Task> task_queue;
std::mutex        queue_gx;

void producer_push(const Task& t) {
    std::lock_guard<std::mutex> lk(queue_gx);  // 多生产者 push 加锁
    task_queue.push(t);
}

void consumer_loop() {
    while (running) {
        Task t;
        {
            std::lock_guard<std::mutex> lk(queue_gx);
            if (task_queue.empty()) { /* 等待/超时 */ continue; }
            t = task_queue.front(); task_queue.pop();
        }
        dispatch_to_execution(t);
    }
}
```

:::{warning}
上述模型未覆盖的边界：背压策略（队列暴涨防护）、消费者异常重试、任务幂等性、
跨线程生命周期管理 —— 真实 HLD 需在此展开。
:::

## 6. 北向接口契约

HLD 层面约定：设备/上下文管理、内存管理、执行与同步三类接口（详见 [API 参考](../03_reference/api.md)）；
配置与告警模型在 [需求文档](requirements.md) 中定义；版本兼容走 Phase Gate 评审。

## 7. 错误处理与告警

- 错误模型：统一错误码 + 人类可读原因 + 可操作建议；
- 告警分级：Critical / Major / Minor / Warning；
- 去抖：R1.0 为基础去抖（窗口化去抖见 [R2.0](hld_r2.md)）。

## 8. 性能与可靠性目标（占位，勿编）

- 算子端到端时延：`<填入真实指标，勿编>`
- 内存拷贝带宽利用率：`<填入真实指标，勿编>`
- 软件栈可用性：`<填入真实指标，勿编>`

## 9. 评审记录（三方 PR 评审示意）

本文档通过 Pull Request 提交，评审人包含：领域技术主管（架构正确性）、
集成测试主管（可测性）、关联模块 Owner（接口契约一致性）。
评审采用「修改前 / 修改后双版本对比」方式，见 [文档体系方法论](../07_about/methodology.rst)。
