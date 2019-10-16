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

danmark_income = ['3665.5103', '48927.7843', '63434.2302', '75744.2086', '85639.6467', '94293.7128', '101959.7124', '107369.5022', '111698.5689', '115536.5154', '119210.014', '122609.5077', '125706.5773', '128725.3751', '131744.698', '134822.8126', '137777.0293', '140781.6395', '143730.2423', '146585.2193', '149509.9531', '152425.6022', '155262.4982', '158171.0174', '161156.5989', '164076.7104', '166855.456', '169696.8717', '172364.2891', '174943.548', '177454.5951', '179969.2298', '182555.1515', '185092.5766', '187748.2417', '190540.1543', '193517.7743', '196683.8718', '200123.1069', '203813.5053', '207564.6642', '211414.4648', '215243.9395', '219176.1106', '222985.5948', '226819.9106', '230761.3546', '234603.6177', '238539.3021', '242375.8925', '246230.9872', '250064.2094', '253970.6586', '257783.4961', '261654.8337', '265529.146', '269549.3878', '273619.2353', '277521.6899', '281549.3391', '285588.4496', '289671.3325', '293875.5908', '298117.9355', '302329.7173', '306648.4385', '311105.3032', '315570.5965', '319994.1862', '324687.7059', '329518.931', '334718.8886', '340245.5549', '346055.886', '352284.4964', '358694.5273', '365225.5253', '371826.7756', '378543.9183', '385726.7005', '393786.9566', '402544.3164', '411801.2318', '422237.2791', '434560.2058', '447392.5168', '459366.3676', '471847.2974', '485332.2092', '500258.8917', '517066.0675', '536328.4437', '559758.7416', '589026.638', '626890.7991', '678305.3717', '753289.4642', '876239.7657', '1131189.297', '3456590.323']
danmark_after_tax_income = [3372.269476, 43984.641318040005, 51858.74015256, 58540.59642808, 63911.84022876, 68609.26730784, 72770.37189072, 75706.80579416001, 78056.62319892, 80139.86055912, 82133.8355992, 83979.08077956, 85660.17015844, 87298.77360428001, 88937.6620744, 90608.46267928, 92212.01150404, 93842.9139206, 95443.41552044002, 96993.09703604001, 98580.64254268, 100163.25687416001, 101703.12402296001, 103281.86824472001, 104902.44188292, 106487.47840512001, 107995.7815168, 109538.10195875999, 110985.97612348, 112385.9978544, 113748.99422028, 115113.93793544002, 116517.57623420001, 117894.89057848, 119336.38559476002, 120851.83575403999, 122468.08789004, 124186.64561304002, 126053.46242532002, 128056.61067684, 130092.73972776, 132182.41149344, 134261.0503606, 136395.43283368, 138463.22085744, 140544.48747368, 142683.90327687998, 144769.48368756002, 146905.77317988, 148988.274449, 151080.81985216, 153161.49286232, 155281.91348808, 157351.52168308, 159452.88373236, 161555.86044880003, 163738.04769784003, 165947.16092084002, 168065.41327771998, 170251.62126348, 172444.05044288, 174660.23928100002, 176942.31068624, 179245.05538940002, 181531.21055044, 183875.41241780002, 186294.59857696004, 188718.3597802, 191119.48426936, 193667.12676252, 196289.5157468, 199112.05273208002, 202111.92719972, 205265.7749208, 208646.66464591998, 212126.02941844, 215671.05513284, 219254.21379568, 222900.27885324002, 226799.0930314, 231174.20004248002, 235927.69494192, 240952.34862104, 246617.03509548004, 253305.91970824002, 260271.29811904, 266770.70433328, 273545.35302871995, 280864.96315376, 288967.16641476, 298090.10143900005, 308545.71924035996, 320742.1543978112, 327732.26463081606, 336775.4379546512, 349054.8831578544, 366963.4839378144, 396327.9503456624, 457218.05680510396, 1012598.2346467358]

def income_tax(x):
    if (x > 558043):
        x -= (x - 558043)*.56
    if (x > 46200):
        x -= (x - 46200) * .41
    if (x >= 0):
        x -= (x - 0) * .08
    return x

# import numpy as np
# li = []
# for i in danmark_income:
#     li.append(income_tax(float(i)))
# print(li)




##################################################



