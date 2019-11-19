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

# <codecell>

%pylab inline

# <markdowncell>

# # Sistemas lineares
# 
# Um sistema linear é uma equação da forma $Ax = b$ onde $A$ e $b$ são dados, e $x$ é uma incógnita.
# Normalmente, só usamos este nome quando $A$ é uma matriz e $b$ um vetor, e portanto $x$ será um vetor também,
# mas em geral poderíamos tanto usar o caso em que $b$ é "maior" (por exemplo, uma matriz também)
# quando o caso em que $A$ é menor (um vetor, ou até mesmo um escalar).
# Entretanto, os casos em que $A$ é "pequena" são "fáceis",
# e o caso em que $b$ é grande não apresenta mais dificuldade do que o caso normal.
# 
# Já encontramos alguns exemplos em que aparecem equações lineares,
# por exemplo na interpolação de splines ou em mínimos quadrados.
# (Lembre que o caso da interpolação de Lagrange ou FFT a solução do sistema linear é explícita,
# devido a sua forma especial, o que já não é o caso das outras duas acima citadas.)

# <markdowncell>

# ## Observação
# 
# Como vários outros problemas matemáticos deste curso,
# também as questões relativas a sistemas lineares já foram _muito_ estudadas.
# Assim, não é de se espantar que, da mesma forma que já encontramos a função
# `scipy.interpolate.interp1d` para calcular splines,
# também já há diversas funções (desta vez, no `numpy` mesmo, em geral)
# que tratam de sistemas lineares e problemas matriciais em geral.
# 
# Vamos (re-)implementar algumas delas (e muitas vezes de forma menos eficiente ou menos correta)
# para compreender o mecanismo e os algoritmos.
# Mas, provavelmente, tanto por questões de velocidade como de praticidade,
# será bastante útil conhecer as funções do `numpy.linalg`.

# <markdowncell>

# ## Eliminação
# 
# O primeiro algoritmo de solução de sistemas lineares é conhecido por "eliminação de Gauss",
# apesar de ter sido descoberto pela primeira vez na China por volta de 150 a.C.
# e aparecer sob uma forma relativamente moderna com Newton (uns 150 anos antes de Gauss).
# 
# A idéia é bastante simples:
# seja um sistema com $n$ equações e $m$ incógnitas.
# Usa-se uma das equações (a primeira, em geral) para escrever uma das variáveis
# (também em geral a primeira) em função das outras.
# Em seguida, substitui-se esta variável em todas as outras equações,
# obtendo um sistema com $n-1$ equações e $m-1$ incógnitas,
# após reagrupar os coeficientes de cada termo.
# 
# Exemplo:
# $$ \begin{align*}
#    x + 2y + 3z & = 10 \\
#   4x + 5y + 6z & = 15
# \end{align*} $$
# Obtemos $x = 10 - 2y - 3z$ que na segunda equação dá
# $$ \begin{align*}
#   4(10 - 2y - 3z) + 5y + 6z & = 15 \\
#   40 - 8y - 12z + 5y + 6z & = 15 \\
#   -3y - 6z & = - 25
# \end{align*} $$

# <markdowncell>

# ## Industrializando a eliminação: notação matricial
# 
# Um dos méritos de Gauss foi ter inventado a notação matricial
# (inicialmente, para resolver problemas de aritmética!)
# e com isso poupar muito espaço e tempo ao se resolver sistemas.
# Com esta nova roupagem, foi possível refinar o método acima para torná-lo
# praticamente automático.
# 
# Observe que _eliminar a primeira variável da segunda equação, usando a primeira_
# pode ser obtido ao multiplicar a primeira equação por $-4$ e somar à segunda.
# Assim, podemos trabalhar unicamente com os coeficientes
# (aliás, se você pensar bem, o **nome** que damos às incógnitas é totalmente irrelevante)
# num "dispositivo prático":
# 
# $$ \begin{bmatrix}1 & 2 & 3 & \vert & 10 \\ 4 & 5 & 6 & \vert & 15 \end{bmatrix} $$
# $$ \begin{bmatrix}1 & 2 & 3 & \vert & 10 \\
#   4 + (-4)\times 1 & 5 + (-4)\times 2 & 6 + (-4) \times 3 & \vert & 15 + (-4)\times 10
#   \end{bmatrix} $$

# <markdowncell>

# ### Exercício
# 
# Implemente a eliminação para matrizes.

# <codecell>

def elim(A,b):
    """ Elimina as equações do sistema  Ax = b.
        A matriz  A  será modificada, ficando sob forma triangular superior, e b será o vetor correspondente ao novo sistema. """
    # Os coeficientes de A estão em A[i][j]
    #for i in #:
    #    for ii in #:
    #        for j in #:
    #
    # Como A e b serão modificados, não é preciso retorná-los

# <codecell>

def elim(A,b):
    """ Elimina as equações do sistema  Ax = b.
        A matriz  A  será modificada, ficando sob forma triangular superior, e b será o vetor correspondente ao novo sistema. """
    # Os coeficientes de A estão em A[i][j]
    (n,m) = shape(A)
    for i in range(min(n,m)):
        pivot_coeff = A[i][i]
        pivot_line = A[i][i+1:]
        for ii in range(i+1,n):
            multiplier = A[ii][i]/pivot_coeff
            A[ii][i] = 0
            A[ii][i+1:] -= multiplier * pivot_line
            b[ii] -= multiplier * b[i]
        #print_matrix_fmt("{: 6.2g}", A)
        #print()

# <codecell>

def print_matrix_fmt(fmt, A):
    for line in A:
        for elm in line:
            print(fmt.format(elm), end=' ')
        print()

# <markdowncell>

# Para testar, use o sistema que já resolvemos:

# <codecell>

A = array([[1, 2, 3], [4, 5, 6]])
b = array([10, 25])
elim(A,b)
print(A)
print(b)

# <codecell>

A = array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = array([10, 25, 12])
elim(A,b)
print(A)
print(b)

# <markdowncell>

# E quando você estiver confiante, elimine em sistemas de maior dimensão!

# <codecell>

A = rand(8, 10)
b = rand(12)

# <codecell>

elim(A,b)
np.set_printoptions(precision=4,linewidth=100)#, suppress=True) # Para ficar com cara de matriz no print
print(A)
print(b)

# <markdowncell>

# ## Substituição
# 
# Ao eliminar, obtemos um sistema cada vez menor, até que ele tenha $n-m$ equações e $0$ incógnitas,
# ou o contrário: $0$ equações e $m-n$ incógnitas.
# 
# ### O caso simples: $n = m$
# 
# Se $n$ = $m$, não restam nem equações nem incógnitas, e portanto o nosso trabalho acabou.
# Na verdade, vamos parar uma etapa antes, com uma equação e uma incógnita,
# o que dará o valor desta.
# Em seguida, usamos este valor que acabamos de descobrir para determinar a outra incógnita na etapa $(2,2)$.
# E assim por diante, vamos determinando sucessivamente os valores de cada uma das incógnitas,
# até que as tenhamos todas.
# 
# ### O caso subdeterminado: $m > n$
# 
# Temos mais equações do que incógnitas,
# então vamos obter, ao final, $m-n$ incógnitas "livres",
# que não estão sujeitas a nenhuma relação.
# Podemos proceder de várias formas, mas a mais simples é fixá-las todas em zero
# e a partir daí aplicar o procedimento anterior nas outras variávies,
# que têm equações associadas.
# 
# ### O caso superdeterminado: $n > m$
# 
# Aqui, temos o contrário: ao final, obtemos $n-m$ equações **sem** incógnitas.
# Assim, a menos de ter muita sorte e que estas equações sejam todas equivalentes a $0 = 0$,
# este sistema será impossível.
# Mais uma vez, há algumas formas de continuar,
# dentre as quais, determinar a "solução de mínimos quadrados" associada.

# <markdowncell>

# ### Exercício
# 
# Implemente a substituição para o caso $n = m$.
# O seu programa deve testar se a matriz $A$ é triangular superior
# e que o par $(A,b)$ corresponde efetivamente ao caso $n = m$.

# <codecell>

def subst_solve(A,b):
    # Checar A e b
    #
    #
    #
    
    # Resolver e determinar x
    #
    #
    #
    return x

# <codecell>

def subst_solve(A,b):
    # Checar A e b
    (n,m) = shape(A)
    assert len(b) == n, 'A and b dimensions do not agree'
    assert all([all(A[i][:i] == 0)] for i in range(1,n)), 'A is not in row-reduced form'

    if any(b[min(n,m)+1:] != 0):
        print('System is impossible: contains 0 = 1')
        return
    
    # Resolver e determinar x
    x = [0]*m
    for i in range(n-1,-1,-1):
        acc = b[i]
        for j in range(i+1,n):
            acc -= A[i][j]*x[j]
        x[i] = acc/A[i][i]
        
    return array(x)

# <markdowncell>

# Verifique resolvendo um sistema aleatório,
# e compare com o resultado de `solve`.

# <codecell>

A = rand(10,10)
b = rand(10)
elim(A,b)
subst_solve(A, b)

# <codecell>

solve(A,b)

# <markdowncell>

# Você também pode verificar "na mão" fazendo o produto:

# <codecell>

numpy.dot(A,_) - b

# <markdowncell>

# O que é melhor, é que este código também resolve sistemas sobredeterminados:

# <codecell>

A = rand(10,12)
b = rand(10)
elim(A,b)
subst_solve(A,b)

# <codecell>

dot(A,_) - b

