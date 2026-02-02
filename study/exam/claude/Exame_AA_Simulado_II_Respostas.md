# Exame AA Simulado II (Advanced) - Chave de Respostas

## Escolha Múltipla (0,6 valores por resposta certa; -0,2 por resposta errada)

**1.** b) O tempo de execução pode variar para diferentes arrays de dimensão n, dependendo do conteúdo.
> Um algoritmo determinístico executa sempre a mesma sequência para o mesmo INPUT EXATO. Mas para inputs diferentes (mesmo que da mesma dimensão), o tempo pode variar. Exemplo: Quick Sort é determinístico mas o tempo depende da ordenação inicial dos elementos.

**2.** b) f(n) pertence a Θ(g(n)).
> f(n) = n² e g(n) = n² + n log n. Como n log n = o(n²), temos g(n) = Θ(n²). Logo f(n) = Θ(n²) = Θ(g(n)).
> A opção a) está errada porque g(n) também pertence a O(f(n)) = O(n²).

**3.** a) O(n log n).
> Verificando: T(n) = n × log(n)
> - T(2) = 2 × 1 = 2 ✓
> - T(4) = 4 × 2 = 8 ✓
> - T(8) = 8 × 3 = 24 ✓
> - T(16) = 16 × 4 = 64 ✓
> - T(32) = 32 × 5 = 160 ✓
> - T(64) = 64 × 6 = 384 ✓

**4.** a) Da tabela obtém-se T(n) = n(n+1)/2.
> T(n) = 1+2+3+...+n = n(n+1)/2 (números triangulares)
> Verificando: T(8) = 8×9/2 = 36 ✓
> Esta função é Θ(n²), não O(n log n). Logo apenas a) está correta.

**5.** d) O Teorema Mestre não se aplica diretamente a esta recorrência.
> T(n) = 4T(n/2) + n² log n
> Temos a=4, b=2, logo log_b(a) = log_2(4) = 2.
> f(n) = n² log n.
> Comparando com n^(log_b(a)) = n².
> f(n) = n² log n não é Θ(n²), nem O(n^(2-ε)), nem Ω(n^(2+ε)).
> Cai no "gap" entre os casos 2 e 3. O Teorema Mestre standard não cobre este caso.
> (A solução é T(n) = Θ(n² log² n), mas requer análise mais detalhada.)

**6.** c) Ambas estão corretas.
> Dijkstra é classificado como algoritmo greedy (escolhe sempre o vértice não visitado com menor distância).
> Bellman-Ford usa DP (relaxa arestas iterativamente, construindo soluções ótimas incrementalmente).

**7.** c) Ambas estão corretas.
> Problema fracionário: ordenar por valor/peso é O(n log n), greedy é ótimo.
> Problema 0-1: DP com tabela n×W é O(nW), que é pseudo-polinomial (exponencial no tamanho da entrada se W for dado em binário).

**8.** b) Fixando a cidade inicial, é necessário avaliar (n-1)!/2 percursos distintos (grafo não-dirigido).
> Opção a) está errada: fixando a cidade inicial, são (n-1)! percursos, não n!.
> Opção b) está correta: em grafo não-dirigido, cada ciclo é contado duas vezes (sentidos opostos), logo (n-1)!/2.

**9.** c) Ambas estão corretas.
> É Las Vegas: sempre retorna resposta correta (só termina quando encontra 'a').
> Tempo esperado: E[tentativas] = 1/p = 1/(1/4) = 4 = O(1).
> P(não encontrar após k tentativas) = (1-1/4)^k = (3/4)^k ✓

**10.** c) Ambas estão corretas.
> P(CARA) = 2/3, P(COROA) = 1/3.
> P(exatamente 2 CARAs) = C(3,2) × (2/3)² × (1/3)¹ = 3 × 4/9 × 1/3 = 12/27 = 4/9 ✓
> P(mais CARAs que COROAs) = P(2 CARAs) + P(3 CARAs) = 4/9 + (2/3)³ = 12/27 + 8/27 = 20/27 ✓

**11.** d) Nenhuma está correta.
> Estado inicial: c=0.
> Evento 1 (c=0): P(0→1) = 1/2^0 = 1, logo c=1 com certeza.
> Evento 2 (c=1): P(1→2) = 1/2. Então P(c=1)=1/2, P(c=2)=1/2.
> Evento 3:
>   P(c=1) = 1/2 × 1/2 = 1/4
>   P(c=2) = 1/2 × 1/2 + 1/2 × 3/4 = 1/4 + 3/8 = 5/8
>   P(c=3) = 1/2 × 1/4 = 1/8
> Evento 4:
>   P(c=1) = 1/4 × 1/2 = 1/8
>   P(c=2) = 1/4 × 1/2 + 5/8 × 3/4 = 1/8 + 15/32 = 19/32
>   P(c=3) = 5/8 × 1/4 + 1/8 × 7/8 = 5/32 + 7/64 = 17/64
>   P(c=4) = 1/8 × 1/8 = 1/64
> 
> Logo: P(c=2) = 19/32 ≠ 3/8, e P(c=3) = 17/64 ≠ 1/8.
> Nenhuma das opções está correta.

**12.** c) Ambas estão corretas.
> Com p=1/2:
> P(contador=2 após 4 eventos) = C(4,2) × (1/2)⁴ = 6/16 = 3/8 ✓
> E[contador após m eventos] = m × p = m/2 ✓

**13.** c) Ambas estão corretas.
> FP rate ≈ (1 - e^(-kn/m))^k = (1 - e^(-2×3/10))^2 = (1 - e^(-0.6))^2 ≈ (1-0.549)^2 ≈ 0.203 ≈ 0.22 ✓
> k_opt = (m/n) × ln(2) = (10/3) × 0.693 ≈ 2.31 ✓

**14.** a) A união de dois Filtros de Bloom pode ser obtida através do OR bit-a-bit.
> A união via OR está correta: se x está em A ou B, estará no filtro união.
> A interseção via AND NÃO representa exatamente a interseção dos conjuntos!
> Pode produzir falsos positivos adicionais. Logo b) está errada.

**15.** b) O algoritmo de Misra-Gries com k=4 irá incluir 'x' no conjunto de candidatos.
> Boyer-Moore (MJRTY) encontra elementos maioritários (freq > m/2). Como x tem freq = m/3 < m/2, NÃO será identificado como maioritário. Opção a) está errada.
> Misra-Gries com k=4 encontra elementos com freq > m/4. Como m/3 > m/4, 'x' será incluído nos candidatos. Opção b) está correta.

**16.** c) Ambas estão corretas.
> Count-Min Sketch apenas sobrestima (colisões só adicionam). ✓
> Parâmetros: w = ⌈e/ε⌉ para erro ≤ εN, d = ⌈ln(1/δ)⌉ para probabilidade ≥ 1-δ. ✓

**17.** c) Ambas estão corretas.
> Erro padrão do HyperLogLog: σ ≈ 1.04/√m ✓
> Espaço: m registos, cada um guarda max zeros observados ≈ log log n bits. Total: O(m log log n). ✓

**18.** a) Se o máximo número de zeros à direita observado for R, a estimativa é 2^R.
> Flajolet-Martin: estimativa = 2^R onde R = max trailing zeros. ✓
> Porém, a variância é ALTA com uma única função de hash. Precisa-se de múltiplas funções e médias. Opção b) está errada.

**19.** c) Ambas estão corretas.
> Ambos podem subestimar: Space-Saving pode ter contagens inflacionadas de elementos substituídos, e Lossy-Counting pode perder contagens durante decrementos. ✓
> Space-Saving: número fixo k de contadores. Lossy-Counting: número variável (cresce/decresce com buckets). ✓

**20.** c) Ambas estão corretas.
> Data streams: algoritmos devem usar espaço o(m) ou O(polylog m). ✓
> Count Sketch usa funções de sinal {-1,+1}, logo pode subestimar ou sobrestimar (erro bilateral). Count-Min só sobrestima (erro unilateral). ✓

---

## Verdadeiro / Falso (0,4 valores por resposta certa; -0,2 por resposta errada)

1. **Verdadeiro** - Transitividade de Big-O: se f=O(g) e g=O(h), então f=O(h).

2. **Falso** - Contraexemplo: f(n)=2n, g(n)=n. f=O(g), mas 2^(2n) = 4^n não é O(2^n).

3. **Verdadeiro** - T(n) = 2T(n/2) + n log n. Pelo caso 2 "estendido" do Master Theorem (quando f(n) = Θ(n^c log^k n) com c=log_b(a)), T(n) = Θ(n log^(k+1) n) = Θ(n log² n).

4. **Verdadeiro** - Quick Sort com pivô aleatório ou assumindo permutações equiprováveis tem complexidade esperada O(n log n).

5. **Verdadeiro** - Ciclo Hamiltoniano está em NP: dado um certificado (a sequência de vértices), podemos verificar em tempo polinomial.

6. **Falso** - Nem todo problema DP pode ser resolvido por greedy. Exemplo: 0-1 Knapsack requer DP; greedy não dá ótimo.

7. **Verdadeiro** - Kruskal é greedy (escolhe aresta mais leve que não forma ciclo) e prova-se que produz MST ótima.

8. **Falso** - Floyd-Warshall é O(V³), não O(V² log V).

9. **Falso** - Esta técnica de amplificação (repetir e tomar maioria) funciona para erros bilaterais (two-sided). Para erros unilaterais, a estratégia é diferente. Além disso, a fórmula está simplificada demais para o caso geral.

10. **Verdadeiro** - Miller-Rabin: se diz "composto", está sempre certo. Se diz "primo", pode estar errado (erro unilateral/one-sided).

11. **Verdadeiro** - P(A∪B∪C) = 1 - P(Ā∩B̄∩C̄) = 1 - P(Ā)P(B̄)P(C̄) = 1 - (1/2)³ = 1 - 1/8 = 7/8.

12. **Verdadeiro** - Com 23 pessoas, P(pelo menos duas com mesmo aniversário) ≈ 50.7% > 50%.

13. **Verdadeiro** - Morris counter com n bits: valor representado ≈ 2^(valor_contador). Com n bits, contador vai até 2^n-1, representando ≈ 2^(2^n).

14. **Verdadeiro** - Contador de probabilidade decrescente: E[c] ≈ log₂(m+1) após m eventos.

15. **Verdadeiro** - Taxa FP ótima com k ótimo: (1/2)^k. E k_opt = (m/n)ln(2), logo m/n = k/ln(2).

16. **Verdadeiro** - Quotient Filter suporta remoções (usa quociente/resto do hash e metadata bits).

17. **Verdadeiro** - Misra-Gries com parâmetro k mantém no máximo k-1 contadores/elementos.

18. **Verdadeiro** - Em CMS: d (linhas) controla probabilidade de erro (δ), w (colunas) controla magnitude do erro (ε).

19. **Verdadeiro** - HyperLogLog é "mergeable": max dos registos correspondentes dá sketch da união.

20. **Verdadeiro** - Cuckoo Filter: tipicamente 2 lookups vs k lookups do Bloom Filter. Melhor cache performance.

---

## Resumo das Respostas

**Escolha Múltipla:**
1. b | 2. b | 3. a | 4. a | 5. d | 6. c | 7. c | 8. b | 9. c | 10. c
11. d | 12. c | 13. c | 14. a | 15. b | 16. c | 17. c | 18. a | 19. c | 20. c

**Verdadeiro/Falso:**
1. V | 2. F | 3. V | 4. V | 5. V | 6. F | 7. V | 8. F | 9. F | 10. V
11. V | 12. V | 13. V | 14. V | 15. V | 16. V | 17. V | 18. V | 19. V | 20. V

---

## Notas sobre a dificuldade acrescida

Este exame é mais difícil que o anterior devido a:

1. **Questões com "armadilhas"**: Q1 (determinístico vs mesmo tempo), Q2 (funções equivalentes assintoticamente), Q5 (gap no Master Theorem)

2. **Cálculos mais complexos**: Q10 (probabilidade com moeda enviesada), Q11 (contador de probabilidade decrescente multi-evento), Q13 (Bloom Filter com parâmetros específicos)

3. **Distinções subtis**: Q6 (Dijkstra greedy vs Bellman-Ford DP), Q14 (união vs interseção em Bloom), Q15 (Boyer-Moore vs Misra-Gries)

4. **Verdadeiro/Falso com nuances**: Q2 (exponencial de Big-O), Q9 (amplificação de MC), Q15 (fórmula ótima de Bloom)

5. **Análise de tabelas não óbvia**: Q3 (n log n), Q4 (números triangulares)
