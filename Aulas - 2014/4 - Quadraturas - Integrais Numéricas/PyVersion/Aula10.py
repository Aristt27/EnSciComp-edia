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
#     1. Primeiras aproximações: Fórmula do ponto médio e dos trapézios (Seções 4.3.1 e 4.3.2)
#     2. Melhores aproximações: Fórmula de Simpson e métodos iterativos (Seções 4.3.3 e 4.5)

# <markdowncell>

# # A fórmula de Simpson
# 
# Em vez de usarmos uma aproximação "de Riemann" para a integral,
# vamos usar a idéia principal das outras demonstrações:
# queremos estimar com maior precisão as integrais
# $$ I _ {n,k} = \int_{c_k}^{d_k = c_k + h} f(x)\,dx. $$
# 
# É claro (pense porquê!) que se só tivermos acesso a um ponto, o melhor que podemos fazer é usar o ponto médio $m_k = \frac{c_k + d_k}{2}$.
# Se só tivermos dois pontos, a situação é mais complicada (...), usando $c_k$ e $d_k$ nem fica melhor do que apenas o ponto médio.
# Mas podemos combinar os pontos extremos $c_k$ e $d_k$ com o ponto médio, e ter 3 pontos.
# 
# Com um pouco de trabalho, podemos mostrar que a combinação certa será:
# $$ I _ {n,k} \sim \frac{h}{6} \big[ f(c_k) + 4 f(m_k) + f(d_k) \big]. $$

# <markdowncell>

# ### Exercício
# 
# Implemente a fórmula de Simpson (não esqueça que você tem que somar todas as aproximações dos $I _ {n,k}$!).
# Faça um gráfico do erro em função de $n$ (ou $h$).

# <codecell>


# <markdowncell>

# ### Exercício
# 
# Suponha que $f$ é 4 vezes derivável, e calcule o erro de aproximação.

# <markdowncell>

# ### Exercício
# 
# É melhor usar a fórmula de Simpson com passo $0.1$ ou a fórmula do ponto médio com passo $0.05$? (Note que o passo foi escolhido de forma a que ambas calculem aproximadamente o mesmo número de termos de $f$.) E se fosse $0.01$ e $0.005$?

# <markdowncell>

# # Fórmulas adaptativas
# 
# O problema maior da integração é que, ao diminuir $h$, aumentamos o tempo de cálculo.
# O que gostaríamos de fazer é, então, poder variar $h$ ao longo do algoritmo,
# em função do intervalo que estejamos calculando.
# 
# Ou seja, vamos ter que achar, dependendo da função, os valores de $h$ "certos".
# Mais ainda, gostaríamos que o método fosse "de passo variável":
# isso permite "dar um zoom" quando a função variar muito (segunda ou quarta derivada de $f$,
# dependendo de usar ponto médio ou Simpson)
# 
# ## Recursão, o retorno da vingança
# 
# Uma solução para este problema é recursiva
# 
# 1. Tomamos um intervalo $I$ sobre o qual vamos calcular uma "boa" aproximação da integral
# 2. Usamos alguma fórmula para calcular sua aproximação $A$
# 3. Usamos outra fórmula, teóricamente mais precisa, para calcular uma segunda aproximação $A'$.
# 4. Com $A$ e $A'$, podemos estimar o **erro** cometido pelas integrais
#     1. Se ambas aproximações estiverem próximas, o erro deve ser pequeno, e usamos $A'$.
#     2. Senão, dividimos o intervalo em duas partes (esquerda e direita, olhaí a bisseção) $I_e$ e $I_d$,
#        calculamos ambas as integrais com precisão suficiente, e usamos a soma.

# <codecell>

def simpson_adaptativo(f, a,b, tol=1e-6):
    h = (b-a)
    m = a + h/2.

    fa = f(a)
    fb = f(b)
    fm = f(m)
    
    # II e III
    Igrossa = h*(fa + 4*fm + fb)/6
    Ifina   = h*(fa + 4*f((a+m)/2) + 2*fm + 4*f((m+b)/2) + fb)/12
    
    # IV
    if abs(Igrossa - Ifina) < tol: return Ifina
    else:
        esquerda = simpson_adaptativo(f, a,m, tol/2)
        direita  = simpson_adaptativo(f, m,b, tol/2)
        return esquerda+direita

# <codecell>

%pylab inline

# <codecell>

simpson_adaptativo(sin, 0,10)

# <codecell>

1 - cos(10)

# <codecell>

Out[4] - Out[3]

# <codecell>

def simpson_adaptativo(f, a,b, tol=1e-6):
    def loop(a,b,m,fa,fb,fm,Icur,tol):
        h = (b-a)
        m1 = a + h/4.
        m2 = b - h/4.
        fm1 = f(m1)
        fm2 = f(m2)
    
        # II e III (II = Iprev)
        Ileft  = h*(fa + 4*fm1 + fm)/12
        Iright = h*(fm + 4*fm2 + fb)/12
        Inext = Ileft + Iright
    
        # IV
        if abs(Icur - Inext) < tol: return Inext
        else:
            esquerda = loop(a,m,m1,fa,fm,fm1, Ileft, tol/2)
            direita  = loop(m,b,m2,fm,fb,fm2, Iright, tol/2)
            return esquerda+direita
    
    m = (a+b)/2.
    h = (b-a)
    fa = f(a)
    fb = f(b)
    fm = f(m)
    I0 = h*(fa + 4*fm + fb)/6
    I = loop(a,b,m,fa,fb,fm, I0,tol)
    
    return I

# <codecell>

simpson_adaptativo(sin,0,1)

# <codecell>

1 - cos(1)

# <codecell>


