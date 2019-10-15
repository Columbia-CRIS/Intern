# show the agent distributions on a plot
import matplotlib.pyplot as plt
import numpy as np


def plot(num_levels,num_classes, count_levels_list,count_levels_combined,plt_title):
    x = np.linspace(0, num_levels, num_levels)
    for i in range(num_classes):
        #plt.plot(x, count_levels_list[:, i], marker='') # just a different style
        plt.bar(x, count_levels_list[:, i], alpha=0.45)

    # Uncomment the line below to show a curve of all classes combined.
    plt.plot(x, count_levels_combined, label="total", marker='', color='black', linewidth=0.5)
    plt.title(plt_title)
    plt.show()

def plot_wealth(agent_wealth_list,plt_title):
    n, bins, patches = plt.hist(x=agent_wealth_list, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(plt_title)
    std = np.std(agent_wealth_list)
    mean = np.mean(agent_wealth_list)
    plt.annotate("Sigma: " + str(std) + " Mean: " + str(mean),
                xy=(80, 300), xycoords='figure points')
    print("Sigma: " + str(std))
    print("Mean: " + str(mean))
    print("Max: " + str(np.max(agent_wealth_list)))
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()

def plot_save(num_levels,num_classes, count_levels_list,count_levels_combined,plt_title):
    x = np.linspace(0, num_levels, num_levels)
    for i in range(num_classes):
        #plt.plot(x, count_levels_list[:, i], marker='') # just a different style
        plt.bar(x, count_levels_list[:, i], alpha=0.45)

    # Uncomment the line below to show a curve of all classes combined.
    plt.plot(x, count_levels_combined, label="total", marker='', color='black', linewidth=0.5)
    plt.title(plt_title)
    plt.savefig(plt_title)
    plt.close()

def plot_wealth_save(agent_wealth_list,plt_title):
    n, bins, patches = plt.hist(x=agent_wealth_list, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(plt_title)
    std = np.std(agent_wealth_list)
    mean = np.mean(agent_wealth_list)
    # plt.annotate("Sigma: " + str(std) + " Mean: " + str(mean),
    #             xy=(80, 300), xycoords='figure points')
    print("Sigma: " + str(std))
    print("Mean: " + str(mean))
    print("Max: " + str(np.max(agent_wealth_list)))
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.savefig(plt_title)
    plt.close()