---
course: AMA572 Fixed-Income and Credit Risk
source: 03_Lecture1_配套计算_生成矩阵的矩阵指数.ipynb
cells: 17
created: 2026-10-15
---

> [!info] 原始 Notebook
> 下文按单元格顺序保留全部 Markdown 与 Python 代码，代码内容不作改写。输出来自 Notebook 文件中已经保存的结果；本次导入没有重新运行代码。点击「中文译文」显示 Markdown 说明的中文。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 1/附件/03_Lecture1_配套计算_生成矩阵的矩阵指数.ipynb|打开原始 Notebook]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 1/01 - Lecture 1（英文原文与折叠译文）#PDF p.8|返回讲义第 8 页]]


<!-- Notebook cell 1: markdown -->


# Matrix Exponential Approximation

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">矩阵指数近似。</span></details>



This notebook computes the matrix exponential $e^A$ in two ways:

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">本 Notebook 用两种方法计算矩阵指数 eᴬ：</span></details>



1. Directly with SciPy. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 直接使用 SciPy。</span></details>


2. With the truncated Taylor series for $k=3$, $k=5$, and $k=10$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 分别使用截断到 k = 3、5、10 的泰勒级数。</span></details>


<!-- Notebook cell 2: markdown -->


## Setup

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">准备工作。</span></details>



<!-- Notebook cell 3: code -->


```python
import numpy as np
import scipy
import math

# np.set_printoptions(suppress=True, threshold=100)
A = [[-0.21622, 0.21622, 0, 0],
     [0.09677, -0.19354, 0.09677, 0],
     [0, 0.10435, -0.31305, 0.20870],
     [0, 0, 0, 0]]
```


<!-- Notebook cell 4: markdown -->


## Method 1: Direct calculation

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">方法 1：直接计算。</span></details>



Use the SciPy library to calculate $e^A$ directly.

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用 SciPy 库直接计算矩阵指数 eᴬ。</span></details>



<!-- Notebook cell 5: code -->


```python
exp_A = scipy.linalg.expm(A)
print(exp_A)
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> [[8.14071598e-01 1.77073158e-01 8.24604656e-03 6.09197976e-04]
>  [7.92496969e-02 8.36624989e-01 7.55568624e-02 8.56845205e-03]
>  [3.97962704e-03 8.14752360e-02 7.35066959e-01 1.79478178e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]]
> ```


<!-- Notebook cell 6: markdown -->


## Method 2: Taylor-series approximation

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">方法 2：泰勒级数近似。</span></details>



Use the formula

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用以下公式：</span></details>



$$e^A = \lim_{k \to \infty} \sum_{i=0}^{k} \frac{A^i}{i!}.$$



<!-- Notebook cell 7: markdown -->


### Case 1: $k=3$

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">情形 1：k = 3。</span></details>



Calculate $\sum_{i=0}^{3} \frac{A^i}{i!}$ to approximate $e^A$.

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算从 i = 0 到 3 的 Aⁱ/i! 之和，近似矩阵指数 eᴬ。</span></details>



<!-- Notebook cell 8: code -->


```python
exp_A_3 = 0
for i in range(4):
    term = np.linalg.matrix_power(A, i) / math.factorial(i)
    print(f'A^{i}/{i}!= \n {term}\n')
    exp_A_3 += term
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> A^0/0!= 
>  [[1. 0. 0. 0.]
>  [0. 1. 0. 0.]
>  [0. 0. 1. 0.]
>  [0. 0. 0. 1.]]
>
> A^1/1!= 
>  [[-0.21622  0.21622  0.       0.     ]
>  [ 0.09677 -0.19354  0.09677  0.     ]
>  [ 0.       0.10435 -0.31305  0.2087 ]
>  [ 0.       0.       0.       0.     ]]
>
> A^2/2!= 
>  [[ 0.03383735 -0.04429915  0.0104618   0.        ]
>  [-0.01982624  0.03423965 -0.02451136  0.01009795]
>  [ 0.00504897 -0.02643133  0.05404913 -0.03266677]
>  [ 0.          0.          0.          0.        ]]
>
> A^3/3!= 
>  [[-0.00386771  0.00566055 -0.00252063  0.00072779]
>  [ 0.0025334  -0.00449044  0.00366222 -0.00170517]
>  [-0.00121648  0.00394908 -0.00649261  0.00376002]
>  [ 0.          0.          0.          0.        ]]
> ```


<!-- Notebook cell 9: code -->


```python
print(exp_A_3)
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> [[8.13749635e-01 1.77581399e-01 7.94117235e-03 7.27792880e-04]
>  [7.94771623e-02 8.36209202e-01 7.59208598e-02 8.39277609e-03]
>  [3.83249160e-03 8.18677454e-02 7.34506513e-01 1.79793250e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]]
> ```


<!-- Notebook cell 10: markdown -->


### Case 2: $k=5$

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">情形 2：k = 5。</span></details>



Calculate $\sum_{i=0}^{5} \frac{A^i}{i!}$ to approximate $e^A$.

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算从 i = 0 到 5 的 Aⁱ/i! 之和，近似矩阵指数 eᴬ。</span></details>



<!-- Notebook cell 11: code -->


```python
exp_A_5 = 0
for i in range(6):
    term = np.linalg.matrix_power(A, i) / math.factorial(i)
    print(f'A^{i}/{i}!= \n {term}\n')
    exp_A_5 += term
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> A^0/0!= 
>  [[1. 0. 0. 0.]
>  [0. 1. 0. 0.]
>  [0. 0. 1. 0.]
>  [0. 0. 0. 1.]]
>
> A^1/1!= 
>  [[-0.21622  0.21622  0.       0.     ]
>  [ 0.09677 -0.19354  0.09677  0.     ]
>  [ 0.       0.10435 -0.31305  0.2087 ]
>  [ 0.       0.       0.       0.     ]]
>
> A^2/2!= 
>  [[ 0.03383735 -0.04429915  0.0104618   0.        ]
>  [-0.01982624  0.03423965 -0.02451136  0.01009795]
>  [ 0.00504897 -0.02643133  0.05404913 -0.03266677]
>  [ 0.          0.          0.          0.        ]]
>
> A^3/3!= 
>  [[-0.00386771  0.00566055 -0.00252063  0.00072779]
>  [ 0.0025334  -0.00449044  0.00366222 -0.00170517]
>  [-0.00121648  0.00394908 -0.00649261  0.00376002]
>  [ 0.          0.          0.          0.        ]]
>
> A^4/4!= 
>  [[ 0.00034601 -0.00054871  0.00033421 -0.00013151]
>  [-0.00024558  0.00044975 -0.00039525  0.00019108]
>  [ 0.0001613  -0.00042621  0.00060367 -0.00033875]
>  [ 0.          0.          0.          0.        ]]
>
> A^5/5!= 
>  [[-2.55827251e-05  4.31775438e-05 -3.15449076e-05  1.39500890e-05]
>  [ 1.93242573e-05 -3.62775934e-05  3.34510421e-05 -1.64977060e-05]
>  [-1.52238975e-05  3.60712643e-05 -4.60443944e-05  2.51970276e-05]
>  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]
> ```


<!-- Notebook cell 12: code -->


```python
print(exp_A_5)
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> [[8.14070065e-01 1.77075865e-01 8.24384136e-03 6.10228976e-04]
>  [7.92509085e-02 8.36622675e-01 7.55590615e-02 8.56735455e-03]
>  [3.97856279e-03 8.14776074e-02 7.35064135e-01 1.79479695e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]]
> ```


<!-- Notebook cell 13: markdown -->


### Case 3: $k=10$

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">情形 3：k = 10。</span></details>



Calculate $\sum_{i=0}^{10} \frac{A^i}{i!}$ to approximate $e^A$.

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算从 i = 0 到 10 的 Aⁱ/i! 之和，近似矩阵指数 eᴬ。</span></details>



<!-- Notebook cell 14: code -->


```python
exp_A_10 = 0
for i in range(11):
    term = np.linalg.matrix_power(A, i) / math.factorial(i)
    print(f'A^{i}/{i}!= \n {term}\n')
    exp_A_10 += term
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> A^0/0!= 
>  [[1. 0. 0. 0.]
>  [0. 1. 0. 0.]
>  [0. 0. 1. 0.]
>  [0. 0. 0. 1.]]
>
> A^1/1!= 
>  [[-0.21622  0.21622  0.       0.     ]
>  [ 0.09677 -0.19354  0.09677  0.     ]
>  [ 0.       0.10435 -0.31305  0.2087 ]
>  [ 0.       0.       0.       0.     ]]
>
> A^2/2!= 
>  [[ 0.03383735 -0.04429915  0.0104618   0.        ]
>  [-0.01982624  0.03423965 -0.02451136  0.01009795]
>  [ 0.00504897 -0.02643133  0.05404913 -0.03266677]
>  [ 0.          0.          0.          0.        ]]
>
> A^3/3!= 
>  [[-0.00386771  0.00566055 -0.00252063  0.00072779]
>  [ 0.0025334  -0.00449044  0.00366222 -0.00170517]
>  [-0.00121648  0.00394908 -0.00649261  0.00376002]
>  [ 0.          0.          0.          0.        ]]
>
> A^4/4!= 
>  [[ 0.00034601 -0.00054871  0.00033421 -0.00013151]
>  [-0.00024558  0.00044975 -0.00039525  0.00019108]
>  [ 0.0001613  -0.00042621  0.00060367 -0.00033875]
>  [ 0.          0.          0.          0.        ]]
>
> A^5/5!= 
>  [[-2.55827251e-05  4.31775438e-05 -3.15449076e-05  1.39500890e-05]
>  [ 1.93242573e-05 -3.62775934e-05  3.34510421e-05 -1.64977060e-05]
>  [-1.52238975e-05  3.60712643e-05 -4.60443944e-05  2.51970276e-05]
>  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]
>
> A^6/6!= 
>  [[ 1.61829796e-06 -2.86329830e-06  2.34223738e-06 -1.09723704e-06]
>  [-1.28147894e-06  2.44834543e-06 -2.33040524e-06  1.16353875e-06]
>  [ 1.13038789e-06 -2.51294603e-06  2.98413565e-06 -1.60157752e-06]
>  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]
>
> A^7/7!= 
>  [[-8.95699658e-08  1.64069087e-07 -1.44331255e-07  6.98321343e-08]
>  [ 7.34296805e-08 -1.42015991e-07  1.38065678e-07 -6.94793677e-08]
>  [-6.96557510e-08  1.48880371e-07 -1.68194493e-07  8.89698729e-08]
>  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]
>
> A^8/8!= 
>  [[ 4.40547294e-09 -8.27271444e-09  7.63248312e-09 -3.76524162e-09]
>  [-3.70248162e-09  7.22123675e-09 -7.12054351e-09  3.60178838e-09]
>  [ 3.68351500e-09 -7.67829611e-09  8.38255495e-09 -4.38777384e-09]
>  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]
>
> A^9/9!= 
>  [[-1.94789104e-10  3.72233570e-10 -3.54433269e-10  1.76988803e-10]
>  [ 1.66594406e-10 -3.26797495e-10  3.25320581e-10 -1.65117492e-10]
>  [-1.71053148e-10  3.50802961e-10 -3.74131949e-10  1.94382135e-10]
>  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]
>
> A^10/10!= 
>  [[ 7.81383426e-12 -1.51144497e-11  1.46976377e-11 -7.39702232e-12]
>  [-6.76452361e-12  1.33216632e-11 -1.33465801e-11  6.78944052e-12]
>  [ 7.09323142e-12 -1.43920186e-11  1.51069209e-11 -7.80813378e-12]
>  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]
> ```


<!-- Notebook cell 15: code -->


```python
print(exp_A_10)
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> [[8.14071598e-01 1.77073158e-01 8.24604656e-03 6.09197976e-04]
>  [7.92496969e-02 8.36624989e-01 7.55568624e-02 8.56845205e-03]
>  [3.97962704e-03 8.14752360e-02 7.35066959e-01 1.79478178e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]]
> ```


<!-- Notebook cell 16: markdown -->


## Comparison

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">结果比较。</span></details>



<!-- Notebook cell 17: code -->


```python
print(f"Exact value of exp(A) is: \n {exp_A} \n")
print(f"Case 1, k = 3, approximate value of exp(A) is: \n {exp_A_3}\n\n")
print(f"Case 2, k = 5, approximate value of exp(A) is: \n {exp_A_5}\n\n")
print(f"Case 3, k = 10, approximate value of exp(A) is: \n {exp_A_10}\n\n")
```


> [!example]- Notebook 已保存输出（点击展开）
> ```text
> Exact value of exp(A) is: 
>  [[8.14071598e-01 1.77073158e-01 8.24604656e-03 6.09197976e-04]
>  [7.92496969e-02 8.36624989e-01 7.55568624e-02 8.56845205e-03]
>  [3.97962704e-03 8.14752360e-02 7.35066959e-01 1.79478178e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]] 
>
> Case 1, k = 3, approximate value of exp(A) is: 
>  [[8.13749635e-01 1.77581399e-01 7.94117235e-03 7.27792880e-04]
>  [7.94771623e-02 8.36209202e-01 7.59208598e-02 8.39277609e-03]
>  [3.83249160e-03 8.18677454e-02 7.34506513e-01 1.79793250e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]]
>
>
> Case 2, k = 5, approximate value of exp(A) is: 
>  [[8.14070065e-01 1.77075865e-01 8.24384136e-03 6.10228976e-04]
>  [7.92509085e-02 8.36622675e-01 7.55590615e-02 8.56735455e-03]
>  [3.97856279e-03 8.14776074e-02 7.35064135e-01 1.79479695e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]]
>
>
> Case 3, k = 10, approximate value of exp(A) is: 
>  [[8.14071598e-01 1.77073158e-01 8.24604656e-03 6.09197976e-04]
>  [7.92496969e-02 8.36624989e-01 7.55568624e-02 8.56845205e-03]
>  [3.97962704e-03 8.14752360e-02 7.35066959e-01 1.79478178e-01]
>  [0.00000000e+00 0.00000000e+00 0.00000000e+00 1.00000000e+00]]
> ```
