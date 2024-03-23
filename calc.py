from scipy.stats import binom

res = 0.0
for k in range(0, 87):
    res = res + binom.pmf(k, 256, 0.5)
for k in range(170, 257):
    res = res + binom.pmf(k, 256, 0.5)

iterations_per_one_sol = (1 / res)
print(iterations_per_one_sol)


ts = 272480
passed = 44 * 3600
print(ts / passed)
print((ts / passed) * iterations_per_one_sol)


print(3600 / (1 / res / 19700 ))
