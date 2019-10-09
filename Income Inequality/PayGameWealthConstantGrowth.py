#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Oct 4 12:50:31 2019

@author: Hongyi Wang
"""


import numpy as np
import matplotlib.pyplot as plt
import math
import util


# basic settings
num_levels = 100 # number of salary levels
num_agents = 10000
# num_classes = 5
num_classes = 1
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
# N_list = [0.5, 0.3, 0.15, 0.03, 0.02] # class composition of whole population
# alpha_list = [93.4, 95.8, 97, 99, 100]
# beta_list = [3.87, 3.67, 3.67, 3.67, 4]
# gamma_list = [2.17, 4.34, 4.34, 4.34, 1]
#
#
N_list = [1]
alpha_list = [93.4]
beta_list = [3.87]
gamma_list = [2.17]





# for level -> salary value
s_min = 20000.0
s_max = 3000000.0

# stopping conditions
epsilon = 10
epoch_max = 100

# === DO NOT MODIFY THIS  ===
count_levels_list = np.zeros((num_levels, num_classes)) # number of agents by level and class
count_levels_combined = np.zeros(num_levels) # number of all agents by level
agent_levels_list = np.zeros(num_agents) # which level the agent is at
agent_classes_list = np.zeros(num_agents) # which level the agent belongs to
agent_wealth_list = np.zeros(num_agents) # Total income cumulated over time


# level -> salary value
def level_to_salary(x):
    return s_min + (s_max - s_min) / (num_levels - 1) * (x - 1)


# initialze global variables, including classes and parameter lists
def setup():
    # assign each agent to a class
    agent_classes_list[:] = np.random.choice(num_classes, num_agents, p=N_list)

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

    # Generate random array
    level_target_arr = np.random.randint(0, num_levels - 1, size=num_agents)
    level_self_arr = np.round(agent_levels_list).astype(int)
    c_arr = np.round(agent_classes_list).astype(int)

    level_target_arr_plus_one = level_target_arr + 1
    level_self_arr_plus_one = level_self_arr + 1
    s_target_arr =np.apply_along_axis(level_to_salary, 0, level_target_arr_plus_one)
    s_self_arr =np.apply_along_axis(level_to_salary, 0, level_self_arr_plus_one)

    # log utility functions with out third/competition term
    log_utility_payoff_target_alpha = np.multiply(agent_alpha_list, np.log(s_target_arr))
    log_utility_payoff_target_beta = np.multiply(agent_beta_list, np.power(np.log(s_target_arr),2))
    log_utility_payoff_target_a_b = np.subtract(log_utility_payoff_target_alpha, log_utility_payoff_target_beta)

    log_utility_payoff_self_alpha = np.multiply(agent_alpha_list, np.log(s_self_arr))
    log_utility_payoff_self_beta = np.multiply(agent_beta_list, np.power(np.log(s_self_arr), 2))
    log_utility_payoff_self_a_b = np.subtract(log_utility_payoff_self_alpha, log_utility_payoff_self_beta)

    # Increase wealth by 20%

    arrtmp = agent_wealth_list * 0.2
    print(type(agent_wealth_list))
    for i in range(num_agents):
        # # pick a random level as target
        # r = random.randint(0, num_levels - 1)
        #
        # c = int(round(agent_classes_list[i]))
        #
        # # find levels
        # level_target = r
        # level_self = int(round(agent_levels_list[i]))



        # # calculate salaries
        # s_target = level_to_salary(level_target + 1)
        # s_self = level_to_salary(level_self + 1)

        s_target = s_target_arr[i]
        s_self = s_self_arr[i]

        level_target = level_target_arr[i]
        level_self = level_self_arr[i]
        c = c_arr[i]

        # Note: agents should make decisions one by one, not all at once as
        # previously programmed. Otherwise, the program will produce wrong
        # results. Thus, we use count_levels_combined_copy instead of
        # count_levels_combined.
        num_target = count_levels_combined_copy[level_target]
        num_self = count_levels_combined_copy[level_self]

        alpha, beta, gamma = agent_alpha_list[i], agent_beta_list[i], agent_gamma_list[i]

        # target utility & current utility
        if utility_function == 'log':
            # payoff_target = alpha * math.log(s_target)
            # payoff_target = log_utility_payoff_target_alpha[i]
            # payoff_target -= beta * math.log(s_target) ** 2
            # payoff_target -= log_utility_payoff_target_beta[i]
            payoff_target = log_utility_payoff_target_a_b[i]
            payoff_target -= gamma * math.log(num_target + 1.0 / num_agents)

            # payoff_self = alpha * math.log(s_self)
            # payoff_self = log_utility_payoff_self_alpha[i]
            # payoff_self -= beta * math.log(s_self) ** 2
            # payoff_self -= log_utility_payoff_self_beta[i]
            payoff_self = log_utility_payoff_self_a_b[i]
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

        #Cumulate Wealth
        agent_wealth_list[i] += s_self

    # calculate the least square difference of count change
    loss = sum((count_levels_combined_copy - count_levels_combined) ** 2)

    # update state variable(s)
    count_levels_combined[:] = count_levels_combined_copy[:]

    return loss


if __name__ == '__main__':
    setup()
    print("Started... ")
    # plot() #initial

    import time
    start_time = time.time()
    loss = epsilon + 1
    epoch = 0
    while loss > epsilon and epoch < epoch_max:
        loss = turtle()
        print("Epoch " + str(epoch) + " Loss: " + str(loss))
        epoch += 1
    util.plot(num_levels,num_classes, count_levels_list,count_levels_combined)
    util.plot_wealth(agent_wealth_list, "Wealth Histogram with Constant Growth One Class")

    print("Converged after " + str(epoch) + " epoches. ")
    print("--- %s seconds ---" % (time.time() - start_time))