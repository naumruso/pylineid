import numpy as np
import matplotlib.pyplot as plt

import pylineid


get_line_flux = lambda newx, x, y: np.interp(newx, x, y)

wave = 1240 + np.arange(300) * 0.1
flux = np.random.normal(size=300)

cwaves = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
fluxes = get_line_flux(cwaves, wave, flux)
bars = np.random.rand(fluxes.size) #This shows the relative strength of each line
labels = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
labels = [str("%s %9.3f" %(label,cwave)) for cwave, label in zip(cwaves, labels)]

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

ax.plot(wave, flux)
ax.set_xlim(wave[0],wave[-1])
ax.set_ylim(-4,7)
fig.show()
fig.tight_layout()


ypos2 = 3.3
ypos3 = 4.4
lines_plot = pylineid.put_lines(ax, cwaves, fluxes, ypos2, ypos3, labels, bars=bars)

fig.savefig('pylineid_example.pdf')