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

# <codecell>

%pylab inline

# <markdowncell>

# # Fenômeno de Runge
# 
# Vimos na aula passada que os polinômios especiais -
# os $\phi_i(x)$ que se anulam em todos os pontos de interpolação exceto um deles -
# são oscilatórios, e isso causa erros de aproximação.
# Veremos aqui um exemplo onde estes erros ficam cada vez maiores conforme
# o número de pontos de interpolação aumenta!

# <codecell>

def f(x): return 1/(1 + x**2)

# <codecell>

def lagrange(x,y):
    """ Calcula o polinômio interpolador de Lagrange dos pontos $(x_i, y_i)$,
        resolvendo a matriz de Vandermonde correspondente. """
    assert(len(x) == len(y))
    n = len(x) - 1
    maxx = max(x)
    minx = min(x)
    medx = (maxx + minx)/2
    diffs = array(x) - medx
    M = [ones_like(x)]
    for i in range(n):
        M.append(M[-1]*diffs)
    M = array(M).T
    a = solve(M,y)
    
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

# <markdowncell>

# ### Exercício:
# 
# Interpole $f(x) = \frac{1}{1 + x^2}$, usando 5, 10 e 15 pontos igualmente espaçados,
# nos três intervalos $[-1,1]$, $[-5,5]$, $[1,5]$.
# 
# Veja se o erro aumenta ou diminui conforme usamos mais pontos para interpolar.

# <codecell>

def varios_lagrange(f,a,b,ns):
    maxn = max(ns)
    ts = linspace(a,b,30*maxn)
    figure(figsize=(18,5))

    for n in ns:
        xs = linspace(a,b,n)
        ys = f(xs)
        p_i_l = lagrange(xs,ys)
        subplot(1,3,1)
        plot(ts, p_i_l(ts), label='ordem {}'.format(n))
        subplot(1,3,2)
        plot(ts, p_i_l(ts) - f(ts), label='ordem {}'.format(n))
        subplot(1,3,3)
        semilogy(ts, abs(p_i_l(ts) - f(ts)), label='ordem {}'.format(n))

    subplot(1,3,1)
    plot(ts, f(ts))

    for i in range(1,4):
        subplot(1,3,i)
        legend(loc=0);

# <codecell>

varios_lagrange(f,-1,1,[5,10,15])

# <codecell>

varios_lagrange(f,-5,5,[5,10,15])

# <markdowncell>

# Veja que este erro "nos cantos" não é tão grande se o intervalo for _apenas_ $[1,5]$:

# <codecell>

varios_lagrange(f,1,5,[5,10,15])

# <markdowncell>

# ## Análise
# 
# Se $f$ é uma função com $n+1$ derivadas,
# podemos estimar o erro cometido pelo polinômio interpolador de grau $n$ através da fórmula:
# $$ P_n(x) - f(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \prod_{i = 0}^n (x - x_i) $$
# onde, como de hábito, $\xi$ é um ponto do intervalo $[a,b]$ que depende de $x$.
# 
# Se quisermos estimar o erro, precisamos entender o comportamento de duas componentes:
# 
# - a $(n+1)$-ésima derivada de $f$
# - o fator $\omega_n(x) = \prod_{i = 0}^n (x - x_i)$, conhecido como *polinômio nodal*.
# 
# Comecemos por $\omega$.

# <markdowncell>

# ### Exercício:
# 
# Calcule os polinômios nodais para 5 e 15 nós no intervalo $[-5,5]$, e compare suas magnitudes.

# <codecell>

def nodal(x):
    def f(z):
        return prod([z - xi for xi in x], 0)
    return f

# <codecell>

p5 = nodal(linspace(-5,5,5))
p15 = nodal(linspace(-5,5,15))
t = linspace(-5,5,200)
figure(figsize=(15,5))
subplot(1,2,1)
plot(t, p5(t), label='5 nós')
plot(t, p15(t), label='15 nós')
legend()
subplot(1,2,2)
semilogy(t, abs(p5(t)), label='5 nós')
semilogy(t, abs(p15(t)), label='15 nós')
legend();

# <markdowncell>

# ### Exercício
# 
# Mostre que, se dividirmos o intervalo $[0,1]$ em $n$ partes iguais, e se $x \in (0,1)$, então
# $$ \omega_n(x) \leq \frac{n!}{4 n^{n+1}}. $$
# 
# Dica: Vimos experimentalmente que os máximos estão perto dos extremos, então comece supondo que $x \in (0, 1/n)$.
# 
# Deduza o que acontece num intervalo $[a,b]$ qualquer.

# <markdowncell>

# ## Limitando
# 
# Assim, vemos que o erro de aproximação usando interpolação de Lagrange com pontos igualmente espaçados será, no máximo:
# $$ \frac{f^{(n+1)}(\xi)}{(n+1)!} \frac{n!}{4 n^{n+1}} = \frac{f^{(n+1)}(\xi)}{n+1} \frac{1}{4 n^{n+1}}. $$
# Portanto, conforme $n$ cresce, temos que compensar a derivada $(n+1)$-ésima
# com um fator que é cada vez "melhor" $n^{n+1}$ no denominador.
# Infelizmente, para algumas funções, a derivada cresce bem mais rápido do que este fator,
# e isso causa os erros que vimos.

# <markdowncell>

# # Estabilidade
# 
# Uma característica bastante desejável de métodos de interpolação é que estes sejam robustos.
# Por exemplo, imagine que estamos usando interpolação para analisar o comportamento de uma função
# a partir de dados experimentais.
# É claro que estes dados contém erros, e portanto nossa interpolação, também.
# Porém, seria extremamente nocivo se os erros da interpolação fossem _muito_ maiores do que os erros iniciais:
# o método seria praticamente inútil!
# 
# Diremos que um método (algoritmo) é _estável_ quando os erros de saída sejam comparáveis aos dos dados fornecidos.

# <markdowncell>

# ### Exercício
# 
# Analise a robustez dos métodos de derivada discreta em função de $h$.

# <markdowncell>

# ## Análise de estabilidade
# 
# Se temos uma função $f$ que produz os valores $y_i$ dados os pontos $x_i$,
# e que há erros de medição e usamos valores perturbados $z_i = (y_i + \varepsilon_i)$,
# a diferença entre os polinômios interpoladores $P$ (correto) e $Q$ (com erros) será:
# $$ P(x) - Q(x) = \sum_{i = 0}^n y_i \phi_i(x) - \sum_{i = 0}^n z_i \phi_i(x)
#   = \sum_{i = 0}^n \varepsilon_i \phi_i(x).$$
# Tomando valores absolutos e usando a desigualdade triangular:
# $$ \lvert P(x) - Q(x) \rvert \leq \big(\max_i |\varepsilon_i|\big) \sum_{i = 0}^n \lvert \phi_i(x) \rvert.$$
# 
# Assim, o "fator de distorção" será, no máximo,
# $$\sum_{i = 0}^n \lvert \phi_i(x) \rvert,$$
# que só depende dos pontos $x_i$ usados para interpolação.

# <codecell>

def phi(xi, xjs):
    def f(z):
        return prod([(z - xj)/(xi - xj) for xj in xjs],0)
    return f
def lagrange_basis(x):
    xs = set(x)
    P =[]
    for xi in x:
        xjs = xs - {xi}
        P.append(phi(xi, xjs))
    return P

# <codecell>

x = linspace(0,1,10)
Pis = lagrange_basis(x)

# <codecell>

t = linspace(0,1,200)
plot(t, sum([abs(P(t)) for P in Pis],0))
plot(x, zeros_like(x), 'o')

# <markdowncell>

# Assim, tomando $n$ pontos igualmente espaçados, temos infelizmente que o fator de distorção será algo como
# $$ \frac{2^n}{n} $$
# que tende para infinito quando $n$ aumenta.
# Assim, não adianta usar mais pontos para garantir um menor erro.

# <markdowncell>

# # Polinômios de Chebyshev
# 
# Mas, a priori, nada nos obriga a usar pontos equiespaçados para calcular a função.
# Dependendo de como os dados $y_i$ serão obtidos, talvez seja possível usar outros pontos $x_i$,
# que produzam um polinômio nodal "menor".
# Assim, gostaríamos de resolver o seguinte problema:
# 
# Achar pontos $x_0$, $x_1$, $\ldots$, $x_n$ no intervalo $[-1,1]$ de forma a minimizar o polinômio nodal
# $$ \prod_{i = 0}^{n+1} (x - x_i). $$

# <markdowncell>

# ### Exercício:
# 
# Resolva o caso $n = 1$.

# <markdowncell>

# Queremos minimizar (em $a$ e $b$) o máximo do valor absoluto de $(x-a)(x-b)$ onde $x$ percorre o intervalo $[-1,1]$.
# Fixos $a$ e $b$, há três candidatos para o máximo: $x = -1$, $x = 1$, $x = (a+b)/2$.
# O valor nestes três pontos é
# - $(a+1)(b+1)$
# - $(1-a)(1-b)$
# - $(b-a)^2/4$

# <codecell>

def nodalmax(a,b):
    return max((a+1)*(b+1), (1-a)*(1-b), (b-a)**2/4,0)

a = linspace(-1,1,100)
b = linspace(-1,1,100)

matshow([[nodalmax(x,y) for x in a] for y in b])
colorbar();

# <codecell>

plot(a, [nodalmax(x,-x) for x in a]);

# <markdowncell>

# ## Caso geral: funções trigonométricas!
# 
# É possível mostrar que o caso geral tem uma solução bastante simples:
# basta escolher os pontos $x_i = \cos\left(\pi\frac{2i + 1}{2(n+1)}\right)$ 

# <codecell>

n = 8
ang = pi*arange(1,2*n+3,2)/(2*(n+1))
x = cos(ang)
P = nodal(x)

t = linspace(-1,1,200)
plot(t, P(t));

# <markdowncell>

# Note que os pontos estão mais espaçados no meio do que nos cantos:
# assim, diminuímos o produto $\omega$ para os pontos nesta região,
# e aumentamos no resto, mas de forma equilibrada.

# <markdowncell>

# Existe também uma outra solução, que inclui os extremos do intervalo como pontos de interpolação,
# o é bastante razoável.
# Neste caso, os pontos serão
# $x_i = \cos\left( \pi \frac{i}{n} \right)$ para $i = 0, \ldots, n$.

# <codecell>

ang = pi*arange(0,n+1)/n
x = cos(ang)
P = nodal(x)

t = linspace(-1,1,200)
plot(t, P(t))

# <markdowncell>

# Observe que o máximo do polinômio nodal incluindo os extremos é maior do que o anterior:
# isso é esperado, já que o polinômio de Chebyshev é o que minimiza a amplitude do polinômio nodal.

# <markdowncell>

# Ainda assim, temos que o polinômio nodal tende a zero bastante rápido quando $n$ aumenta,
# o que garante a convergência da interpolação usando estes nós:

# <markdowncell>

# ### Exercício
# 
# Interpole, de novo, $f(x) = \frac{1}{1 + x^2}$, mas agora usando os pontos de Chebyshev.
# Observe como o erro evolui conforme usamos mais pontos para interpolar.

# <codecell>

def chebyshev_nodes(a,b,n):
    """ Calcula os (n+1) pontos de Chebyshev para interpolação de ordem n """
    ang = pi*arange(1,2*n+3,2)/(2*(n+1))
    x = (a+b)/2 + (b-a)*cos(ang)/2
    return x

# <codecell>

def varios_chebyshev(f,a,b,ns):
    maxn = max(ns)
    ts = linspace(a,b,30*maxn)
    figure(figsize=(18,5))

    for n in ns:
        xs = chebyshev_nodes(a,b,n)
        ys = f(xs)
        p_i_l = lagrange(xs,ys)
        subplot(1,3,1)
        plot(ts, p_i_l(ts), label='ordem {}'.format(n))
        subplot(1,3,2)
        plot(ts, p_i_l(ts) - f(ts), label='ordem {}'.format(n))
        subplot(1,3,3)
        semilogy(ts, abs(p_i_l(ts) - f(ts)), label='ordem {}'.format(n))

    subplot(1,3,1)
    plot(ts, f(ts), label='original')

    for i in range(3):
        subplot(1,3,i+1)
        legend(loc=0);

# <codecell>

varios_chebyshev(f,-1,1,[5,10,15])

# <codecell>

varios_chebyshev(f,-5,5,[5,10,15])

# <codecell>

varios_chebyshev(f,1,5,[5,10,15])

# <markdowncell>

# # Erros numéricos
# 
# Enfim, um outro problema que podemos ter que enfrentar é a perda de precisão numérica,
# seja ao resolver um sistema linear,
# seja ao calcular a função polinomial resultante.
# Vejamos uma nova expressão para o polinômio interpolador de Lagrange,
# que será menos sensível a este tipo de erros: a fórmula baricêntrica.

# <markdowncell>

# Já notamos que o polinômio interpolador $P$ é dado de forma explícita por
# $$ P(x) = \sum_{i=0}^n f(x_i) \phi_i(x) $$
# onde os $\phi_i(x)$ são os polinômios especiais de interpolação.
# Vamos expandir:
# $$\begin{align*}
# P(x) & = \sum_{i=0}^n f(x_i) \phi_i(x) = \sum_{i=0}^n f(x_i) \prod_{j \neq i} \frac{x - x_j}{x_i - x_j} \\
#      & = \sum_{i=0}^n f(x_i) \prod_{j \neq i} (x - x_j) \prod_{j \neq i} \frac{1}{x_i - x_j} \\
#      & \text{como o último fator não depende de $x$, vamos denotá-lo por $w_i$:} \\
#      & = \sum_{i=0}^n f(x_i) w_i \prod_{j \neq i} (x - x_j) \\
#      & \text{suponhamos que não vamos querer calcular em $x_i$ - já que sabemos que deve dar $f(x_i)$ de antemão!} \\
#      & = \sum_{i=0}^n \frac{f(x_i) w_i}{x - x_i} \prod_{j} (x - x_j) = \sum_{i=0}^n \frac{f(x_i) w_i}{x - x_i} \omega(x)\\
#      & \text{e agora o último fator não depende de $i$, podemos fatorá-lo:} \\
#      & = \omega(x) \sum_{i=0}^n \frac{f(x_i) w_i}{x - x_i} \\
# \end{align*}$$

# <markdowncell>

# Agora, um truque: o que acontece se estivéssemos tentando interpolar a função $f(x) = 1$?
# Neste caso, teríamos que o polinômio interpolador seria também a função constante igual a um,
# e assim:
# $$ 1 = \omega(x) \sum_{i = 0}^n \frac{w_i}{x - x_i} $$.

# <markdowncell>

# Com isso, podemos eliminar o $\omega(x)$ da fórmula acima, e ficamos com
# $$ P(x) = \frac{\displaystyle \sum_{i=0}^n \frac{f(x_i) w_i}{x - x_i} }{ \displaystyle \sum_{i=0}^n \frac{w_i}{x - x_i} }. $$
# Esta fórmula é conhecida como **forma baricêntrica**,
# porque os $w_i$ funcionam como "pesos" para os termos $\frac{1}{x - x_i}$,
# e para interpolar $f$, vamos "corrigir" os pesos da função constante para usar os que são dados pela $f$.

# <codecell>

def baricentrica(x,y):
    """ Calcula o polinômio interpolador de Lagrange nos pontos $(x_i, y_i)$ usando a forma baricêntrica. """
    w   = [1/(prod([xi - xj for xj in x if xj != xi])) for xi in x]
    def P(z):
        num = 0
        den = 0
        for i in range(len(x)):
            t = w[i]/(z - x[i])
            den += t
            num += t * y[i]
        return num/den
    return P

# <codecell>

y = f(x)
P = baricentrica(x,y)

# <codecell>

ts = linspace(-1,1,100)
plot(ts,P(ts), label='interpolador');
plot(ts,f(ts), label='original');
legend(loc=0);

# <markdowncell>

# ### Exercício
# 
# Enfim, use os pontos de Chebyshev e a fórmula baricêntrica para interpolar $f$.
# Agora, tente usar **muitos** pontos de interpolação, e veja como o erro evolui.

# <codecell>

def varios_chebyshev_bar(f,a,b,ns):
    maxn = max(ns)
    ts = linspace(a,b,30*maxn)
    figure(figsize=(18,5))

    for n in ns:
        xs = chebyshev_nodes(a,b,n)
        ys = f(xs)
        p_i_l = baricentrica(xs,ys)
        subplot(1,3,1)
        plot(ts, p_i_l(ts), label='ordem {}'.format(n))
        subplot(1,3,2)
        plot(ts, p_i_l(ts) - f(ts), label='ordem {}'.format(n))
        subplot(1,3,3)
        semilogy(ts, abs(p_i_l(ts) - f(ts)), label='ordem {}'.format(n))

    subplot(1,3,1)
    plot(ts, f(ts), label='original')

    for i in range(3):
        subplot(1,3,i+1)
        legend(loc=0);

# <codecell>

varios_chebyshev_bar(f,-5,5,[5,10,15])

# <codecell>

varios_chebyshev_bar(f,-5,5,[25,50,75,100,125])

# <codecell>

varios_chebyshev(f,-5,5,[25,50,75,100,125])

