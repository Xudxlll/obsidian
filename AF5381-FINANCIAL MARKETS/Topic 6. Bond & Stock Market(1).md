# Topic 6. Bond & Stock Market(1)

## Slide 1

Topic 6.Bond and Stock Valuation
Bond Price (Ch.8)
Bond Yields
Bond Quotation
Stock Price (Ch.9)
Parameter Estimation & Comparables
Growth Opportunities
The Stock Markets
4:

## Slide 2

Bond Features
Nature
Bonds are debt. Issuers are borrowers and holders are creditors.
The indenture is the contract between the issuer and the bondholder.
The indenture gives the coupon rate, maturity date, and par value.
Bonds consist of
Face or par value is typically $1000; this is the principal repaid at maturity.
The coupon rate determines the interest payment.
Interest is usually paid semiannually.
The coupon rate can be zero.

## Slide 3

Bond Features
Accrued Interest
The quoted price (called the “clean price”) does not include the interest accrued between coupon payment dates. Specifically, the investor must compensate the seller for the coupon interest earned during the period, which is called the dirty/full/invoice price :
Invoice Price = Quoted Price + C * (t/182)
where C is the coupon payment and t is the dates lapsed after the previous coupon payment date.
E.g. You bought a 12% semiannual coupon-paying bond with 4 months to the next coupon-paying date at a price of $1,080.
Invoice price = $1,080.
Accrued interest = $60 x 2/6 = $20.
Clean price = $1,080 - $20 = $1,060.
Note that for corporate bonds, we assume one month (year) having 30 (360) days but for Treasury bonds, actual day counts are used.
4:

## Slide 4

Bond Features
Types
U.S. Treasury Bonds
Bills, Notes, and Bonds
Corporate Bonds
Straight (plain vanilla) bonds
Fixed coupon rate
Floating rate bonds
adjustable coupon rate
Option-embedded Bonds
Callable/ Puttable/Convertible bonds

## Slide 5

Bond Features
Types
Structured Bonds
Inverse Floaters
coupon rate varies inversely with a benchmark interest rate.
Asset-Backed Bonds
ELNs/RELNs
Currency Linked Investments (CLIs)
Indexed Bonds
Treasury Inflation Protected Securities (TIPS).
Assume 4% coupon rate
Year 1: $1,000 x 1.02 x 4% = $40.80.
Year 2: $1,020 x 1.03 x 4% = $42.024.
Note that TIPS have semi-annual payments with a lag in the inflation adjustment.

## Slide 6

Inflation and Interest Rates
Real versus Nominal Rates
The Fisher Equation
(1 + Nominal interest rate)
= (1 + Real interest rate) * (1 + Inflation rate)
Nominal interest rate
 Real interest rate + Inflation rate
Similarly, cash flows in nominal terms can be expressed in real terms by
(Real cash flows)o
= (Nominal cash flows)t / (1 + Inflation rate)t.
Inflation Risk and Inflation-Linked Bonds
Any fixed-income securities face inflation risk as the payments are fixed.
US Treasury inflation-protected securities (TIPS) and HK inflation-linked retail bonds (iBond) are bonds with promised payments specified in real terms, not nominal terms.
The difference in yields of the Treasury Bond and TIPS of the same maturity provides the expected inflation rate over the bonds’ maturity period.
4:

## Slide 7

Bond Markets
How Bonds are Bought & Sold
Bond Price Reporting
Corporate bond dealers are required to report trade information through the Trade Reporting and Compliance Engine (TRACE).
The Financial Industry Regulatory Authority (FINRA) provides the daily data from TRACE by reporting the most active issues.
PV of the bond 	= $100
YTM		= {Dollar coupon + (Face Value – Price)/t}/{FV – 2*Price)/3}
= {2.95 + (100 – 113)/5.5}/{100 – 2*113)/3}= 0.586/108.66
= 0.54%.
YTM		= YIELD("1/1/20", "1/7/25", 2.95%, 112.998, 100, 2)
= 0.0055.
| Issuer | Symbol | Callable | Type | Coupon | Maturity | Moody’s | S&P | Price | Yield |
| CISCO | CSCO4337700 | Yes | Corp Bond | 2.600 | 2/28/2023 | A1 | AA- | 105.699 | 0.315 |
| CISCO | CSCO4337813 | No | Corp Bond | 2.950 | 2/28/2026 | A1 | AA- | 112.998 | 0.550 |
4:

## Slide 8

Bond Markets
How Bonds are Bought & Sold
Bond Price Reporting
Sample TRACE Bond Quotations
Most active investment grade bonds
The price of the Noble Energy bond dropped by 0.294%. What about the bond yield?
Note that Noble Energy was at a premium and Pacific Gas & Elect was at a discount.
Treasury Bond Price Reporting (from wsj.com)
Prices are quoted as a percentage of face value (of $1,000)
The last bond listed (30-year bond) is called the ‘bellwether” bond.
| Issuer | Symbol | Coupon | Maturity | Moody’s/ S&P | High | Low | Last | Change | Yield% |
| Noble Energy | NBL4529193 | 4.950% | 8/15/2047 | Baa3/ BBB- | 134.139 | 133.221 | 133.593 | -0.294 | 3.084 |
| Pacific Gas & Elec | PCG5002762 | 3.300% | 8/01/2040 | Baa3/ BBB- | 94.699 | 93.599 | 93.781 | -1.622 | 3.745012 |
| Maturity | Coupon | Bid | Asked | Chg | Asked Yld |
| 8/15/2028 | 2.875 | 118.116 | 118.126 | -0.03 | 0.517 |
| 8/15/2050 | 1.375 | 100.202 | 100.222 | 0.02 | 1.347 |
4:

## Slide 9

How to Value Bonds
Semi-annual coupon payments
e.g.: A bond of face value $1,000, 7 years to maturity, has a coupon rate of 14% paid semi-annually. What is its price if the market rate is 14%?
Answer:
PV(coupons) = $70 x (1 – 1/1.0714) / 0.07
= $612.18.
PV(par value) = $1,000/1.0714 = $ 387.82.
Bond price = $1,000.
4:

## Slide 10

How to Value Bonds
Note that bond price will change only because r and t change.
e.g.: Assume right after you have bought the above bond, the market rate goes up to 16%. What is its price now?
Ans.: 	PV(coupons) = $70 x (1 – 1/1.0814)/0.08 = $577.10
PV(par value) = $1,000/1.0814 = $340.46.
Bond price = $917.56.
e.g.: Assume one year has passed and the market rate remains 16%. What is its price now?
Ans.: 	PV(coupons) = $70 x (1 – 1/1.0812)/0.08 = $527.52
PV(par value) = $1,000/1.0812 = $ 397.11.
Bond price = $ 924.64.
Console
d
4:

## Slide 11

Bond Yields (Returns)
Different Measures
The rates of return of investing in a bond are called yields. Perhaps a bit confusing, there can be different ways to measure and make sure, they measure different things.
Coupon Yield
Coupon Yield = Coupon Payments / Face Value = Coupon Rate.
Current Yield
Current Yield = Coupon Payments / Bond Price .
Yield to Maturity (YTM)
Bond Price =
It is the discount rate that equates bond price with its discounted cash flows.
It is usually referred to as the bond yield.
4:

## Slide 12

Bond Yields
e.g. Suppose a 10-year, 8% coupon bond with face value of $1,000 is trading at $980. What is its YTM if coupons are paid semi-annually?
Ans.: 980 = 40 x PVAF20, r% + 1,000 x PVIF20, r%.
r = YTM = 8.298%.
Note that YTM is quoted like APR, the EAR = 8.46%.
Spreadsheet formula = YIELD(settlement, holding pd, rate, price, face value, frequency) = YIELD("1/1/00", "1/1/10", 8%, 98, 100, 2) = 0.0829823.
4:

## Slide 13

Bond Yields
Realized Compound Yield
Realized yield is the actual rate of return of holding a bond to maturity with coupon reinvestment.
e.g. Consider a 2-year, par-value bond of annual coupon payment of $100 that can be reinvested at 10%.
Bond total value at maturity = $100 x 1.10 + $1,100 = $1,210.
Actual total ROR = $(1,210 – 1,000)/$1,000 = 0.21.
Realized Yield = [(1 + 0.21)] – 1 = 10%.
Hence, it can be seen that if coupons can be reinvested at the rate of YTM, the realized (actual) bond yield will be the same as the YTM.
However, if coupons cannot be reinvested at the rate of YTM, the realized (actual) bond yield will not be the same as the YTM.
e.g. Consider the previous example but the coupons can be reinvested at 8%.
Bond total value at maturity = $100 x 1.08 + $1,100 = $1,208.
Actual total ROR = $(1,208 – 1,000)/$1,000 = 0.208.
Realized Yield = [(1 + 0.208)] – 1 = 9.91%.
4:

## Slide 14

Bond Yields
Holding Period Yield (HPY)
e.g. Consider a 30-year, par-value bond of annual coupon payment of $80 that sells at $1,050 at yearend.
HPY = [$(80 + 1,050) / $1,000] – 1 = 13%.
Notice that the bond’s initial YTM is 8% and is below 8% at yearend.
Notice that such definition of HPY is not the actual holding-period return.
e.g. Peter purchased a 20-year 8% coupon bond for $828.40. The YTM is 10%. The interest rate then changed to 6% and maintained there till Peter sold the bond after 3 years at a yield of 7%.
HPY
Bond price after 3 years:
$40 * PVAF34,3.5% + $1,000 * PVIF34,3.5% = $1,098.51.
$828.40 = $40 * PVAF6,r% + $1,098.51 * PVIF6,r%
HPY = r = 9.14% (or 18.28% p.a.).
= YIELD(settlement, holding pd, rate, price, resale price, frequency)
4:

## Slide 15

Bond Yields
The Relationship among Various Measures
If  = T then HPY  YTM.
Coupon yield = YTM if the bond is purchased at par and held to maturity.
Current yield = YTM if the bond is a perpetuity.
YTM = Current Yield + Capital Gains Yield.
YTM = ROR = (P1 + C + Po) / Po.
4:

## Slide 16

Callable Bonds
Valuation:
Callable Bond = Straight Bond - Call Value
The market value of callable bond is less than comparable straight bond.
The yield-to-maturity of a callable bond is greater than that of a comparable straight bond.
4:

## Slide 17

Callable Bonds & Yields
Valuation:
Callable Bond = Straight Bond - Call Value
The market value of callable bond is less than comparable straight bond.
YTM of a callable bond > YTM of a comparable straight bond.
If a bond is callable, YTC is the more relevant yield than YTM, especially for premium bonds with high coupons.
US newspapers report YTC for premium bonds and YTM for discount bonds.
Yield Graph
4:

## Slide 18

Callable Yields
Yield to (First) Call
It is calculated as YTM except using call price as the par value and the first callable date as the maturity date.
e.g. 30-year, 8% coupon bond sells for $1,150 and is callable in 10 years at a call price of $1,100.
4:

## Slide 19

Determinants of Bond Yields
The Term Structure of Interest Rates
It is the relationship  between ST and LT interest rates.
To be more precise, it is the nominal interest rates on default-free, pure discount bonds of all maturities.
There are essentially 3 shapes of the term structure.
Upward sloping
Hump shape
Downward sloping
There are 3 basic components that determine the shape of the term structure.
The real rate of interest
The rate of inflation (the inflation premium)
The interest rate risk (the interest rate risk premium)
4:

## Slide 20

Determinants of Bond Yields
Bond Yields and the Yield Curve
The WSJ provides a plot of T-yields relative to maturity, which is called Treasury Yield Curve.
The T-yield curve and the term structure of interest rates are almost the same except that the former is based on coupon bond yields and the latter is based on pure discount bonds.
In general, bonds bear the following risk premia.
The default risk premium
The taxability premium
A liquidity premium
4:

## Slide 21

The Stock Markets
Dealers & Brokers
A dealer maintains an inventory and posts bid and ask quotes to stand ready to buy and sell at any time.
A broker brings buyers and sellers together without maintaining an inventory.
Organization of the NYSE
Members (trading license holders of 3 types)
Designated market makers (DMMs) --- formally known as “specialists”.
Floor brokers --- generally employees of large brokerage firms such as Merrill Lynch.
Supplementary liquidity providers (SLPs) --- they are floor traders of very small number.
Operations
Floor Activity
Arca (an e-trading platform)
Types of Orders
Market order
Limit order
Stop (buy/sell) order
Day order vs good-till-canceled order
4:

## Slide 22

The Stock Markets
NASDAQ Operations
Major differences with the NYSE
A pure computer network with no physical location
Has a multiple market maker system.
Often being called an OTC market.
In the late 1990s, it was opened to so-called electronic communications networks (ECNs), websites that allow investors to trade directly with one another.
Stock Market Reporting
4:

## Slide 23

Stock Valuation
Dividends versus Capital Gains
The value of any financial asset equals the PV of all of its future cash flows. Hence, the value of a stock:
(What happen if a stock never pays dividends?)
4:

## Slide 24

Valuation of Common Stocks
Valuation of Different Types of Stocks
Zero Growth
Dt = D
This pricing relationship is true also for preferred stocks.
Required ROR = Dividend Yield (as there is no capital gain)
Constant Growth (Gordon Growth Model)
D2 = D1(1+g)
D3 = D1(1+g)2
Dt = D1(1+g)t-1
4:

## Slide 25

Valuation of Common Stocks
4:

## Slide 26

Valuation of Common Stocks
Differential Growth
Usually, a firm has unstable growth rate at its beginning stage, and then stabilizes.
4:

## Slide 27

Valuation of Common Stocks
Valuation of Different Types of Stocks
Usually, a firm has unstable growth rate at its beginning stage, and then stabilizes.
4:

## Slide 28

Parameter Estimation
Where does g come from?
Earningst+1 = Earningst + REt * RoR.
Earningst+1 / Earningst = 1 + (REt / Earningst) * RoR.
1 + g = 1 + Retention Ratio * Return on RE (= ROE)
E.g. Reporting earnings = $2m, Retention ratio = 40%, ROE = 16%.
The anticipated ∆Earnings = $2m * 40% * 16% = $128K.
∆Earnings in %age = $128K / $2m = 6.4%.
Using the formula, g = Retention Ratio x ROE = 40% * 16% = 6.4%.
Where does R come from?
Based on the constant growth model, Po = D1/(R – g)
R = D1/Po + g.
Dividends or Earnings: Which to Discount?
The No-dividend Firm
Empirical evidence suggests that firms with high growth rates are likely to pay lower dividends.
Agency problem re-considered.
4:

## Slide 29

Parameter Estimation
Cost of Debt
Bank Loan
The cost of debt is simply the interest rate, adjusted for tax relief as interest payments are tax deductible.
Let tc be the corporate tax rate, then
RD = i * (1 - Tc).
Bond/Debenture
The cost of debt is the current YTM of the bond outstanding.
Cost of Equity
Using CAPM: E(Ri) = Rf + βi [E(Rm) – Rf]

## Slide 30

Weight Average Cost of Capital (WACC)

## Slide 31

Growth Opportunities
Stock Price and Growth
Stock price can be viewed as consisting of two components, P = EPS/r + NPVGO.
No-growth cash cow, P = EPS/r.
NPV of growth opportunities, P = NPVGO.
4:

## Slide 32

Growth Opportunities
Only one growth opportunity
e.g. Sarro Inc. of 100,000 shares expects to earn $1M per year forever. If spending $1M next year in a marketing campaign, it will increase Sarro’s earnings by $210,000 forever starting from the end of the investment year. What is the value per share before and after deciding to take up the campaign if the firm’s discount rate is 10%?
Share value before the decision, PV = $10/0.10 = $100.
NPV of the investment = -$1M + $210,000/0.10 = $1.1M.
NPVGO = $1.1M/1.10 = $1M (or $10 per share).
Share value after the decision = $100 + $10 = $110.
4:

## Slide 33

Growth Opportunities
Continuous growth opportunities
e.g. If whenever Sarro spends $1M on marketing campaign, its earnings will increase by $210,000 forever, what is its share price if the firm does invest every year?
NPVGO = $1.1M/0.10 = $11M (or $110 per share).
Share value, PV = $100 + $110 = $210.
4:

## Slide 34

Growth Opportunities
4:

## Slide 35

Growth Opportunities
Increase in share value due to
NPVGO being positive.
Earnings are retained to take up the positive NPV project.
Project returns are higher than the cost of capital.
Assume the returns are 16% (instead of 20%) in the above example:
g = 0.6 * 0.16 = 0.096.
P = Div / (r – g) = $4 / (0.16 – 0.096) = $62.5.
The projects do not add value to the company.
If project returns are lower than 16%, P < $62.5.
Discounting earnings is not right in the sense that it ignores the investment a firm must make today in order to generate future returns.
4:

## Slide 36

Growth Opportunities
Price-Earnings Ratio and Growth
Three factors can be seen to determine the p/e ratio of a stock:
Price per share = EPS/r + NPVGO
NPVGO, which reflects the growth opportunities.
r, which reflects the risk of the firm.
EPS, which reflects firm’s choice of accounting methods.
4:

## Slide 37

Valuing Stocks using FCF
Different Ways to Evaluate Stocks
Using dividend-discount model
Using FCF (CFA)
One can discount the FCF to get the total value of the company and then divided that by the total number of shares outstanding to get the stock price (provided the firm is all-equity).
Using comparable ratios
E.g. Multiply a firm’s forecast earnings by the industry’s p/e ratio to get the stock price estimate.
Which method should be used?
The 3 methods are conceptually equivalent but in practice,
The dividend discount model is useful for firms paying steady dividends.
The comparables methods are useful for firms with similar investment opportunities.
The FCF model is helpful for non-dividend-paying firms with external financing needs.
4:

## Slide 38

End
