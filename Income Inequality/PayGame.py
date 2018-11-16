#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Nov 15 12:50:31 2018

@author: XIN
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import random
import math


#agent_alpha_list = np.zeros(10000)
#agent_beta_list = np.zeros(10000)
#agent_gamma_list = np.zeros(10000)

N_list = [0.5, 0.5, 0, 0, 0]
alpha_list = [93.4, 95.8, 100, 100, 100]
beta_list = [3.87, 3.67, 4, 4, 4]
gamma_list = [2.17, 4.34, 5, 5, 5]

num_levels = 100
count_levels_list = np.zeros((100, 5)) # number of agents for given level and class
count_levels_combined = np.zeros(100) # number of agents for given level
num_agents = 10000
agent_levels_list = np.zeros(10000) # which level the agent is at
num_classes = 5
agent_classes_list = np.random.choice(5, 10000, p=N_list) # which level the agent belongs to

s_min = 20000.0
s_max = 3000000.0

epoch = 50

def level_to_salary(x):
    return s_min + (s_max - s_min) / (num_levels - 1) * (x - 1)

def setup():
    mean = num_levels / 2
    for i in range(num_agents):
        r = int(round(mean)) # all agents start at the mean level
        c = agent_classes_list[i]
        count_levels_list[r, c] += 1
        count_levels_combined[r] += 1
        agent_levels_list[i] = r
    
    #agent_alpha_list[:] = np.random.normal(alpha_list[0], 0.2, 10000)
    #agent_beta_list[:] = np.random.normal(beta_list[0], 0.02, 10000)
    #agent_gamma_list[:] = np.random.normal(beta_list[0], 0.02, 10000)
    

def turtle():
    # make a copy
    count_levels_list_copy = count_levels_list
    count_levels_combined_copy = count_levels_combined
    
    for i in range(num_agents):
        r = random.randint(0, num_levels - 1)
        c = agent_classes_list[i]
        
        level_target = r
        level_self = int(round(agent_levels_list[i]))
        
        s_target = level_to_salary(level_target + 1)
        s_self = level_to_salary(level_self + 1)
        
        num_target = count_levels_combined[level_target]
        num_self = count_levels_combined[level_self]
        
        #alpha, beta, gamma = agent_alpha_list[i], agent_beta_list[i], agent_gamma_list[i]
        alpha, beta, gamma = alpha_list[c], beta_list[c], gamma_list[c]
        
        payoff_target = alpha * math.log(s_target) 
        payoff_target -= beta * math.log(s_target) ** 2
        payoff_target -= gamma * math.log(num_target + 1.0 / num_agents)
        
        payoff_self = alpha * math.log(s_self)
        payoff_self -= beta * math.log(s_self) ** 2
        payoff_self -= gamma * math.log(num_self + 1.0 / num_agents)
        
        
        if payoff_target > payoff_self:
            # move from self to target
            count_levels_list_copy[level_self, c] -= 1
            count_levels_combined_copy[level_self] -= 1
            count_levels_list_copy[level_target, c] += 1
            count_levels_combined_copy[level_target] += 1
            agent_levels_list[i] = level_target
    
    count_levels_list[:, :] = count_levels_list_copy[:, :]
    count_levels_combined[:] = count_levels_combined_copy[:]
    
def plot():
    x = np.linspace(0, num_levels, num_levels)
    plt.plot(x, count_levels_list[:, 0], label="class 1", marker='', color='skyblue')
    plt.plot(x, count_levels_list[:, 1], label="class 2", marker='', color='olive')
    #plt.plot(x, count_levels_combined, label="total", marker='', color='black') # total
    

if __name__ == '__main__':
    setup()
    for i in range(epoch):
        turtle()
    plot()