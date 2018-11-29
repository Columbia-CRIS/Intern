#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Nov 15 12:50:31 2018

@author: XIN
"""


import numpy as np
import matplotlib.pyplot as plt
import random
import math


mode = 'random' # either 'constant' or 'random' parameters
# standard dev. under random mode
sigma_alpha = 0.2
sigma_beta = 0.02
sigma_gamma = 0.02

# parameters for each agent
agent_alpha_list = np.zeros(100000)
agent_beta_list = np.zeros(100000)
agent_gamma_list = np.zeros(100000)

# parameters for each class
N_list = [0.6, 0.3, 0.05, 0.03, 0.02] # class composition of whole population
alpha_list = [93.4, 95.8, 100, 100, 100]
beta_list = [3.87, 3.67, 4, 4, 4]
gamma_list = [2.17, 4.34, 5, 5, 5]

num_levels = 100 # number of salary levels
count_levels_list = np.zeros((100, 5)) # number of agents for given level and class
count_levels_combined = np.zeros(100) # number of all agents for given level
num_agents = 100000
agent_levels_list = np.zeros(100000) # which level the agent is at
num_classes = 5 
agent_classes_list = np.zeros(100000) # which level the agent belongs to

# for level -> salary value
s_min = 20000.0
s_max = 3000000.0

# stopping conditions
epsilon = 140000
epoch_max = 50


# level -> salary value
def level_to_salary(x):
    return s_min + (s_max - s_min) / (num_levels - 1) * (x - 1)


def setup():
    # assign each agent to a class
    agent_classes_list[:] = np.random.choice(5, num_agents, p=N_list)
    
    mean = num_levels / 2
    for i in range(num_agents):
        r = int(round(mean)) # all agents start at the mean level
        c = int(round(agent_classes_list[i]))
        count_levels_list[r, c] += 1
        count_levels_combined[r] += 1
        agent_levels_list[i] = r
        
        if mode == 'constant':
            agent_alpha_list[i] = alpha_list[c]
            agent_beta_list[i] = beta_list[c]
            agent_gamma_list[i] = gamma_list[c]
        else:
            agent_alpha_list[i] = np.random.normal(alpha_list[c], sigma_alpha, 1)
            agent_beta_list[i] = np.random.normal(beta_list[c], sigma_beta, 1)
            agent_gamma_list[i] = np.random.normal(gamma_list[c], sigma_gamma, 1)

   
# simulate for one round and return the least square difference of count change
def turtle():
    # make a copy for later comparisons
    count_levels_combined_copy = count_levels_combined.copy()
    
    for i in range(num_agents):
        # pick a random level as target
        r = random.randint(0, num_levels - 1)
        c = int(round(agent_classes_list[i]))
        
        # find levels
        level_target = r
        level_self = int(round(agent_levels_list[i]))
        
        # calculate salaries
        s_target = level_to_salary(level_target + 1)
        s_self = level_to_salary(level_self + 1)
        
        num_target = count_levels_combined[level_target]
        num_self = count_levels_combined[level_self]
        
        alpha, beta, gamma = agent_alpha_list[i], agent_beta_list[i], agent_gamma_list[i]
        
        # target utility
        payoff_target = alpha * math.log(s_target) 
        payoff_target -= beta * math.log(s_target) ** 2
        payoff_target -= gamma * math.log(num_target + 1.0 / num_agents)
        
        # current utility
        payoff_self = alpha * math.log(s_self)
        payoff_self -= beta * math.log(s_self) ** 2
        payoff_self -= gamma * math.log(num_self + 1.0 / num_agents)
        
        
        if payoff_target > payoff_self:
            # move agent from self to target
            count_levels_list[level_self, c] -= 1
            count_levels_combined_copy[level_self] -= 1
            count_levels_list[level_target, c] += 1
            count_levels_combined_copy[level_target] += 1
            agent_levels_list[i] = level_target
    
    # calculate the least square difference of count change
    loss = sum((count_levels_combined_copy - count_levels_combined) ** 2)
    
    # update state variable(s)
    count_levels_combined[:] = count_levels_combined_copy[:]
    
    return loss

    
def plot():
    x = np.linspace(0, num_levels, num_levels)
    for i in range(num_classes):
        plt.plot(x, count_levels_list[:, i], marker='')
    
    #plt.plot(x, count_levels_combined, label="total", marker='', color='black') # total
    plt.show()

if __name__ == '__main__':
    setup()
    print("Started... ")
    loss = epsilon + 1
    epoch = 0
    while loss > epsilon and epoch < epoch_max:
        loss = turtle()
        print("Epoch " + str(epoch) + " Loss: " + str(loss))
        epoch += 1
        plot()
    
    print("Converged after " + str(epoch) + " epoches. ")