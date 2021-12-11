import numpy as np


def get_levenshtein_distance(a : str, b : str) -> int:
    w1 = ' ' + a
    w2 = ' ' + b
    N = len(w1)
    M = len(w2)
    D = np.zeros((N, M), dtype=np.int16)
    D[0:N, 0] = np.arange(N)
    D[0, 0:M] = np.arange(M)
    for i in range(1, N):
        for j in range(1, M):
            D[i, j] = min(
                D[i, j - 1] + 1,
                D[i - 1, j] + 1,
                D[i - 1, j - 1] + (w1[i] != w2[j])
            )
    return D[N - 1, M - 1]


if __name__ == '__main__':
    while True:
        query = input()
        try:
            a, b = query.split(' ')
        except Exception:
            if len(query) != 0:
                print("Invalid input. Expected two words separated with 1 space. Example:\nсобака сабака")
            break
        print(get_levenshtein_distance(a, b))
