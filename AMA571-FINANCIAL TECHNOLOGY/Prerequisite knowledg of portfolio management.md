# Why Portfolio

![](images/53cf36fbe2861ff2154815aef05f9109081bf58032d30be3e97b37d374257399.jpg)

<details>
<summary>text_image</summary>

IF WE invest in an ice-cream shop
</details>

# Example

• Two scenarios

<table><tr><td></td><td>Scenario 150%probability</td><td>Scenario 250%probability</td></tr><tr><td>Asset A</td><td>10%</td><td>-6%</td></tr><tr><td>Asset B</td><td>-5%</td><td>8% Example 1</td></tr></table>

• In you have \$1000 to make investment you can:

1. Invest in A, earn \$100, or lose \$60   
2. Invest in B, lose \$50, or earn \$80   
3. Invest \$ 500 in A and \$ 500 in B, to earn \$25 or \$10

• We call option 3 a ‘portfolio’

# Expected Return of Portfolio

• Recall expected return of an asset

• (rA)=(0.2%+0.5%+…+0.2%)/10=0.25%   
• (rB)=(0.3%+0.5%+…+0.1%)/10=0.20%

• We can make a portfolio P with weight (0.6, 0.4)

• (rP)=0.25%∗0.6+0.20%∗0.4=0.23%

• Different portfolio is indicated by its weight

? (rP)= (rA)∗��+ (r�)∗��

• E.g. when $\omega = ( 0 . 3 , 0 . 7 )$ ,

$$
E(\mathsf{r}_{\mathsf{P}}) = 0.25\% *\mathsf{0.7} + 0.20\% *\mathsf{0.3} = 0.24\%
$$

# Variance of Portfolio

• Correlation is also a part of risk   
• Negative correlated

<table><tr><td></td><td>Scenario 1</td><td>Scenario 2</td></tr><tr><td>Company A</td><td>10%</td><td>-6%</td></tr><tr><td>Company B</td><td>-5%</td><td>8%</td></tr></table>

Example 2-1

• Positive correlated

<table><tr><td></td><td>Scenario 1</td><td>Scenario 2</td></tr><tr><td>Company A</td><td>10%</td><td>-6%</td></tr><tr><td>Company B</td><td>8%</td><td>-5%</td></tr></table>

Example 2-2

• Correlation coefficient is indicated by ρ

# Variance of Portfolio

• If we have two assets:

<table><tr><td></td><td>ω</td><td>E(r)</td><td>σ</td><td>ρ</td></tr><tr><td>A</td><td>0.4</td><td>12%</td><td>6%</td><td rowspan="2">0.5</td></tr><tr><td>B</td><td>0.6</td><td>10%</td><td>5%</td></tr></table>

Example 3

• the portfolio return

$$
E \left(\mathrm{r} _ {\mathrm{P}}\right) = 12 \% * 0.4 + 10 \% * 0.6 = 10.8 \%
$$

• the portfolio risk

$$
\begin{array}{l} \sigma_ {P} ^ {2} = (6 \% * 0. 4) ^ {2} + (5 \% * 0. 6) ^ {2} + 2 * 0. 5 * 6 \% \\ * 5 \% = 0.44 \% \\ \end{array}
$$

• The formula is

$$
\sigma_ {P} ^ {2} = (\sigma_ {A} * \omega_ {A}) ^ {2} + (\sigma_ {B} * \omega_ {B}) ^ {2} + 2 \rho \sigma_ {A} \sigma_ {B}
$$

# Three Assets: Matrix Notation

• If we have three assets:

$$
E (\mathsf {r} _ {i}) = (\mathsf {r} _ {1}, \mathsf {r} _ {2}, \mathsf {r} _ {3}), \omega_ {i} = (\omega_ {1}, \omega_ {2}, \omega_ {3}), \sigma_ {i j} = [ \begin{array}{c c c} \sigma_ {1 1} & \sigma_ {1 2} & \sigma_ {1 3} \\ \sigma_ {2 1} & \sigma_ {2 2} & \sigma_ {2 3} \\ \sigma_ {3 1} & \sigma_ {3 2} & \sigma_ {3 3} \end{array} ]
$$

• $\sigma _ { 1 1 } = ( \sigma _ { 1 } ) ^ { 2 }$ , it is variance of asset 1   
• $\sigma _ { 1 2 } = \rho _ { 1 2 } \sigma _ { 1 } \sigma _ { 2 }$ , it is covariance between asset 1 and 2

• the portfolio return

$$
E (\mathsf {r} _ {p}) = (\omega_ {1}, \omega_ {2}, \omega_ {3}) (\mathsf {r} _ {1}, \mathsf {r} _ {2}, \mathsf {r} _ {3}) ^ {T}
$$

• the portfolio risk

$$
\sigma_ {P} ^ {2} = \left(\omega_ {1}, \omega_ {2}, \omega_ {3}\right) \left[ \begin{array}{c c c} \sigma_ {1 1} & \sigma_ {1 2} & \sigma_ {1 3} \\ \sigma_ {2 1} & \sigma_ {2 2} & \sigma_ {2 3} \end{array} \right] (\omega_ {1}, \omega_ {2}, \omega_ {3}) ^ {T}
$$

# Drawing Efficient Frontier

Return μ   
![](images/d6be1cdb3df121648cc0e9376e8e184c85f6631c7e4bbb86ad4a122ffd23d9b0.jpg)

<details>
<summary>scatter</summary>

| Asset   | Risk σ | Percentage |
|---------|--------|----------|
| Asset A | 0.32   | 6.00%    |
| Asset B | 0.55   | 8.00%    |
| Asset C | 0.64   | 10.00%   |
| Asset D | 0.71   | 15.00%   |
</details>

Portfolio Efficient Frontier

# Drawing Efficient Frontier

![](images/02206f9fc45862eb08294a8c5dfc57914a78bb055be05c80e21c98f85cdce068.jpg)

<details>
<summary>scatter</summary>

| Asset   | Risk σ | Return μ |
|---------|--------|----------|
| Asset A | 0.32   | 6.00%    |
| Asset B | 0.55   | 8.00%    |
| Asset C | 0.64   | 10.00%   |
| Asset D | 0.71   | 15.00%   |
</details>

# Drawing Efficient Frontier

![](images/5a1bad274b948186f78890173b45a0d2a339d66f99f05b121babba3ccb81bc25.jpg)

<details>
<summary>scatter</summary>

| Asset   | Risk σ | Return μ |
|---------|--------|----------|
| Asset A | 0.32   | 6.00%    |
| Asset B | 0.55   | 8.00%    |
| Asset C | 0.63   | 10.00%   |
| Asset D | 0.71   | 15.00%   |
</details>

# Drawing Efficient Frontier

![](images/9b69e4c7c30b8ed7f3b23bbcccb71e665c456beb3dbe6bfc2871773d4b6a783d.jpg)

<details>
<summary>scatter</summary>

| Asset | Risk σ | Return μ |
|-------|--------|----------|
| Asset A | 0.32 | 6.00% |
| Asset B | 0.55 | 8.00% |
| Asset C | 0.63 | 10.00% |
| Asset D | 0.71 | 15.00% |
</details>

# Drawing Efficient Frontier

![](images/e03d167125e1c40abfca7195ea95715935164330cdbf54c26e127808f2fa389d.jpg)

<details>
<summary>scatter</summary>

| Asset | Risk σ | Return μ |
|-------|--------|----------|
| Asset A | 0.32 | 6.00% |
| Asset B | 0.55 | 8.00% |
| Asset C | 0.63 | 10.00% |
| Asset D | 0.71 | 15.00% |
| 0.41, 0.12 | 0.41 | 12.00% |
</details>

# Drawing Efficient Frontier

![](images/ad89b1d2d2fa10a298ef7db49a9fd21273bcb58fc654fe45df777306c72dc35e.jpg)

<details>
<summary>line</summary>

| Asset   | Risk σ | Return μ |
|---------|--------|----------|
| GMVP    | 0.27   | 7.80%    |
| Asset A | 0.32   | 6.10%    |
| Asset B | 0.54   | 8.10%    |
| Asset C | 0.63   | 10.00%   |
| Asset D | 0.71   | 15.00%   |
| 0.32    | 0.32   | 10.00%   |
| 0.41    | 0.41   | 12.00%   |
| 0.53    | 0.53   | 14.00%   |
</details>

# Drawing Efficient Frontier

![](images/f9ae76b6eb328b0a0f75fd24eb5d510fb7346b0768b941a8d2c286994284aa9d.jpg)

<details>
<summary>line</summary>

| Port | Risk σ | Return μ |
|------|--------|----------|
| port 1 | 0.49 | 13.5% |
| port 2 | 0.49 | 11.0% |
| port 3 | 0.49 | 8.5% |
</details>

# Drawing Efficient Frontier

![](images/0a5f6750949a202541b9fbbe4fa9780032ca68f2e18caf5fd60e2ea297f17148.jpg)

<details>
<summary>line</summary>

| Port | Risk σ | Return μ |
|------|--------|----------|
| port 1 | 0.49 | 13.5% |
| port 2 | 0.59 | 13.5% |
| port 3 | 0.69 | 13.5% |
</details>

# Capital Allocation Line

Return μ   
Optimal Capital Allocation Line (CAL)   
![](images/d7da1da03ede97a5bf3be24b44eea49157196951191a5f93c0c652f2123be38d.jpg)

<details>
<summary>line</summary>

| Risk σ | CAL (P) | CAL (A) | CAL (G) | Risk free rate |
| ------ | ------- | ------- | ------- | -------------- |
| 0.0    | 6.00%   | 6.00%   | 6.00%   | 6.00%          |
| 0.3    | 9.00%   | 9.00%   | 7.50%   | 7.50%          |
| 0.65   | 16.00%  | -       | -       | -              |
</details>

# Optimal CAL and Optimal Portfolio

Return μ Optimal Capital Allocation Line (CAL)   
![](images/b2e2e4248ad6d42dc1d0bb4313e63acc7766abc9ac29059bc177a6c3f3e17df9.jpg)

<details>
<summary>line</summary>

| Risk σ | Percentage |
| ------ | ---------- |
| 0.0    | 6.00%      |
| 0.27   | 8.00%      |
| 0.65   | 16.00%     |
</details>

# Optimal CAL & Optimal Portfolio

Return μ   
Optimal Capital Allocation Line (CAL)   
![](images/7d105aca1f490d1ae7d4987cdf7059c642a5522c2beba2de4e1dc5d901aa50d8.jpg)

<details>
<summary>line</summary>

| Risk σ | Value   |
| ------ | ------- |
| 0.00   | 6.00%   |
| 0.30   | 11.00%  |
| 0.65   | 16.00%  |
| 0.80   | 18.00%  |
</details>