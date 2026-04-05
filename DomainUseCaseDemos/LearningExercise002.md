Activity: Wealth Management (Robo Advisory) 

+ Create synthetic data as per the details given below 

+ Group the customers into classes (Clustering) based on their current investment profile 

+ Group the customers by age and relatively rank them in terms of their wealth 

+ Profile the customers by their risk profile 

+ Develop algorithm to provide investment recommendations (Robo Advisory) so that each customer can achieve their retirement corpus goals 

 

Synthetic Data generation for 10000 rows (customers) - 1 row per customer 

+ customer Id – Unique value for each customer 

+ current_age (between 21 and 50) - As a trigonometric distribution with a median of 27 

+ current_annual_salary - As a Normal distribution with a mean of 7,20,000 and a standard deviation of 3,00,000, Values between 0 and 1,00,00,000 

+ current_bank_deposits - 

++ Values between 0 and 10,00,00,000 

++ As a Normal distribution 

++ mean of 1,00,000 * Max(0, (current_age – 20)) 

++ standard deviation of 5,000 * Max(0, (current_age – 20)) 

 

+ current_value_shares 

++ Values between 0 and 10,00,00,000 

++ As a Normal distribution 

++ mean of 60,000 * Max(0, (current_age – 20)) 

++ standard deviation of 4,000 * Max(0, (current_age – 20)) 

 

+ current_value_equity_mutual_funds 

++ Values between 0 and 10,00,00,000 

++ As a Normal distribution 

++ mean of 50,000 * Max(0, (current_age – 20)) 

++ standard deviation of 3,000 * Max(0, (current_age – 20)) 

 

+ current_value_debt_mutual_funds - with the following 

++ Values between 0 and 10,00,00,000 

++ As a Normal distribution 

++ mean of 40,000 * Max(0, (current_age – 20)) 

++ standard deviation of 2,000 * Max(0, (current_age – 20)) 

 

+ current_value_gold - As a Normal distribution with a mean of 1,50,000 and a standard deviation of 15,000 

 

 





 

Industry data points (once a year) [Data available at the end of the year] 

+ Bank Deposit Returns (Annual) - Range [3 to 12 percent] - with mean of 8% and standard deviation of 2% 

+ Stock Markets Returns (Annual) – Range [-5 to +25 percent] - with mean of 15% and standard deviation of 5% 

+ Equity Mutual Funds Returns (Annual) – Range of [-2 to +18 percent] - with mean of 10% and standard deviation of 4% 

+ Debt Mutual Funds Returns (Annual) – Range of [-2 to +12 percent] - with mean of 9% and standard deviation of 2% 

+ Digital Gold Returns (Annual) - Minimum of 2.5%, Maximum of 15% - uniform distribution 

+ Annuity Returns (Annual) - Range [3 to 18 percent] - with mean of 10% and standard deviation of 3% 

 

 

 





 

Wealth Management Rules + Goals 

+ salaries are expected to increase 6% every year 

+ increase in wealth each year is savings from salary + growth in assets in each category 

+ For each customer, you decide the asset allocation once a year, at the beginning of the year. You can recommend rebalancing of portfolio only once every year 

+ You do not know the exact rate of return at the beginning of the year, but you know the indicative ranges 

+ the growth rate of each asset class is decided each year is known at the end of the year (and not at the beginning of the year), but is applicable for the year 

+ the same actual growth rate at the end of the year for each asset class has to be used for all customers. All customers get the same rate of return for the same asset class in the year. 

+ the retirement corpus goals are decided when they join your robo advisory and does not change as they age. 

+ Savings rate (out of salary) 

++ Age [15 to 20] - 10% of annual salary 

++ Age [21 to 25] - 25% of annual salary 

++ Age [26 to 30] - 30% of annual salary 

++ Age [31 to 35] - 45% of annual salary 

++ Age [36 to 40] - 50% of annual salary 

++ Age [41 to 45] - 35% of annual salary 

 

+ Assume retirement age is 60 for all customers 

+ Assume that all customers withdraw money at 60 years and invest to get a monthly pension at the prevailing annuity rate 

+ Target is to ensure minimum retirement corpus as per following: 

++ Age [15 to 20] - 30 times current annual salary 

++ Age [21 to 25] - 25 times current annual salary 

++ Age [26 to 30] - 20 times current annual salary 

++ Age [31 to 35] - 15 times current annual salary 

++ Age [36 to 40] - 10 times current annual salary 

++ Age [41 to 45] - 5 times current annual salary 

 

+ Pension Regulator Guidelines on allocation of investments 

--> Bank Deposit : Shares : Equity Mutual Funds : Debt Mutual Funds : Gold 

--> Total distribution percentage should be 100 

++ Age [15 to 20] - Ratios [0 – 15] : [15 – 75] : [20-75] : [0 – 10] : [0 – 5] 

++ Age [21 to 25] - Ratios [0 – 15] : [15 – 60] : [20-60] : [0 – 15] : [0 – 10] 

++ Age [26 to 30] - Ratios [0 – 20] : [15 – 55] : [20-55] : [0 – 20] : [0 – 15] 

++ Age [31 to 35] - Ratios [0 – 20] : [15 – 50] : [20-50] : [0 – 25] : [0 – 20] 

++ Age [36 to 40] - Ratios [0 – 20] : [10 – 40] : [15-40] : [0 – 30] : [0 – 20] 

++ Age [41 to 45] - Ratios [0 – 20] : [5 - 30] : [5-40] : [0 – 30] : [0 – 20] 

++ As people age the percentage of risky assets should reduce 

 

 

Expected output 

+ Years to retirement (simple calc) 

+ Total Current Networth (simple calc) 

+ What is the retirement corpus goal (target) for each customer (ignore inflation) (based on current annual salary) 

+ What is the expected total asset value of each customer when they hit retirement age. [Important] 

+ Did the customer fall below or meet or exceed their retirement corpus goals (simple subtraction) 

+ What is the corpus invested in annuity to get a monthly pension 

+ What is the monthly pension 

