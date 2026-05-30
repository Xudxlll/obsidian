# Topic 3&4. Time value & DCF & Capital Budgeting

## Slide 1

Topic 3.Time Value & DCF
Time Value of Money
DCF Method

## Slide 2

I. Time Value of Money
Compounding
Example: Annual interest rate = 10%.
Simple Interest

## Slide 3

I. Time Value of Money

## Slide 4

I. Time Value of Money
Semi-annual Compound Interest
In this example, the annual percentage rate (APR) is 10% but the effective annual rate (EAR) is 10.25% due to semi-annual compounding. In general,
EAR = (1 + APR/m)m – 1
where m = frequency of compounding in a year.
As m approaches infinity, it is continuous compounding, EAR = eAPR*t.

## Slide 5

I. Time Value of Money
Present Value

## Slide 6

II. Discounted Cash Flows (DCF)
Annuities

## Slide 7

II. Discounted Cash Flows (DCF)

## Slide 8

II. Discounted Cash Flows (DCF)

## Slide 9

II. Discounted Cash Flows (DCF)
Example: Loan Amortization
Suppose you apply a 1-year bank loan of $10,000 at 2% per month, repayable in equal instalments at the end of each month. How much do you need to pay each month?
The actuarial method
Principal = Payment * PVAF12, 2%
Payment = 10,000 / 10.5753 = 945.60.

## Slide 10

II. Discounted Cash Flows (DCF)
The amortization schedule

## Slide 11

II. Discounted Cash Flows (DCF)
Cash flows with constant growth

## Slide 12

II. Discounted Cash Flows (DCF)
Exercise
Alan wants to buy a 42” LCD TV.  Rather than purchase and finance now, he plans to save every 3 months and increase the deposits by 3% per annum.  How much must the first deposit 3 months from now be if the TV costs $25,000 today and he expects to earn 10% on the money over the next 5 years. Assume annual compounding.
A)	$1,501.56
B)	$1,561.49
C)	$2,081.99
D)	$2,359.82
E)	$6,097.27

## Slide 13

II. Discounted Cash Flows (DCF)
Answer
Alan wants to buy a 42” LCD TV.  Rather than purchase and finance now, he plans to save every 3 months and increase the deposits by 3% per annum.  How much must the first deposit 3 months from now be if the TV costs $25,000 today and he expects to earn 10% on the money over the next 5 years. Assume annual compounding.
Constant growth formula:
4S * {1 – [(1+3%)/(1+10%)5] } / (10% - 3%) = $25K.
$25,000 = 4S* (1 - 0.7198) / 0.07 = 4S * 4.0026
S = 1561.484999.

## Slide 14

II. Discounted Cash Flows (DCF)
Exercise: Irregular cash flows
Given the following irregular cash flows coming out from an asset, what value of X should be to make the value of the cash flow be $800 at t = 4 if r = 7% and T = 12 ?

## Slide 15

II. Discounted Cash Flows (DCF)
Ans.:
100 * [1.3108 - 8.88 + 4.2056 + (X /1.1449) + 2.4489 + 8.3674] = 800
X = 62.65.

## Slide 16

The End

## Slide 17

Topic 4.Capital Budgeting
Capital Budgeting Rules
Some Applications
Break-Even Analysis
Real Options

## Slide 18

I. Capital Budgeting Rules (NPV)
NPV  PV(future cash flows) - Initial Cost
Since this method evaluates an investment by discounting its future cash flows, the procedure is called discounted cash flow (DCF) valuation.
Accept only +NPV projects. If projects are mutually exclusive, choose the one with the highest NPV.

## Slide 19

The NPV Rule
Example:
* Spreadsheet calculation: = NPV(10%, A2:A6) + A1

## Slide 20

The Payback Rule
The payback period = the amount of time required for an investment to generate cash flows enough to recover the initial cash outlay.
This rule chooses projects with payback periods shorter than a prescribed cutoff period, the shorter the better.
Surveys suggest that the technique is widely used by practitioners, especially in the health care industry and for projects in politically unstable countries.

## Slide 21

The Payback Rule
Example:

## Slide 22

The Payback Rule
Advantages:
Easy to calculate
Biased towards liquidity which can be important to illiquid firms.
Ignoring distant cash flows, which may be highly uncertain. (The longer the funds are “out there”, the greater the likelihood they will not be returned.)
Disadvantages:
A project can have more than one payback period if there are negative cash flows in some periods.
May accept bad projects like -NPV projects.
Timing of cash flows is ignored.
Payments after the payback period are ignored.

## Slide 23

The Discounted Payback Rule
Use the discounted value of cash flows to calculate the payback period.
* DPP(B) = ((1000 - 225 - 478) / 807) + 4 = 4.37.

## Slide 24

The Discounted Payback Rule
Normally, a project with a finite payback period has +NPV.
However, a -NPV project may have a finite payback period when there are negative cash flows.
Also, when there are negative cash flows, the project may have multiple discounted payback periods.
In practice, people seldom use this method because the information used in this rule is also used in NPV rule which is better.

## Slide 25

The Internal Rate of Return (IRR) Rule
It is the discount rate that makes the NPV of the project zero.
A project is accepted if its IRR > the hurdle rate (usually the opportunity cost of capital used to finance the project).
Find out by trial and error

## Slide 26

The IRR Rule
Example:
 Spreadsheet calculation: = IRR(B1:B6,guess).

## Slide 27

The IRR Rule
Advantage:
Easy to use as unlike NPV, IRR relies only on the project cash flows.
Disadvantage:
There may have no IRR or multiple IRRs.

## Slide 28

The IRR Rule
e.g. Consider a project having initial outlay of $100 and year-1 cash flow of $230 and year-2 cash flow of -$132. What is the IRR of the project?
Ans.: Let X = 1/(1+IRR). By definition,
-132X2 + 230X - 100 = 0.
If X = 0.91, IRR = (1/0.91) – 1 = 10%.
If X = 0.83, IRR = (1/0.83) – 1 = 20%.

## Slide 29

The IRR Rule
Problems specific to mutually exclusive projects
The scale problem
Example:
The timing (of the cash flows) problem

## Slide 30

NPV vs IRR
The two rules pick different projects if the cost of capital is below 10%.
The IRR rule assumes the cash flows can be reinvested at the IRR rate but the best possible return is below that if the cost of capital is below 10%.

## Slide 31

NPV vs IRR
The cross-over rate (also called the “incremental IRR”) is one that gives the same NPV to projects A and B:
r = 10.55%.
If r < cross-over rate, NPVA < NPVB because when the discount rate is low, the distant but larger cash flows of project B become more important.
If r > cross-over rate, NPVA > NPVB because when the discount rate is large, the distant though larger cash flows of project B become less important.

## Slide 32

The Profitability Index (PI)
PI  PV(future cash flows) / Initial Cost = 1 + NPV/(Initial Cost).
Accept only projects of PI > 1. If projects are mutually exclusive, choose the one with the highest PI.

## Slide 33

The Profitability Index (PI)
PI > 1 iff NPV > 0.
PI rule favors projects with smaller initial costs even though they may be of lower +NPV.
Capital rationing.
Under limited funding, ranking projects based on PI could be better than using NPV.
Consider the following 3 projects with funding constraint of $20 millions.
| Project | Co | C1 | C2 | PV(12%) | PI | NPV (12%) |
| 1 | -$20 | $70 | $10 | $70.47 | 3.52 | $50.47 |
| 2 | -10 | 15 | 40 | 45.28 | 4.53 | 35.28 |
| 3 | -10 | 55 | -30 | 25.19 | 2.52 | 15.19 |

## Slide 34

An Example
Projection of Sales and Costs
Sales Volume		=	50,000 cans per year
Selling Price		=	$4 per can
Manufacturing Costs	=	$2.50 per can
Fixed Costs		=	$12,000 per year
Equipment Costs		=	$90,000
Project Life		=	3 years
Depreciation		=	straight-line method
Salvage Value		=	$0.0
Discount Rate		=	20%
Projection of Net Working Capital
All sales and expenditure will be in cash.
Inventory of $15,000 needs to be kept to avoid stockout.
Cash of $5,000 will be kept for flexibility.

## Slide 35

An Example

## Slide 36

An Example
Projection of Cash Flows
Recall the earlier definition of cash flow from assets (CFA) as:
CFA  OCF – NWC – FA
OCF = EBIT – TAX + Depreciation
= EBIT – tc*(EBIT – Interest) + Depreciation
= EBITDA – tc*(EBITDA – Interest – Depreciation)
CFA = EBITDA – tc*EBITDA + tc*Interest + tc*Depreciation – NWC – FA
tc*Interest is called the interest tax shield.
tc*Depreciation is called the depreciation tax shield.
For capital budgeting purpose, we exclude all the cash flows resulting from financing choices.
OCF = (1-tc)EBIT + Depreciation = 0.66 x 33,000 + $30,000.
∆NWC = 0.
∆FA = 0.
CFA = 21,780 + 30,000 = $51,780.
In the final year of the project, no NWC is needed, implying
NWC = -$20,000.
CFA = 21,780 + 30,000 + 20,000 = $71,780.

## Slide 37

An Example
NPV Calculation
Assuming the discount rate (cost of capital) being 20%,
NPV = -110,000 + 51,780/1.2 + 51,780/1.22 + 71,780/1.23 = 10,648.
Thus, the project is accepted.

## Slide 38

II. Some Applications
Cost-cutting Proposals
e.g. A cost-saving equipment of 5-year life costing $80K with a scrap value of $20K can save $22K per year. Would it be worth buying if tax rate is 21% and the discount rate is 10%, assuming straight-line depreciation?
OCF per year
Approach 1
OCF = EBIT – Taxes + Depreciation
Depreciation = $80K/5 = $16K
EBIT = $22K - $16K = $6K.
Taxes = $6K x 21% = $1,260.
OCF = $6,000 – $1,260 + $16,000 = $20,740.
Approach 2
OCF = EBITDA – tc*(EBITDA –Depreciation)
= $22K – 21% x ($22K – $16K)
= $22K – 21% x $6K = $22K - $1,260 = $20,740.
OCF from the scrap value = $20K x (1 – 0.21) = $15,800.
NPV = $20,740 x PVAF5,10% + $15,800 x PVIF5,10% - $80K = $8,431.

## Slide 39

Some Applications
Investment of Unequal Lives
e.g. You need to buy a new machine and there are two choices. Given the following information, which machine should you buy?
* Two machines cannot be compared unless they share the same life span.

## Slide 40

Some Applications
Investment of Unequal Lives
Matching Cycles
Assuming that you use the machine for 6 years.
Machine A:
PVA = 100 + 10/1.1 + 10/1.12 = $117.36.
For 6 years,
Machine B:
PVB = 140 + 8/1.1 + 8/1.12 + 8/1.13 = $159.89
Hence, Machine B should be used.

## Slide 41

Some Applications
Investment of Unequal Lives
Alternatively, assuming that you use the machine forever.
Again, Machine B should be used.
The Equivalent Annual Cost (EAC) Method.

## Slide 42

III. Break-Even Analysis
Break-Even Analysis
Frequently, the crucial variable for a project is sales volume. Hence, it is usually analyzed more closely.
Break-even analysis is a tool for analyzing the relationship between sales volume and profitability.
Two major measures:
Accounting profit break-even point
Accounting Profit
= [(Sales price – Variable cost) Q – Fixed cost – Depreciation] * (1 – tc)
Breakeven point is the Q amount that makes the accounting profit equal to zero.

## Slide 43

Break-Even Analysis
Financial, present-value break-even point
PV Profit
= [(Sales price – Variable cost) Q – Fixed cost – Depreciation]
x (1 – tc) – EAC + Depreciation
PV breakeven point is the Q amount that makes the PV profit equal to zero.

## Slide 44

Break-Even Analysis
Example

## Slide 45

IV. Real Options
Nature
The NPV analysis ignores the adjustments that a firm can make after a project is accepted.
Since option has value, a project with such kind of options bears an NPV higher than what is computed using the DCF method:
M = NPV + Option Value.

## Slide 46

Real Options
Several Types
Option to Expand (Growth Option)
Expand when conditions become favorable and contract when they are not.
Many strategically important investments, such as investments in R&D, factory automation, a brand name, or a distribution network, provide growth opportunities because they are the first link in a chain of subsequent investment decisions.

## Slide 47

Real Options
Option to expand
Example: With an initial investment of $12 million on a hotel, there will be a 50% chance that annual cash flows be $3 million forever and a 50% chance that annual cash flows be  $1 million forever. If the good outcome is realized, an expansion of building 10 more hotels is possible. The discount rate is 20%.
NPV (w/o growth option)
= -$12m + $[(3 + 1)m x 50%] / 20% = -$2m.
NPV (with growth option)
= [-$12m + $(3m / 20%)] x 10 x 50%
+ [-$12m + $(1m / 20%)] x 50% = $11.5m.

## Slide 48

Real Options
Option to Abandon
Example: With an initial investment of $12 million on a hotel, there will be a 50% chance that annual cash flows be $6 million forever and a 50% chance that annual cash flows be  -$2 million forever. Now, assume expansion is not possible but instead, if the bad outcome is realized, closing down the operation is possible.
NPV (with abandon option)
= [-$12m + $(6m / 20%)] x 50%
+ [-$12m + $(-2m / (1 + 20%)] x 50%
= $2.17m.

## Slide 49

Real Options
Timing Options
One often finds urban land that has been vacant for many years. Yet, this land is bought and sold from time to time. The developers are buying a timing option.
e.g. An apartment complex needs 3 years to develop and sell:

## Slide 50

Real Options
Decision Trees
Example: A company wants to do a marketing test first to confirm if a 5-year project is worth carrying out. The information is as follows:
Marketing test cost = $100 million.
Probability proving the project being successful = 75%.
Project initial investment cost = $1,500 million
Annual cash flow from the project = $900 million.
Project discount rate = 15%.
Project NPV = -$1,500m + $900m x PVAF15%,5 = $1,518m.
Expected Payoff = $1,518m x 75% + $0 x 25% = $1,139m.
NPV (including marketing cost) = -$100m + $1,139m / 1.15
= $890 million.

## Slide 51

The End
