# Debt-Reset-Calculator

Enter debt, APR, and savings goal amounts.

When asked for percentage of payment to debt, this is what percentage of your monthly payment will go to debt. The remainder will go to savings.

This calculator will return dates of payoff for 3 different payoff methods.
Once the goal savings date is calculated, this calculator also prints the remaining debt balances on that date.

Debt balances and APR will be stored in a local .pkl file (of filename entered) for reuse of different savings calculations later.

The first payoff method is the maximum balance paid off first.
The second is the minimum balance paid off first.
The third is paying each account by an even amount every month, regardless of balance total. 

APR is compounded on a monthly basis on the remaining balance for each account.
