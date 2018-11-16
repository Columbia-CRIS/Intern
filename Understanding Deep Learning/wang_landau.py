g_map = {}
histogram = {}

def cost_function(weights):
    cur_cost = 0    

def g_function(weights):
    if weights in g_map:
        return g_map[weights]
    else:
        return 1
    
def update_g_function(weights, alpha):
    if weights in g_map:
        g_map[weights] = g_map[weights]*alpha

def update_histogram(weights):
    if weights in histogram:
        histogram[weights] += 1
    else:
        histogram[weights] = 1

def wang_landau(alpha, epsilon):
    x_i = cost_function(np.rand()) # a random initial configuration
    currentEnergy = cost_function(x_i)
    
    while (alpha - 1 > epsilon):
        x_propose = np.random()  
        proposedEnergy = cost_function(x_propose) # the energy of the proposed configuration computed
       
        p_i = 1/(g_function(currentEnergy)*1.0)
        p_propose = 1/(g_function(proposedEnergy)*1.0)
        p = min(1, p_propose/p_i)
        
        indicator = np.random.binomial(1, p)
        if indicator == 1:
            x_i = x_propose
            currentEnergy = proposedEnergy
        
        update_histogram(x_i)
        update_g_function(x_i, alpha)
        