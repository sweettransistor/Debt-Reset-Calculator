# Debt Reset Calculator (FOR MULTIPLE DEBTS)
 
############################################
##                                        ##
##          by: SWEET TRANSISTOR          ##
##                                        ##
############################################

import datetime as dt
import pickle
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from dateutil.relativedelta import relativedelta

DAY = dt.date.today()
# OverflowError solved for dt.timedelta(days=30) changed to relativedelta()
rel_month = relativedelta(months=1)
DEBTLIST = []
APRLIST = []

# Pickle filename intialization
debt_pkl_file = ""

# For file dialog box in pickleopen()
root = tk.Tk()
root.withdraw() # Hide the root window

# Input function if debt needs to be entered and saved.
def InputDebt():
    listdebt = []
    listapr = []
    answer = "Y"
    i = 1
    print("Enter a name for the account save file for future use:")
    debt_pkl_file = input()
    debt_pkl_file.join(debt_pkl_file + ".pkl")

    while answer in ["Y", "y"]:
        print("Input Debt #", i, "amount:")
        debt = input()
        print("Input associated interest rate (% APR) for Debt #", i, ":")
        apr = input()
        listdebt.append(float(debt))
        listapr.append(float(apr))
        print("Any additional debts you wish to calculate (Y/N)?")
        answer = input()
        i += 1

    return listdebt, listapr, debt_pkl_file

# Function in main after input type specified (pkl or manual)
def goals():
    print("Enter debt goal:")
    goaldebt = int(input())

    print("Enter goal savings:")
    goalsavings = int(input())
    
    print("Enter any existing savings (0 if NONE):")
    currentsavings = int(input())
    
    print("Enter monthly contribution:")
    payment = int(input())
    
    print("What percentage of your monthly contribution will go to debt payment?")
    #Debt payment amount at percentage
    debtpayment = int(input()) * payment / 100 
    #Remainder = savings payment
    savingspayment = payment - debtpayment

    return goaldebt, goalsavings, currentsavings, debtpayment, savingspayment, payment

# Payoff maximum account balance first strategy
def MaxFirst(maxdebtpays, maxdgoal, save, maxmaxpayment):
    i = 0
    d = 0
    maxsorted = []
    aprsorted = []
    listdebtmax = DEBTLIST.copy()
    maxday = DAY
    balance = 0

    # Highest balance first
    for i in range(len(listdebtmax)):
        maximum = max(listdebtmax)
        max_index = listdebtmax.index(maximum)
        maxsorted.append(maximum)
        aprsorted.append(APRLIST[max_index])
        listdebtmax.pop(max_index)
        i += 1
    while sum(maxsorted) > maxdgoal:
        if (maxsorted[d] > 0) & (sum(maxsorted) > maxdgoal):
            maxsorted[d] -= maxdebtpays
        if maxsorted[d] < 0:
            maxsorted[d-1] += maxsorted[d]
            d += 1
        elif maxsorted[d] == 0:
            maxsorted.pop(d)
        # Increment date by rel_month
        try:
            maxday += rel_month
        except ValueError:
            print("\nPaying the maximum debt amount first, payoff will not happen in your lifetime.")
            break

        # Calculate balance for savings reached day
        if maxday == save:
            balance = sum(maxsorted)
            # If savings is met, contribution is max contribution.
            maxdebtpays = maxmaxpayment
        for i in range(len(maxsorted)):
            if maxsorted[i] > 0:
                maxsorted[i] += (maxsorted[i] * aprsorted[i] / 100 / 12)
            else:
                pass

    # Account for lost monies in balance overpayment at 100% upfront debt payment
    if sum(maxsorted) < maxdgoal:
        balance = sum(maxsorted)        

    return maxday, balance
        
# Payoff smallest account balance first strategy        
def LeastFirst(leastdebtpays, leastdgoal, save, leastleastpayment):
    i = 0
    d = 0
    minsorted = []
    aprsorted = []
    listdebtmin = DEBTLIST.copy()
    leastday = DAY
    balance = 0

    # Lowest balance first
    for i in range(len(listdebtmin)):
        
        minimum = min(listdebtmin)
        min_index = listdebtmin.index(minimum)
        minsorted.append(minimum)
        aprsorted.append(APRLIST[min_index])
        listdebtmin.pop(min_index)
        i += 1
    while sum(minsorted) > leastdgoal:
        if (minsorted[d] > 0) & (sum(minsorted) > leastdgoal):
            minsorted[d] -= leastdebtpays
        if minsorted[d] <= 0: 
            d += 1
            # if d < len(minsorted) added for single debt case
            if d < len(minsorted):
                minsorted[d] += minsorted[d-1]
        
        try:
            # Increment date by rel_month
            leastday += rel_month
        except ValueError:
            print("\nPaying the lowest debt amount first, payoff will not happen in your lifetime.")
            break

        # Calculate balance for savings reached day
        if leastday == save:
            balance = sum(minsorted)
            # If savings is met, contribution is max contribution.
            leastdebtpays = leastleastpayment

        for i in range(len(minsorted)):
            if minsorted[i] > 0:
                minsorted[i] += (minsorted[i] * aprsorted[i] / 100 / 12)
            else:
                pass
    # Account for lost monies in balance overpayment at 100% upfront debt payment
    if sum(minsorted) < leastdgoal:
        balance = sum(minsorted)        

    return leastday, balance

# Payoff in even amounts spread over all accounts
def EvenSpread(evendebtpays, evendgoal, save, evenevenpayment):
    evenlistdebt = DEBTLIST.copy()
    d = 0
    evenday = DAY
    balance = 0
    
    # Avoid division by zero and divide by positive values of evenlistdebt
    nonzeroes = len(evenlistdebt)
    while (sum(evenlistdebt) > evendgoal):
        for i in range(len(DEBTLIST)):
            # Clearing d OUT OF RANGE FOR evenlistdebt[d] > 0 
            if i < len(evenlistdebt):    
                d = i
            if i >= len(evenlistdebt):
                break
                        
            if ((evenlistdebt[d] > 0) & (nonzeroes > 0)):
                evenlistdebt[d] -= (evendebtpays / nonzeroes)
                # d += 1

            elif (evenlistdebt[d] < 0):
                evenlistdebt[0] += evenlistdebt[d]
                # Breaks the if statement
                evenlistdebt[d] = 0
                
            elif (evenlistdebt[d] == 0):
                evenlistdebt.pop(d)
                nonzeroes = len(evenlistdebt)
                
            elif (nonzeroes == 0):
                break
        # Increment date by rel_month
        try:
            evenday += rel_month
        except ValueError:
            print("\nWith an evenly spread payment plan, payoff will not happen in your lifetime.")
            break

        # Calculate balance for savings reached day
        if evenday == save:
            balance = sum(evenlistdebt)
            # If savings is met, contribution is max contribution.
            evendebtpays = evenevenpayment

        for i in range(len(evenlistdebt)):
            if evenlistdebt[i] > 0:
                evenlistdebt[i] += (evenlistdebt[i] * APRLIST[i] / 100 / 12)  
            else:
                pass

    # Account for lost monies in balance overpayment at 100% upfront debt payment
    if sum(evenlistdebt) < evendgoal:
        balance = sum(evenlistdebt)        

    return evenday, balance

# Calculate date savings goal reached
def Savings(sgoal, savingsstart, savemonthly, saveday):
    savetotal = savingsstart
    
    # If monthly debt contribution starts at 100%
    if saveday == None:
        saveday = DAY   
    else:
        pass

    while (savetotal < sgoal):
        savetotal += savemonthly
        saveday += rel_month

    return saveday, savetotal

# Save Input function account balance and interest rate information in local folder
def picklesave(debtlist, aprlist):
    # Save that Pickle!
    data = {'Debt':debtlist, 'APR':aprlist}
    df1 = pd.DataFrame(data)

    print(df1)
    df1.to_pickle(debt_pkl_file)
    return

# Reopen previously input account information
def pickleopen():
    file_path = filedialog.askopenfilename()

    # Open that Pickle RICK!
    with open(file_path, 'rb') as file:
        debtmodel = pickle.load(file)
    debt = debtmodel['Debt'].tolist()
    apr = debtmodel['APR'].tolist()

    return debt, apr, file_path

# Edit the account entry list
def editlist(debt, apr):
    print("What account row # needs to be re-entered?")
    rownum = int(input())
    print("Input debt amount for row #", rownum, ":")
    newdebt = float(input())
    debt[rownum] = newdebt
    print("Input associated interest rate (% APR) for debt row #", rownum, ":")
    newapr = float(input())
    apr[rownum] = newapr

    return debt, apr


if __name__ == '__main__':

    print("\nDEBT AND SAVINGS ESTIMATOR\n")
    print("Would you like to upload previous debt profile (Y or N)?")
    upload = input()

    if upload in ["N", "n"]:
        DEBTLIST, APRLIST, debt_pkl_file = InputDebt()
        picklesave(DEBTLIST, APRLIST)
        print("Do you need to edit any account inputs?")
        edit = input()
        while edit in ["Y", "y"]:
            DEBTLIST, APRLIST = editlist(DEBTLIST, APRLIST)
            picklesave(DEBTLIST, APRLIST)
            print("Do you need to edit any additional account inputs?")
            edit = str(input())
        pass
    else:
        DEBTLIST, APRLIST, debt_pkl_file = pickleopen()
        # View entries and edit as needed
        picklesave(DEBTLIST, APRLIST)
        print("Do you need to edit any account inputs?")
        edit = input()
        while edit in ["Y", "y"]:
            DEBTLIST, APRLIST = editlist(DEBTLIST, APRLIST)
            picklesave(DEBTLIST, APRLIST)
            print("Do you need to edit any additional account inputs?")
            edit = input()

    debtgoal, savegoal, savings, dpay, spay, fullpayment = goals()
    
    print("\nDate of achieving debt goal sorted by payoff technique:")
    # Run savings first to calculate remaining debt once savings is reached
    ## if, elif added for 100% debt contribution upfront
    if spay > 0:
        save, stotal = Savings(savegoal, savings, spay, None)

        max, maxbalance = MaxFirst(dpay, debtgoal, save, fullpayment)
        print("Pay Max Amount First: ", max)

        least, leastbalance = LeastFirst(dpay, debtgoal, save, fullpayment)
        print("Pay Least Amount First: ", least)
        
        even, evenbalance = EvenSpread(dpay, debtgoal, save, fullpayment)
        print("Pay in Even Spread: ", even)

        print("\nSavings achieved date: ", save)
    
        print("Savings balance: ", stotal) 
        print("\nOn date savings is reached, the remaining debt for all methods are:\n")
        print("Pay Max Amount First: ", "{:.2f}".format(maxbalance))
        print("Pay Least Amount First: ", "{:.2f}".format(leastbalance))
        print("Pay Even Amount First: ", "{:.2f}".format(evenbalance))
        input("Press Enter to exit...")

    elif spay == 0 :
        print("\nDebt paid at 100% upfront, goals achieved on the following dates (Negative Debt Balance is added to Savings):")

        max, maxbalance = MaxFirst(dpay, debtgoal, None, fullpayment)
        print("\nPay Max Amount First: ", max)
        print("Remaining Debt Balance: ", "{:.2f}".format(maxbalance))

        savemax, stotal = Savings(savegoal, savings-maxbalance, fullpayment, max)
        print("Savings achieved date: ", savemax)
        print("Savings balance: ", "{:.2f}".format(stotal)) 

        least, leastbalance = LeastFirst(dpay, debtgoal, None, fullpayment)
        print("\nPay Least Amount First: ", least)
        print("Remaining Debt Balance: ", "{:.2f}".format(leastbalance))

        saveleast, stotal = Savings(savegoal, savings-leastbalance, fullpayment, least)
        print("Savings achieved date: ", saveleast)
        print("Savings balance: ", "{:.2f}".format(stotal)) 

        even, evenbalance = EvenSpread(dpay, debtgoal, None, fullpayment)
        print("\nPay in Even Spread: ", even)
        print("Remaining Debt Balance: ", "{:.2f}".format(evenbalance))

        saveeven, stotal = Savings(savegoal, savings-evenbalance, fullpayment, least)
        print("Savings achieved date: ", saveeven)
        print("Savings balance: ", "{:.2f}".format(stotal)) 

        input("Press Enter to exit...")










                                                                                             ##                                                                                           
                                                                                           #####                                                                                          
                                                                                          ### ####                                                                                        
                                                                                        ####    ###                                                                                       
                                                                                       ###       ####                                                                                     
                                                                                      ###          ###                                                                                    
                                          ##################                        ####            ###                          ###############                                          
                                          ###          ##########                  ####              ###                   ##########         ##                                          
                                           ##                 #######             ####                ###              #######                ##                                          
                                           ##                     ######         ###                   ###          ######                    ##                                          
                                           ###                        ####       ###                    ###       ####                       ###                                          
                                            ##                          #####   ###                      ###   #####                         ###                                          
                                            ###                           ########                        #######                            ###                                          
                                            ###                              ####                          ####                             ###                                           
                                             ##                                #                           ##                               ###                                           
                                             ###     ###########                      #############                        #########       ###                                            
                                              ########### ##########               #######     ########                ################## ###                                             
                                             #####               #####          #####                #####          #####              ######                                             
                                           ####                      ###      ####                     #####      ####                    ####                                            
                                         ####                          ###   ###                          ###    ###                        ####                                          
                                        ###                             #######                            ### ####                           ###                                         
                                       ###                                ###                               #####                              ###                                        
                                      ###                                  #                                 ###                                ###                                       
                                     ###                                                                                                         ###                                      
                                     ###                                      ############################                                        ###                                      
                                     ###                                   ##################################                                     ##                                      
                                     ##                                  ####                              ####                                   ##                                      
                                     ###                              #####    ###########################   #####                                ##                                      
                                     ###                            ####    #################################  #####                             ###                                      
                                     ###                          ####   #####            #####            #####  ####                           ###                                      
                                      ##                         ###   #####           ###########            ###   ###                         ###                                       
                                      ###                        ###  ###             ###       ###            ###   ##                        ###                                        
                                 ########                        ###  ###             ##         ###            ###  ##                       ####                                        
                            #############                        ###  ###             ###       ###             ###  ##                      ############                                 
                         #####                                   ###  ###              ###########              ###  ##                               #######                             
                       ####                                      ###  ###                #######                ###  ##                                    ####                           
                     ####                                        ###  ###                                       ###  ##                                      ####                         
                    ####                                         ###  ############################################   ##                                        ###                        
                   ###                                           ###                                                 ##                                         ####                      
                   ##                                            ###                                                 ##                                          ###                      
                  ###                                            ###                                                 ##                                           ###                     
                  ##                                             ###                                                 ##                                            ###                    
                  ##                                             ###                                                 ##                                            ###                    
                  ##                                             ###                                                 ##                                            ###                    
                  ##                                             ##                                                  ##                                            ###                    
                  ###                                            ##                                                  ##                                            ###                    
                  ###                                            ##                                                  ##                                            ##                     
                   ###                                           ##                                                  ##                                           ###                     
                    ###                                          ##                                                  ##                                          ###                      
                     ###                                         ##                                                  ##                                         ###                       
                      ###                                        ##                                                  ##                                       ####                        
                        ###                                      ##                                                  ##                                      ####                         
                         #####                                   ###                                                ###                                   #####                           
                            #####                                #####################################################                                 #####                              
                               #######                              ##############################################                                   ####                                 
                                   ####                                   #########     ##########     #########                                  #####                                   
                                  ####                                   ##########    ###########    ##########                                  ###                                     
                                 ###                                     ##      ##    ##      ###    ##      ##                                   ###                                    
                                 ##                                      ##      ##    ##      ###    ##      ##                                    ###                                   
                                ###                                      ##      ##    ##      ###   ###      ##                                     ###                                  
                               ###                                       ##      ##    ##       ##   ###      ##                                      ###                                 
                               ###                                       ##      ###   ##       ##   ###      ##                                       ###                                
                               ##                                        ##      ###   ##       ##   ###      ##                                       ###                                
                               ##                                        ##      ###   ##       ##   ###      ##                                        ##                                
                               ##                                        ##      ###   ##       ##   ###      ##                                        ##                                
                               ###                                       ##      ###   ##       ##    ##      ##                                        ##                                
                               ###                                       ##      ###   ##       ##    ##      ##                                       ###                                
                                ###                                      ##      ###   ###      ##    ##      ##                                       ###                                
                                 ###                                     ##      ##    ###      ##    ##      ##                                      ###                                 
                                 ####                                    ##      ##    ###     ###    ##      ##                                     ###                                  
                                   ###                                   ##      ##    ###     ###    ##      ##                                    ###                                   
                                    ###                                  ##      ##    ###     ###    ##      ##                                   ###                                    
                                     ####                                ##      ##    ###     ##     ##     ###                                 ####                                     
                                       #####                             ###    ###     ##     ##     ##     ###                              ####                                        
                                          ########                       ###    ###     ##     ##     ##     ##                         ########                                          
                                              #############              ###    ##      ##    ###     ###    ##              ###############                                              
                                                         ###              ##    ##      ##    ##      ###   ###              #####                                                        
                                                         ###              ##   ###      ###   ##       ##   ##               ###                                                          
                                                         ###              ##   ##       ###  ###       ##   ##               ##                                                           
                                                          ###             ###  ##        ##  ##        ##  ###              ###                                                           
                                                           ###             ######        ######        ######               ##                                                            
                                                            ###                                                            ###                                                            
                                                             ###                                                          ###                                                             
                                                              ####                        ####                          ####                                                              
                                                                #####                  #########                      ####                                                                
                                                                   #######        #######     #####                ######                                                                 
                                                                       ###############           #####################                                                                    
                                                                                                     ############                                                                         