#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Oct 4 12:50:31 2019

@author: Hongyi Wang
"""


# import numpy as np
import matplotlib.pyplot as plt
import random
import math
import numpy as np
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


N_list = [1]
alpha_list = [93.4]
beta_list = [3.87]
gamma_list = [2.17]

#Tax Brackets
# tax_rate = [1-0,1-.32,1-.52,1-.57]
tax_rate = [.1]







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
    #Calculate after tax target
    length_of_range = (num_levels + 1) / len(tax_rate)


    target_tax_bracket_arr = level_target_arr / length_of_range
    target_tax_bracket_arr = np.floor(target_tax_bracket_arr)



    self_tax_bracket_arr = level_self_arr / length_of_range
    self_tax_bracket_arr = np.floor(self_tax_bracket_arr)



    s_target_tax_rate_arr = np.array(tax_rate)[target_tax_bracket_arr.astype(int)]
    s_self_tax_rate_arr = np.array(tax_rate)[self_tax_bracket_arr.astype(int)]

    s_target_after_tax_arr = np.multiply(s_target_arr, s_target_tax_rate_arr)
    s_self_after_tax_arr = np.multiply(s_self_arr,s_self_tax_rate_arr)
    s_target_arr = s_target_after_tax_arr
    s_self_arr =s_self_after_tax_arr



    log_utility_payoff_target_alpha = np.multiply(agent_alpha_list, np.log(s_target_arr))
    log_utility_payoff_target_beta = np.multiply(agent_beta_list, np.power(np.log(s_target_arr),2))
    log_utility_payoff_target_a_b = np.subtract(log_utility_payoff_target_alpha, log_utility_payoff_target_beta)

    log_utility_payoff_self_alpha = np.multiply(agent_alpha_list, np.log(s_self_arr))
    log_utility_payoff_self_beta = np.multiply(agent_beta_list, np.power(np.log(s_self_arr), 2))
    log_utility_payoff_self_a_b = np.subtract(log_utility_payoff_self_alpha, log_utility_payoff_self_beta)







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

        level_target = level_target_arr[i]
        level_self = level_self_arr[i]


        s_target = s_target_arr[i]
        s_self = s_self_arr[i]

        # Tax
        # length_of_range = (num_levels + 1) / len(tax_rate)
        # target_tax_bracket = math.floor(level_target / length_of_range)
        # self_tax_bracket = math.floor(level_self / length_of_range)

        # s_target_after_tax = s_target * tax_rate[target_tax_bracket]
        # s_self_after_tax = s_self * tax_rate[self_tax_bracket]
        #
        # s_target = s_target_after_tax
        # s_self = s_self_after_tax
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


if __name__ == '__main__':
    setup()
    print("Started... ")
    plot() #initial

    import time
    start_time = time.time()
    loss = epsilon + 1
    epoch = 0
    while loss > epsilon and epoch < epoch_max:
        loss = turtle()
        print("Epoch " + str(epoch) + " Loss: " + str(loss))
        epoch += 1

    import warnings
    import numpy as np
    import pandas as pd
    import scipy.stats as st
    import statsmodels as sm
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
    matplotlib.style.use('ggplot')


    # Create models from data
    def best_fit_distribution(data, bins=200, ax=None):
        """Model data by finding best fit distribution to data"""
        # Get histogram of original data
        y, x = np.histogram(data, bins=bins, density=True)
        x = (x + np.roll(x, -1))[:-1] / 2.0

        # Distributions to check
        DISTRIBUTIONS = [
            st.alpha, st.anglit, st.arcsine, st.beta, st.betaprime, st.bradford, st.burr, st.cauchy, st.chi, st.chi2,
            st.cosine,
            st.dgamma, st.dweibull, st.erlang, st.expon, st.exponnorm, st.exponweib, st.exponpow, st.f, st.fatiguelife,
            st.fisk,
            st.foldcauchy, st.foldnorm, st.frechet_r, st.frechet_l, st.genlogistic, st.genpareto, st.gennorm,
            st.genexpon,
            st.genextreme, st.gausshyper, st.gamma, st.gengamma, st.genhalflogistic, st.gilbrat, st.gompertz,
            st.gumbel_r,
            st.gumbel_l, st.halfcauchy, st.halflogistic, st.halfnorm, st.halfgennorm, st.hypsecant, st.invgamma,
            st.invgauss,
            st.invweibull, st.johnsonsb, st.johnsonsu, st.ksone, st.kstwobign, st.laplace, st.levy, st.levy_l,
            st.levy_stable,
            st.logistic, st.loggamma, st.loglaplace, st.lognorm, st.lomax, st.maxwell, st.mielke, st.nakagami, st.ncx2,
            st.ncf,
            st.nct, st.norm, st.pareto, st.pearson3, st.powerlaw, st.powerlognorm, st.powernorm, st.rdist,
            st.reciprocal,
            st.rayleigh, st.rice, st.recipinvgauss, st.semicircular, st.t, st.triang, st.truncexpon, st.truncnorm,
            st.tukeylambda,
            st.uniform, st.vonmises, st.vonmises_line, st.wald, st.weibull_min, st.weibull_max, st.wrapcauchy
        ]

        # Best holders
        best_distribution = st.norm
        best_params = (0.0, 1.0)
        best_sse = np.inf

        # Estimate distribution parameters from data
        for distribution in DISTRIBUTIONS:

            # Try to fit the distribution
            try:
                # Ignore warnings from data that can't be fit
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore')

                    # fit dist to data
                    params = distribution.fit(data)

                    # Separate parts of parameters
                    arg = params[:-2]
                    loc = params[-2]
                    scale = params[-1]

                    # Calculate fitted PDF and error with fit in distribution
                    pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                    sse = np.sum(np.power(y - pdf, 2.0))

                    # if axis pass in add to plot
                    try:
                        if ax:
                            pd.Series(pdf, x).plot(ax=ax)
                        end
                    except Exception:
                        pass

                    # identify if this distribution is better
                    if best_sse > sse > 0:
                        best_distribution = distribution
                        best_params = params
                        best_sse = sse

            except Exception:
                pass

        return (best_distribution.name, best_params)


    def make_pdf(dist, params, size=10000):
        """Generate distributions's Probability Distribution Function """

        # Separate parts of parameters
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]

        # Get sane start and end points of distribution
        start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
        end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

        # Build PDF and turn into pandas Series
        x = np.linspace(start, end, size)
        y = dist.pdf(x, loc=loc, scale=scale, *arg)
        pdf = pd.Series(y, x)

        return pdf


    # Load data from statsmodels datasets
    # data = pd.Series(sm.datasets.elnino.load_pandas().data.set_index('YEAR').values.ravel())
    data = pd.Series(count_levels_combined)
    # Plot for comparison
    plt.figure(figsize=(12, 8))
    ax = data.plot(kind='hist', bins=50, normed=True, alpha=0.5)
    # Save plot limits
    dataYLim = ax.get_ylim()

    # Find best fit distribution
    best_fit_name, best_fit_params = best_fit_distribution(data, 200, ax)
    best_dist = getattr(st, best_fit_name)

    # Update plots
    ax.set_ylim(dataYLim)
    ax.set_title(u'El Niño sea temp.\n All Fitted Distributions')
    ax.set_xlabel(u'Temp (°C)')
    ax.set_ylabel('Frequency')

    # Make PDF with best params
    pdf = make_pdf(best_dist, best_fit_params)

    # Display
    plt.figure(figsize=(12, 8))
    ax = pdf.plot(lw=2, label='PDF', legend=True)
    data.plot(kind='hist', bins=50, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)

    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.2f}'.format(k, v) for k, v in zip(param_names, best_fit_params)])
    dist_str = '{}({})'.format(best_fit_name, param_str)

    ax.set_title(u'El Niño sea temp. with best fit distribution \n' + dist_str)
    ax.set_xlabel(u'Temp. (°C)')
    ax.set_ylabel('Frequency')




    print("Converged after " + str(epoch) + " epoches. ")
    print("--- %s seconds ---" % (time.time() - start_time))