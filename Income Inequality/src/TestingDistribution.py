import numpy as np
import util
x1 = np.random.lognormal(0,1.0,1000)
x2 = np.random.lognormal(0,1.0,1000)

util.plot_wealth(x1+x2,"Sum of Lognormal")
print((x1+x2).shape)
print(util.best_fit_distribution(x1+x2))