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
#     3. **Autovalores e autovetores**

# <codecell>

%pylab inline

# <markdowncell>

# # Autovetores e autovalores
# 
# Um autovetor de uma matriz quadrada $A$ é um vetor não nulo $v$ tal que $Av$ seja colinear a $v$.
# Em termos mais algébricos, existe um escalar $\lambda$ tal que
# $$ Av = \lambda v.$$
# 
# Os autovetores fornecem uma nova forma de fatorar a matriz $A$.
# Se esta admitir uma base de autovetores (por exemplo, for simétrica!),
# podemos formar a _diagonalização_ da matriz $A$,
# que é dada pela matriz dos autovetores $V = [v_1, v_2, \ldots, v_n]$
# e pela matriz diagonal dos autovalores $D = \text{diag}(\lambda_1, \lambda_2, \ldots, \lambda_n)$:
# $$ AV = VD. $$
# 
# Quando a matriz $A$ é simétrica, os autovetores são ortogonais entre si.
# Isso permite inverter a matriz $V$ com grande facilidade, já que
# $V^{T} V = \text{diag}(N_1^2, N_2^2, \ldots, N_n^2)$ onde $N_i$ é a _norma_ do vetor $v_i$.
# Em particular, se tivermos o cuidado de tomar autovetores de norma $1$,
# a transposta de $V$ será a sua inversa!

# <markdowncell>

# ## Calculando autovetores
# 
# Um dos algoritmos mais clássicos de cálculo de autovetores é "multiplicar e normalizar":
# tome um vetor "qualquer" $u_0$ e aplique a matriz $A$, obtendo $w_1 = Au_0$.
# Normalize $w_1$, ou seja, divida pela sua norma para obter um vetor unitário de mesma direção,
# e chame-o de $u_1$.
# Repita: $w_2 = Au_1$, e $u_2 = \frac{w_2}{N(w_2)}$.
# E assim por diante.
# Em geral (isso depende de $u_0$), a sequência dos $u_n$ converge para um autovetor $u$ correspondente
# ao autovalor de $A$ de maior módulo.

# <markdowncell>

# ## Estudando a convergência
# 
# Suponha que o "segundo" autovalor de $A$ seja $\lambda_2$, em módulo menor do que $\lambda_1$.
# Isso quer dizer que, para todo vetor $u = \sum c_i v_i$ (onde os $v_i$ são os autovetores de $A$),
# temos
# $$ Au = \sum \lambda_i c_i v_i. $$
# Além disso, note que a normalização poderia ser feita depois:
# se definirmos $x_n = A^n u_0$, temos que $u_n = \frac{x_n}{N(x_n)}$.
# 
# Cada iteração deste método irá aumentar o peso do coeficiente de $v_1$,
# pois ele será multiplicado pelo maior dos números $\lambda_i$,
# e temos $A^n u = \sum \lambda_i^n c_i v_i$.
# Para ver como o método converge, vamos olhar para o erro, ou seja,
# a componente de $u_n$ que não está na direção de $v_1$:
# $$ \frac{\sum _ {i > 1} \lambda_i^n c_i v_i}{N(x_n)}. $$
# Só que a norma de $x_n$ é determinada principalmente por $c_1 \lambda_1^n$,
# que é muito maior do que todos os outros.
# Idem, inclusive, para o termo de erro:
# a maior contribuição para sua norma vem de $c_2 \lambda_2^n$.
# Assim, o erro é $\left| \frac{\lambda_2}{\lambda_1} \right|^n \to 0$.

# <markdowncell>

# ### Exercício
# 
# Implemente este algoritmo,
# e pense sobre o critério de parada para o mesmo.
# Observe a velocidade de convergência.

# <codecell>

def autovetor(A, tol=1e-6):
    n,m = shape(A)
    assert n==m, 'A must be square'
    
    u = rand(n)
    w = dot(A,u)
    wnorm = norm(w,ord=2)
    w = w/wnorm
    while norm(u-w, ord=2) > tol:
        u = w
        w = dot(A,u)
        wnorm = norm(w, ord=2)
        w = w/wnorm
    return w, wnorm

# <markdowncell>

# Use este algoritmo para calcular o "maior" autovalor de algumas matrizes (por exemplo, a matriz de Hilbert!).

# <codecell>

A = rand(20,20)
#print(A)
v, l = autovetor(A)

# <codecell>

diff = dot(A,v) - l*v
print('Norma 2: {}, Norma 1: {}'.format(norm(diff), norm(diff,ord=1)))

# <markdowncell>

# ### Observação
# 
# Se o limite um autovetor tal que $Av = \lambda v$, é possível também ter uma estimativa de $\lambda$
# comparando os módulos de $v_n$ e $A v_n = u _ {n+1}$.

# <markdowncell>

# ## Calculando autovalores
# 
# É possível determinar os autovalores de uma matriz através de uma equação polinomial em $\lambda$:
# $$ \det(A - \lambda I) = 0. $$
# 
# O cálculo "pela definição" do polinômio característico de uma matriz $n \times n$
# requer calcular todas as $n!$ permutações.
# Isso é muito custoso, e após o quê ainda teríamos que achar as raízes de um polinômio de grau relativamente grande,
# o que dará trabalho também para o método de Newton (por exemplo).
# 
# Existem métodos mais eficientes para calcular o polinômio característico,
# mas não vamos entrar no detalhe agora, pela razão a seguir:

# <markdowncell>

# ## Autovalores $\not\Rightarrow$ autovalores! 
# 
# Uma vez conhecidos os autovalores, podemos resolver o sistema $(A - \lambda_k)v = 0$
# (que é **singular**!) e encontrar uma solução não-nula, determinando o autovetor correspondente.
# 
# Em geral, calcular raízes de polinômios também se faz por um método iterativo
# (quando o grau é maior do que 4, por exemplo),
# e haverá um erro (numérico, por exemplo) no valor de $\lambda$
# que será aproximado por $\tilde\lambda$.
# Assim, é possível que a matriz $A - \tilde\lambda I$ seja inversível,
# e que o sistema na verdade só tenha a solução $v = 0$, que não desejamos.
# Portanto, é preciso fazer as contas de $(A - \lambda I)v = 0$ levando em conta que
# a matriz será "quase-singular" e que isto corresponde à liberdade necessária para achar um autovetor!

# <markdowncell>

# # Calculando autovetores correspondentes a outros autovalores

# <markdowncell>

# Poderíamos calcular o autovetor correspondente ao **menor** autovalor fazendo o contrário:
# multiplicamos $u_0$ por $A^{-1}$ sucessivamente, o que **divide** os coeficientes.
# Claro, isso só funciona se $A$ não tiver um autovalor igual a zero.
# 
# Poderíamos modificar um pouco este procedimento:
# chutamos (de alguma forma) que há um autovalor próximo a $z$, um número complexo.
# Assim, vamos tentar calcular qual será o autovetor correspondente.
# Para isso, veja que $A_z = A - zI$ tem um autovalor bem próximo de zero,
# e assim iterando o procedimento acima, temos o autovetor correspondente.

# <markdowncell>

# ### Exercício
# 
# Incorpore a solução de sistemas lineares para implementar a multiplicação por $(A - zI)^{-1}$.
# Use a fatoração LU de $(A - zI)$ para tornar a solução muito mais rápida!

# <codecell>

def lu(A):
    """ Fatoração LU da matriz  A.
        Retorna duas novas matrizes L e U; A não será alterada. """
    # Os coeficientes de A estão em A[i][j]
    (n,m) = shape(A)
    rank = min(n,m)
    L = zeros((n, rank), dtype=A.dtype)
    U = A.copy()
    for i in range(rank):
        pivot_coeff = U[i][i]
        pivot_line = U[i][i+1:]
        L[i][i] = 1
        for ii in range(i+1,n):
            multiplier = U[ii][i]/pivot_coeff
            U[ii][i] = 0
            U[ii][i+1:] -= multiplier * pivot_line
            L[ii][i] = multiplier
    U = U[:rank]
    return L,U

# <codecell>

def nearest_eigenvalue(A,z, tol=1e-6, nmax=100):
    """ Finds the eigenvalue of  A  nearest to  z (complex). Iterative method. """
    n,m = shape(A)
    assert n==m, 'A must be square'
    
    q,r = qr(A - z*identity(n))
    u = rand(n)
    w = solve(r,dot(q.T,u))
    wnorm = norm(w, ord=2)
    w = w/wnorm
    n = 0
    while norm(u-w) > tol and n < nmax:
        u = w
        w = solve(r,dot(q.T,u))
        wnorm = norm(w, ord=2)
        w = w/wnorm
        n += 1
    return w, wnorm, n

# <codecell>

A = rand(10,10)
eigvals(A)

# <codecell>

z = .5
v, l, n = nearest_eigenvalue(A,z)

# <codecell>

print('Produto ', dot(A,v))
print('Prod - z', dot(A - z*identity(10),v))
print('Solve   ', solve(A - z*identity(10),v))

print('v       ', v, l)
print(n)

# <codecell>

# (A - zI)^{-1} . v = l v <=> v * (1/l) = (A - zI)v <=> Av = (z + 1/l)v
diff = dot(A,v) - (z + 1/l)*v
print('Norma 2: {}, Norma 1: {}'.format(norm(diff), norm(diff,ord=1)))

# <markdowncell>

# # Calculando todos os autovalores e autovetores

# <markdowncell>

# Pode ser que seja necessário conhecer todos os autovalores e autovetores de uma matriz.
# Neste caso, uma solução (além de calcular todas as raízes do polinômio característico de $A$)
# é criar uma série de transformações de $A$ que **preservam** os autovalores.
# Da mesma forma como transformamos $A = PLU$ através de operações de linhas
# (e poderíamos ter feito colunas também),
# outras operações levam a matrizes com mesmos autovalores,
# como é o caso de _similitudes_:
# dizemos que $A$ é similar a $B$ se existe uma matriz $P$ tal que
# $A = P^{-1} B P$.
# Se $Av = \lambda v$, então
# $$ P^{-1} B P v = \lambda v \Leftrightarrow B (Pv) = \lambda (Pv) $$
# o que mostra que $Pv$ é um autovetor de $B$ com o mesmo autovalor.
# 
# Assim, buscamos uma seqüência de transformações que sejam similitudes.

# <markdowncell>

# ## Fatoração QR e similitudes
# 
# Uma das maneiras mais curiosas de obter estas similitudes é a fatoração QR:
# ela é bastante similar à fatoração LU: ainda há um bloco triangular superior, que agora chamamos $R$,
# mas $Q$ é uma matriz mais especial: é uma matriz ortogonal,
# ou seja, suas colunas (e linhas) são ortogonais entre si e de norma 1.
# Isso (como já vimos na diagonalização) é muito útil para calcular inversas!
# 
# Assim, se temos $A = QR$, também é verdade que $Q^{-1}A = Q^T A = R$
# e portanto a matriz $B = RQ$ é igual a $Q^{-1} A Q$, ou seja, $B$ é similar a $A$.
# Também $A$ é similar a $B$, já que $A = Q B Q^{-1}$.
# 
# Vamos continuar: fatoramos $B$ novamente em $Q_2 R_2$, e permutamos,
# obtendo $C = R_2 Q_2$.
# Isso dá $B = Q_2 R_2 Q_2^{-1}$, e portanto
# $A = Q Q_2 R_2 Q_2^{-1} Q^{-1}$.
# 
# Da mesma forma que iteramos a aplicação da matriz $A$ em um vetor $u$,
# podemos ver a repetição desta "troca de lados" entre $Q$s e $R$s sucessivos como uma aplicação de $A$
# aos vetores de $Q$ (que são ortogonais entre si, como uma base de autovetores de $A$ deve ser, se $A$ é simétrica).
# 
# Quando $A$ é simétrica, isso funciona exatamente assim:
# os vetores dos produtos das $Q$s convergem para autovetores de $A$,
# e a seqüência $A$, $B$, $C$, $\ldots$ converge para uma matriz diagnoal,
# formada pelos autovalores de $A$ (que também são de $B$, $C$, etc.).

# <codecell>

def qrsequence(A, tol=1e-6, nmax=100):
    q, r = qr(A)
    B = dot(r,q)
    prodq = q
    while rms_flat(B - A) > tol:
        A = B
        q, r = qr(A)
        B = dot(r,q)
        prodq = dot(prodq,q)
    return B, prodq

# <codecell>

A = array([[1,2,3], [3,4,3], [7,6,5]])
Rlim, Qlim = qrsequence(A)
print(Qlim)
print(Rlim)

# <codecell>

dot(Qlim,dot(Rlim,Qlim.T))

# <codecell>

Qlim.T[0]

# <codecell>

dot(A, Out[15])

# <codecell>

Out[15]*Rlim[0][0]

# <markdowncell>

# # Fatoração / Decomposição SVD
# 
# SVD (_Singular Value Decomposition_) é uma outra fatoração de matrizes,
# mais geral do que a diagonalização, e que serve também para matrizes retangulares.
# Essencialmente, ela consiste em encontrar **duas** bases
# (em vez de apenas uma que é o caso de autovetores da diagonalização)
# que sejam adaptadas à matriz $A$.
# Assim, queremos escrever
# $$ A = U \Sigma V^{-1} , $$
# onde $U$ e $V$ são ortogonais (correspondendo a mudanças de base "por rotação")
# e $\Sigma$ é uma matriz diagonal (correspondendo a multiplicações entre as bases).
# 
# Neste caso, a idéia é usar uma matriz simétrica
# (para a qual sabemos existir a diagonalização e bases "apropriadas")
# associada a $A$: $A^T A$.
# Parece apelação, mas ao supor a decomposição $A = U \Sigma V^{-1}$,
# com matrizes ortogonais $U$ e $V$, temos
# $$ A^T A = {V^{-1}}^T \Sigma^T U^T U \Sigma V^{-1} = V \Sigma^T \Sigma V^{-1} $$
# que é **a diagonalização** de $A^T A$, se tomarmos $\Sigma^T \Sigma = D$.
# 
# Assim, podemos obter uma base de "vetores especiais" a partir de $V$,
# e em seguida tomamos uma matriz diagonal $\Sigma$ tal que $\Sigma^T \Sigma = D$;
# o mais simples é usar a raiz quadrada dos elementos diagonais de $D$
# (que são positivos porque $A^T A$ é simétrica!).
# Enfim, para obter $U$, basta resolver o sistema $A = U \Sigma V^{-1}$,
# que é linear em $U$.

# <markdowncell>

# ### Exercício
# 
# Escreva um código para a decomposição SVD.
# Para diagonalizar $A^T A$, você pode usar o cálculo de autovalores e autovetores da iteração QR.

# <codecell>

def svd(A):
    pass

