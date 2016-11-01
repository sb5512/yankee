from random import randint
import numpy as np
import matplotlib.pyplot as plt

#10 random number between 0 to 90
x = [randint(1,89) for p in range (0,10)]
print(x)

#performing sine and cosine on above generated random numbers
print(np.cos(x))
print(np.sin(x))

#storing values of sine and cosine value on variable SIN and COSIN 
SIN = np.sin(x)
COSIN = np.cos(x)

#plotting value of SIN and COSIN in two different colors
x = [randint(0,90) for p in range (0,10)]
SIN = np.sin(x)
COSIN = np.cos(x)

plt.plot(SIN, color = "red", label = 'Sine')
plt.plot(COSIN, color = "black", label = 'Cosine')
plt.xlabel("Random number Index")
plt.ylabel("Values")
plt.legend(loc=(0,-0.4), ncol = 2)
plt.show()