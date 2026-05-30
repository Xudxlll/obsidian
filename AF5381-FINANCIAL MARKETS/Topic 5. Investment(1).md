# Topic 5. Investment(1)

## Slide 1

Topic 5. Investment
Return & Return Measurements
Dollar Return and Rate of Return
Rates of Returns across Time
Risk & Risk Premium
Portfolio Return & Risk
2-security portfolio
N-security portfolio & Efficient Frontier
Diversification
Capital Allocation Line (CAL)
Utility Function
Risk & Risk Aversion
Asset Allocation & Utility Maximization
The Capital Asset Pricing Model (CAPM)
Efficiency Market Hypothesis (EMH)

## Slide 2

Return Measurements
Measuring Rates of Returns
Dollar Return = Dt + (P’t - Pt-1)
Rates of Return (Single Period)
Ending Price, P1 			= 110
Beginning Price, Po 		= 100
Dividend, D1	 		= 4
HPR = (110 - 100 + 4 ) / (100)	= 14%

## Slide 3

Return Measurements
Measuring Rates of Returns
Rates of Returns (Across Periods)
Dollar-weighted return
[-51 / (1 + r)] + [112 / (1 + r)2] – 50 = 0.
r (= IRR) = 7.117%.
-51 / (1 + 7.117%) = -47.61.
112 / (1 + 7.117%)2 = 97.61.
Time-weighted return
Period 1 return, R1 = (53 + 2 – 50) / 50 = 10%
Period 2 return, R2 = (54 + 2 – 53) / 53 = 5.66%
Simple average return = (10% + 5.66%) / 2 = 7.83%.
| Period | Action | Cash Flow |
| 0 | Purchase 1 share at $50 | -$50 (1 share purchase) |
| 1 | Purchase 1 share at $53 |  |
|  | Stock pays a dividend of $2 per share | +$2 dividend   -$53 (1 share purchase) |
| 2 | Stock pays a dividend of $2 per share |  |
|  | Stock is sold at $54 per share | +$4 dividend  + $108 (2 shares sold) |

## Slide 4

Return Measurements
Measuring Rates of Returns
Rates of Returns: Across Periods
Dollar-weighted return
r (= IRR) = 7.117%.
Time-weighted return
Simple average return, r = 7.83%.
Which measure is better?
If it is a buy-and-hold portfolio, dollar-weighted return is better because it reflects the terminal wealth.
If managers have no control over the timing and/or the magnitude of cash flows, time-weighted return is fair.

## Slide 5

Return Measurements
Measuring Average Rates of Returns over Multiple Periods
Buy and Hold through periods
Average Returns
Which measure is better?
Past Performance (Average Return)
Generally the geometric mean is preferable to arithmetic
Predicting Future Performance (Expected Return)
Generally the arithmetic average is preferable to geometric
Geometric mean has a downward bias.
Annual, Effective Annual Rates & Continuous Compounding
1 + EAR = (1 + APR/n)n.
When n approaches to infinity, 1 + EAR = eAPR.

## Slide 6

Nominal Rates & Real Rates
Real, Nominal Interest Rates and Inflation Rate
Let i = nominal rate,  r = real rate and πe = expected inflation rate. Then:
(1 + r)(1 + πe) = (1 + i)
r + πe  ~= i.
Fisher Equation: i = r + πe.
Equilibrium Real Rates of Interest

## Slide 7

Risk & Risk Premiums
Risk
Risk means uncertainty about future rates of return.
It is measured by the return standard deviation, σ.
The uncertainty can be quantified by the probability of occurrence of different states of the economy.
Example:
What will be the average market return and return variance given the following information?
Average Return = (60 * 20% + 40 * 5%) / 100
= 0.6 * 20% + 0.4 * 5% = 14%.
Return Variance = {40 * (5% - 14%)2 + 60 * (20% - 14%)2} / 100
| State of the Economy | Times of Occurrence | Return |
| Good | 60 | 20% |
| Bad | 40 | 5% |

## Slide 8

Risk & Risk Premiums
Risk
In general,
There are S states of the economy,
Expected return,
Expected variance,
Ps = the probability that the state s will occur.
Rs = the return of a security when the state of the economy is s.

## Slide 9

Risk & Risk Premiums
Risk
Example
E(r) = (0.25)(0.31) + (0.45)(0.14) + (0.25)(-0.0675) + (0.05)(-0.52)
= 0.0976 or 9.76%.
E(σ2) = 0.25(0.31 – 0.0976)2 + 0.45(0.14 – 0.0976)2
+ 0.25(-0.0675 – 0.0976)2
+ 0.05(-0.52 – 0.0976)2  = 0.038.
E(σ) = √0.038 = 0.1949.
Volatility over time intervals
 per year =  * T
T=12/52/252 if monthly/weekly/daily , respectively
Risk Premium and the Sharpe Ratio
Risk premium is defined as the return in excess of the risk-free return.
Sharpe Ratio = Risk premium / SD of excess return
State		Prob. of State	r in State
Excellent	0.25	0.3100
Good		0.45	0.1400
Poor		0.25	-0.0675
Crash		0.05	-0.5200

## Slide 10

Portfolio Risk
Portfolio risk depends on the correlation between the returns of the assets in the portfolio.
Covariance and the correlation coefficient provide a measure of the way returns of two assets vary.
Two-Security Portfolio
Return:
Risk:
Covariance, Cov(rD,rE) = DEDE
+ 1.0 >= r >= -1.0

## Slide 11

2-Security Portfolio Risk (Example)
| WD | WE | E(Rp) | SD=-1 | SD=0 | SD=0.30 | SD=1 |
| 1.0 | 0.0 | 8.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 0.9 | 0.1 | 8.50 | 8.80 | 10.98 | 11.56 | 12.80 |
| 0.8 | 0.2 | 9.00 | 5.60 | 10.40 | 11.45 | 13.60 |
| 0.7 | 0.3 | 9.50 | 2.40 | 10.32 | 11.70 | 14.40 |
| 0.6 | 0.4 | 10.00 | 0.80 | 10.76 | 12.26 | 15.20 |
| 0.5 | 0.5 | 10.50 | 4.00 | 11.66 | 13.11 | 16.00 |
| 0.4 | 0.6 | 11.00 | 7.20 | 12.92 | 14.20 | 16.80 |
| 0.3 | 0.7 | 11.50 | 10.40 | 14.16 | 15.47 | 17.60 |
| 0.2 | 0.8 | 12.00 | 13.60 | 16.18 | 16.88 | 18.40 |
| 0.1 | 0.9 | 12.50 | 16.80 | 18.04 | 18.40 | 19.20 |
| 0.0 | 1.0 | 13.00 | 20.00 | 20.00 | 20.00 | 20.00 |

## Slide 12

2-Security Portfolio Risk (Example)

## Slide 13

2-Security Portfolio Risk (Example)

## Slide 14

3-Security Portfolio Risk (Example)
Expected return and variance of a 3-asset Portfolio
Var(Rp) = Var(w1R1 + w2R2+ w3R3)2
= w12Var(R1) + w22Var(R2) + w32Var(R3)
+2w1w2Cov(R1,R2) +c2w1w3Cov(R1,R3) + 2w2w3Cov(R2,R3)
| WD | WE | WF | E(Rp=2) | SD(Rd,Re) |  | E(Rp=3) | SD(Rd,Re,Rf) |  |  |  |
|  |  |  |  | de = 0.30 |  |  | de = 0.30 | df = 0.50 | ef = 0.40 |  |
|  |  |  |  | Cov = 72 |  |  | Cov = 72 | Cov = 90 | Cov = 120 |  |
| 1.0 | 0.0 | 0.0 | 8.00 |  | 12.00 | 8.00 |  |  |  | 12.00 |
| 0.9 | 0.1 | 0.0 | 8.50 |  | 11.56 |  |  |  |  |  |
| 0.8 | 0.2 | 0.0 | 9.00 |  | 11.45 |  |  |  |  |  |
| 0.8 | 0.1 | 0.1 |  |  |  | 8.70 |  |  |  | 11.26 |
| 0.7 | 0.3 | 0.0 | 9.50 |  | 11.70 |  |  |  |  |  |
| 0.7 | 0.2 | 0.1 |  |  |  | 9.20 |  |  |  | 11.24 |
| 0.6 | 0.4 |  | 10.00 |  | 12.26 |  |  |  |  |  |
| 0.6 | 0.13 | 0.27 |  |  |  | 9.20 |  |  |  | 11.13 |
| 0.5 | 0.5 |  | 10.50 |  | 13.11 |  |  |  |  |  |
| 0.4 | 0.6 |  | 11.00 |  | 14.20 |  |  |  |  |  |
| 0.3 | 0.7 |  | 11.50 |  | 15.47 |  |  |  |  |  |
| 0.2 | 0.8 |  | 12.00 |  | 16.88 |  |  |  |  |  |
| 0.1 | 0.9 |  | 12.50 |  | 18.40 |  |  |  |  |  |
| 0.0 | 1.0 |  | 13.00 |  | 20.00 |  |  |  |  | 20.00 |
| 0.0 | 0.0 | 1.0 |  |  |  | 10.00 |  |  |  | 15.00 |

## Slide 15

Efficient Frontier
Portfolio Variance
N-asset Portfolio
Var(Rp) = ∑i∑jwiwjCov(Ri,Rj)
Summing all the terms inside the variance-covariance matrix:
|  | w1σ1 | w2σ2 | w3σ3 | w4σ4 | … | wnσn |
| w1σ1 | w1w1σ1σ1 | w1w2σ12 | w1w3σ13 | w1w4σ14 | … | w1wnσ1n |
| w2σ2 | w2w1σ21 | w2w2σ2σ2 | w2w3σ24 | w2w4σ24 | … | w3wnσ3n |
| w3σ3 | w3w1σ31 | w3w2σ32 | w3w3σ3σ3 | w3w4σ34 | … | w3wnσ3n |
| w4σ4 | w4w1σ41 | w4w2σ42 | w4w3σ43 | w4w4σ4σ4 | … | w4wnσ4n |
| … | … | … | … | … | … | … |
| wnσn | wnw1σn1 | wnw2σn2 | wnw3σn3 | wnw4σn4 | … | wnwnσnn |

## Slide 16

Efficient Frontier
When 2 risky assets are expanded to n risky assets, the envelope of the opportunity set is called the minimum-variance frontier.
The frontier is a set of portfolios with the lowest standard deviation for a given expected return.
The way to determine the minimum-variance frontier of N risky assets is due to Markowitz (to be discussed in detail later.)
The upper portion of the min-variance frontier is called the efficient frontier.
The frontier is a set of portfolios which dominate any other portfolios with a given standard deviation.
The portfolios on the efficient frontier are said to be mean-variance efficient.

## Slide 17

Efficient Frontier
Minimum-variance Frontier and Efficient Frontier
Q1: Which one of the following portfolios cannot lie on the efficient frontier as described by Markowitz?
Q2: If two assets are perfectly correlated, can risk be reduced?
Q3: Is the global minimum variance portfolio an optimal risky portfolio?
| Portfolio | Expected Return (%) | S.D. (%) |
| W | 15 | 36 |
| X | 12 | 15 |
| Y | 5 | 7 |
| Z | 9 | 21 |

## Slide 18

Diversification
Portfolio Diversification

## Slide 19

Risk & Diversification

## Slide 20

Risk & Diversification
The Power of Diversification
Table 7.4 Risk Reduction of Equally Weighted Portfolios in Correlated and Uncorrelated Universes:

## Slide 21

Diversification
Market risk
Systematic or non-diversifiable
Firm-specific risk
Diversifiable or nonsystematic

## Slide 22

Capital Allocation Line (CAL)
Portfolios of One Risky Asset and One Risk-Free Asset
Risk-free Asset
Free from what kind of risks?
Default risk -- Government bonds
Interest rate risk -- Short maturity
What can proxy for a risk-free asset?
Treasury bills
Exchange fund bill
Consider a portfolio of holding w amount of a risky asset A of E(RA) and σA and (1-w) amount of risk-free asset of Rf.
E(Rp) = (1-w) Rf + wE(RA).
σp = wσA.
By eliminating y, E(RP) =

## Slide 23

Capital Allocation Line (CAL)
Portfolios of One Risky Asset and One Risk-Free Asset
By eliminating w, E(RP) =
If E(RA) = 15%, A = 22%, and Rf = 7%, then
E(Rp) = 7% + {(15% - 7%) / 22%} * 22% * w.
Graphical representation

## Slide 24

Capital Allocation Line (CAL)
If w > 1, the portfolio is beyond Point P
if short-sales is restricted, then the efficient frontier will be inferior.
Margin buying (leverage):
Borrow at the risk-free rate and invest in stock
Using 50% Leverage, w = -50%; 1-w = 150%
E(Rp)= (-0.5) (7%) + (1.5) (15%) = 19%.
σp = (1.5) (22%) = 33%.
If lending and borrowing rates are different:

## Slide 25

Utility Function
Speculation, Gambling & Investment
Speculation
Taking considerable risk for a commensurate gain
Parties have heterogeneous expectations
Gamble
Bet or wager on an uncertain outcome for enjoyment
Parties assign the same probabilities to the possible outcomes
Investment
Willing to take risky assets only with positive risk premiums

## Slide 26

Utility Function
Risk Aversion & Utility Values
U = utility
E ( r ) = expected return on the asset or portfolio
A = coefficient of risk aversion
s2 = variance of returns
½ = a scaling factor.
Mean-Variance (M-V) Criterion
Portfolio A dominates portfolio B if:
E(rA) >= E(rB)	and   	σA <= σB.

## Slide 27

Capital Allocation
Risk Tolerance and Asset Allocation
Optimal Portfolio Choice
Choose a portfolio mix to maximize utility (mean-variance optimal)
Example: One risk-free and one risky assets
U = E(R) - 0.005Aσ2
E(Rp) = (1-w) Rf + wE(RA).
σp = w σA .
E(Rp) = Rf + {E(RA) – Rf}*w.
Optimal weight, w* =
If E(RA) = 15%, σA = 22%, Rf = 7%, and A = 4, then
w* = 0.41.
E(Rp) = (1 – 0.41) x 7% + 0.41 x 15% = 10.28%.
σP = 0.41 x 22% = 9.02%.

## Slide 28

Capital Allocation
Risk Tolerance and Asset Allocation
Optimal Portfolio Choice
Optimal weight, w* = (E(RA) – Rf) / 0.01Aσ2A
If E(RA) = 15%, σA = 22%, Rf = 7%, and A = 2, then
w* = 0.41 x 2 = 0.82.
E(Rp) = (1 – 0.82) x 7% + 0.82 x 15% = 13.56%.
σP = 0.82 x 22% = 18.04%.

## Slide 29

Capital Allocation
Risk Tolerance and Asset Allocation
Optimal Portfolio Choice
Greater levels of risk aversion lead to larger proportions of the risk-free asset.
Lower levels of risk aversion lead to larger proportions of the portfolio of risky assets.
Willingness to accept high levels of risk for high levels of returns would result in leveraged combinations.
E(r)

7%
P
Lender
Borrower
σp = 22%

## Slide 30

Capital Allocation
Capital Market Line (CML)
If Portfolio P is the market portfolio (i.e. an optimal portfolio of common stocks), CAL becomes the CML.
Example: Look at the following information:
Given w* = (E(RA) – Rf) / 0.01Aσ2A. If your risk-aversion coefficient is 4, how would you allocate if you believe in the entire 1941-1980 (1981 -2020) period is representative of future expected performance?
Optimal weight (1941-1980), w* = 8.7/(0.01*4*20.82) = 0.503.
Optimal weight (1981-2020), w* = 9.6/(0.01*4*13.52) = 1.317.
Why such change?
|  | Common Stock |  | 1-Month Bills |  | Risk Premium |  |
|  | Mean | S.D. | Mean | S.D. | Mean | S.D. |
| 1941-1980 | 12.5 | 20.4 | 3.8 | 3.4 | 8.7 | 20.8 |
| 1981-2020 | 17.1 | 13.1 | 7.5 | 3.2 | 9.6 | 13.5 |

## Slide 31

Asset Allocation under Utility Maximization
Portfolio Selection & Risk Aversion
N-risky assets without risk-free asset
E(r)
Efficient
frontier of
risky assets
More
risk-averse
investor
U’’’
U’’
U’
Q
P
S
Std. Dev
Less

## Slide 32

Asset Allocation under Utility Maximization
N-Risky Assets and One Risk-free Asset
With a risk-free asset, the (new) efficient frontier becomes linear and is called the CAL.
The optimal portfolio can be found mathematically by solving the following maximization problem.
The objective is to maximize the reward-to-variability ratio (Sharpe’s measure):
Maxwi(Sp) = [E(Rp) – Rf] / σp		s.t.  ∑wi = 1.
The  slope is also the Sharpe ratio.
The solution is the tangential portfolio.

## Slide 33

Asset Allocation under Utility Maximization
N-Risky Assets and One Risk-free Asset
The tangential portfolio, P, is the market portfolio.
That’s why the CAL passing through P is called the CML.
Two-fund Separation
Asset allocation is boiled down to investing in (certain amount of) risk-free asset and (certain amount of) the market portfolio, P.
E(r)
F
rf
A
P
Q
B
CAL
Std. Dev

## Slide 34

Asset Allocation under Utility Maximization
Implication
CML implies a passive strategy.
Investment decision is reduced to an allocation between risk-free asset and a well-diversified portfolio.
Index Funds
Exchange-traded funds
Index Futures
Q: If there is only one optimal risky portfolio, why are there so many different mutual funds?

## Slide 35

The Capital Asset Pricing Model
Assumptions
Individual behaviour
Investors are rational mean-variance optimizers
Single-period investment horizon
Homogeneous expectations.
Investors all use identical input lists
Information is costless and available to all investors
Market structure
All assets are publicly held and trade on public exchanges.
Individual investors can borrow or lend at a common risk-free rate, and they can take short positions on traded securities.
No taxes
No transaction costs

## Slide 36

The Capital Asset Pricing Model
The Market Portfolio
The assumptions result the following equilibrium conditions
All investors will hold the same portfolio for risky assets – market portfolio.
Market portfolio contains all securities and the proportion of each security is its market value as a percentage of total market value.

## Slide 37

The Capital Asset Pricing Model
Market Price of Risk
Assume an investor holding 100% of the market portfolio increases holding δ fraction of it through borrowing at the risk-free rate.
E(R) = (1 + δ)*E(Rm) – δ*Rf = E(Rm) + δ*[E(Rm) –Rf].
E(R) - E(Rm) ≡ ∆E(R) = δ*{E(Rm) – Rf}.
σ2 = (1 + δ)2σm2 ≈ σm2 + 2δσm2
σ2 - σm2 ≡ ∆σ2 = 2δσm2
The marginal price of risk of the market portfolio is,
∆E(R) / ∆σ2 = δ*{E(Rm) – Rf} / 2δσm2
= {E(Rm) – Rf} / 2σm2

## Slide 38

The Capital Asset Pricing Model
Market Price of Risk
Assume an investor holding 100% of the market portfolio increases holding δ fraction of Stock X through borrowing at the risk-free rate.
E(R) = E(Rm) + δ*E(Rx) – δ*Rf.
E(R) - E(Rm) ≡ ∆E(R) = δ*{E(Rx) – Rf}.
σ2 = σm2 + δ2σx2 + 2*δ*Cov(Rx,Rm) ≈ σm2 + 2δ*Cov(Rx,Rm)
σ2 - σm2 ≡ ∆σ2 = 2*δ*Cov(Rx,Rm).
The marginal price of risk of Stock X is,
∆E(R) / ∆σ2 = δ*{E(Rx) – Rf} / 2δ Cov(Rx,Rm)
= {E(Rx) – Rf} / 2 Cov(Rx,Rm).
In equilibrium, the marginal prices of risk have to be the same.

## Slide 39

The Capital Asset Pricing Model
An economic intuition of the CAPM is that the appropriate risk premium on an asset will be determined by its contribution to the risk of investors’ overall portfolios.
Recall the variance-covariance matrix of a portfolio:
|  | w1σ1 | w2σ2 | w3σ3 | w4σ4 | … | wnσn |
| w1σ1 | w1w1σ1σ1 | w1w2σ12 | w1w3σ13 | w1w4σ14 | … | w1wnσ1n |
| w2σ2 | w2w1σ21 | w2w2σ2σ2 | w2w3σ23 | w2w4σ24 | … | w3wnσ3n |
| w3σ3 | w3w1σ31 | w3w2σ32 | w3w3σ3σ3 | w3w4σ34 | … | w3wnσ3n |
| w4σ4 | w4w1σ41 | w4w2σ42 | w4w3σ43 | w4w4σ4σ4 | … | w4wnσ4n |
| … | … | … | … | … | … | … |
| wnσn | wnw1σn1 | wnw2σn2 | wnw3σn3 | wnw4σn4 | … | wnwnσnσn |

## Slide 40

The Capital Asset Pricing Model
Expected Return-Beta Relationship
CAPM holds for the overall portfolio, i.e. E(rp) = βp[E(rm) – rf] because:
This also holds for the market portfolio:
Note that βm= 1.
The SML (different from CML)
Figure 9.2
CAPM & the Single-Index Model
To move from expected to realized returns, use the index model in excess return form;
The index model beta-coefficient is the same as the beta of the CAPM expected return-beta relationship.

## Slide 41

Efficient Market Hypothesis (EMH)
Definition
Security prices fully reflect all available information.
3 versions of EMH differ in the information set defined.
Weak Form:
Historical market trading data
Semi-strong Form:
All publicly available information
Strong Form:
All information including insider information
Paradox?
Information is costly.
If prices fully reflect all information, do you still need to analyze financial statements?
If nobody does it, how can market be efficient?
Competition as the Source of Efficiency

## Slide 42

Efficient Market Hypothesis (EMH)
Random Walk and EMH
Random Walk:
Stock price changes are random.
Expected return is positive over time
Positive trend and random about the trend.
Why are price changes random?
Prices react to information.
Flow of information is random.
Implications for Equity Analysis
Technical Analysis - using past prices and volume information to predict future prices
Weak form efficiency implies technical analysis cannot generate abnormal returns.
Fundamental Analysis - using economic and accounting information to predict stock prices
Semi-strong form efficiency implies fundamental analysis cannot generate abnormal returns.

## Slide 43

Efficient Market Hypothesis (EMH)
Implications of Efficiency for Active and Passive Management
Active Management
Stock picker
Timing
Passive Management
Buy and hold
Index funds
Portfolio Management in an Efficient Market
Role for portfolio management still exists:
Diversify
Asset allocation
Consider taxes
Consider marketability

## Slide 44

Efficient Market Hypothesis (EMH)
Empirical Tests of Market Efficiency
Event studies
Returns are adjusted to the systematic risk and market returns, to determine abnormal return:
1) Estimate a single factor model over an estimation period:
Rt = a + bRmt + et
2) Calculate the abnormal return (AR):
AR = (Actual Return – Expected Return)
et = Rt - (a + bRmt)
3) Calculate the cumulative abnormal return (CAR) over the event window (-t, +t):
CAR = ∑ et

## Slide 45

Efficient Market Hypothesis (EMH)
Empirical Tests of Market Efficiency
Event studies
Market Anomalies: Evidence that appears to be in violation of EMH.
What can you conclude by observing CAR?
0
+t
-t
Overreaction and reversion
Early response
Delayed response
Efficient market response to new information
-30
+30
Stock Return
Public announcement day

## Slide 46

Efficient Market Hypothesis (EMH)
Weak-form Tests: Anomalies
Returns over the Short Horizon
Serial correlation
Conrad and Kaul (1988) and Lo & MacKinlay (1988) find positive serial correlations of weekly stock returns but not large.
Stock index daily return exhibits positive serial correlation due to nonsynchronous trading.
Momentum: Good or bad recent performance continues over short to intermediate time horizons
Jegadeesh and Titman (1993) – the momentum effect
Returns over Long Horizons
Episodes of overshooting followed by correction
DeBondt and Thaler (1985) – the reversal effect
Predictors of Broad Market Returns
Aggregate stock market returns are higher with higher dividend yield.
Fama and French (1988)
Earnings yield can predict market returns
Campbell and Shiller (1988)
Bond yield spreads can predict market returns
Keim and Stambaugh (1986)

## Slide 47

Efficient Market Hypothesis (EMH)
Semistrong Tests: Anomalies
P/E Effect
Basu (1977)
Small Firm Effect (January Effect)
Banz (1981)
Neglected Firm Effect and Liquidity Effects
Merton (1987)
Amihud and Mendelson (1986)
Book-to-Market Ratios
Fama and French (1992)
Post-Earnings Announcement Price Drift (PEAD)
Ball and Brown (1968)

## Slide 48

Efficient Market Hypothesis (EMH)
Semi-strong Tests: Anomalies

## Slide 49

Efficient Market Hypothesis (EMH)
Strong-Form Tests: Inside Information
Profits from insider trading
Jaffe (1974) and Seyhun (1986)
SEC requires all insiders to register their trading activity

## Slide 50

Efficient Market Hypothesis (EMH)
Interpreting the Anomalies
The most puzzling anomalies are price-earnings, small-firm, market-to-book, momentum, and long-term reversal.
Efficient market explanation
Fama and French (1993) argue that these effects can be explained by risk premiums.
Liew and Vassalou (2000) show that returns on BTM and Size portfolios can predict business cycles in many countries.
Inefficiency explanation
Lakonishok, Shleifer, and Vishny (1995) argue analysts extrapolate past performance too far into the future.
La Porta (1996) confirms that shares of firms for which analysts predict low earnings growth perform better than those with high expected earnings growth.

## Slide 51

Efficient Market Hypothesis (EMH)
Interpreting the Anomalies
Anomalies or data mining?
Anomalies over time (some anomalies have disappeared)
McLean and Pontiff (2016) find post-publication effects
decay in abnormal return of about 60%
Trading volume and variance of anomalous stocks increase.
Chordia, Subrahmanyam and Tong(2014) find many anomalies disappear in the post-1993 period when the trading costs declined rapidly.
Bubbles and market efficiency
Prices appear to differ from intrinsic values and crash after rapid run up.
Bubbles are difficult to predict and exploit.
Most bubbles become “obvious” only in retrospect.
At the time, the price run-up often seems to have a defensible rationales.
The dot-com bubble in the late 1990s.
What about Bitcoin?

## Slide 52

End
