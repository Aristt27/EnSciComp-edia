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
# 6. Álgebra linear computacional
#     1. Resolvendo sistemas lineares
#     2. Fatoração
#     3. Autovalores e autovetores
#     4. **Erros e estabilidade**
#     5. **Métodos iterativos**

# <codecell>

%pylab inline

# <markdowncell>

# # Erros e estabilidade de $Ax = b$
# 
# Ao resolver um sistema linear, pode haver erros numéricos ou erros de medida.
# Vamos apenas observar um exemplo em que o modelo é relativamente simples.
# 
# Suponha que, em vez de termos medido $b$ exatamente, temos $b + e$, onde $e$ é um (pequeno!) erro.
# Isso quer dizer, em geral, que $\displaystyle \frac{\lVert e\rVert}{\lVert b\rVert} << 1$.
# 
# Seja, agora, $x$ a solução "real" de $Ax = b$, e $y$ a solução de $Ay = (b+e)$.
# Qual o erro?
# Ou seja, como podemos avaliar $\displaystyle \frac{\lVert (y - x)\rVert}{\lVert x\rVert}$ ?

# <markdowncell>

# Substituindo as equações de $x$ e $y$, temos que $A(y - x) = e$, e portanto $y - x = A^{-1}e$.
# Assim, temos
# $$ \frac{\lVert (y - x)\rVert}{\lVert x\rVert} = \frac{\lVert A^{-1}e\rVert}{\lVert A^{-1}b\rVert} .$$
# 
# Pensando que $A^{-1}$ vai "dilatar" alguns vetores e "contrair" outros (mas não sabemos quais!),
# o que podemos dizer, com certeza, é que a dilatação é menor do que $\lambda_{\text{max}}$
# e maior do que $\lambda_{\text{min}}$.
# Se $A$ for simétrica e positiva definida, estes serão o maior e o menor autovalor, respectivamente.
# 
# Só que pode ser que o sistema conspire contra nós: $b$ pode estar na direção de menor dilatação,
# e $e$ na de maior dilatação.
# Assim, mesmo no pior dos casos, temos:
# $$ \frac{\lVert (y - x)\rVert}{\lVert x\rVert}
#    \le \frac{\lambda _ {\text{max}}}{\lambda _ {\text{min}}} \frac{\lVert e\rVert}{\lVert b\rVert}. $$

# <markdowncell>

# ## Número de condicionamento
# 
# Vemos que o erro será propagado de $b$ para $x$, e sofrerá um aumento (no máximo) proporcional a
# $\frac{\lambda _ {\text{max}}}{\lambda _ {\text{min}}}$.
# Esse valor é chamado de número de condicionamento de uma matriz, e,
# se for muito grande, indica que o sistema que estamos resolvendo será muito "instável":
# pequenos erros de medida podem ser magnificados extraordinariamente.

# <markdowncell>

# ### Exercício
# 
# Calcule o número de condicionamento da matrix de Hilbert, em função do seu tamanho.
# Lembre, a matriz é formada por $a _ {i,j} = \frac{1}{i + j}$.

# <codecell>

def hilbert(n):
    m = []
    for i in range(1,n+1):
        m.append([1/(i+j) for j in range(1,n+1)])
    return array(m)

# <codecell>

%pylab inline

# <codecell>

for n in range(5,16,2):
    print (n, cond(hilbert(n)))

# <codecell>

ns = range(3, 20)
semilogy(ns, [cond(hilbert(n)) for n in ns])

# <markdowncell>

# # Métodos iterativos
# 
# Uma outra forma de resolver sistemas lineares, além das que já vimos,
# se baseia em métodos iterativos.
# Da mesma forma que os métodos iterativos para encontrar raízes,
# a sua grande utilidade é que, _quando convergem_,
# eles vão diminuindo o erro do resultado,
# o que pode inclusive tornar métodos mais robustos quanto aos erros numéricos.
# (Claro que nada irá reduzir erros de medida...)
# 
# O protótipo básico destes métodos é uma iteração de ponto fixo:
# $$ x _ {n+1} = f(x_n) = Cx_n + d,$$
# onde $C$ e $d$ dependem dos $A$ e $b$ originais.
# Para que a iteração convirja, é preciso que ela seja uma _contração_, ou seja, que
# $$\lVert f(y) - f(z) \rVert \lt \lVert y - z\rVert$$
# para **todos** $y$ e $z$.
# No caso de sistemas lineares como acima, basta que a matriz $C$ seja uma contração;
# ou seja, que seus valores singulares sejam todos menores do que um.

# <markdowncell>

# ## Pre-condicionadores
# 
# O problema do método acima é que ele não diz como construir $C$ e $d$ em função de $A$ e $b$.
# 
# Uma tática esperta para contornar este problema é o uso de pré-condicionadores.
# Um **pré-condicionador** é uma matriz $P$, da mesma ordem de $A$,
# e que usamos para "decompor" $A$ em duas partes: $P$ e "o resto", $A - P$.
# 
# Se $x$ satisfaz $Ax = b$, temos também que
# $$ Px = (P - A + A)x = (P - A)x + b, $$
# e ao inverter $P$ temos um protótipo de iteração de ponto fixo:
# $$ x = P^{-1} (P - A) x + P^{-1}b .$$
# 
# Todo o valor de um método de pré-condicionador está na facilidade (e estabilidade!)
# para calcular as inversas de $P$ necessárias.

# <markdowncell>

# ## Primeiro exemplo: Jacobi
# 

# <markdowncell>

# Entre as matrizes mais simples de se inverter estão as matrizes diagonais.
# 
# O **método de Jacobi** corresponde a decompor $A$ em sua parte diagonal $D$ e "no resto".
# O método associado será relativamente restritivo, não podendo ser aplicado a muitos casos,
# mas tem a vantagem de ser bastante simples.
# 
# ### Teorema
# 
# Se a matriz $A$ possuir uma diagonal dominante de linhas
# (ou seja, $a _ {ii}$ é maior do que a soma dos outros $a _ {ij}$)
# o método de Jacobi converge.

# <markdowncell>

# ### Exercício
# 
# Implemente este algoritmo,
# e pense sobre o critério de parada para o mesmo.
# Observe a velocidade de convergência.

# <codecell>


# <markdowncell>

# ## Segundo exemplo: gradientes conjugados
# 
# Re-escrevendo a fórmula de ponto fixo, temos:
# 
# $$ x _ {n+1} = P^{-1} (P - A) x_n + P^{-1}b = (I -  P^{-1} A) x_n + P^{-1}b = x_n + P^{-1} A x_n + P^{-1}b = x_n + v_n,$$
# onde podemos interpretar $v_n$ como sendo uma "correção" de $x_n$,
# na direção de ficar mais próximo da solução real $x$ do sistema
# (se o método estiver convergindo, claro!).
# 
# Vamos agora focalizar em matrizes simétricas positivas definidas.
# Uma idéia interessante neste caso é buscar $v_n$ perpendiculares entre si,
# para evitar ficar "zigue-zagueando" demais.
# Além disso, se todos os $v_n$ forem ortogonais entre si,
# e cada um corrigir "a quantidade certa",
# teremos exatamente $N$ passos, onde $N$ é a dimensão de $A$.
# Garantir convergência em um número finito de etapas é melhor ainda!

# <markdowncell>

# Seja $x_0$ dado (pode ser inclusive $x_0 = 0$...), e formemos o resto $r_0 = b - Ax_0$.
# Vamos andar com $x$ na direção $r_0$.
# Se quisermos minimizar o erro na direção $r_0$, temos a seguinte situação:
# $$\begin{align*}
#      x_1 & = x_0 + \alpha r_0 \\
# b - Ax_1 & = b - Ax_0 - \alpha Ar_0 \\
# \end{align*}
# 
# A nova direção do erro será dada por $r_1 - \beta p_0$

