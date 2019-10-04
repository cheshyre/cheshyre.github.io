import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec

matplotlib.rc('font',**{'family':'serif','serif':['Palatino'],'size':16})

# matplotlib font configurations
matplotlib.rcParams["text.latex.preamble"] = [
    # i need upright \micro symbols, but you need...
    r"\usepackage{siunitx}",
    # ...this to force siunitx to actually use your fonts
    r"\sisetup{detect-all}",
    # set the normal font here
    r"\usepackage{lmodern}",
    # load up the sansmath so that math -> helvet
    #  r"\usepackage{sansmath}",
    # <- tricky! -- gotta actually tell tex to use!
    #  r"\sansmath",
]

# Use tex for matplotlib
plt.rc("text", usetex=True)

def create_trans_matrix(n):
    matrix = np.zeros((n, n))
    for i in range(n - 1):
        j = i + 1
        matrix[i][j] = 0.5
        matrix[j][i] = 0.5
    return matrix


b = 30
size = 2 * b - 1

ones_vector = np.array([1] * size)

trans = create_trans_matrix(size)

ident = np.identity(size)

g = np.dot(np.linalg.inv(ident - trans), ones_vector)

t0 = ones_vector - np.dot(trans, ones_vector)

tau = np.array([0.0]*size)
tau[b] = 1.0

#  print(g)
#  print(t0)

n_vals = np.array(list(range(1, 8 * b**2, 2)))
vals = []
for n in n_vals:
    vals.append(np.dot(t0, np.dot(np.linalg.matrix_power(trans, n - 1), tau)))

print(sum(vals))
plt.plot(n_vals + 1, vals)
plt.xlabel(r"Number of steps $N$")
plt.ylabel("Probability")
plt.title(r"Probability to reach boundary after $N$ steps")
plt.gcf().subplots_adjust(left=0.20)
plt.gcf().subplots_adjust(right=0.95)
plt.gcf().set_size_inches(6.0, 6.0)
plt.savefig("src/assets/images/post/2019-bounded-random-walk/distribution.svg")
#  plt.show()
