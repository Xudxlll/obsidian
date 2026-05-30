# AMA535: Mathematics of Derivative Pricing AMA535A: Mathematical Models of Derivative Pricing

XU, Zuo Quan

The Hong Kong Polytechnic University

# Interest & Bond

# Types of Interests

# Simple interest

The simple interest is calculated based only on the amount of initially investment (called principal). Accumulated interest from prior periods is not used in calculations for the following periods. Simple interest is normally used for a single period of less than a year, such as 30 or 60 days.

Simple Interest = principal ⇤ interest rate ⇤ number of periods.

# Example 3.1

Deposit \$10, 000 for 3 months at 5% annual simple rate. Then

Simple Interest = 10000 5% 3/12 = 125.

# Types of Interests

# Compound interest

Additional to simple interest, also get interest on the interest.

Discretely compounded: The process of discrete compounding is utilized at specific finite periods of time, such as daily, monthly, or annually.

Continuously compounded: Calculating the compounding period infinitesimally small.

# Discretely Compounded Interest

Suppose you invest M dollars in a bank account with a fixed annual interest rate r.

If interest is paid every half-year at rate r/2, after half a year:

$$
M (1 + r / 2).
$$

After another half-year:

$$
M (1 + r / 2) ^ {2}.
$$

# Discretely Compounded Interest (General Case)

If interest is compounded m times per year, the value after one year is:

$$
M (1 + r / m) ^ {m}.
$$

After n years:

$$
M (1 + r / m) ^ {n m}.
$$

Here, r is called the annual percentage rate (APR) or nominal rate.

# Effective Annual Rate (EAR)

• APR does not reflect the true interest earned!   
The effective annual rate (EAR) is the actual interest earned in one year, accounting for compounding.

# Theorem

The relationship between EAR and m-times compounded APR is:

$$
\operatorname{EAR} = \left(1 + \frac {\operatorname{APR}}{m}\right) ^ {m} - 1.
$$

# EAR Example

# Example 3.2

Suppose the APR is 12% compounded monthly. Then the EAR is:

$$
E A R = \left(1 + \frac {12\%}{12}\right) ^ {12} - 1 = 12.68 \% .
$$

# Exercise 3.1

Which is larger, EAR or APR? Why?

# Continuously Compounded Interest

If the APR r is compounded infinitely often, we have continuous compounding:

# Theorem

The relationship between EAR and continuous compounded APR is:

$$
\mathsf {E A R} = \lim _ {m \to \infty} \left(1 + \frac {\mathsf {A P R}}{m}\right) ^ {m} - 1 = e ^ {\mathsf {A P R}} - 1.
$$

# Example 3.3

Suppose the APR is 12% compounded continuously. Then the EAR

$$
E A R = e ^ {0. 1 2} - 1 = 1 2. 7 4 \%.
$$

# Continuously Compounded Interest

# Exercise 3.2

Suppose the continuously compounded APR is r. Show that if we deposit M (0) dollars at time 0, then after t years:

$$
M (t) = M (0) e ^ {r t}.
$$

# Types of Interest Rates

There are different types of interest rates in the market:

Government rate: The rate implied by government-issued bonds. The most important are Treasury rates, which are often artificially low due to tax and regulatory factors.

Interbank rate: The rate at which banks lend to each other. The most widely used is LIBOR (London Interbank Offered Rate). Other examples include HIBOR (Hong Kong) and SHIBOR (China).

# What is a Bond?

# Bond

A bond is a type of fixed-income security. In essence, a bond is a loan: the bond issuer (borrower) promises to repay the amount borrowed (called the face value or par value) at a specified maturity date, plus interest at an agreed rate. Bonds are issued by governments and corporations to raise capital, and are bought by investors seeking predictable returns.

# Types of Bonds

Every bond has a face value (par value), which is the amount the holder receives at maturity. There are two main types of bonds:

Zero-coupon (discount) bond: Pays only the face value at maturity; sold at a discount to face value.

Coupon bond: Pays periodic interest (coupons) during its life, plus the face value at maturity.

# Example 3.4

US Treasury bonds have face values in multiples of \$1,000. Twoyear bonds are typically coupon bonds; 30-year Treasury bonds are often zero-coupon bonds.

# Zero Rate: Definition

# t-year zero rate

The t-year zero rate (or zero-coupon yield) is the annualized rate of return on a zero-coupon bond maturing in t years from now. It is the interest rate for an investment made today and held for t years with no intermediate payments.

If a zero-coupon bond with face value F matures in t years and is currently priced at $P ,$ , then the (continuously compounded) zero rate $R _ { t }$ satisfies:

$$
P e ^ {t R _ {t}} = F.
$$

Thus,

$$
R _ {t} = \frac {1}{t} \ln \left(\frac {F}{P}\right).
$$

# Zero Rate: Practical Computation

In practice, most bonds are coupon bonds, and zero-coupon bonds for every maturity may not exist. To extract zero rates from market data, we use the bootstrap method:

Start with the shortest-maturity zero-coupon bond to find the shortest zero rate.   
Use coupon bond prices and previously determined zero rates to solve for longer-maturity zero rates.

# Bootstrap Method: Example

Example 3.5 (Market Data) 

<table><tr><td>Face value</td><td>Time to maturity (years)</td><td>Semi-annual coupon</td><td>Price</td></tr><tr><td>100</td><td>0.25</td><td>0</td><td>97.5</td></tr><tr><td>100</td><td>0.50</td><td>0</td><td>94.9</td></tr><tr><td>100</td><td>1.00</td><td>0</td><td>90.0</td></tr><tr><td>100</td><td>1.50</td><td>4</td><td>96.0</td></tr><tr><td>100</td><td>2.00</td><td>6</td><td>101.6</td></tr></table>

One coupon has just been paid if today is a payment date.

From the first row:

$$
97.5 e^{0.25R_{0.25}} = 100 \quad \Longrightarrow \quad R_{0.25} = 10.127\% .
$$

Similarly, $R _ { 0 . 5 } = 1 0 . 4 6 9 \% , R _ { 1 } = 1 0 . 5 3 6 \%$ .

# Bootstrap Method: Coupon Bond

There is no 1.5-year zero-coupon bond available in the table, however the 1.5-year zero rate $R _ { 1 . 5 }$ can be computed from the fourth bond. The cash flow for the bond is given as below.

<table><tr><td>$0</td><td>$4</td><td>$4</td><td>$100 + 4</td></tr><tr><td>now</td><td>6 months</td><td>12 months</td><td>18 months</td></tr></table>

Using the zero rates obtained above, we add the present values of all these payments and equate the sum to the present value of the bond:

$$
4 e ^ {- 0. 5 * R _ {0. 5}} + 4 e ^ {- 1 * R _ {1}} + 1 0 4 e ^ {- 1. 5 * R _ {1. 5}} = 9 6. 0.
$$

The answer is $R _ { 1 . 5 } = 1 0 . 6 8 1 \%$ .

# Bootstrap Method: Summary Table

<table><tr><td>Time to Maturity (years)</td><td>Zero Rate (%)</td></tr><tr><td>0.25</td><td>10.127%</td></tr><tr><td>0.50</td><td>10.469%</td></tr><tr><td>1.00</td><td>10.536%</td></tr><tr><td>1.50</td><td>10.681%</td></tr><tr><td>2.00</td><td>10.808%</td></tr></table>

# Zero Curve

![](images/7b495077e1614d406fa8e660df5d83206ea8473cfecac808c5cc807360098b13.jpg)

<details>
<summary>line</summary>

| X | Y |
|---|---|
| 0.25 | 10.1 |
| 0.5 | 10.45 |
| 1 | 10.55 |
| 1.5 | 10.65 |
| 2 | 10.85 |
| 2.5 | 10.85 |
</details>

Time to maturity (years)

# Bond Yield Measures

When a bond is purchased at a price different from its face value, three common yield measures are used:

Coupon rate: Annual coupon payment as a percentage of face value.

Current yield: Annual coupon payment divided by current market price.

Yield-to-maturity (YTM): The annualized return if the bond is held to maturity, accounting for all coupons and price difference, also called bond yield.

# Bond Yield: Example

Consider the fifth bond in the earlier table:

Face value: \$100; Price: \$101.6   
• Coupon: \$6 every six months (12% annual coupon rate)   
Current yield: 6/101.6 = 5.91% semi-annually; 11.82% annually   
Yield-to-maturity y solves:

$$
6 e ^ {- 0. 5 y} + 6 e ^ {- 1. 0 y} + 6 e ^ {- 1. 5 y} + 1 0 6 e ^ {- 2. 0 y} = 1 0 1. 6.
$$

Solution: y = 10.79% (below the 2-year zero rate 10.808%)

# Exercise 3.3

What is the new bond price after one month if the yield remains unchanged?

# Forward Rate: Concept

# Forward Rate

A forward rate is the interest rate implied by current zero rates for a period of time beginning in the future. While zero rates apply from today to a future date, forward rates apply between two future dates.

# Forward Rate: Example

# Example 3.6

Example Suppose the 1-year zero rate is 8% and the 2-year zero rate is 8.5% (both continuously compounded). What is the implied forward rate for the second year?

Invest \$100 at 8% for 1 year: $\$ 100\to\$ 100 e ^ { 0.08 }$ .   
Reinvest at forward rate r for the second year: $\$ 100 e ^ { 0.0 8 } e ^ { r } =$ $\$ 100 e ^ { 0.08 + r }$ .   
Alternatively, invest for 2 years at 8.5%: $\$ 100 e ^ { 2 \times 0.08 5 }= \ S 100 e ^ { 0 . 1 7 }$ .   
Equate: $e ^ { 0 . 0 8 + r } = e ^ { 0 . 1 7 } \implies r = 0 . 0 9 = 9 \%$

# Forward Rate: General Formula

Let $R _ { t }$ be the t-year zero rate, and $R _ { s , t }$ the forward rate from s to t (both continuously compounded). Then:

$$
e ^ {s R _ {s}} \cdot e ^ {(t - s) R _ {s, t}} = e ^ {t R _ {t}}
$$

# Theorem

The continuously compounded zero and forward rates satisfy

$$
\boxed {R _ {s, t} = \frac {t R _ {t} - s R _ {s}}{t - s}}
$$

# Short Rate (Instantaneous Forward Rate): Concept

# Short Rate

The instantaneous forward rate or short rate at time t is:

$$
r _ {t} = \lim _ {s \to t} R _ {s, t} = R _ {t} + t R _ {t} ^ {\prime},
$$

where $R _ { t }$ is the continuously compounded t-year zero rate. It represents the instantaneous annualized return at time t.

# Short Rate and Zero-Coupon Bond Price

Let $P _ { t }$ be the price of a zero-coupon bond with par value 1 maturing in t years. Then:

$$
P _ {t} = e ^ {- t R _ {t}},
$$

where $R _ { t }$ is the continuously compounded t-year zero rate.

# Theorem 3.1

It holds that

$$
r _ {t} = R _ {t} + t R _ {t} ^ {\prime} = - (\ln P _ {t}) ^ {\prime} = - \frac {P _ {t} ^ {\prime}}{P _ {t}},
$$

$$
R _ {t} = \frac {1}{t} \int_ {0} ^ {t} r _ {s} \mathrm{d} s,
$$

$$
P _ {t} = e ^ {- \int_ {0} ^ {t} r _ {s} \mathrm{d} s}.
$$

# Present Value and Short Rate

Suppose $M ( t )$ is the value of a bank account at time t. Over a small interval $[ t , t + \Delta ]$ :

$$
\text { Average   return   rate } = \frac {M (t + \Delta) - M (t)}{M (t) \Delta}
$$

Taking $\Delta \to 0$ gives the instantaneous return rate (short rate):

$$
\boxed {r _ {t} = \frac {M ^ {\prime} (t)}{M (t)}}.
$$

# Present Value (Discounting)

Solving the differential equation for M (t) gives

$$
\boxed {M (T) = M (t) e ^ {\int_ {t} ^ {T} r _ {s} \mathrm{d} s},} \boxed {M (t) = M (T) e ^ {- \int_ {t} ^ {T} r _ {s} \mathrm{d} s}.}
$$

We call M (T ) the future value of M (t), and M (t) the present value or discounting of $M ( T )$ .

# Money has time value

One needs to pay the amount M(t) now (time t) in order to receive a guaranteed amount M (T ) at the future (time T ). In other words, M (t) at time t is equivalent to M (T ) at time T if invested at the prevailing short rate.