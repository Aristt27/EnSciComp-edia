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
#     1. **Sobrou a fatoração LU**

# <codecell>

%pylab inline

# <markdowncell>

# ## Fatoração LU
# 
# Um subproduto da eliminação é a fatoração LU: podemos escrever $A = LU$ onde $L$ é triangular inferior (_lower_)
# e $U$ é triangular superior (_upper_).
# 
# ### Exercício
# 
# Deduza o algoritmo que permite obter $L$, sabendo que $U$ será a matriz resultante da eliminação.
# 
# Deduza também que é possível guardar $L$ e $U$ no mesmo espaço de $A$.
# 
# Note que, da mesma forma que é possível resolver $Ux = b'$ com relativa facilidade (substituição),
# também é possível resolver $Ly = b$ com a mesma facilidade.
# Assim, a fatoração LU permite "quebrar" o problema de resolver $Ax = b$ em duas etapas:
# primeiro, resolva $Ly = b$; em seguida, resolva $Ux = y$.

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

# Use, de novo, a matriz fácil para testes:

# <codecell>

A = array([[1, 2, 3], [4, 5, 6]])
L,U = lu(A)
print(L)
print(U)
dot(L,U) - A

# <markdowncell>

# E agora, use matrizes aleatórias para verificar que realmente tudo funciona como previsto:

# <codecell>

np.set_printoptions(precision=4,linewidth=100)#, suppress=True) # Para ficar com cara de matriz no print

# <codecell>

A = rand(4,6)
L,U = lu(A)
print(L)
print(U)
dot(L,U) - A

# <codecell>

A = rand(6,4)
L,U = lu(A)
print(L)
print(U)
dot(L,U) - A

# <codecell>

A = rand(6,6)
L,U = lu(A)
print(L)
print(U)
dot(L,U) - A

# <markdowncell>

# ## Pivôs e permutações
# 
# Nem sempre é possível obter a fatoração LU diretamente, pois podemos encontrar um zero na diagonal,
# o que torna impossível usar a equação para eliminar.
# A saída é permutar as equações para poder continuar.
# Isso não muda em nada as variáveis (claro!) mas mudará $b$, pois vamos também permutar seus elementos.
# Assim, é preciso memorizar esta operação, o que é feito em geral numa
# "matriz de permutações".
# 
# ### Exercício
# 
# Além do critério óbvio que buscamos um coeficiente que seja não-nulo
# (na coluna correspondente à variável),
# também é comum escolher o coeficiente de maior módulo.
# Implemente isso.

