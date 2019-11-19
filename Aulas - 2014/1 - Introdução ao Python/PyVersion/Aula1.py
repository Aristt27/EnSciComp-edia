# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Plano de Hoje
# =============
# 
# 1. Ambiente de programação
#     1. Interpretador interativo, Interpretador de arquivos, iPython
#     1. Revisão da sintaxe de python
#     1. Funções
#     1. Números "reais"
#     1. NumPy, SciPy: Matrizes e o mais
#     1. MatPlotLib: gráficos

# <markdowncell>

# Python
# ------
# Pode ser:
# 
# - Uma linguagem (versões, ...)
# - Um programa (que você chama na linha de comando)
# 
# Funciona como:
# 
# - executável
# - "debugger" interativo (_toplevel_)
# 
# iPython
# -------
# Mistura tudo num lugar só:
# 
# - editor de texto
# - toplevel
# - comentários e documentação
# - gráficos !

# <markdowncell>

# Exemplo:

# <codecell>

print(1+2+3)
a = [1,2,3]
print(a, sum(a))

# <markdowncell>

# Voltar acima, e incluir mais alguns comandos.
# O que acontece se um comando "retorna" algo, como
# 
#     2 + 3
# ou como
# 
#     5 == 6
# ?

# <markdowncell>

# Em Python, tudo, **tudo mesmo**, pode ser "inspecionado". Isso tem duas conseqüências:
# 
# 1. o iPython usa essas capacidades para
#     - auto-completamento
#     - documentação on-line
#     - guardar todas as entradas e saídas usadas.
# 2. você pode usar isso para descobrir todos os detalhes de uma variável, função, objeto, classe, ...

# <codecell>

# Escreva "su" e espere

# Complete "sum(, " e espere

# Use "sum(a, " e dê "tab"

# <codecell>

# Mesmo entradas que não estão mais visíveis ainda estão na memória
print(In[1])

# <markdowncell>

# Sintaxe Python
# ==============
# 
# /!\ /!\ **Espaços significativos** /!\ /!\ :
# isso obriga o código a ficar mais "bonitinho", mas pode gerar bugs meio difíceis de resolver.
# **Use um editor de texto capaz de ajudar a identar corretamente**.
# 
# Referência: https://docs.python.org/3/reference/lexical_analysis.html e https://docs.python.org/3/reference/expressions.html
# 
# Palavras-chave
# --------------
# 
# (veja http://www.programiz.com/python-programming/keyword-list)

# <codecell>

# Todas as palavras-chave"
import keyword
print(keyword.kwlist)

# <markdowncell>

# Em grupos:
# 
# - `False`, `True`, `None`: valores pré-definidos (os dois booleanos, e um "_void_")
# - `and`, `or`, `not`: conectores lógicos
# - `in`: operador lógico "_pertence a_" (`not in` também existe)
# - `break`, `continue` ; `if`, `else`, `elif` ; `while`: estruturas de controle de fluxo
# 
# - `for ... in`: iterador
# - `def`, `lambda`, `class`, `pass`: definindo funções e classes
# - `return`, `yield`: retornando de funções e iteradores
# 
# - `raise`; `try`, `except`, `else`, `finally`: usando excessões
# 
# - `from`, `import`, `as`: usando módulos
# 
# Partes mais avançadas:
# 
# - `assert`: debug
# 
# - `del`: apaga uma variável do contexto (ou de uma lista / dicionário)
# - `global`, `nonlocal`: força uma variável a ser considerada global / mais geral do que o contexto da função atual
# 
# - `is`: igualdade física (ao contrário de ==, que é igualdade semântica) (também existe `is not`)
# - `with`, `as`: gestão de recursos

# <markdowncell>

# Operadores
# ----------
# 
# Aritméticos:
# 
#     +       -       *       **      /       //      %  
#     <<      >>
# 
# Lógicos
# 
#     &       |       ^       ~
# 
# Comparação
# 
#     <       >       <=      >=      ==      !=

# <markdowncell>

# Símbolos especiais
# ------------------
# 
# Grupos
# 
# - `()` : listas de argumentos, precedência
# - `[]` : construir listas, indexar listas e dicionários, "fatiar" listas
# - `{}` : conjuntos e dicionários
# 
# Operadores com uso e atribuição da mesma variável: `a $= b` é equivalente a `a = a $ b`
# 
#     +=      -=      *=      **=     /=      //=     %=
#     <<=     >>= 
#     &=      |=      ^=
# 
# Outros
# 
# - `=` : atribuição
# - `,` : separador de elementos em listas (tanto com `[]` como em funções)
# - `:` : separador de blocos (`if`, `def`, `for`, ...)
# - `.` : acesso de propriedades (`math.pi`)
# - `;` : seqüência (quase nunca utilizado)
# - `@` : decorador
# - `->` : anotação de funções

# <markdowncell>

# Estruturas de dados
# -------------------
# 
# Referência: https://docs.python.org/3/tutorial/index.html, em especial https://docs.python.org/3/tutorial/introduction.html
# 
# * Primitivas
#     - Números
#     - Strings e "bytestrings"
# * Compostas
#     - Listas, dicionários, conjuntos
#     - Pares e seqüências

# <markdowncell>

# ### Números

# <markdowncell>

# #### Números inteiros

# <markdowncell>

# Operações simples

# <codecell>

20 + 3, 20 - 3, 20 * 3, 20 / 3, 20 // 3, 20 % 3, 20 ** 3, 20 << 3, 20 >> 3

# <markdowncell>

# #### Números inteiros podem ser bem grandes!

# <codecell>

2 ** 20, 2 ** 30, 2 ** 100

# <codecell>

2 ** 500

# <markdowncell>

# Tente ver até que número o seu computador consegue calcular "sem titubear"!

# <markdowncell>

# #### Números de ponto flutuante

# <codecell>

(1./3)*3, 1./7, 4.5 % 2.1

# <markdowncell>

# Também podem ser grandes!

# <codecell>

2. ** 500

# <markdowncell>

# Mas podem acontecer coisas estranhas...

# <codecell>

x = 1.2e-16
y = 1
z1 = (y + x) - y - x
z2 = (y + x) - x - y
print(z1, z2, y+x)

# <markdowncell>

# ###Listas, dicionários, conjuntos

# <codecell>

# Declarando variáveis
li = [1,2,3,4,5,6]
conj = {1, 2, 3, 4, 5, 6}
dic = {1:2, 3:'4', "5":6}

# <codecell>

print(li)
print(conj)
print(dic)

# <markdowncell>

# Operações básicas: pertence

# <codecell>

3 in li, 3 in conj, 3 in dic

# <codecell>

2 in li, 2 in conj, 2 in dic

# <markdowncell>

# comprimento,

# <codecell>

len(li), len(conj), len(dic)

# <markdowncell>

# modificação,

# <codecell>

li.append(7)
li.remove(3)
conj.add(7)
conj.remove(3)
dic.update({7 : 8.})
dic.pop(3)

# <markdowncell>

# e iteração

# <codecell>

for x in li:
    print (x, x*x)
print("")
for v in conj:
    print(v, v**v)
print("")
for k in dic:
    print(k, dic[k])   

# <markdowncell>

# Operações de acesso indexado

# <codecell>

li[1], dic[1], li[5], dic["5"]

# <codecell>

# Indexar e fatiar: trabalhando com listas
li[-2], li[:3], li[3:], li[3:-1]

# <markdowncell>

# Acesso e modificação simultâneos

# <codecell>

li[2] = 42
print(li)
dic[1] = [1,2,3]
print(dic)

# <markdowncell>

# Podemos modificar um monte de campos ao mesmo tempo, usando "fatias":

# <codecell>

li[3:5] = [10,11,12,13]
print(li)

# <markdowncell>

# O que ocorre, na verdade, é que a lista é separada em três partes, **antes**, **fatia** e **depois**, e a parte da fatia é substituída pelo que você pedir.

# <codecell>

# Note a diferença
x = [1,2,3]

tmp = li[:]  # copia li...
tmp[1] = x   # e substitui o elemento de índice 1 por uma lista
print(tmp)

tmp = li[:]  # copia li...
tmp[1:2] = x # e insere na lista substituindo o elemento de índice 1
print(tmp)

# <codecell>

tmp[1:1] = [0,0,0] # insere no meio da lista
print(tmp)

# <markdowncell>

# ###Strings

# <codecell>

x = 'Tudo'
y = "isso"
z = """são
três"""
w = '''strings


diferentes'''
print((x, y, z, w))
print(w)

# <markdowncell>

# Operações: "aritméticas"

# <codecell>

x + y, x * 3, len(z)

# <markdowncell>

# e indexação (strings são listas imutáveis)

# <codecell>

print(z[5])
print(w[5:-5])

# <markdowncell>

# ###Pares e além
# 
# Um par é construído como em matemática:
# 
#     (1, 2)
# É possível fazer com mais dimensões:

# <codecell>

(1,2,3,4,5)

# <markdowncell>

# e também usar vários níveis de "pares"

# <codecell>

(1,(2,3),(4,(5,))) # Note a vírgula para que (5) != 5

# <markdowncell>

# O além: é possível combinar tudo isso de várias formas:

# <codecell>

listaestranha = [1, (2,3), {4,5}]
for x in listaestranha:
    print(x)

# <codecell>

dicbizarro = {1:(2,[3]), (4,5):"6"}
for k,v in dicbizarro.items():
    print(k,v)

print("")
print(dicbizarro[(4,5)])

# <markdowncell>

# Módulos
# -------
# 
# Esse é o sistema de "bibliotecas" de Python. E a biblioteca _standard_ do Python (em https://docs.python.org/3/library/index.html) é bastante completa.
# Alguns exemplos:
# 
# - string
# - datetime, calendar
# - math, fractions, random
# - pickle, marshal
# - zipfile, tarfile
# - csv, configparser
# - os, time, argparse, getpass, logging
# - threading, multiprocessing, concurrent
# - email, html, xml, http
# - pydoc, unittest, timeit
# - sys

