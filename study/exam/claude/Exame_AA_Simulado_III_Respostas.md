# Exame AA Simulado III - Chave de Respostas

## Escolha Múltipla (0,6 valores por resposta certa; -0,2 por resposta errada)

**1.** a) pode executar diferentes sequências de instruções.
> Um algoritmo não-determinístico pode seguir caminhos diferentes em execuções distintas para o mesmo input. Pode também devolver resultados diferentes, logo b) está errada.

**2.** c) Ambas estão corretas.
> t(n) = 4n³ + 2n² log n + 100n é dominada pelo termo 4n³.
> Logo t(n) = Θ(n³), o que significa que pertence simultaneamente a O(n³) e Ω(n³).
> Como Ω(n³) implica Ω(n²), a opção a) também está correta.

**3.** c) Ambas estão corretas.
> O caso médio considera a média ponderada sobre todas as entradas possíveis. ✓
> O pior caso dá um limite superior garantido para qualquer entrada. ✓

**4.** b) quadrática.
> T(n) = n². Verificando: T(1)=1², T(2)=2²=4, T(4)=4²=16, T(8)=8²=64, T(16)=16²=256, T(32)=32²=1024, T(64)=64²=4096. ✓

**5.** a) O(n log n).
> T(n) = n × (log₂(n) + 1) = n log n + n = Θ(n log n).
> Verificando: T(2)=2×2=4, T(4)=4×3=12, T(8)=8×4=32, T(16)=16×5=80, T(32)=32×6=192, T(64)=64×7=448, T(128)=128×8=1024. ✓

**6.** c) Ambas estão corretas.
> T(n) = n(n+1)/2 (números triangulares): T(0)=0, T(1)=1, T(2)=3, T(3)=6, T(4)=10, T(5)=15, T(6)=21, T(7)=28. ✓
> n(n+1)/2 = (n² + n)/2 = Θ(n²). ✓

**7.** c) Ambas estão corretas.
> Procura exaustiva gera todas as soluções candidatas e avalia cada uma. ✓
> É tipicamente ineficiente (exponencial/fatorial) mas garante encontrar o ótimo. ✓

**8.** c) Ambas estão corretas.
> T(n) = 2T(n/2) + n: a=2, b=2, f(n)=n.
> log_b(a) = log₂(2) = 1. ✓
> f(n) = n = Θ(n^1) = Θ(n^(log_b(a))), logo é o Caso 2 do Teorema Mestre.
> T(n) = Θ(n^1 × log n) = Θ(n log n). ✓

**9.** c) Ambas estão corretas.
> Programação dinâmica constrói a solução ótima a partir de soluções ótimas dos sub-problemas (subestrutura ótima). ✓
> O problema deve satisfazer o princípio da otimalidade para que DP funcione. ✓

**10.** c) Ambas estão corretas.
> Para o problema fracionário da mochila, o algoritmo greedy seleciona itens por ordem decrescente de valor/peso. ✓
> Este algoritmo greedy garante a solução ótima para o problema fracionário (não para o 0-1). ✓

**11.** c) Ambas estão corretas.
> É Monte Carlo: tempo limitado (máximo 5 iterações), pode falhar (retornar -1). ✓
> P(encontrar 'a') = 1 - P(não encontrar em 5 tentativas) = 1 - (1/2)⁵ = 31/32. ✓

**12.** c) Ambas estão corretas.
> P(duas faces iguais) = 6/36 = 1/6 (combinações: 1-1, 2-2, 3-3, 4-4, 5-5, 6-6). ✓
> P(soma par) = P(par+par) + P(ímpar+ímpar) = (3/6)² + (3/6)² = 1/4 + 1/4 = 1/2. ✓

**13.** c) Ambas estão corretas.
> P(CARA) = 1/3, P(COROA) = 2/3.
> P(exatamente 1 CARA) = C(3,1) × (1/3)¹ × (2/3)² = 3 × 1/3 × 4/9 = 12/27 = 4/9. ✓
> P(pelo menos 2 COROAs) = P(2 COROAs) + P(3 COROAs) = C(3,2)×(2/3)²×(1/3) + (2/3)³ = 12/27 + 8/27 = 20/27. ✓

**14.** c) Ambas estão corretas.
> Com p = 1/4 (probabilidade de incremento):
> P(contador = 0 após 2 eventos) = (1-p)² = (3/4)² = 9/16. ✓
> P(contador = 1 após 2 eventos) = C(2,1) × p × (1-p) = 2 × 1/4 × 3/4 = 6/16. ✓

**15.** a) Após o primeiro evento, o contador terá sempre o valor 1.
> Evento 1 (c=0): P(incrementar) = 1/2^0 = 1. Logo c=1 com certeza. ✓
> Após 3 eventos:
> - Evento 2 (c=1): P(1→2)=1/2, P(ficar 1)=1/2
> - Evento 3: P(c=2) = 1/2×1/2 + 1/2×3/4 = 1/4 + 3/8 = 5/8 ≠ 1/2
> Logo b) está errada.

**16.** a) podem existir falsos positivos, mas nunca existem falsos negativos.
> A opção a) é a característica fundamental dos Bloom Filters. ✓
> A opção b) está errada: existe um k ótimo. Aumentar k além do ótimo AUMENTA a taxa de falsos positivos (porque mais bits ficam a 1).

**17.** c) Ambas estão corretas.
> Counting Bloom Filter substitui cada bit por um contador (tipicamente 4 bits). ✓
> Permite remoções através do decremento dos contadores correspondentes. ✓

**18.** c) Ambas estão corretas.
> Misra-Gries com parâmetro k usa no máximo k-1 contadores. ✓
> Garante encontrar todos os elementos com frequência > m/k (sem falsos negativos, mas pode ter falsos positivos). ✓

**19.** c) Ambas estão corretas.
> Count-Min Sketch usa uma matriz 2D de contadores (d linhas × w colunas). ✓
> Para uma query, consulta d contadores (um por linha) e retorna o mínimo. ✓

**20.** b) utiliza múltiplos registos e combina as estimativas usando a média harmónica.
> A opção a) está ERRADA: HyperLogLog usa zeros à DIREITA (trailing zeros), não à esquerda (leading zeros).
> A opção b) está correta: usa m registos e média harmónica para reduzir variância. ✓

---

## Verdadeiro / Falso (0,4 valores por resposta certa; -0,2 por resposta errada)

1. **Verdadeiro** - Definição correta de algoritmo.

2. **Verdadeiro** - Se f(n) ≤ c×g(n), então g(n) ≥ (1/c)×f(n), logo g = Ω(f).

3. **Verdadeiro** - O termo dominante é n², logo t(n) = Θ(n²).

4. **Verdadeiro** - Merge Sort é divide-and-conquer com O(n log n) garantido em todos os casos.

5. **Falso** - O problema 0-1 Knapsack requer programação dinâmica. Greedy não garante ótimo.

6. **Verdadeiro** - Memoização é exatamente isso: armazenar resultados para evitar recálculos.

7. **Falso** - Dijkstra NÃO funciona com pesos negativos, mesmo sem ciclos negativos. Usar Bellman-Ford.

8. **Falso** - NP significa que existe verificador em tempo polinomial, não solucionador. P é a classe dos problemas com solução polinomial.

9. **Falso** - Las Vegas SEMPRE devolve resultado correto. É Monte Carlo que pode errar.

10. **Verdadeiro** - Números de Carmichael passam no teste de Fermat apesar de serem compostos.

11. **Verdadeiro** - P(soma=7) = 6/36, P(soma=6) = 5/36. Logo P(7) > P(6).

12. **Verdadeiro** - P(exatamente 2 CARAs em 4 lançamentos) = C(4,2) × (1/2)⁴ = 6/16 = 3/8.

13. **Verdadeiro** - Morris counter com n bits guarda valor c até 2^n-1, representando aproximadamente 2^c ≈ 2^(2^n).

14. **Verdadeiro** - E[contador] ≈ log₂(m+1). Para m=7: log₂(8) = 3. ✓

15. **Verdadeiro** - Fórmula correta para a taxa de falsos positivos de um Bloom Filter.

16. **Falso** - Bloom Filter clássico NÃO suporta remoções (precisaria de Counting Bloom Filter).

17. **Verdadeiro** - Boyer-Moore (MJRTY) identifica candidato a elemento maioritário (freq > n/2).

18. **Falso** - Count-Min Sketch apenas SOBRESTIMA (colisões só adicionam), nunca subestima.

19. **Falso** - Space-Saving mantém exatamente k contadores, mas não necessariamente para os k mais frequentes (pode ter falsos positivos).

20. **Falso** - HyperLogLog usa O(m × log log n) ≈ O(1) espaço (constante para precisão fixa), não O(log n).

---

## Resumo das Respostas

**Escolha Múltipla:**
1. a | 2. c | 3. c | 4. b | 5. a | 6. c | 7. c | 8. c | 9. c | 10. c
11. c | 12. c | 13. c | 14. c | 15. a | 16. a | 17. c | 18. c | 19. c | 20. b

**Verdadeiro/Falso:**
1. V | 2. V | 3. V | 4. V | 5. F | 6. V | 7. F | 8. F | 9. F | 10. V
11. V | 12. V | 13. V | 14. V | 15. V | 16. F | 17. V | 18. F | 19. F | 20. F
