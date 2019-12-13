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

def plot_with_income_data(num_levels, income_data, count_levels_list, plt_title):

    # plt.plot(x, count_levels_list[:, i], marker='') # just a different style
    plt.plot(np.asarray(income_data).astype(float)[:], count_levels_list[:, 0],alpha=.45)

    # Uncomment the line below to show a curve of all classes combined.
    # plt.plot(x, count_levels_combined, label="total", marker='', color='black', linewidth=0.5)
    plt.title(plt_title)
    plt.show()


def plot_with_income_data_save(num_levels, income_data, count_levels_list, plt_title):

    # plt.plot(x, count_levels_list[:, i], marker='') # just a different style
    plt.plot(np.asarray(income_data).astype(float)[:], count_levels_list[:, 0])

    # Uncomment the line below to show a curve of all classes combined.
    # plt.plot(x, count_levels_combined, label="total", marker='', color='black', linewidth=0.5)
    plt.title(plt_title)
    plt.savefig(plt_title)
    plt.close()

def plot(num_levels,num_classes, count_levels_list, count_levels_combined):
    x = np.linspace(0, num_levels, num_levels)
    for i in range(num_classes):
        #plt.plot(x, count_levels_list[:, i], marker='') # just a different style
        plt.bar(x, count_levels_list[:, i], alpha=0.45)

    # Uncomment the line below to show a curve of all classes combined.
    plt.plot(x, count_levels_combined, label="total", marker='', color='black', linewidth=0.5)

    plt.show()


danmark_income = ['3665.5103', '48927.7843', '63434.2302', '75744.2086', '85639.6467', '94293.7128', '101959.7124', '107369.5022', '111698.5689', '115536.5154', '119210.014', '122609.5077', '125706.5773', '128725.3751', '131744.698', '134822.8126', '137777.0293', '140781.6395', '143730.2423', '146585.2193', '149509.9531', '152425.6022', '155262.4982', '158171.0174', '161156.5989', '164076.7104', '166855.456', '169696.8717', '172364.2891', '174943.548', '177454.5951', '179969.2298', '182555.1515', '185092.5766', '187748.2417', '190540.1543', '193517.7743', '196683.8718', '200123.1069', '203813.5053', '207564.6642', '211414.4648', '215243.9395', '219176.1106', '222985.5948', '226819.9106', '230761.3546', '234603.6177', '238539.3021', '242375.8925', '246230.9872', '250064.2094', '253970.6586', '257783.4961', '261654.8337', '265529.146', '269549.3878', '273619.2353', '277521.6899', '281549.3391', '285588.4496', '289671.3325', '293875.5908', '298117.9355', '302329.7173', '306648.4385', '311105.3032', '315570.5965', '319994.1862', '324687.7059', '329518.931', '334718.8886', '340245.5549', '346055.886', '352284.4964', '358694.5273', '365225.5253', '371826.7756', '378543.9183', '385726.7005', '393786.9566', '402544.3164', '411801.2318', '422237.2791', '434560.2058', '447392.5168', '459366.3676', '471847.2974', '485332.2092', '500258.8917', '517066.0675', '536328.4437', '559758.7416', '589026.638', '626890.7991', '678305.3717', '753289.4642', '876239.7657', '1131189.297', '3456590.323']
danmark_income_after_tax = [3372.269476, 44113.392737, 52672.195818, 59935.083074, 65773.391553, 70879.29055199999, 75402.230316, 78594.00629800001, 81148.15565100001, 83412.54408600001, 85579.90826, 87585.609543, 89412.880607, 91193.97130900002, 92975.37182, 94791.459434, 96534.447287, 98307.167305, 100046.84295700002, 101731.279387, 103456.872329, 105177.10529800001, 106850.873938, 108566.90026600001, 110328.393351, 112051.25913600001, 113690.71904, 115367.15430299999, 116940.93056899999, 118462.69332, 119944.211109, 121427.84558200001, 122953.53938500001, 124450.620194, 126017.46260300002, 127664.691037, 129421.486837, 131289.48436200002, 133318.63307100002, 135495.968127, 137709.151878, 139980.534232, 142239.924305, 144559.905254, 146807.500932, 149069.747254, 151395.199214, 153662.13444300002, 155984.188239, 158247.776575, 160522.282448, 162783.883546, 165088.688574, 167338.262699, 169622.351883, 171908.19614000001, 174280.13880200003, 176681.348827, 178983.79704099998, 181360.110069, 183743.185264, 186152.086175, 188632.598572, 191135.581945, 193620.533207, 196168.578715, 198798.12888800004, 201432.651935, 204042.569858, 206811.746481, 209662.16929, 212730.14427400002, 215990.877391, 219418.97274, 223093.852876, 226875.771107, 230729.059927, 234623.797604, 238586.911797, 242824.753295, 247580.304394, 252747.146676, 258208.726762, 264365.99466900004, 271636.521422, 279207.584912, 286272.156884, 293635.90546599997, 301592.003428, 310398.746103, 320314.97982500005, 331679.781783, 345246.29630399996, 358124.17072000005, 374784.401604, 397406.813548, 430399.81424800004, 484497.94690800004, 596675.74068, 1619852.1921199998]


# usa_income = ['-3978.2491', '-1813.6335', '-643.5802', '-58.4687', '292.5133', '1521.1202', '2574.1511', '3568.7132', '4563.2757', '5323.8783', '6084.3958', '6786.4448', '7371.4713', '7898.029', '8424.5874', '9009.6138', '9536.1718', '10121.1984', '10647.7564', '11291.2516', '11876.3633', '12461.3899', '12987.8628', '13572.9744', '14216.4697', '14801.4964', '15386.608', '16030.1032', '16673.6834', '17317.1788', '17902.2054', '18487.317', '19072.3436', '19774.3926', '20417.887', '21119.9376', '21763.5171', '22407.0973', '23109.1462', '23869.6638', '24571.7127', '25332.2304', '26151.3008', '26911.9033', '27672.4219', '28549.961', '29427.585', '30305.1266', '31182.6683', '32118.7618', '33054.7687', '33932.3928', '34926.9558', '35862.9627', '36799.0564', '37793.6194', '38846.7345', '39958.319', '41011.3517', '42064.4667', '43117.4993', '44287.5533', '45457.6899', '46569.2744', '47739.3286', '48967.9346', '50255.0101', '51600.5552', '52946.1828', '54291.8145', '55637.3553', '57041.4566', '58504.109', '60025.1417', '61604.8129', '63418.4473', '65232.0825', '67279.6739', '69561.316', '71784.4852', '74183.1452', '76581.8053', '79097.4835', '81788.6603', '84655.4064', '87873.1395', '91500.4064', '95478.6554', '100042.0161', '105248.8718', '110982.2007', '117768.7305', '125842.2592', '135846.4268', '148892.8433', '166853.6109', '193414.4397', '238404.1338', '330899.0175', '1181782.321']
usa_income = ['292.5133', '1521.1202', '2574.1511', '3568.7132', '4563.2757', '5323.8783', '6084.3958', '6786.4448', '7371.4713', '7898.029', '8424.5874', '9009.6138', '9536.1718', '10121.1984', '10647.7564', '11291.2516', '11876.3633', '12461.3899', '12987.8628', '13572.9744', '14216.4697', '14801.4964', '15386.608', '16030.1032', '16673.6834', '17317.1788', '17902.2054', '18487.317', '19072.3436', '19774.3926', '20417.887', '21119.9376', '21763.5171', '22407.0973', '23109.1462', '23869.6638', '24571.7127', '25332.2304', '26151.3008', '26911.9033', '27672.4219', '28549.961', '29427.585', '30305.1266', '31182.6683', '32118.7618', '33054.7687', '33932.3928', '34926.9558', '35862.9627', '36799.0564', '37793.6194', '38846.7345', '39958.319', '41011.3517', '42064.4667', '43117.4993', '44287.5533', '45457.6899', '46569.2744', '47739.3286', '48967.9346', '50255.0101', '51600.5552', '52946.1828', '54291.8145', '55637.3553', '57041.4566', '58504.109', '60025.1417', '61604.8129', '63418.4473', '65232.0825', '67279.6739', '69561.316', '71784.4852', '74183.1452', '76581.8053', '79097.4835', '81788.6603', '84655.4064', '87873.1395', '91500.4064', '95478.6554', '100042.0161', '105248.8718', '110982.2007', '117768.7305', '125842.2592', '135846.4268', '148892.8433', '166853.6109', '193414.4397', '238404.1338', '330899.0175', '1181782.321']
# usa_income_after_tax = [-3978.2491, -1813.6335, -643.5802, -58.4687, 263.26197, 1369.00818, 2316.73599, 3211.84188, 4106.94813, 4791.490470000001, 5475.95622, 6107.80032, 6634.32417, 7108.2261, 7582.12866, 8108.652419999999, 8582.55462, 9100.654591999999, 9564.025632, 10130.301408, 10645.199704, 11160.023112, 11623.319264000002, 12138.217472, 12704.493336, 13219.316832, 13734.21504, 14300.490816, 14866.841392000002, 15433.117344000002, 15947.940751999999, 16462.83896, 16977.662368, 17595.465487999998, 18161.74056, 18779.545088, 19345.895048000002, 19912.245624000003, 20530.048656, 21199.304143999998, 21817.107176, 22486.362752, 23207.144704000002, 23876.474904000002, 24545.731272, 25317.96568, 26090.2748, 26862.511408, 27634.748104000002, 28458.510384, 29282.196456, 30054.505664, 30929.721104000004, 31753.407175999997, 32577.169632, 33452.385072000005, 34379.126359999995, 35308.98882, 36130.354326, 36951.784025999994, 37773.149454, 38685.791574, 39598.498122, 40465.534032, 41378.176308, 42336.488988, 43340.407878, 44389.933056, 45439.522584000006, 46489.11531, 47538.637134000004, 48633.836148, 49774.705019999994, 50961.110526000004, 52193.254062, 53607.888894, 55022.52435, 56619.645641999996, 58399.32648, 60133.398455999995, 62004.353256, 63875.308134000006, 65837.53713, 67936.655034, 70163.60886400001, 72609.08602, 75365.808864, 78389.278104, 81857.432236, 85814.642568, 90171.972532, 95329.73518, 101465.616992, 109068.784368, 118984.06090800001, 132143.955412, 150205.318996, 179769.18697, 239890.861375, 779535.36223]
usa_income_after_tax = [263.26197, 1369.00818, 2316.73599, 3211.84188, 4106.94813, 4791.490470000001, 5475.95622, 6107.80032, 6634.32417, 7108.2261, 7582.12866, 8108.652419999999, 8582.55462, 9100.654591999999, 9564.025632, 10130.301408, 10645.199704, 11160.023112, 11623.319264000002, 12138.217472, 12704.493336, 13219.316832, 13734.21504, 14300.490816, 14866.841392000002, 15433.117344000002, 15947.940751999999, 16462.83896, 16977.662368, 17595.465487999998, 18161.74056, 18779.545088, 19345.895048000002, 19912.245624000003, 20530.048656, 21199.304143999998, 21817.107176, 22486.362752, 23207.144704000002, 23876.474904000002, 24545.731272, 25317.96568, 26090.2748, 26862.511408, 27634.748104000002, 28458.510384, 29282.196456, 30054.505664, 30929.721104000004, 31753.407175999997, 32577.169632, 33452.385072000005, 34379.126359999995, 35308.98882, 36130.354326, 36951.784025999994, 37773.149454, 38685.791574, 39598.498122, 40465.534032, 41378.176308, 42336.488988, 43340.407878, 44389.933056, 45439.522584000006, 46489.11531, 47538.637134000004, 48633.836148, 49774.705019999994, 50961.110526000004, 52193.254062, 53607.888894, 55022.52435, 56619.645641999996, 58399.32648, 60133.398455999995, 62004.353256, 63875.308134000006, 65837.53713, 67936.655034, 70163.60886400001, 72609.08602, 75365.808864, 78389.278104, 81857.432236, 85814.642568, 90171.972532, 95329.73518, 101465.616992, 109068.784368, 118984.06090800001, 132143.955412, 150205.318996, 179769.18697, 239890.861375, 779535.36223]
usa_income_danish_tax = [269.112236, 1399.4305840000002, 2368.219012, 3283.216144, 4198.213644, 4897.968036, 5597.644136, 6243.529216, 6781.7535960000005, 7266.186680000001, 7750.620408000001, 8288.844696, 8773.278056, 9311.502527999999, 9795.935888, 10387.951471999999, 10926.254236, 11464.478708, 11948.833776000001, 12487.136448, 13079.152124, 13617.376688, 14155.67936, 14747.694943999999, 15339.788728000001, 15931.804496, 16470.028968, 17008.33164, 17546.556112, 18192.441192, 18784.456039999997, 19430.342592, 20022.435732, 20614.529516000002, 21260.414504, 21960.090696, 22605.975684, 23305.651968000002, 24059.196736, 24758.951036000002, 25458.628148, 26265.96412, 27073.3782, 27880.716472, 28688.054836000003, 29549.260856, 30410.387204, 31217.801376000003, 32132.799336000004, 32993.925683999994, 33855.131888, 34770.129848000004, 35738.99574, 36761.65348, 37730.443564, 38699.309364, 39668.099356000006, 40744.549036, 41821.074708, 42721.871896000004, 43412.203874, 44137.081414, 44896.455959, 45690.327568, 46484.247852, 47278.170555000004, 48072.039627000006, 48900.459394, 49763.42431, 50660.833603, 51592.839611, 52662.883906999996, 53732.928675, 54941.007601, 56287.17644, 57598.846267999994, 59014.055668, 60429.265127000006, 61913.515265, 63501.30957700001, 65192.68977600001, 67091.152305, 69231.239776, 71578.406686, 74270.789499, 77342.834362, 80725.498413, 84729.550995, 89492.932928, 95395.39181199999, 103092.777547, 113689.630431, 129360.51942299999, 155904.438942, 210476.420325, 618936.6712399999]
france_income = ['1.4257', '25.8533', '138.4864', '426.8652', '1000.8664', '1981.8676', '3500.5609', '4966.7875', '6275.0424', '7868.54', '8752.5907', '9035.4562', '9536.4601', '10101.4316', '10683.2267', '11303.7069', '11967.5293', '12668.516', '13371.8789', '14027.8123', '14600.1976', '15100.8209', '15580.7244', '16090.8517', '16662.3825', '17268.3201', '17867.9826', '18426.5867', '18909.817', '19329.4585', '19712.3151', '20073.5955', '20416.2473', '20742.0764', '21058.2095', '21376.3395', '21710.9122', '22070.5758', '22460.9432', '22865.0917', '23285.0183', '23720.0578', '24152.0556', '24588.5218', '25039.5295', '25493.4827', '25938.4073', '26375.0626', '26813.4287', '27254.1721', '27702.9927', '28157.1379', '28592.1764', '29019.0416', '29443.8158', '29861.0811', '30262.093', '30644.9495', '31019.918', '31383.2914', '31744.0995', '32108.5156', '32460.197', '32806.4616', '33163.2738', '33559.6283', '33993.8133', '34462.502', '34973.958', '35524.675', '36137.9304', '36823.8984', '37572.2204', '38378.6145', '39261.431', '40232.8321', '41274.0943', '42360.6018', '43479.1351', '44618.5839', '45762.7852', '46922.0973', '48075.5174', '49219.4326', '50391.1981', '51642.6156', '52854.1078', '54259.4078', '55851.7653', '57651.3297', '59195.2122', '62526.3017', '66413.0422', '70394.6465', '74242.9967', '79550.342', '89558.6274', '108149.8372', '140599.3032', '371195.0943']
france_income_after_tax = [1.4257, 25.8533, 138.4864, 426.8652, 1000.8664, 1981.8676, 3500.5609, 4966.7875, 6275.0424, 7868.54, 8752.5907, 9035.4562, 9536.4601, 10082.191176, 10582.534962, 11116.147933999999, 11687.035198, 12289.883759999999, 12894.775854, 13458.878578, 13951.129936, 14381.665974, 14794.382984, 15233.092461999999, 15724.60895, 16245.715286, 16761.425036, 17241.824562, 17657.40262, 18018.29431, 18347.550986, 18658.25213, 18952.932677999997, 19233.145704000002, 19505.02017, 19778.611969999998, 20066.344492, 20375.655187999997, 20711.371152, 21058.938862, 21420.075738, 21794.209708, 22165.727816, 22541.088748, 22928.95537, 23319.355122, 23701.990277999997, 24077.513836000002, 24454.508682, 24833.548006, 25190.09489, 25507.99653, 25812.52348, 26111.32912, 26408.67106, 26700.75677, 26981.4651, 27249.464649999998, 27511.942600000002, 27766.303979999997, 28018.86965, 28273.960919999998, 28520.1379, 28762.52312, 29012.291660000003, 29289.73981, 29593.66931, 29921.7514, 30279.7706, 30665.272500000003, 31094.55128, 31574.72888, 32098.554279999997, 32663.030150000002, 33281.00169999999, 33960.98247, 34689.86601, 35450.421259999996, 36233.394570000004, 37031.00873, 37831.94964, 38643.46811, 39450.86218, 40251.60282, 41071.83867, 41947.83092, 42795.875459999996, 43779.58546, 44894.23571, 46153.93079, 47234.64854, 49566.41119, 52287.129539999994, 55074.252550000005, 57717.058053, 60848.391780000005, 66753.280166, 77722.093948, 96867.278888, 224320.75186499997]


def income_tax_danmark(x):
    total_tax = 0
    y = x
    if (x > 558043):
        total_tax += (y - 558043)*.56
        y = 558043
    if (x > 46200):
        total_tax += (y - 46200) * .41
        y = 46200
    if (x >= 0):
        total_tax += (y - 0) * .08
    return x - total_tax

def income_tax_usa(x):
    y = x
    total_tax = 0
    if (x > 510300):
        total_tax += (y - 510300) * .37
        print(total_tax)
        y = 510300
    if (x > 204100):
        total_tax += (y- 204100) * .35
        print(total_tax)
        y = 204100
    if (x > 160725):
        total_tax += (y - 160725) * .32
        print(total_tax)
        y = 160725
    if (x > 84200):
        total_tax += (y - 84200) * .24
        print(total_tax)
        y = 84200
    if (x > 39475):
        total_tax += (y - 39475) * .22
        print(total_tax)
        y = 39475
    if (x > 9700):
        total_tax += (y - 9700) * .12
        print(total_tax)
        y = 9700
    if (x > 0):
        total_tax += (y - 0) * .1
    print(total_tax)
    return x - total_tax

def income_tax_france(x):
    y = x
    total_tax = 0
    if (x > 156244):
        total_tax += (y - 156244) * .45
        y = 156244
    if (x > 73779):
        total_tax += (y- 73779) * .41
        y = 73779
    if (x > 27519):
        total_tax += (y - 27519) * .30
        y = 27519
    if (x > 9964):
        total_tax += (y - 9964) * .14
        y = 9964
    if (x > 0):
        total_tax += (y - 0) * 0
    return x - total_tax


#
# import numpy as np
# li = []
# for i in france_income:
#     li.append(income_tax_france(float(i)))
# print(li)




##################################################
'''
The following code was used to find the best distribution to describe data.
'''
# import warnings
# import numpy as np
# import pandas as pd
# import scipy.stats as st
# import statsmodels as sm
# import matplotlib
# import matplotlib.pyplot as plt
# from scipy.stats._continuous_distns import _distn_names
#
# def best_fit_distribution(data, bins=100, ax=None):
# #"""Model data by finding best fit distribution to data"""
# # Get histogram of original data
#     y, x = np.histogram(data, bins=bins, density=True)
#     x = (x + np.roll(x, -1))[:-1] / 2.0
#
#     # Distributions to check
#     DISTRIBUTIONS = [
#        distname for distname in _distn_names
#     ]
#
#     # Best holders
#     best_distribution = st.norm
#     best_params = (0.0, 1.0)
#     best_sse = np.inf
#
#     # Estimate distribution parameters from data
#     for dist in DISTRIBUTIONS:
#         distribution = getattr(st, dist)
#         # Try to fit the distribution
#         try:
#             # Ignore warnings from data that can't be fit
#             with warnings.catch_warnings():
#                 warnings.filterwarnings('ignore')
#                 # fit dist to data
#                 params = distribution.fit(data)
#
#                 # Separate parts of parameters
#                 arg = params[:-2]
#                 loc = params[-2]
#                 scale = params[-1]
#
#                 # Calculate fitted PDF and error with fit in distribution
#                 pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
#                 sse = np.sum(np.power(y - pdf, 2.0))
#                 # if axis pass in add to plot
#                 try:
#                     if ax:
#                         pd.Series(pdf, x).plot(ax=ax)
#                 except Exception:
#                     pass
#
#                 # identify if this distribution is better
#                 if best_sse > sse > 0:
#                     best_distribution = distribution
#                     best_params = params
#                     best_sse = sse
#
#         except Exception:
#             pass
#
#     return (best_distribution.name, best_params)