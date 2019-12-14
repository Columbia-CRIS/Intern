#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Nov 15 12:50:31 2018

@author: Cindy L.
@editor: Nana T. 
"""

# I added features of tax, savings, wealth


import numpy as np
import matplotlib.pyplot as plt
import random
import math
import pandas as pd



# basic settings
num_levels = 100 # number of salary levels
num_agents = 10000
num_classes = 5

# parameter init mode, either 'constant' or 'random'
mode = 'random'
# utility function choice, either 'log' or 'sqrt'
utility_function = 'log'

# standard dev. under random mode
sigma_alpha = 0.5
sigma_beta = 0.05
sigma_gamma = 0.05

# parameters for each agent
agent_alpha_list = np.zeros(num_agents)
agent_beta_list = np.zeros(num_agents)
agent_gamma_list = np.zeros(num_agents)

# parameters for each class
#N_list = [0.5, 0.3, 0.15, 0.03, 0.02] # class composition of whole population
#alpha_list = [93.4, 95.8, 97, 99, 100]
#beta_list = [3.87, 3.67, 3.67, 3.67, 4]
#gamma_list = [2.17, 4.34, 4.34, 4.34, 1]
#tax_rate_list= [0.3, 0.35, 0.4,0.45, 0.5]
#tax_rate_list= [0.1, 0.2, 0.3,0.4, 0.5]

N_list = [1]
alpha_list = [93.4]
beta_list = [3.87]
gamma_list = [2.17]



# for level -> salary value
s_min = 100
s_max = 5080353

# stopping conditions
epsilon = 10
epoch_max = 100

#User 1's level's trace 
level_individual = []

#tax_level


tax = 0


# === DO NOT MODIFY THIS  ===
count_levels_list = np.zeros((num_levels, num_classes)) # number of agents by level and class
count_levels_combined = np.zeros(num_levels) # number of all agents by level
agent_levels_list = np.zeros(num_agents) # which level the agent is at
agent_classes_list = np.zeros(num_agents) # which class the agent belongs to
agent_wealth_list = np.zeros(num_agents)
agent_tax_list = np.zeros(num_agents)
agent_pre_tax_list = np.zeros(num_agents)
agent_post_tax_list = np.zeros(num_agents)


# level -> salary value
def level_to_salary(x):
    return s_min + (s_max - s_min) / (num_levels - 1) * (x - 1)

def level_to_savings(x, salary):
    #constant 
    savings = 0
    if x >= 99 and x < 101:
        savings = salary *0.512
    if x > 95 and x < 99:
        savings= salary*0.372 
    if x > 76 and x <= 95:
        savings == salary*0.236
    if x > 57 and x <= 76:
        savings = salary * 0.173
    if x > 38 and x <= 57:
        savings = salary*0.111
    if x > 19 and x <= 38 :
        savings = salary*0.09
    else:
        savings = salary * 0.0014
    return savings
    #log
    #return (s_min + (s_max - s_min) / (num_levels - 1) * (x - 1))*0.2*math.log(x+1)
    
def level_to_tax(x,country):
    base = (s_max - s_min) / (num_levels - 1) 
    tax = 0 
    
    if country == 'Sweden':
        if 0 < x and x < 10:
            return 0
        elif 10 <= x and x < 85 :
            return base* (x - 10)*0.32
        elif 85 <= x and x < 95 :
            return base * (x - 85)*0.52 + base * (85)*0.32
        elif 95 <= x and x < 101 :
            return base* (x - 95)*0.57 + base* (10)*0.52 + base* (85)*0.32
        else: 
            return 0 
        
    if country == 'Norway':
        if 0 < x and x < 25 :
            return (s_max - s_min) / (num_levels - 1) * (x)*0.23
        elif 25 <= x and x < 50:
            return (s_max - s_min) / (num_levels - 1) * (25)*0.23 + (s_max - s_min) / (num_levels - 1) * (x-25)*0.014
        elif 50 <= x and x < 75 :
            return (s_max - s_min) / (num_levels - 1) * (50)*0.23 + + (s_max - s_min) / (num_levels - 1) * (x-50)*0.033
        elif 75 <= x and x < 90 :
            return (s_max - s_min) / (num_levels - 1) * 75*0.23 + + (s_max - s_min) / (num_levels - 1) * (x- 70)*0.124
        elif 90 <= x and x < 101 :
            return (s_max - s_min) / (num_levels - 1) * (90)*0.23 + + (s_max - s_min) / (num_levels - 1) * (x- 90)*0.154
        else: 
            return 0 
    if country == 'US':
        if 0 < x and x < 14 :
            return base * (x)*0.10
        elif 14 <= x and x < 51 :
            return base * (x - 14)*0.12 + base* (14)*0.10
        elif 51 <= x and x < 80 :
            return base * (x - 51)*0.22 + base* (51 - 14)*0.12 + base* (14)*0.10
        elif 80 <= x and x < 94 :
            return base* (x - 80)*0.24 +  base* (80 - 51)*0.22 + base * (51 - 14)*0.12 + base * (14)*0.10
        elif 94 <= x and x < 96 :
            return base* (x - 94)*0.32 + base* (94 - 80)*0.24 +  base * (80 - 51)*0.22 + base * (51 - 14)*0.12 + base* (14)*0.10
        elif 96 <= x and x < 99 :
            return base * (x - 96)*0.35 + base* (2)*0.32 + base * (94 - 80)*0.24 +  base * (80 - 51)*0.22 + base * (51 - 14)*0.12 + base * (14)*0.10
        elif 99 <= x and x < 101 :
            return base * (x - 99)*0.37 + base * (1)*0.35 + base * (2)*0.32 +base * (94 - 80)*0.24 +  base* (80 - 51)*0.22 + base * (51 - 14)*0.12 + base * (14)*0.10
        else: 
            return 0 
    if country == 'France':
        if 0 < x and x < 13 :
            return 0
        elif 13 <= x and x < 47 :
            return (s_max - s_min) / (num_levels - 1) * (x)*0.14
        elif 47 <= x and x < 93 :
            return (s_max - s_min) / (num_levels - 1) * (x - 47)*0.30 + (s_max - s_min) / (num_levels - 1) * (47)*0.14
        elif 93 <= x and x < 98 :
            return (s_max - s_min) / (num_levels - 1) * (x - 93)*0.41 + (s_max - s_min) / (num_levels - 1) * (93 - 47)*0.30 + (s_max - s_min) / (num_levels - 1) * (47)*0.14
        elif 98 <= x and x < 99 :
            return (s_max - s_min) / (num_levels - 1) * (x - 98)*0.45 + (s_max - s_min) / (num_levels - 1) * (98 - 93)*0.41 + (s_max - s_min) / (num_levels - 1) * (93 - 47)*0.30 + (s_max - s_min) / (num_levels - 1) * (47)*0.14
        elif 99 <= x and x < 99.9 :
            return (s_max - s_min) / (num_levels - 1) * (x - 99)*0.03 + (s_max - s_min) / (num_levels - 1) * (x - 98)*0.45 + (s_max - s_min) / (num_levels - 1) * (98 - 93)*0.41 + (s_max - s_min) / (num_levels - 1) * (93 - 47)*0.30 + (s_max - s_min) / (num_levels - 1) * (47)*0.14
        elif 99.9 <= x and x < 101 :
            return (s_max - s_min) / (num_levels - 1) * (x - 99)*0.04 + (s_max - s_min) / (num_levels - 1) * (x- 98)*0.45 + (s_max - s_min) / (num_levels - 1) * (98 -93)*0.41 + (s_max - s_min) / (num_levels - 1) * (93 - 47)*0.30 + (s_max - s_min) / (num_levels - 1) * (47)*0.14
        else:  
            return 0 
        
            

# initialze global variables, including classes and parameter lists
def setup():
    # assign each agent to a class
    agent_classes_list[:] = np.random.choice(1, num_agents, p=N_list)
    
    
    
    
    mean = num_levels / 2
    for i in range(num_agents):
            
        r = int(round(mean)) # all agents start at the mean level
        c = int(round(agent_classes_list[i]))
        count_levels_list[r, c] += 1
        count_levels_combined[r] += 1
        agent_levels_list[i] = r
        
        #agent_wealth_list[i] = originalWealthDistribution(i, 'Sweden')

        
        
        
        if i == 1:
            level_individual.append(r)
        if mode == 'constant':
            agent_alpha_list[i] = alpha_list[c]
            agent_beta_list[i] = beta_list[c]
            agent_gamma_list[i] = gamma_list[c]
        else:
            agent_alpha_list[i] = np.random.normal(alpha_list[c], sigma_alpha, 1)
            agent_beta_list[i] = np.random.normal(beta_list[c], sigma_beta, 1)
            agent_gamma_list[i] = np.random.normal(gamma_list[c], sigma_gamma, 1)
#            agent_tax_list[i] = tax_rate_list[c]
        

  
# simulate for one round and return the least square difference of count change
def turtle():
    # make a copy for later comparisons
    global tax
    global agent_pre_tax_list
    global agent_post_tax_list
    
    tax = 0 
    count_levels_combined_copy = count_levels_combined.copy()
    agent_wealth_list_copy = agent_wealth_list.copy()

    for i in range(num_agents):
        # pick a random level as target
        r = random.randint(0, num_levels - 1)
        c = int(round(agent_classes_list[i]))
        
        # find levels
        level_target = r
        level_self = int(round(agent_levels_list[i]))
        
        #calculate salaries
        s_target = level_to_salary(level_target + 1) - level_to_tax(level_target , 'US')
        s_self = level_to_salary(level_self + 1) - level_to_tax(level_self, 'US')
      
        #savings 
        e_target = level_to_savings(level_target+ 1, s_target)
        e_self = level_to_savings(level_self + 1,s_self)
     
        #without savings
#        e_target = 0
#        e_self = 0
        
        
        
        # Note: agents should make decisions one by one, not all at once as 
        # previously programmed. Otherwise, the program will produce wrong 
        # results. Thus, we use count_levels_combined_copy instead of 
        # count_levels_combined.
        num_target = count_levels_combined_copy[level_target]
        num_self = count_levels_combined_copy[level_self]
        
        #tax_distributed 
#
#        s_target = (level_to_salary(level_target + 1)) - level_to_tax(level_target + 1) + tax_copy/num_agents
#        s_self = (level_to_salary(level_self + 1)) -level_to_tax(level_self + 1) + tax_copy/num_agents
     
        #tax_not distributed
  #      s_target = (level_to_salary(level_target + 1)) - level_to_tax(level_target + 1) 
   #     s_self = (level_to_salary(level_self + 1)) -level_to_tax(level_self + 1)
    
        
        
        alpha, beta, gamma = agent_alpha_list[i], agent_beta_list[i], agent_gamma_list[i]
        
        # target utility & current utility
        if utility_function == 'log':
            payoff_target = alpha * math.log(s_target) 
            payoff_target -= beta * math.log(s_target) ** 2
            payoff_target -= gamma * math.log(num_target + 1.0 / num_agents)
            
            payoff_self = alpha * math.log(s_self)
            payoff_self -= beta * math.log(s_self) ** 2
            payoff_self -= gamma * math.log(num_self + 1.0 / num_agents)
        else:
            payoff_target = alpha * math.sqrt(s_target) 
            payoff_target -= beta * math.sqrt(s_target) ** 2
            payoff_target -= gamma * math.log(num_target + 1.0 / num_agents)
            
            payoff_self = alpha * math.sqrt(s_self)
            payoff_self -= beta * math.sqrt(s_self) ** 2
            payoff_self -= gamma * math.log(num_self + 1.0 / num_agents)
        
        if payoff_target > payoff_self:
            # move agent from self to target
            count_levels_list[level_self, c] -= 1
            count_levels_combined_copy[level_self] -= 1
            count_levels_list[level_target, c] += 1
            count_levels_combined_copy[level_target] += 1
            agent_levels_list[i] = level_target
            #agent_pre_tax_list[i] = level_to_salary(level_target + 1) + agent_wealth_list_copy[i]*0.1
            #agent_post_tax_list[i] = s_target +  agent_wealth_list_copy[i]*0.1*0.8
            
            if level_target > 80: 
                 agent_pre_tax_list[i] = level_to_salary(level_target + 1) + agent_wealth_list_copy[i]*0.1
                 agent_post_tax_list[i] = s_target +  agent_wealth_list_copy[i]*0.1
                 agent_wealth_list[i] = agent_wealth_list_copy[i] + agent_wealth_list_copy[i]*0.1 + e_target
                 
            else: 
                agent_pre_tax_list[i] = level_to_salary(level_target + 1) + agent_wealth_list_copy[i]*0.1
                agent_post_tax_list[i] = s_target +  agent_wealth_list_copy[i]*0.1
                agent_wealth_list[i] = agent_wealth_list_copy[i] + agent_wealth_list_copy[i]*0.1 + e_target
            if i == 1:
                level_individual.append(level_target)
            #tax = tax + level_to_tax(level_target+1)
    

              

        else: 

#            agent_pre_tax_list[i] = level_to_salary(level_self + 1) + agent_wealth_list_copy[i]*0.1
#            agent_post_tax_list[i] = s_self +  agent_wealth_list_copy[i]*0.1*0.8
            #agent_wealth_list[i] = agent_wealth_list_copy[i] + agent_wealth_list_copy[i]*0.1*0.8 + e_target
            if level_self > 80: 
                 agent_pre_tax_list[i] = level_to_salary(level_self + 1) + agent_wealth_list_copy[i]*0.1
                 agent_post_tax_list[i] = s_self +  agent_wealth_list_copy[i]*0.1
                 agent_wealth_list[i] = agent_wealth_list_copy[i] + agent_wealth_list_copy[i]*0.1 + e_self
            else: 
                 agent_pre_tax_list[i] = level_to_salary(level_self + 1) + agent_wealth_list_copy[i]*0.1
                 agent_post_tax_list[i] = s_self +  agent_wealth_list_copy[i]*0.1
                 agent_wealth_list[i] = agent_wealth_list_copy[i] + agent_wealth_list_copy[i]*0.1 + e_self
            if i == 1:
                level_individual.append(level_self)

    
    # calculate the least square difference of count change
    loss = sum((count_levels_combined_copy - count_levels_combined) ** 2)
    
    # update state variable(s)
    count_levels_combined[:] = count_levels_combined_copy[:]
    
    return loss


# show the agent distributions on a plot
def plot():
    x = np.linspace(0, num_levels, num_levels)
    for i in range(num_classes):
        #plt.plot(x, count_levels_list[:, i], marker='') # just a different style
        plt.bar(x, count_levels_list[:, i], alpha=0.45)
    
    # Uncomment the line below to show a curve of all classes combined.
    plt.plot(x, count_levels_combined, label="total", marker='', color='black', linewidth=0.5)
    
    plt.show()
    


def plot_for_individual():
    number_list = list(range(len(level_individual)))
    plt.plot(level_individual,number_list)
    plt.show()
    

#def plot_wealth():
#    agent_wealth_list_copy= agent_wealth_list.copy()
#    maxNum = np.amax(agent_wealth_list)
#   
#        
#    binwidth= 0.05
#    if maxNum >  0:
#        agent_wealth_list_copy = agent_wealth_list_copy/maxNum
#    binsize = np.arange(min(agent_wealth_list_copy), max(agent_wealth_list_copy) + binwidth, binwidth)
#    hist,bins = np.histogram(agent_wealth_list_copy, binsize)
#    
#    print(hist)
#    print(bins)
#    
#    plt.bar(bins[:-1], hist,width = 0.05)
#    plt.xlim(min(bins), max(bins))
#    plt.show() 
def plotForIncome():
    agent_pre_tax_list_copy = agent_pre_tax_list.copy()
    agent_pre_tax_list_copy.sort()
    agent_post_tax_list_copy = agent_post_tax_list.copy()
    agent_post_tax_list_copy.sort()
    df=pd.DataFrame({'x': range(num_agents), 'y1': agent_pre_tax_list_copy, 'y2': agent_post_tax_list_copy})
    plt.plot( 'x', 'y1', data=df, marker='', color='skyblue', linewidth=2)
    plt.plot( 'x', 'y2', data=df, marker='', color='olive', linewidth=2)
    plt.show()


    
    

def plot_wealth():
    agent_wealth_list_copy= agent_wealth_list.copy()
    
    agent_wealth_list_copy.sort()
    #if maxNum >  0:
       # agent_wealth_list_copy = agent_wealth_list_copy
    cumulative_wealth= np.zeros(100)
    totalWealth = 0
    i = 0
    eachLoop= int(num_agents/100)
    for i in range(100):
        cumulative_wealth[i] =  sum(agent_wealth_list_copy[i*eachLoop:(i+1)*eachLoop])
        totalWealth+= cumulative_wealth[i]
    cumulative_wealth = np.true_divide(cumulative_wealth*100, totalWealth)
    print("Top 1%: ", cumulative_wealth[99])
    print("Top 10%: ", sum(cumulative_wealth[90:100]))
    print("Bottom 90%: ",sum(cumulative_wealth[0:90]))
 


    x_bar = np.arange(1, 101)
    plt.bar(x_bar, cumulative_wealth, width = 1)
    plt.show()
    
def share_pre():
    agent_pre_tax_list_copy= agent_pre_tax_list.copy()
    agent_pre_tax_list_copy.sort()
    #if maxNum >  0:
       # agent_wealth_list_copy = agent_wealth_list_copy
    cumulative_pre_tax= np.zeros(100)
    total = 0
    i = 0
    eachLoop= int(num_agents/100)
    for i in range(100):
        cumulative_pre_tax[i] =  sum(agent_pre_tax_list_copy[i*eachLoop:(i+1)*eachLoop])
        total+= cumulative_pre_tax[i]
    cumulative_pre_tax = np.true_divide(cumulative_pre_tax*100, total)
    print("Pre-Tax Top 1%: ", cumulative_pre_tax[99])
    print("Pre-Tax Top 10%: ", sum(cumulative_pre_tax[90:100]))
    print("Pre-Tax Bottom 90%: ",sum(cumulative_pre_tax[0:90]))
 


#    x_bar = np.arange(1, 101)
#    plt.bar(x_bar, cumulative_pre_tax, width = 1)
#    plt.show()
    
def share_post():
    agent_post_tax_list_copy= agent_post_tax_list.copy()
    agent_post_tax_list_copy.sort()
    #if maxNum >  0:
       # agent_wealth_list_copy = agent_wealth_list_copy
    cumulative= np.zeros(100)
    total = 0
    i = 0
    eachLoop= int(num_agents/100)
    for i in range(100):
        cumulative[i] =  sum(agent_post_tax_list_copy[i*eachLoop:(i+1)*eachLoop])
        total+= cumulative[i]
    cumulative = np.true_divide(cumulative*100, total)
    print("Post Tax Top 1%: ", cumulative[99])
    print("Post Tax Top 10%: ", sum(cumulative[90:100]))
    print("Post Tax Bottom 90%: ",sum(cumulative[0:90]))
 

#
#    x_bar = np.arange(1, 101)
#    plt.bar(x_bar, cumulative, width = 1)
#    plt.show()

    
#       
#def plot_wealth_2():
#    agent_wealth_list_copy= agent_wealth_list.copy()
#    agent_wealth_list_copy.sort()
#    maxNum = np.amax(agent_wealth_list)
#    minNum = np.amin(agent_wealth_list)
#    
#    if maxNum >  0:
#        wealth_level = (maxNum - minNum)/(num_levels-1)
#    wealth_distribution = np.zeros(100)
#    
#    i = 0 
#    current_wealth_level = minNum + wealth_level
#    for item in agent_wealth_list_copy :
#        if item < current_wealth_level :
#            wealth_distribution[i] = wealth_distribution[i] + 1
#        else:
#            current_wealth_level= current_wealth_level + wealth_level 
#            i = i+ 1
#            wealth_distribution[i] = wealth_distribution[i] + 1
#
#    wealth_distribution = np.true_divide(wealth_distribution,)
#    print (np.var(wealth_distribution))
#
#    x_bar = np.arange(1,101)
#    plt.bar(x_bar, wealth_distribution, width = 1)
#    plt.show()

    


if __name__ == '__main__':
    setup()
    print("Started... ")
    plot() #initial
   # plot_for_individual()
    loss = epsilon + 1
    epoch = 0
    plot_wealth()
    while loss > epsilon and epoch < epoch_max:
        loss = turtle()
        
        epoch += 1
        if epoch%20 == 0: 
            print("Epoch " + str(epoch) + " Loss: " + str(loss))
            plot() 
            #plot_for_individual()
            share_pre()
            share_post()
            plot_wealth()
            plotForIncome()
    plot()
            #plot_for_individual()
    share_pre()
    share_post()
    plot_wealth()
    plotForIncome()
            #lot_wealth_2()
    
    print("Converged after " + str(epoch) + " epoches. ")
