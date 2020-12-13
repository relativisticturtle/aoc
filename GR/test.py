import numpy as np
from matplotlib import pyplot as plt




# --- Hyperbolic equation ---
#
#   x**2 / a**2  -  y**2 / b**2  =  1
#
#  - for x = 0, no solution
#  - for y = 0, x = +/- a (vertices)
#
#  - focii at (y = 0, x = +/- f)
#    - f
#   


plt.figure()

a = 0.8    # distance diff
c = 1      # focii separation
b = np.sqrt(c**2 - a**2)
V = np.array([[-a, 0], [a, 0]])
F = np.array([[-c, 0], [c, 0]])

yp = 0
xp = a*np.sqrt(1 + yp**2/b**2)


d1 = np.linalg.norm(np.array([xp, yp]) - F[0, :])
d2 = np.linalg.norm(np.array([xp, yp]) - F[1, :])
print('%.4f - %.4f = %.4f' % (d1, d2, d1 - d2))


y = np.linspace(-2, 2)
x = b*np.sqrt(1 + y**2/a**2)

plt.plot(x, y,
    V[:, 0], V[:, 1], 'k.',
    F[:, 0], F[:, 1], 'kx',
    [F[0, 0], xp, F[1, 0]], [F[0, 1], yp, F[1, 1]], 'r.-'
)
plt.show()


