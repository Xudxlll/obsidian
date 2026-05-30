# Tutorial Three

1. The zero rates are shown in the table below

<table><tr><td>Maturity (years)</td><td>Zero Rate (%)</td><td>Period (month-month)</td><td>Forward Rate (%)</td></tr><tr><td>0.5</td><td>4.0405</td><td></td><td></td></tr><tr><td>1.0</td><td>5.1293</td><td>6-12</td><td>6.2181</td></tr><tr><td>1.5</td><td>5.4429</td><td>12-18</td><td>6.0700</td></tr><tr><td>2.0</td><td>5.8085</td><td>18-24</td><td>6.9054</td></tr></table>

The following table gives the price of bond

<table><tr><td>BondPrincipal ($)</td><td>Time toMaturity (years)</td><td>Annual Coupon Rate*(%)</td><td>BondPrice ($)</td></tr><tr><td>100</td><td>1.20</td><td>10.0</td><td>?</td></tr></table>

? The coupons are paid every six months. All the rates are continuously compounded.

(a) Determine the value of the last bond.   
(b) Determine the bond yield of the last bond.   
(c) If the bond yield becomes 7% in 3 months, determine the price at that time.

# Solution.

(a) The cash flow of the bond is given as below.

<table><tr><td>Cash flow</td><td>5</td><td>5</td><td>105</td></tr><tr><td>Year(s) to maturity</td><td>0.2</td><td>0.7</td><td>1.2</td></tr></table>

We need to compute the zero rates for 0.2, 0.7 and 1.2 years. $R _ { 0 . 2 } \approx R _ { 0 . 5 } =$ 4.0405%.

$$
R _ {0. 7} \approx \frac {0 . 7 - 0 . 5}{1 - 0 . 5} R _ {1} + \frac {1 - 0 . 7}{1 - 0 . 5} R _ {0. 5} = 0. 4 * 5. 1 2 9 3 \% + 0. 6 * 4. 0 4 0 5 \% = 4. 4 7 6 0 2 \%.
$$

$$
R _ {1. 2} \approx \frac {1 . 2 - 1}{1 . 5 - 1} R _ {1. 5} + \frac {1 . 5 - 1 . 2}{1 . 5 - 1} R _ {1} = 0. 4 * 5. 4 4 2 9 \% + 0. 6 * 5. 1 2 9 3 \% = 5. 2 5 4 7 4 \%.
$$

The value of the last bond is about

$$
\begin{array}{l} 5 e ^ {- 0. 2 R _ {0. 2}} + 5 e ^ {- 0. 7 R _ {0. 7}} + 1 0 5 e ^ {- 1. 2 R _ {1. 2}} \\ = 5 e ^ {- 0. 2 * 4. 0 4 0 5 \%} + 5 e ^ {- 0. 7 * 4. 4 7 6 0 2 \%} + 1 0 5 e ^ {- 1. 2 * 5. 2 5 4 7 4 \%} = 1 0 8. 3 8 9. \\ \end{array}
$$

(b) Let R be the bond yield of the last bond. Then

$$
5 e ^ {- 0. 2 R} + 5 e ^ {- 0. 7 R} + 1 0 5 e ^ {- 1. 2 R} = 1 0 8. 3 8 9
$$

The Bisection method yields R 5.223%.

(c) In 3 months, the cash flow of the bond is

<table><tr><td>Cash flow</td><td>5</td><td>105</td></tr><tr><td>Year(s) to maturity</td><td>0.45</td><td>0.95</td></tr></table>

So the price is

$$
5 e ^ {- 0. 4 5 * 7 \%} + 1 0 5 e ^ {- 0. 9 5 * 7 \%} = 1 0 3. 0 9.
$$

2. The spot price of gold is \$1190 per ounce. The storage cost is \$0.88 per ounce per year payable quarterly (\$0.22 each quarter) in advance. Assuming that the risk-free interest rate (with monthly compounding) is 12% per annum, calculate the forward price of gold per ounce for delivery in 9 months.

# Solution.

The present value of the storage costs is

$$
0. 2 2 + 0. 2 2 \left(1 + \frac {12 \%}{12}\right) ^ {- 3} + 0. 2 2 \left(1 + \frac {12 \%}{12}\right) ^ {- 6} = 0. 6 4.
$$

The forward price is given by

$$
(1190 + 0.64) \left(1 + \frac{12\%}{12}\right)^{9} = \$ 1302.19.
$$

3. The following table gives the prices of bonds in a market.

<table><tr><td>Bond Principal ($)</td><td>Time to Maturity (years)</td><td>Coupon Rate* (%)</td><td>Bond Price ($)</td></tr><tr><td>100</td><td>0.50</td><td>0.0</td><td>98</td></tr><tr><td>100</td><td>1.00</td><td>0.0</td><td>95</td></tr></table>

In the same market, a stock is available. Its current price is \$100 and will pay a dividend \$10 in a half year. A forward contract maturing in one year on the stock is signed today. Three months later, the price of the stock is \$90 and the prices of bonds in the market are given below.

<table><tr><td>Bond Principal ($)</td><td>Time to Maturity (years)</td><td>Coupon Rate* (%)</td><td>Bond Price ($)</td></tr><tr><td>100</td><td>0.25</td><td>0.0</td><td>99</td></tr><tr><td>100</td><td>0.75</td><td>0.0</td><td>97</td></tr></table>

(a) Determine the delivery price of the forward contract.   
(b) Determine the value of the forward contract for the long position 3 months later.

# Solution.

(a) The delivery price of the forward contract is determined by

$$
K = (S - I) e ^ {r t}.
$$

By the first bond, we know that the present value of \$100 in a half year is \$98. So the present value of the dividend \$10 in 6 months is \$I = 9.8. Therefore the net present value of the stock is $S - I = 1 0 0 - 9 . 8 = \mathfrak { G } 9 0 . 2 .$ By the second bond, we know that the future value of \$95 in one year is \$100. So the forward value of stock in one year is $K = ( S - I ) e ^ { r t } = 9 0 . 2 / 9 5 * 1 0 0 = \ S 9 4 . 9 5$ . This is the delivery price of the forward contract.

(b) The value of the forward contract for the long position is determined by

$$
S - I - K e ^ {- r t}.
$$

Three months later, by the first bond, we know that the present value of \$100 in 3 months is \$99. So the value of the dividend \$10 in 3 months is $I = \$ 9.9$ . By the second bond, we know that the present value of \$100 in 9 months is \$97. So the present value of the delivery price in 9 months is $K e ^ { - r t } = 9 4 . 9 5 * 9 7 / 1 0 0 = \mathfrak { H } 9 2 . 1 0$ . Therefore, the value of value of the forward contract for the long position is $S - I - K e ^ { - r t } = 9 0 - 9 . 9 - 9 2 . 1 0 = - \Re { 1 2 }$ .

4. Select the features of the futures contract from blew.

(a) Private contract between 2 parties   
(b) Usually one specified delivery date   
(c) Traded on an exchange   
(d) Contract is usually closed out prior to maturity   
(e) Some credit risk   
(f) Settled at end of contract   
(g) Standardized contract

# Solution.

They are (c), (d), (g).

5. (a) In a market, the zero curve with continuous compounding is given by $R _ { t } =$ $ a + b t - e ^ { - c t }$ . Determine the instantaneous forward rate (short rate) with continuous compounding at time t .   
(b) In a market, the short rate with continuous compounding is given by $r _ { t } = a +$ $b t ^ { 2 }$ . Determine the zero curve and forward rate with continuous compounding from $t _ { 1 }$ to $t _ { 2 }$ .

# Solution.

(a) The short rate $\begin{array} { r } { r _ { t } = \frac { \mathrm { d } } { \mathrm { d } t } ( R _ { t } * t ) = \frac { \mathrm { d } } { \mathrm { d } t } ( a t + b t ^ { 2 } - t e ^ { - c t } ) = a + 2 b t + c t e ^ { - c t } - e ^ { - c t } } \end{array}$   
(b) Note $\begin{array} { r } { r _ { t } = \frac { \mathrm { d } } { \mathrm { d } t } ( R _ { t } * t ) , R _ { t } * t = \int _ { 0 } ^ { t } r _ { s } } \end{array}$ ds, so the forward rate from $t _ { 1 }$ to $t _ { 2 }$ is

$$
\begin{array}{l} R (t _ {1}, t _ {2}) = \frac {R _ {t _ {2}} * t _ {2} - R _ {t _ {1}} * t _ {1}}{t _ {2} - t _ {1}} = \frac {1}{t _ {2} - t _ {1}} \int_ {t _ {1}} ^ {t _ {2}} r _ {t} \mathrm{d} t \\ = \frac {1}{t _ {2} - t _ {1}} \int_ {t _ {1}} ^ {t _ {2}} (a + b t ^ {2}) \mathrm{d} t = a + \frac {1}{3} b (t _ {1} ^ {2} + t _ {1} t _ {2} + t _ {2} ^ {2}). \\ \end{array}
$$

The zero rate is given by

$$
R _ {t} = R (0, t) = a + \frac {1}{3} b t ^ {2},
$$

or equivalently,

$$
R _ {t} = \frac {1}{t} \int_ {0} ^ {t} r _ {s} \mathrm{d} s = \frac {1}{t} \int_ {0} ^ {t} (a + b s ^ {2}) \mathrm{d} s = a + \frac {1}{3} b t ^ {2}.
$$

6. The following table gives the information of bonds in the market.

<table><tr><td>Bond Name</td><td>Bond Principal ($)</td><td>Time to Maturity (years)</td><td>Coupon Rate (%)</td><td>Market Price ($)</td></tr><tr><td>A</td><td>100</td><td>0.9</td><td>0</td><td>95</td></tr><tr><td>B</td><td>100</td><td>1.9</td><td>0</td><td>88</td></tr><tr><td>C</td><td>100</td><td>1.9</td><td>8</td><td>104</td></tr></table>

The coupons are paid annually. If shorting is allowed, can you find an arbitrage opportunity?

# Solution.

From A we can find the 0.9-year zero rate is $\begin{array} { r } { R _ { 0 . 9 } = \frac { 1 } { 0 . 9 } \ln ( 1 0 0 / 9 5 ) = 5 . 7 \% } \end{array}$ . From B we can find the 1.9-year zero rate is $\begin{array} { r } { R _ { 1 . 9 } = \frac { 1 } { 1 . 9 } \ln ( 1 0 0 / 8 8 ) = 6 . 7 \% } \end{array}$ . Under these rates, the price of bond C should be

$$
8 e ^ {- 0. 9 R _ {0. 9}} + (1 0 0 + 8) e ^ {- 1. 9 R _ {1. 9}} = 1 0 2. 6 4.
$$

This is lower than the market price, so there is an arbitrage opportunity.

Since the bond C is over-priced in the market, we should take short position in it. At the same time, we nee to take long positions in A and B to cover the coupons paid to the long position of C.

Consider a portfolio: Long in 0.08 share of A and 1.08 shares of B and cash " = 1.36, short in 1 share of C. Now its value is

$$
\Pi (0) = 0. 0 8 * 9 5 + 1. 0 8 * 8 8 + 1. 3 6 - 1 0 4 = 0.
$$

In 0.9 year, we need to pay a coupon of \$8 as we are in the short position of 1 share of C, but we also receive \$0.08 ⇤ 100 from the bond A, so the portfolio becomes: Long in 1.08 shares of B and cash " = 1.36, short in 1 share of C. In 1.9 years from now, its value will be

$$
\Pi (1. 9) = 1. 0 8 * 1 0 0 - (1 0 0 + 8) + 1. 3 6 = 1. 3 6 > 0.
$$

This is an arbitrage portfolio.

We can also invest the cash " = 1.36 in the bond B to achieve a higher final value.