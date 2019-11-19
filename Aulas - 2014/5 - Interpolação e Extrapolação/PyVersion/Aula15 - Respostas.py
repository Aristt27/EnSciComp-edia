# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Plano de hoje
# -------------
# 
# 1. Ambiente de programação
# 2. Usando o computador para calcular    
# 3. Usando o computador para desenhar
# 4. Usando o computador para integrar: quadraturas
# 5. Usando o computador para aproximar: interpolação
#     1. Interpolação local
#     2. Interpolação de Lagrange
#     3. Fenômeno de Runge e pontos de Chebyshev
#     4. Transformada de Fourier
#     5. Splines

# <codecell>

%pylab inline
from scipy.interpolate import interp1d

# <codecell>

xs = linspace(0,10,10)
ys = cos(xs**2/8)
f = interp1d(xs,ys)
fc = interp1d(xs,ys, kind='cubic')

# <codecell>

ts = linspace(0,10,200)
plot(xs,ys,'o')
plot(ts, f(ts), label='default')
plot(ts, fc(ts), label='cubic');

# <codecell>


