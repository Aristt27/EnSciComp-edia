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
#     5. **Splines**

# <markdowncell>

# # Splines: aproximação suave por partes

# <markdowncell>

# Um spline é uma função que interpola (exatamente) dados $(x_k, y_k)$,
# com o objetivo de obter uma função que seja **duas** vezes derivável no intervalo de interpolação.

# <markdowncell>

# ### Exercício
# 
# Tente desenhar uma função que seja apenas duas vezes derivável, ou seja,
# para a qual exista (pelo menos) um ponto onde não há a terceira derivada.

# <markdowncell>

# ## Variáveis e restrições
# 
# Se queremos obter uma interpolação $f$ que seja duas vezes derivável,
# temos vários tipos de condições impostas a priori sobre a interpolação:
# 
# 0. as condições de ordem zero, ou seja, $f(x_k) = y_k$;
# 1. as condições de "colagem" de ordem um, ou seja, que $f' _ + (x_k) = f' _ - (x_k)$;
# 2. as condições de "colagem" de ordem dois, ou seja, que $f'' _ + (x_k) = f'' _ - (x_k)$.
# 
# Se tivermos $n+2$ pontos (dois extremos e $n$ internos), isso nos dá ao todo $3n + 2$ condições.
# Assim, precisamos de, pelo menos, $3n+2$ variáveis para interpolar.

# <markdowncell>

# ### Exercício
# 
# Se tivermos um polinômio de grau $d$ em cada intervalo $(x_k, x _ {k+1})$,
# qual será o número de variáveis livres de que dispomos?
# 
# Ao tomar um polinômio de grau $d$ em cada intervalo, as condições de ordem zero aparecem **duas** vezes em cada um deles.
# Quantas restrições temos?

# <markdowncell>

# ## Scipy

# <codecell>

%pylab inline

# <codecell>

from scipy.interpolate import interp1d

# <codecell>

def f(x):
    return sin(x) + cos(400*x)/1000

# <codecell>

x = rand(10)*7 + 1
x = array([0] + sorted(x) + [9])
y = f(x)
f2 = interp1d(x, y, kind='cubic', assume_sorted=True)

# <codecell>

t = arange(0,9,0.01)
figsize(15,5)
subplot(1,2,1)
plot(t, f(t), label='original')
plot(t, f2(t), label='interpolada')
legend(loc=0)
plot(x, y, 'x');

subplot(1,2,2)
plot(t, f2(t) - f(t));

