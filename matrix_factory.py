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

print(create_identity_matrix(3))

print(create_matrix_zeros(3,3))

print(create_matrix_from_flat_list(4,4,[1,2,3,4,5,6,7,8,0,1,2,3,4,1,2,3,4]))
