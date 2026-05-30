# AMA535: Mathematics of Derivative Pricing AMA535A: Mathematical Models of Derivative Pricing

XU, Zuo Quan

The Hong Kong Polytechnic University

# Introduction to Option

# What is an Option?

# Option

An option is a financial contract that gives the holder (long position) the right, but not the obligation, to buy or sell a specified asset at a predetermined price (strike price) on or before a specified date (expiry/maturity).

Call option: Right to buy the asset.   
Put option: Right to sell the asset.   
European option: Exercisable only at maturity.   
American option: Exercisable at any time up to and including maturity.   
The writer (short position) is obligated to fulfill the contract if the holder exercises the option.

# Vanilla Options: European vs. American

Vanilla options (European/American calls and puts) are the most common and liquid derivatives.   
European call (put): Right to buy (sell) one unit of the underlying asset at the strike price only at maturity.   
American call (put): Right to buy (sell) one unit of the underlying asset at the strike price at any time up to and including maturity.

# Payoff at Maturity: Call and Put

![](images/cf6cbbc8740655d6cca5e412d52a1904ae8bdc9f6d8c35ba37521063e9fe644a.jpg)

<details>
<summary>line</summary>

| S_T | Payoff |
| --- | ------ |
| K   | 0      |
| >K  | >0     |
</details>

![](images/668784d4afbed4d8aa66fb1cf59e8b8baaaec64ee468efed95fa1d264fed72ed.jpg)

<details>
<summary>line</summary>

| ST   | Payoff |
| ---- | ------ |
| K    | 0      |
| > K  | 0      |
</details>

Figure: Payoff at maturity T for a long call (left) and long put (right)

# Payoff Functions

The payoff function gives the profit at exercise (if positive, otherwise zero).   
At maturity, the option’s value equals its payoff; before maturity, the value may differ.   
European call: $\varphi ( S ) = ( S - K ) ^ { + } = \operatorname* { m a x } \{ S - K , 0 \}$ .   
European put: $\varphi ( S ) = ( K - S ) ^ { + } = \operatorname* { m a x } \{ K - S , 0 \} .$ .   
Notation: $x ^ { + } = \operatorname* { m a x } \{ x , 0 \} , x ^ { - } = \operatorname* { m a x } \{ - x , 0 \}$ .

# Beyond Vanilla: Exotic Options

Exotic options have more complex features, often depending on the path of the underlying asset.

# Popular Exotic options

• Asian option: Payoff depends on the average price over a period.   
Lookback option: Payoff depends on the maximum or minimum asset price during the option’s life.   
Barrier option: Activated or extinguished if the asset price crosses a certain level.   
Digital (binary) option: Pays a fixed amount if in-the-money, zero otherwise.

# Option Markets and Underlyings

Options can be written on stocks, indices, currencies, futures, and more.   
Index options (e.g., S&P 100, S&P 500) are widely traded; most are European style.   
Most stock and futures options are American style.   
Example: An S&P 100 index call with strike 2880, index at expiry 2892, pays (2892  2880)  100 = \$1200.

# Intrinsic Value and Time Value

# Intrinsic Value

The value of an option if exercised immediately; equal to its payoff function. Always non-negative.

# Time Value

The difference between the option’s total value and its intrinsic value. Reflects the potential for further gain before expiry.

# Moneyness of an Option

In-the-money (ITM): Option has positive intrinsic value. Call: $S > K ; \mathsf { P u t } ; S < K$ .   
Out-of-the-money (OTM): Option would have zero payoff if exercised now. Call: $S < K ; \mathsf { P u t } ; \ S > K$ .   
At-the-money (ATM): Strike price equals current spot price (S = K). ATM and OTM options have zero intrinsic value, only time value.