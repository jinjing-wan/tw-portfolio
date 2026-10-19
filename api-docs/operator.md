# Operator Library

The Operator Library sits on top of the [Runtime layer](runtime.md) and provides
performance-critical neural-network primitives. Each operator is documented
with the Sphinx **C++ domain**, which registers it as a first-class,
cross-referenceable symbol (try referencing `gxGemm` from another page —
Sphinx resolves it by name via `objects.inv`).

## Matrix Multiplication

:::{cpp:function} gxStatus_t gxGemm(gxHandle_t handle, gxOperation_t transa, gxOperation_t transb, int m, int n, int k, const void *alpha, const void *A, int lda, const void *B, int ldb, const void *beta, void *C, int ldc)
Perform matrix-matrix multiplication `C = alpha * op(A) * op(B) + beta * C`.

* `handle` — operator library handle (created with the Runtime layer).
* `transa` / `transb` — transpose mode for `A` / `B`.
* `m`, `n`, `k` — dimensions of the operands.
* `alpha` / `beta` — host pointers to scalar multipliers.
* `A`, `B`, `C` — device pointers to the operand / result matrices.
* `lda`, `ldb`, `ldc` — leading dimensions.
:::

## Convolution (forward)

:::{cpp:function} gxStatus_t gxConv2dForward(gxHandle_t handle, const gxConvDesc_t desc, const void *alpha, const void *x, const void *w, const void *beta, void *y)
Compute the forward 2-D convolution `y = alpha * conv(x, w) + beta * y`.

* `desc` — convolution descriptor (padding, stride, dilation, groups).
* `x`, `w`, `y` — input tensor, filter, output tensor (device pointers).
:::

## Batch Normalization (forward)

:::{cpp:function} gxStatus_t gxBatchNormForward(gxHandle_t handle, gxBatchNormMode_t mode, const void *alpha, const void *beta, const void *x, const void *scale, const void *bias, const void *mean, const void *variance, double epsilon, void *y)
Apply batch normalization in the forward direction.
:::

## Softmax (forward)

:::{cpp:function} gxStatus_t gxSoftmaxForward(gxHandle_t handle, gxSoftmaxAlgorithm_t algorithm, gxSoftmaxMode_t mode, const void *alpha, const void *x, const void *beta, void *y)
Apply the softmax function along the given dimension.
:::

## Pooling (forward)

:::{cpp:function} gxStatus_t gxPoolingForward(gxHandle_t handle, const gxPoolingDesc_t desc, const void *alpha, const void *x, const void *beta, void *y)
Apply pooling (max / average) in the forward direction.
:::
