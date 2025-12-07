import time

# ------------------------------
#  Алгоритм Боєра–Мура
# ------------------------------
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0

    # побудова таблиці зміщень
    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    skip_default = m

    i = m - 1
    while i < n:
        j = m - 1
        k = i
        while j >= 0 and text[k] == pattern[j]:
            j -= 1
            k -= 1
        if j == -1:
            return k + 1
        i += skip.get(text[i], skip_default)
    return -1

# ------------------------------
#  Алгоритм Кнута–Морріса–Пратта
# ------------------------------
def kmp(text, pattern):
    n, m = len(text), len(pattern)

    # побудова префікс-функції
    lps = [0] * m
    j = 0  
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    # пошук
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1
    return -1

# ------------------------------
#  Алгоритм Рабіна–Карпа
# ------------------------------
def rabin_karp(text, pattern, base=256, mod=101_000_000_7):
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    pat_hash = 0
    txt_hash = 0
    h = 1

    for _ in range(m - 1):
        h = (h * base) % mod

    for i in range(m):
        pat_hash = (pat_hash * base + ord(pattern[i])) % mod
        txt_hash = (txt_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pat_hash == txt_hash:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            txt_hash = (txt_hash - ord(text[i]) * h) * base + ord(text[i + m])
            txt_hash %= mod

    return -1

# ------------------------------
#  Функція для заміру часу
# ------------------------------
def measure(text, pattern):
    results = {}

    start = time.perf_counter_ns()
    boyer_moore(text, pattern)
    results["Boyer–Moore"] = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    kmp(text, pattern)
    results["KMP"] = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    rabin_karp(text, pattern)
    results["Rabin–Karp"] = time.perf_counter_ns() - start

    return results

# ------------------------------
#  ГОЛОВНА ЧАСТИНА
# ------------------------------

# Підрядки для аналізу
pattern1 = "while (range < integers.length && integers[range] <= elementToSearch)"
pattern2 = "Постановка проблеми."

# Завантаження текстів
with open("article1.txt", "r", encoding="utf-8") as f:
    article1 = f.read()

with open("article2.txt", "r", encoding="utf-8") as f:
    article2 = f.read()

# Аналіз
results_article_1 = measure(article1, pattern1)
results_article_2 = measure(article2, pattern2)

# Вивід результатів
print("=== РЕЗУЛЬТАТИ ДЛЯ СТАТТІ 1 ===")
for algo, t in results_article_1.items():
    print(f"{algo}: {t} ns")

print("\n=== РЕЗУЛЬТАТИ ДЛЯ СТАТТІ 2 ===")
for algo, t in results_article_2.items():
    print(f"{algo}: {t} ns")
