from scipy.stats import binom

res = 0.0
diff = 43


for k in range(0, 43):
    res = res + binom.pmf(k, 256, 1/3)
for k in range(128, 257):
    res = res + binom.pmf(k, 256, 1/3)

iterations_per_one_sol = (1 / res)
print(iterations_per_one_sol)


ts = 272480
passed = 44 * 3600
print(ts / passed)
print((ts / passed) * iterations_per_one_sol)


print(3600 / (1 / res / 19700 ))
