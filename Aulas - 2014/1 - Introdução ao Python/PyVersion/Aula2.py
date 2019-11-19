# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Plano de hoje
# -------------
# 
# 1. Ambiente de programação
#     1. Interpretador interativo, Interpretador de arquivos, iPython
#     1. Revisão da sintaxe de python
#     1. **Funções**
#     1. **Números "reais"**
#     1. NumPy, SciPy: Matrizes e o mais
#     1. MatPlotLib: gráficos
# 
# 2. Usando o computador para calcular    
#     1. **Indução e algoritmos recursivos: fatoriais, binomiais, Fibonacci, Hanói**

# <markdowncell>

# Funções
# =======
# 
# Uma função consolida uma fórmula (ou sucessão de fórmulas) com um nome simples.

# <codecell>

def sq(x):
    return x*x

# <codecell>

def hyp(a,b):
    return sqrt(a*a + b*b)

# <codecell>

def quinto_menor(li):
    s = sorted(li)
    if len(s) < 5:
        return None
    else:
        return s[4] # /!\ O quinto elemento tem índice 4.

# <markdowncell>

# Uma função não precisa retornar (ou seja, terminar com o comando `return`). Muitas vezes, funções que não retornam nada são chamadas de **subrotinas** ou (em inglês) **_procedures_**.
# 
# Invente uma subrotina útil.

# <codecell>


# <markdowncell>

# A grande utilidade das funções é organizar o código. Além disso, se você escolher um bom /nome/ para as suas funções, o seu programa sera também mais fácil de entender. (É claro que usar nomes muito grandes tem seus inconvenientes, também)
# 
# Outra característica importante das funções é que você pode ter uma "torre de funções", com funções mais complicadas / especializadas utilizando funções mais simples / genéricas. Por exemplo, podemos re-escrever a função da hipotenusa assim:

# <codecell>

def hyp(a,b):
    return sqrt(sq(a) + sq(b))

# <markdowncell>

# Esta idéia de "torre" é muito similar ao que ocorre em matemática. Por exemplo, vetores:
# 
# Um **vetor** $v$ é um elemento de $R^n$. A **norma** de um vetor é dada pela raiz quadrada da soma dos quadrados de suas coordenadas. A **distância** entre dois vetores é dada pela norma da diferença de ambos. A **diferença** entre dois vetores é o vetor cujas coordenadas são as diferenças entre as suas coordenadas.

# <codecell>

def norma2(v):
    return sum([sq(x) for x in v])

def norma(v):
    return sqrt(norma2(v))

# <codecell>

def diff(v1, v2):
    assert(len(v1) == len(v2))
    return [x1 - x2 for (x1,x2) in zip(v1, v2)]

# <codecell>

def dist(v1, v2):
    return norma(diff(v1, v2))

# <markdowncell>

# Ao longo do curso, vamos construir várias funções que representem os diversos procedimentos que estudamos. Assim, teremos sempre à disposição um conjunto de operações matemáticas tanto _abstratas_ (que utilizaremos para raciocinar e **demonstrar**) quando _concretas_ (que utilizaremos para calcular e **experimentar**)

# <markdowncell>

# ### Exercício
# 
# O **ângulo** $\theta$ entre dois vetores é dado pela fórmula
# $$\langle u, v\rangle = \lvert u\rvert \cdot \lvert v\rvert \cdot \cos(\theta). $$
# 
# Implemente uma função que calcule o **produto interno** ($\langle , \rangle$) de dois vetores,
# e em seguida uma que calcule o ângulo entre os vetores.

# <codecell>


# <markdowncell>

# Números "reais"
# ===============
# 
# É impossível representar todos os números reais no computador: este tem uma capacidade finita, enquanto aqueles são infinitos (e, pior, não-enumeráveis...). Assim, utilizaremos uma _aproximação_ dos mesmos.
# 
# A primeira observação é que, num computador, sempre existe um _maior número "real"_, pois um computador é capaz de representar apenas uma quantidade finita de números.
# A segunda é que sempre existe um _próximo número "real"_, mais uma vez porque há apenas uma quantidade finita deles.
# 
# Dado isto, uma idéia simples para representar números reais seria considerar que a cada número inteiro corresponde um número real, através de uma fórmula do tipo
# $$ real = \frac{inteiro}{10^9} $$
# Isto é o que chamamos **ponto fixo**.
# Este nome vem de imaginarmos que existe um ponto (implícito) no número inteiro que o computador vê,
# e cuja posição é fixa (dada pelo $10^9$).
# 
# É claro que a escolha de $10^9$ para o denominador é completamente arbitrária,
# e diferentes sistemas poderiam escolher diferentes denominadores.
# Assim, uma representação em ponto fixo é dada por
# $$\frac{inteiro}{den} \qquad \text{onde o denominador $den$ está fixo.}$$

# <markdowncell>

# ###Exercícios
# 1. Descubra qual é o maior inteiro que o seu computador conhece
#     1. Deduza a amplitude (o **menor** "real" maior que zero, além do **maior** "real") dos números que podem ser representados em ponto fixo se quisermos 15 casas decimais significativas.
#     1. Idem para 5, 10 e 20 casas decimais.
#     1. Use a Wikipédia e descubra uma constante física que seja conhecida com o maior número possível de casas decimais.
#     1. Observe a **amplitude** das constantes físicas que você procurou.
#     1. Conclua.
# 
# 1. Usando a finitude dos números "reais", escreva uma função que calcula o próximo número "real".
#     1. Como seria a função para o número "real" _anterior_?
#     1. O seu computador usa pontos fixos?
# 
# 1. Use a finitude dos números "reais" para desenvolver um algoritmo que calcule raízes (aproximadas) de uma função contínua.
#     1. Esse algoritmo pode usar uma idéia similar à do exercício anterior.
#     1. Escreva um programa que implemente este algoritmo.

# <codecell>


# <codecell>


# <markdowncell>

# ###Números de ponto flutuante (Konrad Zuse, 1936)

# <markdowncell>

# Uma variação óbvia desta estrutura é representar o número real sempre em duas partes: um numerador e um denominador, ambos inteiros. Assim, na verdade, representamos apenas números racionais (não que isso seja um problema, já que temos apenas uma quantidade finita de números disponíveis), mas ganhamos em flexibilidade.
# 
# Porém, não faz muito sentido poder usar todos os números inteiros no denominador: isso geraria muita redundância!
# Vamos pensar, então, que o denominador pode mudar, mas não para "qualquer coisa", e vamos pensar, principalmente, qual é o nosso objetivo ao representar os números reais de forma aproximada.

# <markdowncell>

# Num sistema discreto de números "reais", o erro que cometemos ao usar aproximações é, no máximo,
# a diferença entre os dois números consecutivos do sistema que estão "logo abaixo" e "logo acima" do verdadeiro número real.
# 
# E, na maior parte das vezes, o que nos interessa são erros relativos, e não erros absolutos.
# Se uma aula leva 120 minutos ou 119, não há muita diferença.
# Se uma aula leva 2h ou 1h, há muita diferença!
# Isso explica porque fixar o denominador não é, na maior parte das vezes, uma boa solução.
# O erro relativo entre $\frac{2}{den}$ e $\frac{1}{den}$ é muito maior do que o erro entre $\frac{120}{den}$ e $\frac{119}{den}$.
# 
# Assim, a nossa escala deve ser adaptada aos erros relativos, e é a escala logarítmica.
# (Se você está preocupado com números negativos, você está certo;
# mas vamos deixar isso de lado por enquanto, e pensar que o sinal do número pode ser separado do resto
# - como realmente ocorre!)
# Deixando o zero de lado (que é especial para o logaritmo), podemos representar um número sob a forma
# $$base^{inteiro}, \qquad \text{onde a base $base$ está fixa.}$$
# 
# Assim, o erro relativo entre dois números nesta representação é o erro entre $1$ e $base$,
# que é o mesmo que entre $base^1$ e $base^2$, e entre quaisquer dois números consecutivos.
# (menos o zero; erros relativos com zero são sempre muito grandes... mais disso, mais tarde)
# Se escolhermos a $base$ suficientemente próxima de $1$, teremos erros relativos suficientement pequenos, em toda a escala!

# <markdowncell>

# Mas há um problema com esta representação: as operações de soma e subtração de números "reais" serão muito custosas.
# As de multiplicação e divisão, por outro lado, podem operar _diretamente_ com os números inteiros correspondentes,
# somando-os ou subtraindo-os, que são operações que o chip já tem que fazer, por outras razões!
# 
# Isso levou a uma outra solução, inspirada em parte da física, da necessidade de erros relativos baixos,
# e de reaproveitar os circuitos lógicos já presentes no computador: usar **notação científica**.
# Um número em notação científica é dado por
# $$ mantissa \times 10^{expoente} \qquad \text{onde $1 \leq mantissa < 10$ e o $expoente$ é um número inteiro}. $$
# 
# Da mesma forma que os números racionais, temos que guardar dois números para cada "real": a $mantissa$ e o $expoente$.
# Mas agora, note que não há redundância, porque restringimos o domínio da mantissa.
# A $mantissa$ será um número racional representado com **ponto fixo**:
# a maior parte da magnitude dos números está capturada pelo $expoente$,
# e ao usar ponto fixo num pequeno intervalo não há _tanta_ variação da precisão.
# 
# Este sistema se chama **ponto flutuante** porque a posição do ponto decimal varia de acordo com o expoente.
# A grande vantagem deste sistema é que as operações aritméticas podem usar as partes do sistema que tratam de números inteiros,
# apenas ajustando os números para "alinhar" os pontos decimais corretamente
# (no caso de somas; os produtos dispensam isto porque a magnitude depende mais dos expoentes do que das mantissas!).

# <markdowncell>

# ### Exercício
# 
# 1. Repita a questão I dos pontos fixos para pontos flutuantes:
#     1. estude sua amplitude (maior / menor) ;
#     1. o número de casas significativas (e o erro relativo);
#     - (Obs: ambas as questões já foram parcialmente estudadas através dos programas acima)
# 
#     1. e compare com o uso de pontos fixos para representar as constantes físicas.

# <markdowncell>

# Num computador, o sistema de representação binário para os inteiros sugere que o ponto flutuante também esteja "em base 2".
# Assim, na verdade: um número em ponto flutuante (em base 2) é dado por
# $$ mantissa \times 2^{expoente} \qquad \text{onde $1 \leq mantissa < 2$ e o $expoente$ é um número inteiro}. $$
# 
# Note que a menor amplitude da mantissa também nos dá uma menor variação do erro relativo no início e no fim da escala!
# Uma outra apresentação para este sistema é a seguinte:
# $$ \left[ 1 + \frac{inteiro}{den} \right] * 2^{expoente} \qquad \text{onde o denominador $den$ está fixo, $0 \leq inteiro < den$ e $expoente \in Z$.}$$
# Nesta notação, é fácil ver que o erro relativo máximo será de $1/(2 * den)$, que é a **resolução** deste sistema de representação.
# 
# Este sitema ainda exige que se armazenem **duas** informações sobre o número real representado:
# a parte fracionária determinada pelo número $inteiro$, e o $expoente$, também inteiro.

