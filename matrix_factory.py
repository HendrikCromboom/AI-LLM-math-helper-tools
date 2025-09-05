def create_matrix_from_flat_list(m: int, n: int, values: list[int]) -> list[list[int]]:
    nested_list = [[0] * n for _ in range(m)]
    index = 0
    for i in range(m):
        for j in range(n):
            if index + 1 < len(values):
                nested_list[i][j] = values[index]
            else:
                nested_list[i][j] = 0
            index += 1
    return nested_list
def create_matrix_zeros(m: int, n: int) -> list[list[int]]:
    nested_list = [[0] * n for _ in range(m)]
    return nested_list
def create_identity_matrix(m: int) -> list[list[int]]:
    matrix = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    return matrix
def create_identity_like_matrix(m: int, n: int) -> list[list[int]]:
    matrix = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
    return matrix


def multiply_matrices(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[int]]:
    """Multiply two matrices A × B. The number of columns in A must equal the number of rows in B."""

    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0]) if matrix_a else 0
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0]) if matrix_b else 0

    if cols_a != rows_b:
        raise ValueError(f"Cannot multiply matrices: {rows_a}×{cols_a} and {rows_b}×{cols_b}. "
                         f"Number of columns in first matrix ({cols_a}) must equal "
                         f"number of rows in second matrix ({rows_b})")

    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]

    return result

def matrix_vector_multiply(a, x):
    return [sum(a[i][j] * x[j] for j in range(len(x))) for i in range(len(a))]


def transpose_matrix(matrix):

    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


def square_root(x: float) -> float:

    if x < 0:
        raise ValueError(f"Cannot compute square root of negative number: {x}")

    if x == 0:
        return 0.0
    if x == 1:
        return 1.0

    guess = x / 2.0
    tolerance = 1e-15
    max_iterations = 100

    for _ in range(max_iterations):
        new_guess = (guess + x / guess) / 2.0

        if abs(new_guess - guess) < tolerance:
            return new_guess

        guess = new_guess

    return guess

def solve_square_system(a, b):
        n = len(a)
        augmented = [a[i][:] + [b[i]] for i in range(n)]

        for i in range(n):
            # Partial pivoting
            max_row = max(range(i, n), key=lambda k_k: abs(augmented[k_k][i]))
            if max_row != i:
                augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

            if abs(augmented[i][i]) < 1e-12:
                raise ValueError("Matrix is singular")

            # Forward elimination
            for k in range(i + 1, n):
                factor = augmented[k][i] / augmented[i][i]
                for j in range(i, n + 1):
                    augmented[k][j] -= factor * augmented[i][j]

        # Back substitution
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = augmented[i][n]
            for j in range(i + 1, n):
                x[i] -= augmented[i][j] * x[j]
            x[i] /= augmented[i][i]

        return x

#TODO: Pretty late when finishing this monolith, check tomorrow for redundancies and indentation mistakes, function works as intended
def solve_linear_system_general(matrix_a: list[list[float]], vector_b: list[float]) -> dict:

    m = len(matrix_a)
    n = len(matrix_a[0]) if matrix_a else 0

    # Validate inputs
    if not all(len(row) == n for row in matrix_a):
        raise ValueError("All rows in matrix A must have the same length")
    if len(vector_b) != m:
        raise ValueError(f"Vector b length ({len(vector_b)}) must match number of rows in A ({m})")

    #Overdetermined system (m > n) - Use least squares solution
    if m > n:
        # Solve normal equations: (A^T A)x = A^T b
        a_t = transpose_matrix(matrix_a)
        a_t_a = multiply_matrices(a_t, matrix_a)
        a_t_b = matrix_vector_multiply(a_t, vector_b)

        try:
            x = solve_square_system(a_t_a, a_t_b)
            residual = [vector_b[i] - sum(matrix_a[i][j] * x[j] for j in range(n))
                        for i in range(m)]
            residual_norm = square_root(sum(r * r for r in residual))

            return {
                "solution": x,
                "type": "least_squares",
                "system": f"overdetermined ({m}×{n})",
                "residual_norm": residual_norm,
                "description": "Least squares solution minimizing ||Ax - b||²"
            }
        except ValueError:
            return {
                "solution": None,
                "type": "no_solution",
                "system": f"overdetermined ({m}×{n})",
                "description": "A^T A is singular - no unique least squares solution"
            }

    #Underdetermined system (m < n) - Use minimum norm solution
    elif m < n:
        # Solve: A(A^T)y = b, then x = A^T y (minimum norm solution)
        a_t = transpose_matrix(matrix_a)
        a_a_t = multiply_matrices(matrix_a, a_t)

        try:
            y = solve_square_system(a_a_t, vector_b)
            x = matrix_vector_multiply(a_t, y)

            return {
                "solution": x,
                "type": "minimum_norm",
                "system": f"underdetermined ({m}×{n})",
                "solution_norm": square_root(sum(xi * xi for xi in x)),
                "description": "Minimum norm solution from infinitely many solutions"
            }
        except ValueError:
            return {
                "solution": None,
                "type": "no_solution",
                "system": f"underdetermined ({m}×{n})",
                "description": "AA^T is singular - system may be inconsistent"
            }

    else:
        try:
            x = solve_square_system(matrix_a, vector_b)
            return {
                "solution": x,
                "type": "unique",
                "system": f"square ({m}×{n})",
                "description": "Unique solution to square system"
            }
        except ValueError:
            return {
                "solution": None,
                "type": "no_solution",
                "system": f"square ({m}×{n})",
                "description": "Matrix is singular - no unique solution"
            }

print(solve_linear_system_general([[1,2],[3,4]],[1,2]))

print(square_root(4))

print(multiply_matrices([[1,2,3],[2,3,7]], [[2,5],[4,4],[5,5]]))

print(multiply_matrices(multiply_matrices([[1,2,3],[2,3,7]], [[2,5],[4,4],[5,5]]), [[1],[2]]))

print(create_identity_like_matrix(5,7))

print(create_identity_matrix(3))

print(create_matrix_zeros(3,3))

print(create_matrix_from_flat_list(4,4,[1,2,3,4,5,6,7,8,0,1,2,3,4,1,2,3,4]))
