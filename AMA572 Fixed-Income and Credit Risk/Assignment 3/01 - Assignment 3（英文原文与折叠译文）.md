---
course: AMA572 Fixed-Income and Credit Risk
source: "Assignment3_作业题目_共2题_截止2026-11-28.pdf"
pages: 1
created: "2026-11-26"
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 英文按 PDF 实际页序完整转录；仅合并排版换行与断词。公式、数值、题号及原文疑似笔误保留，译文不替原文纠错。点击段末「中文译文」展开对应中文；各段之间保留留白。
> [[AMA572 Fixed-Income and Credit Risk/Assignment 3/00 - Assignment 3 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Assignment 3/附件/Assignment3_作业题目_共2题_截止2026-11-28.pdf|原始 PDF]]

## PDF p.1

# Assignment 3 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">作业 3。</span></details>

Due date: November 28, 2026 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">截止日期：2026 年 11 月 28 日。</span></details>

Q1. Hull-White model assumes that, under the risk-neutral measure, the spot rate follows a stochastic differential equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 1 题。Hull–White 模型假设，在风险中性测度（risk-neutral measure）下，即期利率（spot rate）服从如下随机微分方程（stochastic differential equation）：</span></details>

$$
dr(t) = (\alpha(t) - \beta(t)r(t))dt + \sigma(t)dW(t),
$$

where $r(0) = r_0$, coefficients $\alpha(t)$, $\beta(t)$, $\sigma(t)$ are deterministic and time varying, and $W(t)$ is a standard Brownian motion. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 r(0) = r₀，系数 α(t)、β(t)、σ(t) 为确定性的时变函数，W(t) 为标准布朗运动（standard Brownian motion）。</span></details>

(a) Show that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 证明：</span></details>

$$
r(t) = r_0 e^{-\int_0^t \beta(u)du} + \int_0^t \alpha(u)e^{-\int_u^t \beta(v)dv}du + \int_0^t \sigma(u)e^{-\int_u^t \beta(v)dv}dW(u).
$$

(b) What is expression of $\mathbb{E}[r(t)]$? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) E[r(t)] 的表达式是什么？</span></details>

(b) What is expression of $\text{Var}(r(t))$? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) Var(r(t)) 的表达式是什么？（注：原 PDF 中该小问与上一小问均标为 (b)，此处照录。）</span></details>

Q2. CIR model assumes that, under the risk-neutral measure, the spot rate follows a stochastic differential equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 2 题。CIR 模型假设，在风险中性测度下，即期利率服从如下随机微分方程：</span></details>

$$
dr(t) = a(b - r(t))dt + \sigma\sqrt{r(t)}dW(t),
$$

where $r(0) = r_0$, coefficients $a$, $b$, $\sigma$ are deterministic, and $W(t)$ is a standard Brownian motion. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 r(0) = r₀，系数 a、b、σ 为确定性常数，W(t) 为标准布朗运动。</span></details>

What is expression of $\text{Var}(r(t))$? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Var(r(t)) 的表达式是什么？</span></details>
