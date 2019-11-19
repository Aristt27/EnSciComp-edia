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

# <markdowncell>

# # Integrais
# 
# A derivada de uma função (conhecida "explicitamente") sempre pode ser obtida aplicando-se as diversas regras de derivação.
# Assim, até um computador pode calcular _algebricamente_ a derivada de expressões explícitas **arbitrariamente complexas**.
# Como $f(x) = \exp(x^3 - \log(x)) + \frac{\sin(\tan(1-x))}{\cos(\cos(x) - e) + 1}$.
# 
# Mas para integrais não é tão simples obter expressões analíticas explícitas.
# De fato, desde [um teorema de Liouville de 1835][1],
# sabemos que existem funções cuja integral não pode ser expressa em "termos simples".
# Como por exemplo $f(x) = \exp(-x^2)$, portanto bastante "simples" em sua expressão.
# 
# [1]: https://en.wikipedia.org/wiki/Liouville%27s_theorem_(differential_algebra)

# <markdowncell>

# Portanto, possuir métodos para calcular derivadas numericamente é ainda mais importante.
# E, felizmente, há diversos métodos, com bastante precisão.

# <markdowncell>

# # Integrais = somas de Riemann
# 
# Vamos, aqui, nos concentrar no caso mais simples, mas também mais importante,
# do cálculo de uma integral _definida_ de uma função contínua: $$\int_a^b f(x) \, dx. $$
# 
# Uma tal integral é o limite das _somas de Riemann_: $\int f = \lim_{n\to\infty} S_n$, onde
# $$S_n = \sum_{k = 0}^{n-1} f(x_k) \cdot h$$
# onde $x_k$ será um ponto do intervalo [x + kh, x + kh + h],
# e $h = \frac{b-a}{n}$ é o tamanho de cada intervalo da partição.
# 
# Assim como fizemos para a derivada, onde "paramos" o limite antes de obter $h = 0$,
# vamos também, para a integral, calcular apenas $S_n$ para um $n$ suficientemente grande.
# E, também como fizemos para a derivada, vamos usar $h$ como variável principal.

# <markdowncell>

# ## Uma fórmula de Cauchy
# 
# Resta, apenas, dar um critério para escolher os $x_k$.
# O primeiro (historicamente) é tomar $x_k = a + kh$, e é (às vezes) descrito como "soma de Cauchy".
# (Riemann mostrou que não precisávamos de _nenhuma_ regra para os $x_k$:
# conquanto os intervalos diminuíssem e a função fosse contínua,
# as somas $S_n$ convergiriam para a sua integral.
# Mas isso não nos interessa aqui: **precisamos** dar uma regra para o computador!)

# <markdowncell>

# ### Exercício:
# Implemente a soma de Cauchy

# <codecell>

def Cauchy_n(f,a,b,n=100):
    pass

# <markdowncell>

# ## Análise de erro
# 
# O reflexo básico de toda esta seção será analisar como o erro $S_n - I$ tende a zero quando $n \to \infty$,
# ou, o que é o mesmo, quando $h \to 0$.
# 
# ### Decomposição
# 
# A primeira observação quanto ao erro é que este pode ser considerado uma _soma_ de $n$ erros diferentes.
# Isso porque, da aditividade da integral, temos:
# $$\int_a^b f(x) \, dx = \sum_{k=0}^{n-1} \left( \int_{a + k h}^{a + kh + h} f(x) \, dx \right)
#                       = \sum_{k=0}^{n-1} I _ {n,k}$$
# mantendo a mesma notação para $h$, e introduzindo as integrais $I _ {n,k}$ em cada intervalo.
# 
# Para simplificar a notação futura, chamaremos $c_k = a + kh$ a extremidade esquerda de cada intervalo da partição,
# e $d_k = a + kh + h$ a extremidade direita.
# 
# Assim, o _erro_ da estimativa da integral será:
# $$S_n - I = \sum_k \left(f(x_k)\cdot h - I _ {n,k}\right) = \sum_k e _ {n,k}. $$
# Obviamente, alguns erros podem ocorrer por excesso, e outros por falta,
# mas devemos nos previnir - matematicamente - para a pior conspiração possível.

# <codecell>


# <markdowncell>

# ### Erro de um termo
# 
# Como $f$ é contínua, temos que o valor de $f(x)$ não varia muito dentro de um dado intervalo.
# Mais ainda, conforme este intervalo diminui, menor será a variação de $f(x)$.
# Chamamos a diferença entre o mínimo e o máximo de $f$ num intervalo $[x,y]$ de _oscilação_ de $f$ no intervalo,
# muitas vezes denotada $\omega(f;x,y)$.
# 
# Lembre, além disso, que a integral é uma "área", e portanto conforme $h$ diminui,
# também diminui o intervalo de integração, e com ele o valor da integral $I _ {n,k}$.
# Portanto, o erro diminui por duas razões quando $h \to 0$: primeiramente,
# porque a função oscila menos num intervalo menor,
# segundo, porque a própria integral diminui de magnitude.
# 
# Como já estamos treinados para pensar em erros relativos,
# percebemos que a diminuição importante do erro na integral
# vem da menor oscilação, e não da "simples" redução do intervalo de integração.
# Se a oscilação não diminuir, teremos um erro relativo essencialmente igual.

# <markdowncell>

# ### Uma mudança de variáveis
# 
# Ao aplicamos uma mudança de variáveis sobre a integral $I _ {n,k}$,
# de modo que o intervalo de integração não dependa mais de $h$,
# obtemos uma fórmula mais simples para o erro
# (absoluto, ainda: como vamos somar todos para obter o "erro total",
# é mais simples trabalhar com erros absolutos).
# Primeiro, a integral:
# $$I _ {n,k} = \int_{c_k}^{d_k = c_k + h} f(x)\,dx
#             = \int_0^1 f \big( c_k + th \big) \cdot h \, dt
#             = h \int_0^1 f \big( c_k + th \big)  \, dt.$$
# E agora, o erro:
# $$e _ {n,k} = f(x_k) \cdot h - I _ {n,k} = h \int_0^1 \big( f(x_k) - f(c_k + th) \big) \, dt.$$
# 
# Podemos, daí, retirar uma estimativa do erro:
# $$
# e _ {n,k}
#    \leq h \int_0^1 \bigl| f(x_k) - f(c_k + th) \bigr| \, dt
#    \leq h \int_0^1 \omega(f; c_k, d_k) \, dt
#    =    h \cdot \omega(f; c_k, d_k).
# $$

# <markdowncell>

# ### Erro total
# 
# Como vimos anteriormente, o erro é a soma dos erros de cada termo,
# e poderia ocorrer que todos eles estivessem na mesma direção.
# Por isso, no pior dos casos, temos que
# $$
# \left|S_n - I\right|
#    \leq \sum_{k=0}^{n-1} e _ {n,k}
#    \leq \sum_{k=0}^{n-1} h \cdot \omega(f; c_k, d_k).
# $$
# 
# Como $f$ é contínua, quando $h \to 0$, cada um dos $\omega(f; c_k, d_k)$ diminui,
# e vamos, na verdade, estimar ainda mais grosseiramente: usaremos $\omega(f;h)$,
# que é a máxima variação de $f$ num intervalo (qualquer!!) de comprimento $h$.
# Assim, temos, para nossa estimativa:
# $$\left|S_n - I\right| \leq h \cdot \sum_{k=0}^{n-1} \omega(f;h) = nh \cdot \omega(f;h).$$
# Ora, da definição de $h$ temos que $b - a = nh$, logo:
# $$\textstyle E_n \leq (b-a) \cdot \omega\left(f; \frac{b-a}{n} \right). $$
# 
# Nesta fórmula, vemos bem que a importância de $n\to \infty$ (ou, equivalentemente, $h \to 0$)
# reside na redução da oscilação da função, nos pequenos intervalos de discretização.
# Além disso, como só usamos a _continuidade_ de $f$,
# esta estimativa vale qualquer que seja o método de escolha dos pontos $x_k$.

# <markdowncell>

# ## Experiência do erro
# 
# ### Exercício:
# Faça um gráfico do erro de integração de $f(x) = \sin(x)$ no intervalo $[0,\pi]$, em função do número de pontos utilizados.
# Como você faria para estimar o erro ao integrar $\exp(-x^2)$ no intervalo $[0,1]$?

# <codecell>

def f(x): return sin(x)
def g(x): return exp(-x**2)

# Continue

# <markdowncell>

# # Diminuindo o erro: a fórmula do valor médio e a fórmula dos trapézios
# 
# Vimos que o erro ao considerar somas de Riemann (na verdade, deveríamos chamar de "somas de Cauchy" estas que usam o ponto inicial)
# tende a zero porque a oscilação da função diminui conforme o tamanho do intervalo considerado diminui.
# Será que é possível (analogamente às diferenças centrais) obter fórmulas que convirjam mais rápido?
# Em geral (ou seja, para funções apenas contínuas) isso não é possível,
# pois a oscilação $\omega$ é o único mecanismo de controle que possuímos.
# Mas, seguindo o princípio geral do curso, "mais derivadas = melhor convergência",
# vamos procurar métodos que nos dêem erros menores se supusermos que a função seja derivável.
# 
# Começemos com funções uma vez deriváveis.

# <markdowncell>

# ## Erro, com derivadas
# 
# A primeira coisa a ser feita é estimar o erro da fórmula que já temos, supondo que $f$ seja derivável.
# Começamos com as somas de Cauchy, onde $x_k = c_k$:
# $$\begin{align*}
# e _ {n,k} & = h \cdot \left| f(c_k) - \int_0^1 f(c_k + th) \, dt \right|
#    = h \cdot \left| f(c_k) - \int_0^1 \big[ f(c_k) +  f'(\xi) th \big] \, dt \right|
#    = h \cdot \left| \int_0^1 f'(\xi) th \, dt \right| \\
#    & \leq h^2 \cdot \int_0^1 \max \bigl| f'(\xi) \bigr| t \, dt
#    = h^2 \cdot \max \bigl| f'(\xi) \bigr| \cdot \frac{1}{2}
# \end{align*}$$
# 
# Ao somar todos os $e _ {n,k}$, teremos então que o erro $E_n$ será, no máximo,
# $$
# \def\maxhalf{\frac{\max \bigl| f'(\xi) \bigr|}{2}}
# E_n
#   \leq \sum_{k=0}^{n-1} e _ {n,k}
#   \leq n \cdot h^2 \maxhalf
#   \leq h \cdot (b - a) \maxhalf.
# $$
# Assim, o erro da "fórmula de Cauchy" decresce linearmente com $h$.
# 
# Obs: esta melhor estimativa decorre (mais abstratamente) da seguinte relação:
# a oscilação de $f$ num intervalo é sempre menor do que o máximo (do valor absoluto) da derivada $f'$ neste mesmo intervalo.

# <markdowncell>

# ## Como diminuir o erro?
# 
# Para reduzir o erro, podemos apostar em duas vertentes.
# Ou fazemos os erros $e _ {n,k}$ se compensarem, ou reduzimos os $e _ {n,k}$ diretamente.
# A primeira estratégia depende muito da função considerada, então vamos tentar arrumar um outro método.
# Em suma, gostaríamos de reduzir o erro
# $$\big(\text{Estimativa de $f$ no intervalo $[c_k, d_k]$}\big) - \int_0^1 f(c_k + th) \, dt.$$
# 
# Inspirados pela fórmula das diferenças centrais, podemos pensar que, se calcularmos $f$ no meio do intervalo,
# em vez de no bordo, o erro pode ser menor.
# Ou seja, usaremos $f(\frac{c_k + d_k}{2})$ em vez de $f(c_k)$ como estimativa de $f$.
# Assim, em vez de calcularmos $S_n$, calcularemos
# $$M_n = \sum_{k=0}^{n-1} f \left(\frac{c_k + d_k}{2} \right) \cdot h.$$
# Esta fórmula é conhecida como **fórmula do ponto médio**.

# <markdowncell>

# ### Exercício:
# Supondo que $f$ seja **duas** vezes diferenciável, estime o erro cometido pela fórmula do ponto médio.
# 
# Refaça os gráficos para as funções seno e gaussiana.

# <markdowncell>


# <codecell>


# <markdowncell>

# ## A regra do trapézio
# 
# Outra idéia (também com cara de "simetria") para reduzir o erro é usar ambos pontos extremos em cada intervalo.
# A "estimativa para $f$" será a média de $f$ em cada um destes pontos, o que dá
# $$T_n
#   = \sum_{k=0}^{n-1} \left(\frac{f(c_k) + f(d_k)}{2}\right) \cdot h
#   = \frac{f(a) + f(b)}{2} \cdot h + \sum_{k=1}^{n-1} f(c_k) \cdot h.$$
# 
# Desta forma, o erro $e _ {n,k}$ será
# $$\begin{align*}
# e _ {n,k} & = h \cdot \left(\frac{f(c_k) + f(d_k)}{2} - \int_0^1 f(c_k + th) \, dt \right) \\
#    & = h \cdot \left(\frac{f(c_k) + f(c_k) + \int_{c_k}^{d_k} f'(x) \, dx}{2} - \int_0^1 f(c_k) + \int_0^{th} f'(c_k + u) \, du \, dt \right) \\
#    & = h \cdot \left(\frac{\int_0^h f'(c_k + u) \, du}{2} - \int_0^1 \int_0^{th} f'(c_k + u) \, du \, dt \right) \\
#    & = h \cdot \left(\int_0^h \frac{f'(c_k + u)}{2} \, dx - \int_0^h f'(c_k + u) \left(\int_{u/h}^1 dt\right) \, du \right) \\
#    & = h \cdot \left(\int_0^h f'(c_k + u) \left(\frac{1}{2} - \left(1 - \frac{u}{h}\right) \right) \, du \right) \\
#    & = h \cdot \left(\int_0^h f'(c_k + u) \left(\frac{u}{h} - \frac{1}{2} \right) \, du \right)
#        \qquad \text{e substituindo $v = \left(\frac{u}{h} - \frac{1}{2} \right)$:} \\
#    & = h \cdot \left(\int_{-1/2}^{1/2} f'(m_k + hv) v \cdot h \, dv \right) \\
#    & = h^2 \cdot \left(\int_{-1/2}^{1/2} \left( f'(m_k) + f''(\xi) hv \right) v \, dv \right) \\
#    & = h^3 \cdot \left(\int_{-1/2}^{1/2} f''(\xi) v^2 \, dv \right) \\
#    & = h^3 \frac{f''(\zeta)}{12}
# \end{align*}$$

