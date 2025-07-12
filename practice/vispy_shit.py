import vispy.plot as vp
import threading
import time
import numpy as np

def sine_wave_generator():
    t = 0
    while True:
        yield [(x, np.sin(x-t)) for x in np.linspace(0, 2*np.pi, 100)]
        t += 2*np.pi / 200


fig = vp.Fig(size=(800, 400), show=False)
fig.title = "Live Plot"

curve = [(x, x**2) for x in range(20)]

plotwidget = fig[0, 0]
# plotwidget.plot(curve, title="ää")
plotwidget.colorbar(position="top", cmap="autumn")


sine_gen = sine_wave_generator()
sine_plot =plotwidget.plot(next(sine_gen), title="sine!!")

while True:
    sine_plot.set_data(next(sine_gen))
    fig.show(run=True)
    time.sleep(0.2)