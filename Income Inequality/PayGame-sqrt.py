{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
# -*- coding: utf-8 -*-\
\
"""\
Created on Thu Nov 15 12:50:31 2018\
\
@author: XIN\
"""\
\
\
import numpy as np\
import matplotlib.pyplot as plt\
import random\
import math\
\
\
# basic settings\
num_levels = 100 # number of salary levels\
num_agents = 100000\
num_classes = 5 \
\
# parameter init mode, either 'constant' or 'random'\
mode = 'constant'\
\
# standard dev. under random mode\
sigma_alpha = 0.1\
sigma_beta = 0.01\
sigma_gamma = 0.01\
\
# parameters for each agent\
agent_alpha_list = np.zeros(num_agents)\
agent_beta_list = np.zeros(num_agents)\
agent_gamma_list = np.zeros(num_agents)\
\
# parameters for each class\
N_list = [1.0, 0.0, 0.0, 0.0, 0.0] # class composition of whole population\
alpha_list = [4093.0, 95.8, 97, 99, 100]\
beta_list = [4.73, 3.67, 3.67, 3.67, 4]\
gamma_list = [91210.0, 4.34, 4.34, 4.34, 1]\
\
# for level -> salary value\
s_min = 20000.0\
s_max = 3000000.0\
\
# stopping conditions\
epsilon = 100\
epoch_max = 30\
\
\
# === DO NOT MODIFY THIS  ===\
count_levels_list = np.zeros((num_levels, num_classes)) # number of agents by level and class\
count_levels_combined = np.zeros(num_levels) # number of all agents by level\
agent_levels_list = np.zeros(num_agents) # which level the agent is at\
agent_classes_list = np.zeros(num_agents) # which level the agent belongs to\
\
\
# level -> salary value\
def level_to_salary(x):\
    return s_min + (s_max - s_min) / (num_levels - 1) * (x - 1)\
\
\
# initialze global variables, including classes and parameter lists\
def setup():\
    # assign each agent to a class\
    agent_classes_list[:] = np.random.choice(5, num_agents, p=N_list)\
    \
    mean = num_levels / 2\
    for i in range(num_agents):\
        r = int(round(mean)) # all agents start at the mean level\
        c = int(round(agent_classes_list[i]))\
        count_levels_list[r, c] += 1\
        count_levels_combined[r] += 1\
        agent_levels_list[i] = r\
        \
        if mode == 'constant':\
            agent_alpha_list[i] = alpha_list[c]\
            agent_beta_list[i] = beta_list[c]\
            agent_gamma_list[i] = gamma_list[c]\
        else:\
            agent_alpha_list[i] = np.random.normal(alpha_list[c], sigma_alpha, 1)\
            agent_beta_list[i] = np.random.normal(beta_list[c], sigma_beta, 1)\
            agent_gamma_list[i] = np.random.normal(gamma_list[c], sigma_gamma, 1)\
\
   \
# simulate for one round and return the least square difference of count change\
def turtle():\
    # make a copy for later comparisons\
    count_levels_combined_copy = count_levels_combined.copy()\
    \
    for i in range(num_agents):\
        # pick a random level as target\
        r = random.randint(0, num_levels - 1)\
        c = int(round(agent_classes_list[i]))\
        \
        # find levels\
        level_target = r\
        level_self = int(round(agent_levels_list[i]))\
        \
        # calculate salaries\
        s_target = level_to_salary(level_target + 1)\
        s_self = level_to_salary(level_self + 1)\
        \
        # Note: agents should make decisions one by one, not all at once as \
        # previously programmed. Otherwise, the program will produce wrong \
        # results. Thus, we use count_levels_combined_copy instead of \
        # count_levels_combined.\
        num_target = count_levels_combined_copy[level_target]\
        num_self = count_levels_combined_copy[level_self]\
        \
        alpha, beta, gamma = agent_alpha_list[i], agent_beta_list[i], agent_gamma_list[i]\
        \
        # target utility\
        payoff_target = alpha * math.sqrt(s_target) \
        payoff_target -= beta * math.sqrt(s_target) ** 2\
        payoff_target -= gamma * math.log(num_target + 1.0 / num_agents)\
        \
        # current utility\
        payoff_self = alpha * math.sqrt(s_self)\
        payoff_self -= beta * math.sqrt(s_self) ** 2\
        payoff_self -= gamma * math.log(num_self + 1.0 / num_agents)\
        \
        if payoff_target > payoff_self:\
            # move agent from self to target\
            count_levels_list[level_self, c] -= 1\
            count_levels_combined_copy[level_self] -= 1\
            count_levels_list[level_target, c] += 1\
            count_levels_combined_copy[level_target] += 1\
            agent_levels_list[i] = level_target\
    \
    # calculate the least square difference of count change\
    loss = sum((count_levels_combined_copy - count_levels_combined) ** 2)\
    \
    # update state variable(s)\
    count_levels_combined[:] = count_levels_combined_copy[:]\
    \
    return loss\
\
\
# show the agent distributions on a plot\
def plot():\
    x = np.linspace(0, num_levels, num_levels)\
    for i in range(num_classes):\
        #plt.plot(x, count_levels_list[:, i], marker='') # just a different style\
        plt.bar(x, count_levels_list[:, i], alpha=0.45)\
    \
    # Uncomment the line below to show a curve of all classes combined.\
    plt.plot(x, count_levels_combined, label="total", marker='', color='black', linewidth=0.5)\
    \
    plt.show()\
\
\
if __name__ == '__main__':\
    setup()\
    print("Started... ")\
    plot() #initial\
    \
    loss = epsilon + 1\
    epoch = 0\
    while loss > epsilon and epoch < epoch_max:\
        loss = turtle()\
        print("Epoch " + str(epoch) + " Loss: " + str(loss))\
        epoch += 1\
        plot()\
    \
    print("Converged after " + str(epoch) + " epoches. ")}