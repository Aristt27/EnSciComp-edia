# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Plano de hoje
# -------------
# 
# 1. Ambiente de programação
# 2. Usando o computador para calcular    
#     1. **Indução e algoritmos recursivos: fatoriais, binomiais, Fibonacci, Hanói**
#     1. **Aproximações sucessivas: bisseção, Newton**

# <markdowncell>

# # Funções recursivas
# 
# Já vimos a idéia que funções podem chamar outras funções em uma "torre".
# Uma das possibilidades que isto nos dá é que funções chamem a si mesmas, sendo _recursivas_.
# Isso é muito importante porque vários problemas possuem uma solução naturalmente recursiva.
# Em geral, isto se deve a uma dentre as seguintes razões:
# 
# - A definição do problema é recursiva (fatorial, Fibonacci)
# - Os dados manipulados pela função são recursivos (listas, árvores, números inteiros).
# - O problema pode ser separado em subproblemas similares (Hanói)
# - O problema pode ser formulado em uma _seqüência de aproximações_ da solução real.
# 
# Este último é especialmente interessante para nós.
# Vejamos como ele se comporta no caso da aula passada do _próximo número real_:

# <codecell>

def prox_real(x):
    assert (x > 0)
    def dividir(x,y):
        z = (x+y)/2
        if (z == x) or (z == y):
            return y
        else:
            return dividir(x,z)
    return dividir(x, 2*x)

# <markdowncell>

# Vejamos agora um outro exemplo, clássico: os fatoriais.
# Lembramos que o fatorial de um número inteiro $n$ é dado por:
# $$ n! = \cases {1 & se $n = 0$\\ n \cdot (n-1)! & se $n > 0$} $$
# 
# **Exercício**: implemente a função fatorial usando um algoritmo recursivo.
# A função `isinstance` diz se um argumento pertence a uma certa classe.

# <codecell>


# <markdowncell>

# Funções com mais de um argumento também podem ser usadas em recorrências,
# mas estabelecer qual será esta recorrência pode ser mais difícil.
# 
# **Exercício**: implemente uma função que calcule números binomiais usando recorrência (e não os fatoriais).

# <codecell>


# <markdowncell>

# ## O método da bisseção
# 
# O método da bisseção (bi = dois, seção = cortar) consiste em cortar um intervalo em dois a cada passo do programa.
# Já encontramos esta idéia no caso do "próximo número real",
# mas ela é realmente útil para calcular zeros de funções.
# Se $f$ é uma _função contínua_ de $R$ em $R$, e que muda de sinal entre os pontos $a$ e $b$,
# então (pelo **Teorema do valor intermediário**) existe uma raiz de $f$ entre $a$ e $b$.

# <codecell>

def bissecao(f, a, b):
    assert(f(a) * f(b) <= 0)
    
    def dividir(x,y):
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

    return dividir(a,b)

# <markdowncell>

# Esta função vai até o mais preciso possível que o seu computador consegue para a função.
# Isto pode parecer bom, mas nem sempre é a melhor solução possível.
# 
# **Exercício**: adicione um argumento extra, `tol` (tolerância) para achar uma solução a menos de `tol` do valor real.

# <codecell>

def bissecao(f, a, b, tol):
    pass

# <markdowncell>

# Poderíamos ter definido esta funçao como `bissecao(f, a, b, tol=1e-6)`.
# Isso cria `tol` como um _argumento opcional_ com um _valor padrão_ de `1e-6`.
# Assim, ao chamar a função simplesmente como `bissecao(f, -2., 3.)`,
# o Python entende que o argumento `tol` será usado com o seu valor padrão.
# Esta técnica é muito útil para apresentar uma interface
# 
# - "simples", onde o usuário usa apenas os argumentos obrigatórios,
# 
# e uma interface
# 
# - "expert", através da qual o usuário pode ter um melhor controle do programa, quando este for necessário

# <markdowncell>

# ## Fibonacci e performance
# 
# Os números de Fibonacci são definidos por uma recorrência:
# \begin{align} & F_0 = F_1 = 1 \\ & F_{n+2} = F_{n+1} + F_n \end{align}
# 
# **Exercício**: Implemente uma função recursiva que calcule números de Fibonacci.

# <codecell>


# <markdowncell>

# Esta função pode ficar muito lenta já para argumentos relativamente pequenos (n = 100).
# O problema é que esta função calculará $F_{100}$ ao somar tantos `1`s quanto necessário.
# Como $F_{100}$ já é bastante grande, isso implica em muitos `1`s, e logo muitas contas.
# Isso ocorre porque, ao expandir a recorrência, calculamos várias vezes o mesmo $F_k$.
# 
# Uma solução para isto é calcular os números de Fibonacci **ao contrário**,
# _subindo_ a recorrência em vez de descer.
# 
# **Exercício**: implemente uma função (não necessariamente recursiva) que calcule os $F_k$ apenas uma vez.

# <codecell>


# <markdowncell>

# Existem outras formas de calcular os números de Fibonacci, de acordo com o objetivo (leia-se, _precisão_),
# que são mais eficientes tanto em memória quanto em tempo de processamento.
# Mas não vamos falar mais disso.

# <markdowncell>

# ## O método de Newton para calcular raízes
# 
# O método da bisseção é bastante geral (funciona para qualquer função contínua!),
# e converge "geométricamente rápido": o erro na etapa $n+1$ será, aproximadamente,
# a metade do erro da etapa anterior.
# 
# Para funções cuja derivada é conhecida, entretanto,
# o _método de Newton_ é uma alternativa muito poderosa,
# pois converge com maior velocidade.
# Além disso, ele dispensa conhecer dois pontos onde o sinal da função seja diferente.
# Vejamos como ele funciona.

# <markdowncell>

# ### Idéia geométrica
# 
# Dado um ponto $(x,f(x))$ no gráfico de $f$, se traçarmos a tangente,
# esta será uma boa aproximação da função "perto" de $x$.
# Assim, seguimos esta reta tangente até que ela encontre o eixo-$x$ no ponto $(z,0)$,
# esperando que esta interseção esteja próxima da verdadeira raiz,
# que é a interseção da _curva_ descrita por $f$ e o eixo-$x$.
# 
# Em fórmulas, temos:
# $$ (z,0) \in T = \big\{ (x, f(x)) + t (1, f'(x)) \mid t \in R \big\} $$
# para o ponto $(z,0)$ que está na reta tangente $T$ e também no eixo-$x$
# (pois sua coordenada $y = 0$).
# Resolvendo o sistema, encontramos
# $$ z = x - \frac{f(x)}{f'(x)}. $$

# <markdowncell>

# A presença de $f'(x)$ no denominador mostra que este método funciona **mal**
# quando está próximo de uma raiz de $f'$.
# Além disso, o método de Newton não fornece um "intervalo de confiança" como no caso da bisseção.
# 
# Assim, é muito importante ter aqui um critério de convergência para poder parar as iterações.
# Em geral, este pode ser dado por três diferentes parâmetros:
# 
# - O número de iterações feitas: se estamos calculando "há muito tempo", talvez o método esteja "perdido"
# - A distância de $f(x)$ para zero: talvez já tenhamos calculado algo suficientemente próximo de uma raiz,
#     se $\lvert f(x)\rvert << 1$
# - A distância de $x$ para um zero: se a diferença entre dois pontos sucessivos ($x$ e $z$ no nosso exemplo)
#     for pequena, então é _provável_ que estejamos perto de uma raiz.

# <codecell>


