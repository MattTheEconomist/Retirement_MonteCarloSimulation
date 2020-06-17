# Retirement_MonteCarloSimulation
A plotly dashboard for calculating the chances of running out of money needed for retirement. 



Ask the user for:
  * Savaings
  * Annual Spend
  * Minimum Expiration Date
  * Most Likely Expiration Date
  * Maximum Expiration Date

Python then takes these inputs and generates a random array of 3 thousand lifetimes fitting a triangular distribution of the minimum, most likely, and maximum expiration dates. For each of these lifetimes, the program picks a random starting place to start accruing annual S&P 500 returns. Every year, savings are reduced by the expense amount, and the remaining savings grow or shrink according to the S&P 500 return for that year. This process continues until the current lifetime reaches expiration, savings leftover are recorded to a list. 

Once every lifetime loop has finished, the program outputs:
* The distrubiton of lifetimes
* the distribution of savings remaining at the end of each lifetime 
* the percentage of lifetimes with positive savings at the date of expiration 



