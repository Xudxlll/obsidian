# Tutorial Two

1. The six-month and one-year zero rates are both 10% per annum. For a bond that has par value \$100 and a life of 18 months and pays a coupon of 8% per annum (with semiannual payments and one having just been made), the yield is 10.4% per annum. What is the bond’s price? What is the 18-month zero rate? All rates are quoted with semiannual compounding.

# Solution.

Its price is obtained by discounting the cash flows at 10.4%. The price is

$$
4 * \left(1 + \frac {10.4\%}{2}\right) ^ {- 1} + 4 * \left(1 + \frac {10.4\%}{2}\right) ^ {- 2} + (100 + 4) * \left(1 + \frac {10.4\%}{2}\right) ^ {- 3} = 96.74.
$$

If the 18-month zero rate is R, we must have

$$
4 * \left(1 + \frac {10\%}{2}\right) ^ {- 1} + 4 * \left(1 + \frac {10\%}{2}\right) ^ {- 2} + (100 + 4) * \left(1 + \frac {R}{2}\right) ^ {- 3} = 96.74,
$$

which gives $R = 1 0 . 4 2 \%$ .

2. Suppose that zero interest rates with continuous compounding are as follows:

<table><tr><td>Maturity (months)</td><td>Rate (% per annum)</td></tr><tr><td>3</td><td>8.0</td></tr><tr><td>6</td><td>8.2</td></tr><tr><td>9</td><td>8.4</td></tr><tr><td>12</td><td>8.5</td></tr><tr><td>15</td><td>8.6</td></tr><tr><td>18</td><td>8.7</td></tr></table>

Calculate forward interest rates for the second, third, fourth, fifth and sixth quarters.

# Solution.

Because the zero interest rates $R _ { t }$ are given as continuously compounded, the forward rate from s to t with continuous compounding is determined by

$$
R _ {s, t} = \frac {t R _ {t} - s R _ {s}}{t - s} = R _ {t} + \frac {R _ {t} - R _ {s}}{t - s} s.
$$

Therefore, the forward interest rate for Q2 is

$$
R _ {3, 6} = \frac {6 R _ {6} - 3 R _ {3}}{6 - 3} = R _ {6} + R _ {6} - R _ {3} = 8.4 \%.
$$

Similarly, Q3: 8.8% Q4: 8.8% Q5: 9.0% Q6: 9.2%.

3. A three-year bond with par value 100 provides annual coupon rate of 8% with semiannual payment (with one having just been made) and has a cash price of 104. What is the bond’s yield?

# Solution.

The bond pays \$4 in 6, 12, 18, 24 and 30 months, and \$104 in 36 months. The bond yield is the value of y that solves

$$
4 e ^ {- 0. 5 y} + 4 e ^ {- 1. 0 y} + 4 e ^ {- 1. 5 y} + 4 e ^ {- 2. 0 y} + 4 e ^ {- 2. 5 y} + 1 0 4 e ^ {- 3. 0 y} = 1 0 4.
$$

We use the bisection method to solve it. Let $x = e ^ { - 0 . 5 y }$ . Then

$$
f (x) := 4 x + 4 x ^ {2} + 4 x ^ {3} + 4 x ^ {4} + 4 x ^ {5} + 1 0 4 x ^ {6} = 1 0 4.
$$

Clearly, $0 < x < 1$ , so

$$
4 + 4 + 4 + 4 + 4 + 1 0 4 x ^ {6} > f (x) = 1 0 4,
$$

and

$$
(4 + 4 + 4 + 4 + 4 + 1 0 4) x ^ {6} <   f (x) = 1 0 4,
$$

so

$$
\frac {8 4}{1 0 4} <   x ^ {6} <   \frac {1 0 4}{1 2 4}, \quad 0. 9 6 5 <   x <   0. 9 7 2.
$$

Try the middle,

$$
f \left(\frac {0 . 9 6 5 + 0 . 9 7 2}{2}\right) = f (0. 9 6 8 5) = 1 0 4. 0 1 6 \approx 1 0 4.
$$

So $x = 0 . 9 6 8 5$ and $y = - 2 \log x = 6 . 4 \%$ .

4. The following table gives the prices of bonds

<table><tr><td>Bond Principal ($)</td><td>Time to Maturity (years)</td><td>Coupon Rate* (%)</td><td>Bond Price ($)</td></tr><tr><td>100</td><td>0.50</td><td>0.0</td><td>98</td></tr><tr><td>100</td><td>1.00</td><td>0.0</td><td>95</td></tr><tr><td>100</td><td>1.50</td><td>6.2</td><td>101</td></tr><tr><td>100</td><td>2.00</td><td>8.0</td><td>104</td></tr></table>

? The coupons are paid every six months. A coupon has just been paid.

(a) Calculate zero rates for maturities of 6 months, 12 months, 18 months and 24 months.   
(b) What are the forward rates for the periods: 6 months to 12 months, 12 months to 18 months, 18 months to 24 months?

(c) Estimate the price and yield of a two-year bond with par value 100 providing a semiannual coupon of 7% per annum.

# Solution.

(a) The zero rate for a maturity of six months, expressed with continuous compounding is $2 \ln ( 1 0 0 / 9 8 ) \ : = \ : 4 . 0 4 0 5 \%$ . The zero rate for a maturity of one year, expressed with continuous compounding is ln $( 1 0 0 / 9 5 ) = 5 . 1 2 9 3 \%$ . The 1.5-year rate is R where

$$
3. 1 e ^ {- 0. 0 4 0 4 0 5 \times 0. 5} + 3. 1 e ^ {- 0. 0 5 1 2 9 3 \times 1} + 1 0 3. 1 e ^ {- R \times 1. 5} = 1 0 1.
$$

The solution to this equation is $R = 0 . 0 5 4 4 2 9$ . The 2-year rate is R where

$$
4 e ^ {- 0. 0 4 0 4 0 5 \times 0. 5} + 4 e ^ {- 0. 0 5 1 2 9 3 \times 1} + 4 e ^ {- 0. 0 5 4 4 2 9 \times 1. 5} + 1 0 4 e ^ {- R \times 2} = 1 0 4.
$$

The solution to this equation is $R = 0 . 0 5 8 0 8 5$ . These results are shown in the table below

<table><tr><td>Maturity (years)</td><td>Zero Rate (%)</td><td>Period (month-month)</td><td>Forward Rate (%)</td></tr><tr><td>0.5</td><td>4.0405</td><td></td><td></td></tr><tr><td>1.0</td><td>5.1293</td><td>6-12</td><td>6.2181</td></tr><tr><td>1.5</td><td>5.4429</td><td>12-18</td><td>6.0700</td></tr><tr><td>2.0</td><td>5.8085</td><td>18-24</td><td>6.9054</td></tr></table>

(b) The continuously compounded forward rates calculated are shown in the third column of the table.

(c) The price of the bond is

$$
3. 5 e ^ {- 0. 0 4 0 4 0 5 \times 0. 5} + 3. 5 e ^ {- 0. 0 5 1 2 9 3 \times 1} + 3. 5 e ^ {- 0. 0 5 4 4 2 9 \times 1. 5} + 1 0 3. 5 e ^ {- 0. 0 5 8 0 8 5 \times 2} = 1 0 2. 1 3.
$$

The yield on the bond, y satisfies

$$
3. 5 e ^ {- y \times 0. 5} + 3. 5 e ^ {- y \times 1. 0} + 3. 5 e ^ {- y \times 1. 5} + 1 0 3. 5 e ^ {- y \times 2. 0} = 1 0 2. 1 3.
$$

The bisection method gives the solution to this equation $y = 0 . 0 5 7 7 2 3$ . The bond yield is therefore 5.7723%.

5. Suppose that zero interest rates with semi-annual compounding are as follows:

<table><tr><td>Maturity (months)</td><td>Rate (% per annum)</td></tr><tr><td>3</td><td>8.0</td></tr><tr><td>6</td><td>8.2</td></tr><tr><td>9</td><td>8.4</td></tr><tr><td>12</td><td>8.5</td></tr><tr><td>15</td><td>8.6</td></tr><tr><td>18</td><td>8.7</td></tr></table>

Calculate forward interest rates with semi-annual compounding for the second, third, fourth, fifth and sixth quarters.

# Solution.

Let r denote the zero interest rate with continuous compounding and R the zero interest rate with semi-annual compounding. Then

$$
\left(1 + \frac {R}{2}\right) ^ {2} = e ^ {r}.
$$

So the equivalent zero interest rates with continuous compounding are given as follows:

<table><tr><td>Maturity (months)</td><td>Rate (% per annum)</td></tr><tr><td>3</td><td>7.844</td></tr><tr><td>6</td><td>8.036</td></tr><tr><td>9</td><td>8.228</td></tr><tr><td>12</td><td>8.324</td></tr><tr><td>15</td><td>8.420</td></tr><tr><td>18</td><td>8.516</td></tr></table>

Using the method of Question 2, we get the forward interest rates with continuous compounding are

$$
Q2:8.228\% ,\quad Q3:8.612\% ,\quad Q4:8.612\% ,\quad Q5:8.804\% ,\quad Q6:8.996\% ,
$$

and the corresponding forward interest rates with semi-annual compounding are

$$
Q 2: 8.4\%, \quad Q 3: 8.8\%, \quad Q 4: 8.8\%, \quad Q 5: 9\%, \quad Q 6: 9.2\% .
$$