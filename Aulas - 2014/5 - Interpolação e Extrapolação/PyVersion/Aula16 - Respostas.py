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
#     6. **Extrapolação e mínimos quadrados**

# <codecell>

%pylab inline

# <markdowncell>

# # Excesso de dados
# 
# Já vimos que usar pontos demais para interpolar pode trazer problemas:
# ao usar um polinômio de grau muito grande, este pode oscilar demasiadamente;
# ao considerar muitos dados com um pouco de erro, este pode ser magnificado pela interpolação.
# 
# Entretanto, possuir mais informação deveria nos dar **mais** entendimento sobre o nosso problema, não?
# Vamos, aqui, tentar entender como aproveitar estes dados suplementares.

# <codecell>

def f(x):
    return 1/(1 + x**2)

# <codecell>

xs = linspace(-5,5,30)
ys = f(xs)

# <markdowncell>

# # Mínimos quadrados
# 
# Em vez de buscarmos um polinômio de grau 29 que aproxime os 30 pontos acima,
# vamos tentar algo novo:
# gostaríamos de encontrar um polinômio de grau baixo que represente de forma aceitável esta função.
# Por exemplo, suponhamos $P$ de grau 6.
# 
# O sistema linear que obteremos ao escrever as 30 equações $P(x_k) = y_k$ será,
# muito provavelmente, impossível.
# Temos 30 equações e apenas 7 variáveis para os coeficientes de $P$.
# Entretanto, podemos tentar encontrar coeficientes que sejam os "melhores possível"
# segundo algum critério.
# Um critério bastante comum e prático (ou seja, rápido para o computador executar)
# é o de mínimos quadrados:
# $$ \text{tomaremos $c$ tal que } \left\| Ac - y \right\| \text{ seja o menor possível.} $$

# <markdowncell>

# O código é bastante similar ao da interpolação de Lagrange usando a matriz de Vandermonde,
# exceto que agora também devemos dar o grau desejado da interpolação:

# <codecell>

def polyfit_minsq(x,y,n):
    """ Calcula o polinômio de grau até  n  que melhor aproxima os pontos $(x_i, y_i)$. """
    assert(len(x) == len(y))
    maxx = max(x)
    minx = min(x)
    medx = (maxx + minx)/2
    diffs = array(x) - medx
    M = [ones_like(x)]
    for i in range(n):
        M.append(M[-1]*diffs)
    M = array(M).T
    a,_,_,_ = lstsq(M,y)

    def p(z):
        return Horner(z - medx,a[::-1])
    return p

# <codecell>

def Horner(x, rcoeff):
    # Inicialização
    acc = rcoeff[0]
    for c in rcoeff[1:]:
        acc *= x
        acc += c
    return acc

# <codecell>

ts = linspace(-5,5,300)

# <codecell>

f_interp = polyfit_minsq(xs, ys, 8)
plot(ts, f(ts), label='f')
plot(ts, f_interp(ts), label='interp')
legend();

# <markdowncell>

# Veja que, se usássemos polinômios de grau alto demais, obteríamos erros muito maiores:

# <codecell>

figure(figsize=(15,5))
f_interp13 = polyfit_minsq(xs, ys, 13)
f_interp18 = polyfit_minsq(xs, ys, 18)
f_interp23 = polyfit_minsq(xs, ys, 23)
f_interp28 = polyfit_minsq(xs, ys, 28)
subplot(1,2,1)
plot(ts, f(ts), label='f')
plot(ts, f_interp13(ts), label='interp 13')
plot(ts, f_interp18(ts), label='interp 18')
legend();

subplot(1,2,2)
plot(ts, f(ts), label='f')
plot(ts, f_interp23(ts), label='interp 23')
plot(ts, f_interp28(ts), label='interp 28')
legend();

# <markdowncell>

# ## Erros nos dados
# 
# E o que acontece se tivermos erros nos dados?
# Suponhamos que os nossos dados sejam $y_k = f(x_k) + e(x_k)$,
# onde $e$ é um pequeno erro.
# Se tivermos "muita informação",
# talvez sejamos capazes de "eliminar o erro".
# 
# Vejamos um primeiro exemplo, apenas para ilustrar:

# <codecell>

def f(x):
    return x
def e(x):
    return sin(x**2 - 4*x)/100

# <codecell>

import metodos

# <codecell>

xs = linspace(-4,4,30)
ys = f(xs) + e(xs)
ts = linspace(-4,4,300)

p_i_l = metodos.lagrange(xs, ys)
f_int = polyfit_minsq(xs, ys, 1)

plot(ts, p_i_l(ts) - f(ts), label='lagrange')
plot(ts, f_int(ts) - f(ts), label='grau 1')
ylim([-.1,.1])
legend();

# <codecell>

xs = metodos.chebyshev_nodes(-4,4,20)
ys = f(xs) + e(xs)
ts = linspace(-4,4,300)

p_i_l = metodos.lagrange(xs, ys)
f_int = polyfit_minsq(xs, ys, 1)

plot(ts, p_i_l(ts) - f(ts), label='lagrange')
plot(ts, f_int(ts) - f(ts), label='grau 1')
legend();

# <markdowncell>

# Vejamos, agora, um exemplo mais sério.

# <codecell>

def f(x):
    return 1/(1 + x**2)
def e(x):
    return random.normal(size=shape(x))/20

# <codecell>

xs = metodos.chebyshev_nodes(-3,3,50)
ys = f(xs) + e(xs)

f_lagr = metodos.lagrange(xs, ys)
f_minsq = polyfit_minsq(xs, ys, 12)

ts = linspace(-3,3,500)
figure(figsize=(15,5))
subplot(1,2,1)
plot(ts, f(ts), label='original')
plot(ts, f_lagr(ts), label='lagrange')
plot(ts, f_minsq(ts), label='Minsq')
legend();

subplot(1,2,2)
plot(ts, f_lagr(ts) - f(ts), label='lagrange')
plot(ts, f_minsq(ts) - f(ts), label='Minsq')
legend();

# <codecell>


