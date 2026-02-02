# Exame AA Simulado - Chave de Respostas

## Escolha Múltipla (0,6 valores por resposta certa; −0,2 por resposta errada)

**1.** a) executa sempre a mesma sequência de instruções para um mesmo conjunto de dados de entrada.
> Um algoritmo determinístico, por definição, executa sempre a mesma sequência de instruções para o mesmo input.

**2.** c) Ambas estão corretas.
> t(n) = 5n² + 3n log(n) + 100 é dominado pelo termo 5n², logo pertence tanto a O(n²) como a Ω(n²), e portanto a Θ(n²).

**3.** b) A análise do pior caso fornece uma garantia sobre o desempenho máximo do algoritmo.
> A análise do melhor caso raramente é relevante na prática. O pior caso dá-nos um limite superior garantido.

**4.** b) logarítmica.
> T(n) = log₂(n). Por exemplo: T(1)=0, T(2)=1, T(4)=2, T(8)=3, T(16)=4...

**5.** b) Cúbica.
> T(n) = n³. Os valores 1, 8, 27, 64, 125, 216, 343 são 1³, 2³, 3³, 4³, 5³, 6³, 7³.

**6.** a) Da tabela obtém-se a seguinte expressão: T(n) = n².
> T(n) = n² é correto (1, 4, 9, 16, 25...). A opção b) está incorreta pois T(n) = n² é O(n²), não O(n log n).

**7.** b) as soluções de sub-problemas são armazenadas para evitar recálculos.
> Na programação dinâmica os sub-problemas são sobrepostos (não independentes). A característica distintiva é a memoização.

**8.** a) Problema da Mochila ("The Knapsack Problem").
> O problema da mochila 0-1 requer gerar subconjuntos (2ⁿ). O TSP requer gerar permutações (n!).

**9.** c) Ambas estão corretas.
> No Teorema Mestre T(n) = aT(n/b) + f(n): a = número de sub-problemas, n/b = dimensão de cada sub-problema.

**10.** b) faz escolhas localmente ótimas que são irrevogáveis.
> Algoritmos greedy não garantem sempre o ótimo global (ex: problema da mochila 0-1).

**11.** d) Nenhuma está correta.
> É um algoritmo Monte Carlo (tempo fixo, pode falhar), não Las Vegas. E o tempo não é sempre k iterações pois pode terminar antes se encontrar 'x'.

**12.** c) Ambas estão corretas.
> P(soma=7) = 6/36 = 1/6 (combinações: 1+6, 2+5, 3+4, 4+3, 5+2, 6+1).
> P(soma=12) = P(soma=2) = 1/36 (apenas 6+6 ou 1+1).

**13.** c) Ambas estão corretas.
> P(exatamente 2 CARAs) = C(4,2) × (1/2)⁴ = 6/16 = 3/8. ✓
> P(pelo menos 1 CARA) = 1 - P(0 CARAs) = 1 - (1/2)⁴ = 1 - 1/16 = 15/16. ✓

**14.** c) Ambas estão corretas.
> Com p=1/3: P(contador=0 após 3 eventos) = (2/3)³ = 8/27.
> P(contador=3 após 3 eventos) = (1/3)³ = 1/27.

**15.** a) Após 2 eventos, a probabilidade de o contador registar o valor 0 é 0.
> Evento 1: P(0→1) = 1/2^0 = 1, logo contador = 1 com certeza após o primeiro evento.
> Evento 2: P(1→2) = 1/2^1 = 1/2, P(ficar em 1) = 1/2.
> Logo: P(valor=0) = 0 (verdadeiro), P(valor=1) = 1/2, P(valor=2) = 1/2.
> A opção a) está correta. A opção b) está errada pois P(valor=2) = 1/2, não 1/4.

**16.** b) Se um elemento e não pertence a C, uma query ao filtro poderá indicar que e pertence a C.
> Bloom Filters têm falsos positivos mas nunca falsos negativos.

**17.** c) Ambas estão corretas.
> Counting Bloom Filters usam contadores (tipicamente 4 bits) em vez de bits, permitindo remoções seguras.

**18.** b) requer duas passagens sobre os dados: uma para identificar o candidato e outra para verificar.
> Boyer-Moore (MJRTY) encontra candidato a elemento maioritário (>m/2), não elementos frequentes (>m/k).

**19.** c) Ambas estão corretas.
> Misra-Gries: não tem falsos negativos (encontra todos os heavy-hitters), mas pode ter falsos positivos.

**20.** a) utiliza a média harmónica para combinar estimativas de múltiplos registos.
> HyperLogLog usa O(log log n) espaço por registo, não O(n). A média harmónica é usada para reduzir a variância.

---

## Verdadeiro / Falso (0,4 valores por resposta certa; −0,2 por resposta errada)

1. **Verdadeiro** - Definição correta de algoritmo.

2. **Verdadeiro** - Θ(g(n)) significa que t(n) é simultaneamente O(g(n)) e Ω(g(n)).

3. **Falso** - t(n) = 3n³ + 2n² + n pertence a O(n³), não O(n²). O termo dominante é n³.

4. **Verdadeiro** - O TSP é um problema NP-completo clássico.

5. **Verdadeiro** - A programação dinâmica evita recálculos através da memoização.

6. **Verdadeiro** - Merge Sort é O(n log n) em todos os casos (melhor, médio e pior).

7. **Verdadeiro** - Para o problema fracionário da mochila, greedy por valor/peso é ótimo.

8. **Falso** - Dijkstra não funciona com pesos negativos. Usar Bellman-Ford nesses casos.

9. **Verdadeiro** - Monte Carlo: tempo determinístico, resultado pode estar errado.

10. **Falso** - Las Vegas: resultado sempre correto, tempo de execução é aleatório.

11. **Verdadeiro** - P(pelo menos 1 COROA) = 1 - P(2 CARAs) = 1 - (3/4)² = 1 - 9/16 = 7/16.

12. **Verdadeiro** - Cada lançamento é independente dos anteriores.

13. **Falso** - Fermat é probabilístico (Monte Carlo). Pode classificar incorretamente números de Carmichael.

14. **Verdadeiro** - O contador de Morris usa O(log log n) bits.

15. **Verdadeiro** - Para contador de probabilidade decrescente, E[contador] ≈ log₂(eventos+1). log₂(32) = 5.

16. **Verdadeiro** - Característica fundamental dos Bloom Filters.

17. **Verdadeiro** - Fórmula correta para k ótimo que minimiza a taxa de falsos positivos.

18. **Verdadeiro** - Space-Saving mantém k contadores e substitui o mínimo quando necessário.

19. **Falso** - Count-Min Sketch só pode sobrestimar (devido a colisões), nunca subestima.

20. **Verdadeiro** - HyperLogLog usa ~12KB para erros de ~1%, independentemente da cardinalidade.

---

## Resumo das Respostas

**Escolha Múltipla:**
1. a | 2. c | 3. b | 4. b | 5. b | 6. a | 7. b | 8. a | 9. c | 10. b
11. d | 12. c | 13. c | 14. c | 15. a | 16. b | 17. c | 18. b | 19. c | 20. a

**Verdadeiro/Falso:**
1. V | 2. V | 3. F | 4. V | 5. V | 6. V | 7. V | 8. F | 9. V | 10. F
11. V | 12. V | 13. F | 14. V | 15. V | 16. V | 17. V | 18. V | 19. F | 20. V
