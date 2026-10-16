import scipy

result = scipy.optimize.linprog(
    [-50, -40],
    [
        [2, 1],
        [1, 3]
    ],
    [100, 90]
)

if result.success:
    print("Optimal value:", -result.fun)
    print("Values of x:", result.x)