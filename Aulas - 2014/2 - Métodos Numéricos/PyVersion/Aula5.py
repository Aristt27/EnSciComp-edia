# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Plano de hoje
# -------------
# 
# 1. Ambiente de programação
# 2. Usando o computador para calcular    
#     1. Indução e algoritmos recursivos
#     1. Aproximações sucessivas: bisseção, Newton
#     1. **Extra:**
#         1. **Critérios de parada**
#         1. **Newton-Horner (deflação de polinômios)**
#         1. **Schleicher et al.: todas as raízes de uma vez só**

# <markdowncell>

# # Implementando o método de Newton
# 
# Vamos escrever uma implementação do método de Newton com diversos critérios de parada:
# 
# 1. Distância entre as estimativas sucessivas
# 1. Valor da função
# 1. Número máximo de iterações
# 
# Vamos aproveitar para introduzir argumentos opcionais em Python.

# <codecell>

%pylab inline

# <codecell>

def newton(f, df, x0, tolx=1e-10, toly=0, maxiter=100):
    x = x0
    niter = 0
    while True:
        xnew = x - f(x)/df(x)
        niter += 1
        if abs(xnew - x) < tolx: break
        if abs(f(xnew)) < toly: break
        if niter > maxiter: return None
        x = xnew
    
    return xnew, niter

# <codecell>

newton(sin, cos, 2.)

# <markdowncell>

# ## Observações
# 
# Existem algumas considerações a serem feitas sobre os critérios de parada.
# Seja $z$ a raiz para a qual converge o método, quando feitas infinitas iterações.
# 
# 1. Se $\lvert f'(z)\rvert << 1$, a parada em `toly` pode ocorrer muito longe da verdadeira raiz.
# 1. Se, ao contrário, $\lvert f'(z)\rvert >> 1$, a parada em `toly` só ocorrerá muito perto da raiz. (Obs Quarteroni)
# 1. Como a cada etapa calculamos $f'(x)$, poderíamos usar esta informação para "corrigir" o critério.
# 1. Por esta razão, deixamos o valor default de `toly` em zero.
# 1. Enfim, se $z$ é uma raiz múltipla de $f$, o critério em `tolx` é insuficiente,
#     pois o método converge muito lentamente e pode parar muito longe de $z$.

# <markdowncell>

# ## Performance
# 
# Algumas ineficiências óbvias ocorrem no código acima.
# A mais importante delas é que calculamos **3** vezes $f(x)$ para cada valor de $x$ testado (Ache!).
# 
# Uma outra é que, se `toly = 0`, então não deveríamos testar mais nada.
# Como o custo deste teste é relativamente baixo (se comparado a calcular a função $f$),
# e a única solução realmente satisfatória seria usar dois algoritmos exatamente iguais,
# exceto por esta linha, vamos manter tudo junto.

# <markdowncell>

# # Polinômios: Newton-Horner
# 
# Uma das mais importantes aplicações do método de Newton é para polinômios.
# Estas são provavelmente as funções mais simples que podem aparecer em problemas,
# e já o cálculo das suas raízes é bastante complicado.
# Além disso, quando o grau é pelo menos $5$, não existe fórmula explícita para encontrar a solução.

# <markdowncell>

# ## Calculando polinômios
# 
# Uma das primeiras observações sobre polinômios é que calcular usando a definição não é a melhor saída:
# a fórmula
# $$ P(x) = \sum_k a_k x^k $$
# contém muitas multiplicações (para calcular os $x^k$ e em seguida o produto com $a_k$) e $d$ somas.
# Fazendo a conta na ordem crescente dos $k$, temos $2n$ multiplicações se guardarmos o produto $x^k$ para o próximo termo.

# <codecell>

def P(coeff, x):
    px = 1
    acc = 0
    for c in coeff:
        acc += c*px
        px *= x
    return acc

# <markdowncell>

# Mas podemos calcular **ao contrário**.
# Veja que
# $$ P(x) = a_0 + x(a_1 + x(a_2 + \ldots + x (a_n) \ldots )) $$
# o que dá a seguinte fórmula, indo de dentro para fora dos parêntesis:
# $$ \begin{align*} b_n(x) & = a_n \\ b_k(x) & = a_k + x \cdot b_{k+1}(x) \end{align*} $$
# Note que $P(x) = b_0(x)$.

# <codecell>

def Horner(rcoeff, x):
    # Inicialização
    acc = rcoeff[0]
    for c in rcoeff[1:]:
        acc *= x
        acc += c
    return acc

# <markdowncell>

# Vejamos que o método de Horner nos dá uma igualdade poderosa entre os valores de $P$.
# 
# Sejam $x$ e $y$ dois números.
# Vamos calcular $d(x,y) = P(x) - P(y)$ através das recorrências dos $b_k$s.
# 
# Definimos $$d_k(x,y) = b_k(x) - b_k(y) = x \cdot b_{k+1}(x) - y \cdot b_{k+1}(y).$$
# Note que $d_n(x,y) = 0$ e que $d_0(x,y) = P(x) - P(y)$.
# 
# Agora, repare que $b_{k+1}(x) = b_{k+1}(y) + d_{k+1}(x,y)$ e substitua:
# $$d_k(x,y) = x \cdot \big(b_{k+1}(y) + d_{k+1}(x,y)\big) - y \cdot b_{k+1}(y) = x \cdot d_{k+1}(x,y) + (x - y)\cdot b_{k+1}(y).$$
# 
# Assim, $d_n(x,y)$ é múltiplo de $(x - y)$ (pois é igual a zero!), e a cada etapa somamos um termo também múltiplo de $(x - y)$.
# Portanto, $d_0(x,y)$ será múltiplo de $(x - y)$.

# <markdowncell>

# Vamos, então, calcular algo com "menos termos" para fazer menos contas!
# Defina $$q_k(x,y) = \frac{d_k(x,y)}{x - y}$$ e veja que ele satisfaz a recorrência
# $$ q_k(x,y) = x \cdot q_{k+1}(x,y) + b_{k+1}(y). $$
# Rearrumando um pouco, temos:
# $$ \begin{align*} q_{n-1}(x,y) & = b_n(y) \\ q_k(x,y) & = b_{k+1}(y) + x \cdot q_{k+1}(x,y) \end{align*} $$
# que é exatamente o cálculo do polinômio
# $$ Q_y(x) = \sum b_{k+1}(y) \cdot x^k $$
# pelo método de Horner!
# 
# Veja que este polinômio tem grau $n-1$ em $x$, e obtemos uma identidade muito importante:
# $$ P(x) - P(y) = (x - y)Q_y(x). \qquad (1) $$

# <codecell>

# Calcula [P(x)] e [Q(.,x)] dados os coeficientes de P em ordem decrescente [a_n ... a_0] e um ponto [x]
# O polinômio [Q(.,x)] é dado por seus coeficientes em ordem decrescente [b_n(x) ... b_1(x)]
def HornerQ(rcoeff, x):
    # Inicialização
    acc = rcoeff[0]
    b = [acc]
    for c in rcoeff[1:]:
        acc *= x
        acc += c
        b.append(acc)
    return acc, b[:-1]

# <codecell>

HornerQ([1,0,0,0,0,0,0,0,0,0,-1], -1)

# <markdowncell>

# ## Fatorando polinômios
# 
# Ao realizar a divisão euclidiana de $P(x)$ por $(x - Z)$,
# devemos obter algo como
# $$ P(x) = (x - Z)Q(x) + R(x) $$
# onde $Q$ é o quociente e $R$ é o resto, de grau menor do que $1$.
# Logo $R(x)$ é uma constante $R$, e vemos, ao substituir $x = Z$,
# que $R = P(Z)$.
# 
# A identidade acima sobre $Q_y$ dá outra demonstração disso: basta escrever
# $$ P(x) = (x - Z)Q_Z(x) + P(Z). $$
# Assim, a identidade $(1)$ permite calcular o quociente da divisão de um polinômio por um fator simples!

# <markdowncell>

# No caso particular em que $Z$ é uma raiz de $P$, temos $P(Z) = 0$
# e com isso obtivemos uma fatoração de $P$.
# Para achar as outras raízes de $P$, basta achar as raízes de $Q_Z$.

# <markdowncell>

# ### Cálculo da derivada
# Seja, novamente, $y$ um número qualquer (não precisa ser uma raiz).
# Derivando a identidade $(1)$ com relação a $x$, obtemos:
# $$P'(x) = Q_y(x) + (x - y)Q_y'(x).$$
# 
# Em particular, para $x = y$, temos
# $$P'(y) = Q_y(y)$$
# que nos dá uma forma de calcular a derivada de $P$.

# <markdowncell>

# Esta fórmula é bastante útil para o método de Newton:
# ao calcularmos $P(x_i)$, temos os coeficientes para calcular $P'(x_i)$.

# <codecell>

def newtonP(rcoeff, x, tol=1e-10, maxiter=100):
    for i in range(maxiter):
        fx, bx = HornerQ(rcoeff, x)
        dfx, _ = HornerQ(bx, x)
        
        step = fx/dfx
        x = x - step
        if abs(step) < tol: break

    return x, bx, i

# <markdowncell>

# ## Todas as raízes
# 
# Ao calcular uma raiz de $P$, temos já em mãos os coeficientes do fator restante em $Q_Z$.
# Assim, podemos achar, iterativamente, todas as raízes de $P$!

# <codecell>

def newton_all(rcoeff, x, tol=1e-10, maxiter=100):
    roots = []
    steps = []
    while len(rcoeff) > 1:
        x, rcoeff, ni = newtonP(rcoeff, x, tol, maxiter)
        roots.append(x)
        steps.append(ni)
        
    return roots, steps, rcoeff

# <markdowncell>

# Vejamos os resultados deste método:

# <codecell>

newton_all([1, -10, -50, 10, 70, 10], 0.1, tol=1e-17)

# <markdowncell>

# Mas nem sempre dá tudo certo... vejamos este polinômio agora:

# <codecell>

coeffs = [2,-5,1,4,-13,21]
rs, sts, _ = newton_all(coeffs, 2.)
for r,s in zip(rs,sts):
    print("Candidate root: {: .5f}, value = {: 12f} ({:2} steps)".format(r, Horner(coeffs, r), s))

# <markdowncell>

# Este caso não funciona porque a função não 5 raízes reais, mas apenas 1.
# Assim, será impossível achar 5 raízes!
# 
# Mas se usarmos números complexos, ou seja, se começarmos buscando a partir de números complexos,
# o método acha tudo:

# <codecell>

rs, sts, _ = newton_all(coeffs, 2. + 5j)
for r,s in zip(rs,sts):
    print("Candidate root: {: .5f}, value = {: 20.2e} ({:2} steps)".format(r, Horner(coeffs, r), s))

# <codecell>

newton_all([1, -7, 15, -13, 4], 0.1)

# <markdowncell>

# # Achando todos os zeros de uma só vez
# 
# Pode parecer muito ambicioso, mas a verdade é que algoritmos de "deflação"
# (como são conhecidos os métodos que calculam as raízes uma a uma, e dividem o polinômio a cada iteração)
# podem ser muito lentos e, além disso, acumular muito erro pelas "divisões".
# Assim, é razoável buscar métodos que encontrem todas as raízes de um polinômio _diretamente_.
# 
# Uma das abordagens (devida a Schleicher et al.) é determinar um conjunto suficientemente grande de pontos iniciais
# tais que o método de Newton, aplicado a este conjunto, atinja pelo menos uma vez **cada** raíz de $P$.
# Sua idéia, mais ambiciosa ainda, requer que o conjunto seja relativamente _independente_ do polinômio considerado.
# Assim, escolhem-se pontos (complexos) num anel (ou seja, entre dois círculos)
# cuja única dependência no polinômio é que seu interior contenha todos os zeros,
# para o que basta uma homotetia (de cálculo bastante simples!).

