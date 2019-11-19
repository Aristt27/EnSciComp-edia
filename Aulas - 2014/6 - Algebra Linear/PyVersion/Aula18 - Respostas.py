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
#     2. **Fatoração**

# <codecell>

%pylab inline

# <markdowncell>

# # Fatoração LU
# 
# Uma equação matricial $Ax = b$ pode levar muito ou pouco tempo para ser resolvida,
# dependendo da forma da matriz $A$.
# Vimos, na aula passada, que se $A$ estiver sob forma triangular superior,
# a solução do sistema é relativamente simples:
# basta ir achando sucessivamente valores para as variáveis
# $x_n$, $x _ {n-1}$, $\ldots$, $x_2$, $x_1$.
# O mesmo acontece se $A$ fosse triangular inferior,
# mas na ordem contrária.
# 
# O algoritmo de Gauss (eliminação e substituição),
# se examinado cuidadosamente,
# produz uma sequência de operações que equivale a separar a matriz em um produto de duas outras matrizes,
# chamadas classicamente de "$L$" e "$U$",
# que são respectivamente triangulares inferior e superior (_lower_ e _upper_, em inglês):
# $$ A = LU. $$
# Exatamente por isso que o algoritmo vai inicialmente "de cima para baixo",
# porque ele está resolvendo $L(Ux) = b$, e quando ele termina a eliminação
# temos o sistema equivalente
# $$ Ux = b' = L^{-1}b. $$
# A segunda parte é exatamente a "substituição" final,
# mas o que é interessante é que o primeiro passo _também_ pode ser visto
# como uma substituição!
# (e vice-versa, o segundo passo pode ser visto como
# "eliminar as variáveis já determinadas" nas equações "de cima")

# <markdowncell>

# O que este parágrafo deve fazer pensar é que, se já usamos $A$ alguma vez para resolver um sistema,
# e que vamos querer resolver outras equações $Ax = y$ (com outros $y$)
# então deveríamos evitar fazer o mesmo trabalho várias vezes:
# o que podemos fazer é guardar as duas partes $L$ e $U$ de $A$,
# e usá-las para resolver todos os sistemas.
# 
# ### Observação
# 
# É claro que, se já sabemos de antemão quais são os $y$ que vamos querer usar no lado direito,
# não é **necessário** guardar a fatoração (o que vai usar memória).
# Mas, muitas vezes, pode ocorrer que $A$ seja uma matriz de um algoritmo recursivo / iterativo,
# e que os $y$ que aparecem sejam determinados apenas em função dos $x$ da etapa anterior.
# Neste caso, é bastante provável que manter a fatoração de $A$ na memória seja útil.

# <markdowncell>

# ### Exercício
# 
# Deduza o algoritmo que permite obter $L$, sabendo que $U$ será a matriz resultante da eliminação.
# Implemente a fatoração LU.
# 
# Observe também que seria possível guardar $L$ e $U$ no mesmo espaço de $A$. (mas não implemente isso, ainda)

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

# <markdowncell>

# ## Pivôs, permutações e matrizes esparsas
# 
# Pode ocorrer, durante a fatoração, que obtenhamos um zero.
# Isso é bastante inconveniente, já que não poderíamos mais usar esta linha para eliminar.
# A solução é óbvia: tentaremos encontrar outra linha em que a variável correspondente
# não tenha um coeficiente igual a zero.
# Este novo coeficiente é chamado de **pivô**.
# 
# Mudar de pivô implica permutar as equações (e portanto $b$ também)
# mas não as variáveis.
# Ao longo do processo, pode ser necessário realizar diversas permutações "elementares"
# (entre duas linhas),
# mas a composta de duas permutações ainda é uma permutação.
# Este processo gera o que chamamos de fatoração $PLU$,
# pois a permutação de linhas poderia ser feita antes de eliminar com $L$.
# 
# A troca de linhas é, em geral, representada por uma matriz de permutação
# (já que estamos fazendo Álgebra linear),
# mas é um grande desperdício usar $n\times n$ espaços
# para guardar uma matriz de permutação que contém apenas $n$ informações.
# Portanto, seria interessante ter uma representação mais compacta destas matrizes,
# e isto é feito com _matrizes esparsas_.
# Uma matriz esparsa é simplesmente uma matriz que possui "poucas"
# entradas diferentes de zero.
# Exemplos clássicos são matrizes diagonais e tridiagonais
# (que são tão especiais que em geral são tratadas de forma mais dedicada ainda!)
# matrizes de permutação, matrizes de adjacência de grafos (com "poucas arestas", claro!),
# e matrizes advindas da discretização de EDPs.

# <codecell>

from scipy import sparse

# <markdowncell>

# Vamos usar uma forma relativamente simples para descrever uma matriz esparsa,
# a forma de "coordenadas", também conhecida como _ijv_ ou _trincas_.
# 
# Vale notar que usar matrizes esparsas requer um certo cuidado:
# devemos manter as matrizes esparsas tanto tempo quanto possível
# durante os cálculos,
# mas ao mesmo tempo reconhecer quando esta se torna "densa"
# e voltar à descrição usual.
# Além disso, em geral, é mais simples construir a matriz usando uma descrição
# (como _ijv_, ou _lista de listas_, ou _dicionário_),
# mas estas formas são ineficientes para operar com as mesmas
# (por exemplo resolver sistemas ou calcular determinantes).
# Assim, é recomendado que, uma vez fixada a matriz esparsa,
# seja realizada uma conversão para formas mais eficientes.

# <codecell>

rows = list(range(7))
cols = list(range(7))
# Permute!
cols[2] = 5
cols[5] = 2
perm25 = sparse.coo_matrix((ones(7), (rows, cols)))
perm25.todense()

# <markdowncell>

# Verificando que permuta

# <codecell>

b = rand(7)
print(b)
print(perm25.dot(b))

# <markdowncell>

# Verificando que é uma involução: permutar duas linhas duas vezes volta à identidade:

# <codecell>

perm25.dot(perm25).todense()

# <markdowncell>

# ### Exercício
# 
# Mantenha a lista das linhas permutadas na fatoração PLU,
# e retorne a matriz (esparsa!) resultante,
# além de $L$ e $U$.

# <codecell>

def build_permutation(l):
    """ Constrói a matriz de permutação que envia  i  em  l[i]. """
    n = len(l)
    return sparse.coo_matrix((ones(n), (list(range(n)), l)))

# <codecell>

def lu_p(A):
    """ Fatoração PLU da matriz  A.
        Retorna duas novas matrizes  L  e  U  e uma matriz de permutações  P, esparsa.
        A matriz  A  não será alterada. """
    # Os coeficientes de A estão em A[i][j]
    eps = 1e-10 # Use este epsilon para testar se uma entrada é "zero".
    (n,m) = shape(A)
    rank = min(n,m)
    L = zeros((n, rank), dtype=A.dtype)
    U = A.copy()
    perm = list(range(n))
    for i in range(rank):
        print('Passo {}.\n  U = {}\n  L = {}\n  perm = {}'.format(i,U,L,perm))
        pivot_coeff = U[i][i]
        if abs(pivot_coeff) < eps:
            ii = i+1
            while ii < n and abs(U[ii][i]) < eps:
                ii += 1
            assert (ii < n), 'A matriz A não tem pivôs disponíveis.'
            pivot_coeff = U[ii][i]  # Tomar o novo pivô
            temp = U[i].copy()      # Permutar as linhas
            U[i] = U[ii]
            U[ii] = temp
            temp = L[i].copy()      # Permutar P com L
            L[i] = L[ii]
            L[ii] = temp
            perm[i],perm[ii] = perm[ii],perm[i] # E guardar a permutação
            print('Passo {}, permutação.\n  U = {}\n  L = {}\n  perm = {}'.format(i,U,L,perm))
            
        pivot_line = U[i][i+1:]
        L[i][i] = 1
        for ii in range(i+1,n):
            multiplier = U[ii][i]/pivot_coeff
            U[ii][i] = 0
            U[ii][i+1:] -= multiplier * pivot_line
            L[ii][i] = multiplier
    U = U[:rank]
    
    return build_permutation(perm),L,U

# <codecell>

A = array([[1,2.,3], [4,5,6], [7,8,9], [3,5,3]])
P,L,U = lu_p(A)
print(P)
print(L)
print(U)
P.todense()*L*U

# <markdowncell>

# ### Exercício
# 
# Além do critério óbvio que buscamos um coeficiente que seja não-nulo
# (na coluna correspondente à variável),
# também é comum escolher o coeficiente de maior módulo.
# Implemente isso, e veja se o erro $Ax - b$ diminui.

# <codecell>

def lu_p(A):
    """ Fatoração PLU da matriz  A.
        Retorna duas novas matrizes  L  e  U  e uma matriz de permutações  P, esparsa.
        A matriz  A  não será alterada. """
    # Os coeficientes de A estão em A[i][j]
    eps = 1e-10 # Use este epsilon para testar se uma entrada é "zero".
    (n,m) = shape(A)
    rank = min(n,m)
    L = zeros((n, rank), dtype=A.dtype)
    U = A.copy()
    perm = list(range(n))
    for i in range(rank):
        print('Passo {}.\n  U = {}\n  L = {}\n  perm = {}'.format(i,U,L,perm))
        ii = i + argmax([U[j][i] for j in range(i,n)])
        pivot_coeff = U[ii][i]  # Tomar o novo pivô
        assert abs(pivot_coeff) > eps, 'A matriz A não tem pivôs disponíveis.'
        temp = U[i].copy()      # Permutar as linhas
        U[i] = U[ii]
        U[ii] = temp
        temp = L[i].copy()      # Permutar P com L
        L[i] = L[ii]
        L[ii] = temp
        perm[i],perm[ii] = perm[ii],perm[i] # E guardar a permutação
        print('Passo {}, permutação.\n  U = {}\n  L = {}\n  perm = {}'.format(i,U,L,perm))
            
        pivot_line = U[i][i+1:]
        L[i][i] = 1
        for ii in range(i+1,n):
            multiplier = U[ii][i]/pivot_coeff
            U[ii][i] = 0
            U[ii][i+1:] -= multiplier * pivot_line
            L[ii][i] = multiplier
    U = U[:rank]
    
    return build_permutation(perm),L,U

# <codecell>

A = array([[1,2.,3], [4,5,6], [7,8,9], [3,5,3]])
P,L,U = lu_p(A)
print(P)
print(L)
print(U)
P.todense()*L*U

# <markdowncell>

# ## Comentário sobre permutação e esparsidade
# 
# Às vezes, queremos fatorar uma matriz $A$ que **já é esparsa**.
# Seria muito bom manter a esparsidade para as componentes $L$ e $U$ ($P$ é sempre esparsa, claro!).
# Mas nem sempre isso acontece.
# Pode ser interessante permutar **as variáveis** também, para manter a esparsidade da fatoração.
# Isso corresponde a eliminar as variáveis numa ordem diferente,
# evitando introduzir entradas não-zero na matriz.
# Em geral, isso depende da estrutura de esparsidade da matriz original $A$,
# e nem sempre é garantido que funcione.

