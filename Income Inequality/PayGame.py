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


#count_levels_combined = []
num_levels = 100
count_levels_list = np.zeros((100, 1))
num_agents = 10000
agent_levels_list = np.zeros((10000, 1)) # which level the agent is at
agent_alpha_list = np.zeros(10000)
agent_beta_list = np.zeros(10000)
agent_gamma_list = np.zeros(10000)
#count_num_agents_old = 10000
#index_list = [0, 1, 2, 3, 4]
#switch_list = []
N_list = [1.0, 0, 0, 0, 0]
alpha_list = [93.4, 95.8, 100, 100, 100]
beta_list = [3.87, 3.67, 4, 4, 4]
gamma_list = [2.17, 4.34, 5, 5, 5]

s_min = 20000.0
s_max = 3000000.0
#turtle_count = 0

epoch = 100

def level_to_salary(x):
    return s_min + (s_max - s_min) / (num_levels - 1) * (x - 1)

def setup():
    #random.seed()
    mean = num_levels / 2
    for i in range(num_agents):
        #r = random.randint(0, num_levels - 1) # a random level
        r = int(round(mean))
        count_levels_list[r, 0] += 1
        agent_levels_list[i, 0] = r
    
    agent_alpha_list[:] = np.random.normal(alpha_list[0], 3, 10000)
    agent_beta_list[:] = np.random.normal(beta_list[0], 0.3, 10000)
    agent_gamma_list[:] = np.random.normal(beta_list[0], 0.3, 10000)
    

def turtle():
    count_levels_list_copy = count_levels_list # make a copy
    
    for i in range(num_agents):
        r = random.randint(0, num_levels - 1)
        level_target = r
        level_self = int(round(agent_levels_list[i, 0]))
        
        s_target = level_to_salary(level_target + 1)
        s_self = level_to_salary(level_self + 1)
        
        num_target = count_levels_list[level_target, 0]
        num_self = count_levels_list[level_self, 0]
        
        alpha, beta, gamma = agent_alpha_list[i], agent_beta_list[i], agent_gamma_list[i]
        
        payoff_target = alpha * math.log(s_target) 
        payoff_target -= beta * math.log(s_target) ** 2
        payoff_target -= gamma * math.log(num_target + 1.0 / num_agents)
        
        payoff_self = alpha * math.log(s_self)
        payoff_self -= beta * math.log(s_self) ** 2
        payoff_self -= gamma * math.log(num_self + 1.0 / num_agents)
        
        
        if payoff_target > payoff_self:
            # move from self to target
            count_levels_list_copy[level_self, 0] -= 1
            count_levels_list_copy[level_target, 0] += 1
            agent_levels_list[i, 0] = level_target
    
    count_levels_list[:, :] = count_levels_list_copy[:, :]
    
def plot():
    positions = np.arange(num_levels)
    plt.bar(positions, count_levels_list, 1.0)
    plt.xticks(positions + 1.0 / 2, ('0', '1', '2', '3'))
    plt.show()

if __name__ == '__main__':
    setup()
    for i in range(epoch):
        if i % 10 == 0 or i < 10 or i + 1 == epoch:
            plot()
        turtle()