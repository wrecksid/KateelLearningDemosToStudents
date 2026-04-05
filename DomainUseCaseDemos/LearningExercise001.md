Activity: Credit Lending Algorithm Development 

 

Please generate synthetic data for 10000 rows (loan applications) in CSV format with the fields given below 
Calculate the loan eligibility for each one of the loan applicants using the Underwriting Guidelines given below. Classify / group your calculations into the 3Cs of lending. Look at the expected outputs 
Your program has to be on a Google Colab Notebook. 
Do not destroy / delete your code as we are likely to build on top of it. 
Feel free to use ChatGPT, but you are responsible for ensuring that the logic is correct and complete. Make sure you understand all the ChatGPT generated code. 
 

Data Fields 

+. Bank1_Bal - Value between 0 and 100000 - As a Normal distribution with a mean of 60000 and a standard deviation of 5000 

+. Bank2_Bal - Value between 0 and 100000 - As a Normal distribution with a mean of 40000 and a standard deviation of 2000 

+. Bank3_Bal - Value between 0 and 100000 - As a Normal distribution with a mean of 20000 and a standard deviation of 3000 

+. Share_Val - Value between 100000 and 5000000 - As a trigometric distribution with a median of 200000 

+. MF_Val - Value between 100000 and 1000000 - As a trigometric distribution with a median of 500000 

+. FamilyMember_Count - Value between 1 and 8 - with most of the values around 3 

+. Credit_Score - Value between 300 and 900 - As a normal distribution with a mean of 750 and a standard deviation of 75 

+. TenureRequestedInMonths - Value between 12 and 360 - equally distributed 

+. PurchasePriceOfApartment - Value between 1000000 and 30000000 - As a normal distribution with a mean of 7500000 and a standard deviation of 1500000 

+. PercentageOfSharesWillingToSell - Value between 10 and 50 - equally distributed 

+. PercentageOfMFWillingToSell - Value between 10 and 50 - equally distributed 

+. PrimaryMonthlySalary - Value between 100000 and 500000 - equally distributed 

+. SecondaryMonthlySalary - Value between 0 and 100000 - with 30% of the population having value of 0 and the remaining having a mean of 50000 and a standard deviation of 5000 

+. PrimaryBorrwerAgeInYears - Value between 15 and 45 - with a mean of 30 and standard deviation of 3 

+. SecondaryBorrowerAgeInYears - Value between 15 and 45 - with a mean of 30 and standard deviation of 3 

+. PrimaryBorrowerGender - Values (Male/Female) - with Males forming 60% 

+. IncomeStability - Values between 0 and 100 - With a mean of 80 and 10 percent of the population below 20 

  

  

  

Check eligibility for loan for each of the above rows with the following Underwriting Guidelines 

+ Both Primary and Secondary Borrowers have to be adults to get a loan. People above 18 years of age are treated as adults. 

+ If the Age difference between Primary and Secondary borrower is more than 10 years, loan is not granted 

+ If the Gender of the Primary Borrower is Female, a discount of 0.5% is available on the lending rate 

+ The retirement age for both Primary and Secondary is 60 Years 

+ The tenure of the loan is the minimum of TenureRequested, PrimaryTenureToRetirement and SecondaryTenureToRetirement 

+ Income Stability is factored into calculating the income 

+ Inflation and Salary increases over time are ignored 

+ The income from Primary and Secondary is added to get the total income. 

+ Disposable income is calculated as minimum of the following 

++ 50% of TotalIncome 

++ Amount remaining after allowing an expense of Rs 6000 per family member 

+ Bank Guidelines say loan to value of the property has to be below 80% 

+ Amount of loan granted will be minimum of 

++ eligible loan 

++ loan amount requested 

++ Value of the property (factor in loan to value limit here) 

+ Requesting loan amount greater than value of the property to be purchased will NOT be rejected, but the approved loan will be lower. 

+ If the Borrowers cannot put up the amount required to purchase the apartment (after subtracting the eligible loan amount), loan will not be granted 

+ Borrowers are willing to liquidate their Shares and MF holdings upto the percentage mentioned. They prefer to liquidate as less as possible. 

+ The maximum amount the Borrowers are able to contribute to the purchase of the property is limited to 90% of their Bank balances + the value of Shares and MF they sold or liquidated. 

+ The base rate of lending is as follows 

++ Credit Score above 800 – 8% 

++ Credit Score above 700 – 9% 

++ Credit Score above 600 – 10% 

++ Credit score below 600 – Loan is not granted 

 

Your outputs for each loan application should be the following: 

Eligible for Loan – Yes/No 
Maximum Amount of Eligible Loan – Amount 
Tenure of the loan approved 
Monthly EMI 
Amount of Money the Borrowers are expected to bring from their side 
