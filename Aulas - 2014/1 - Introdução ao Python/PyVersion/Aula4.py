# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Plano de hoje
# -------------
# 
# 1. Ambiente de programação
#     1. . . .
#     6. **MatPlotLib: gráficos**
# 
# 2. Usando o computador para calcular    
#     1. Indução e algoritmos recursivos
#     1. **Aproximações sucessivas: bisseção, Newton**

# <markdowncell>

# # Rodar, desenhar, entender
# 
# ## `Plot` = Sobrevivência na selva
# 
# O comando mais importante é, sem dúvida, `plot`.
# Ele tem diversas opções (veja a ajuda correspondente), mas em geral as configurações-padrão são bastante razoáveis.
# Vejamos alguns exemplos.

# <codecell>

# Plotar uma lista, usando o índice como coordenada $x$

lista_random = rand(55)
plot(lista_random);

# <codecell>

# A segunda forma mais útil é plotar uma função.
x = range(100)
y = sin(x)
plot(x, y);

# <codecell>

# A terceira, variação da anterior, é uma curva paramétrica
t = arange(0,10,0.1)
xt = t**2 * sin(t)
yt = t*cos(t)
plot(xt,yt);

# <markdowncell>

# Neste exemplo, usamos `arange`, que é uma função do _NumPy_, que retorna um "vetor numérico".
# A grande vantagem destes vetores com relação às listas é que é possível fazer operações numéricas (coordenada-a-coordenada)
# com mais facilidade e clareza do que com uma lista "normal" do Python.
# Isso será bastante útil durante o curso, seja para gerar dados, seja para escrever programas mais simples.
# 
# E a `matplotlib` usa vetores do NumPy automaticamente.

# <markdowncell>

# ## Algumas opções de argumentos de `plot`

# <codecell>

# Mudando a "linha"
plot(lista_random, 'rx');

# <codecell>

# Pode haver linhas _E_ marcadores num mesmo gráfico.
# Isso pode ser feito com um comando
plot(xt, yt, 'go-')

# Ou com argumentos, onde podemos ter mais variação ainda (mas não exagere!)
figure()
plot(xt, yt, color='green', linestyle='dashed', marker='o', markerfacecolor='red', markersize=4);

# <markdowncell>

# ## Outros gráficos úteis
# 
# - `semilogx`, `semilogy`, `loglog`: escalas logarítmicas
# - `matshow` para "plotar" dados em função de duas variáveis (uma matriz)
# - `plot_surface` para fazer o gráfico de uma superfície dependendo de 2 variáveis (uma matriz, ou três matrizes como argumento)
# - `subplot` para fazer gráficos lado a lado

# <markdowncell>

# ## Informação ao leitor
# - `legend` para dar nomes às curvas (se houver mais de uma)
# - `ylabel` e `xlabel` para dar nome aos eixos

# <codecell>

subplot(211)
plot(t, t*t, 'ro', label='square')
plot(t, t*t*t, 'g-.', label='cube')
legend()

subplot(212)
plot(t*t, t, 'bD', label='inversa da square')
plot(t*t*t, t, 'c*', label='inversa da cube')
legend(loc=0);

# <markdowncell>

# ### Exercício resolvido:
# Fazer um gráfico com os dois pontos extremos dos intervalos do método da bisseção.

# <codecell>

def bissecao(f, a, b):
    assert(f(a) * f(b) <= 0)
    esq = []
    dire = []
    
    def dividir(x,y):
        esq.append(x)
        dire.append(y)
        z = (x+y)/2
        if (z == x) or (z == y):
            fx = f(x)
            fy = f(y)
            if (abs(fx) <= abs(fy)):
                return x
            else:
                return y

        if (f(x)*f(z) <= 0):
            return dividir(x,z)
        else:
            return dividir(z,y)

    return esq, dire, dividir(a,b)

# <codecell>


# <codecell>

def bissecao_dados(f,a,b):
    esquerda = [a]
    direita  = [b]
    
    z = (a/2 + b/2)
    fa = f(a)
    fb = f(b)
    while (z != a and z != b):
        fz = f(z)
        if (fz * fa <= 0):
            esquerda.append(a)
            direita.append(z)
            b = z
            fb = fz
        else:
            esquerda.append(z)
            direita.append(b)
            a = z
            fa = fz
        z = (a/2 + b/2)
        
    return (z, esquerda, direita)

# <codecell>

def plot_bissecao(z, esquerda, direita):
    esquerda = array(esquerda)
    direita = array(direita)
    plot(esquerda, label='liminf')
    plot(direita, label='limsup')
    legend()
    figure()
    subplot(121)
    semilogy(direita - esquerda)
    subplot(122)
    semilogy(direita - z)
    semilogy(z - esquerda)
    

# <codecell>

f = cos
a = 0.
b = 3.

z, esq, dire = bissecao_dados(f, a, b)
print("Uma raiz de f entre {} e {} é {}.".format(a, b, z))
plot_bissecao(z, esq, dire)

# <markdowncell>

# Tudo isso (e muito, muito mais) em http://matplotlib.org/users/ (página oficial da documentação), http://matplotlib.org/users/beginner.html (guia para "iniciantes", tem bastante coisa), http://matplotlib.org/faq/howto_faq.html#plotting-howto (várias dicas, com exemplos, para fazer coisas mais ou menos avançadas)

# <markdowncell>

# # Complexidade, exemplos
# 
# Lembremos da função fatorial

# <codecell>

def fatorial(n):
    assert (isinstance(n, int))
    assert (n >= 0)
    
    p = 1
    while(n > 1):
        p *= n
        n -= 1

    return p

# <markdowncell>

# Vejamos quanto tempo leva para calcular alguns fatoriais.
# Para isso, utilisamos o módulo `timeit`.

# <codecell>

import timeit

# <codecell>

# No ipython, temos o %timeit, um "comando mágico":
%timeit(fatorial(10))
%timeit(fatorial(100))
%timeit(fatorial(1000))
%timeit(fatorial(10000))

# <codecell>

# Senão, podemos usar o comando Python "puro"
timeit.timeit(number=100, setup="from __main__ import fatorial", stmt="x = fatorial(1000)")

# <markdowncell>

# ## Dois códigos, duas performances

# <codecell>

def binom(n,k):
    assert(isinstance(n,int) and isinstance(k,int))
    assert(0 <= n and 0 <= k and k <= n)
    
    i = 0
    p = 1
    while(i < k):
        p = (p * (n-i))/(i+1)
        i += 1
    return p

# <codecell>

def slow_binom(n,k):
    assert(isinstance(n,int) and isinstance(k,int))
    assert(0 <= n and 0 <= k and k <= n)
    
    return fatorial(n)/fatorial(k)/fatorial(n-k)

# <codecell>

print("20 escolhe 10")
%timeit(binom(20,10))
%timeit(slow_binom(20,10))

print("200 escolhe 10")
%timeit(binom(200,10))
%timeit(slow_binom(200,10))

print("200 escolhe 100")
%timeit(binom(200,100))
%timeit(slow_binom(200,100))

# <codecell>

print("Rápida")
%timeit(binom(20,10))
%timeit(binom(200,10))
%timeit(binom(2000,10))
%timeit(binom(20000,10))

print("\nDevagar")
%timeit(slow_binom(20,10))
%timeit(slow_binom(200,10))
%timeit(slow_binom(2000,10))
%timeit(slow_binom(20000,10))

# <codecell>


