from scipy import *
#from scipy import weave
import sys
from pylab import *

Nitt=10000000   # Total number of Monte Carlo steps
N=10            # Linear size of 2D Ising model, lattice = N x N
flatness = 0.9  # The condition to reset the Histogarm when
                # min(Histogram) > average(Histogram)*flattness

N2=N*N          # Total number of lattice sites

def RandomL(N):
    "Generates a random 2D Ising lattice"
# Randomly choosen <--> infinite temperature
    latt = zeros((N,N),dtype=int)
    for i in range(N):
        for j in range(N):
            latt[i,j] = sign(2*rand()-1)
    return latt

def CEnergy(latt):
    "Energy of a 2D Ising lattice"
    Ene = 0
    for i in range(N):
        for j in range(N):
            S = latt[i,j]
            WF = latt[(i+1)%N, j] + latt[i,(j+1)%N] + latt[(i-1)%N,j] + latt[i,(j-1)%N]
            Ene += -WF*S # Each neighbor gives energy 1.0
    return int(Ene/2.)   # Each par counted twice

def Thermod(T, lngE, Energies, E0):
    "Thermodynamics using density of states"
    Z=0
    Ev=0
    E2v=0
    for i,E in enumerate(Energies):
        w = exp(lngE[i]-lngE[0] - (E+E0)/T)
        Z   += w
        Ev  += w * E
        E2v += w * E**2
    Ev *= 1./Z
    cv = (E2v/Z - Ev**2)/T**2
    return (Ev/N2, cv/N2)



def SamplePython(Nitt, N, N2, indE, E0, flatness):
    "Wang Landau algorithm in Python"
    # Ising lattice at infinite temperature
    latt = RandomL(N)
    # Corresponding energy
    Ene = CEnergy(latt)
    # Logarithm of the density of states log(g(E))
    lngE = zeros(len(Energies), dtype=float)
    # Histogram
    Hist = zeros(len(Energies), dtype=float)  
    
    # modification factor which modifies g(E)
    # according to the formula g(E) -> g(E)*f,
    # or equivalently, lngE[i] -> lngE[i] + lnf
    lnf = 1.0
    
    for itt in range(Nitt):
        ii = int(rand()*N2)       # The site to flip
        (i,j) = (int(ii % N), int(ii / N))  # The coordinates of the site
        S = latt[i,j]             # its spin
        WF = latt[(i+1)%N, j] + latt[i,(j+1)%N] + latt[(i-1)%N,j] + latt[i,(j-1)%N]
        Enew = Ene + 2*S*WF       # The energy of the tryed step
        P = exp(lngE[indE[Ene+E0]]-lngE[indE[Enew+E0]])  # Probability to accept according to Wang-Landau
        if P > rand():            # Metropolis condition
            latt[i,j] = -S        # step is accepted, update lattice
            Ene = Enew            #    and energy
            
        Hist[indE[Ene+E0]] += 1.  # Histogram is update at each Monte Carlo step!
        lngE[indE[Ene+E0]] += lnf # Density of states is also modified at each step!
        if itt % 100 == 0:
            aH = sum(Hist)/(N2+0.0) # mean Histogram
            mH = min(Hist)          # minimum of the Histogram
            if mH > aH*flatness:    # Is the histogram flat enough?
                Hist = zeros(len(Hist)) # Resetting histogram
                lnf /= 2.               # and reducing the modification factor
                print(itt, 'histogram is flatt', mH, aH, 'f=', exp(lnf))
    return (lngE, Hist)

if __name__ == '__main__':

    # Possible energies of the Ising model
    Energies = (4*arange(N2+1)-2*N2).tolist()
    Energies.pop(1)   # Note that energies Emin+4 and Emax-4 
    Energies.pop(-2)  # are not possible, hence removing them!
    
    # Maximum energy
    E0 = Energies[-1]                         
    # Index array which will give us position in the Histogram array from knowing the Energy
    indE = -ones(E0*2+1, dtype=int)           
    for i,E in enumerate(Energies): indE[E+E0]=i
    
    (lngE, Hist) = SamplePython(Nitt, N, N2, indE, E0, flatness)

    
    # Normalize the density of states, knowing that the lowest energy state is double degenerate
    # lgC = log( (exp(lngE[0])+exp(lngE[-1]))/4. )
    if lngE[-1]<lngE[0]:
        lgC = lngE[0] + log(1+ exp(lngE[-1]-lngE[0])) - log(4.)
    else:
        lgC = lngE[-1] + log(1+ exp(lngE[0]-lngE[-1])) - log(4.)
    lngE -= lgC
    for i in range(len(lngE)):
        if lngE[i]<0: lngE[i]=0
    # Normalize the histogram
    Hist *= len(Hist)/float(sum(Hist))
    
    
    plot(Energies, lngE, '-o', label='log(g(E))')
    plot(Energies, Hist, '-s', label='Histogram')
    xlabel('Energy')
    legend(loc='best')
    show()
    
    
    Te = linspace(0.5,4.,300)
    Thm=[]
    for T in Te:
        Thm.append(Thermod(T, lngE, Energies, E0))
    Thm = array(Thm)
    
    plot(Te,Thm[:,0], label='E(T)')
    plot(Te,Thm[:,1], label='cv(T)')
    xlabel('T')
    legend(loc='best')
    show()