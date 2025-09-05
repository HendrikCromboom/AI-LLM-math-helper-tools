from mcp.server.fastmcp import FastMCP
from pydantic import Field
import matrix_factory

mcp = FastMCP(
    name = "math-helper",
    stateless_http = True
)

@mcp.tool()
def create_matrix_zeros(m: int = Field(description="The amount of rows of the matrix"),
                        n: int = Field(description="The amount of columns of the matrix"),
) -> list[list[int]]:
    """Create a nested list of zeros, also called a matrix of zeros or 0's of size m x n"""
    return matrix_factory.create_matrix_zeros(m,n)

@mcp.tool()
def create_matrix_from_flat_list(m: int = Field(description="The amount of rows of the matrix"),
                                 n: int = Field(description="The amount of columns of the matrix"),
                                 values: list[int] = Field(description="A one dimensional list of integers"),
) -> list[list[int]]:
    """Create a nested list of numbers based on a flat list of numbers of size m x n"""
    return matrix_factory.create_matrix_from_flat_list(m, n, values)

@mcp.tool()
def create_identity_matrix(m: int = Field(description="The size of the square identity matrix (size x size)")
) -> list[list[int]]:
    """Create a square identity matrix of size 'size x size' with 1's on the diagonal and 0's elsewhere"""
    return matrix_factory.create_identity_matrix(m)

@mcp.tool()
def create_identity_like_matrix(m: int = Field(description="Number of rows"),
                               n: int = Field(description="Number of columns")
) -> list[list[int]]:
    """Create an m x n matrix with 1's on the main diagonal (where i == j) and 0's elsewhere"""
    matrix = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
    return matrix_factory.create_identity_like_matrix(m, n)

@mcp.tool()
def multiply_matrices(matrix_a: list[list[int]] = Field(description="The first matrix (left operand)"),
                      matrix_b: list[list[int]] = Field(description="The second matrix (right operand)")
                      ) -> list[list[int]]:
    """Multiply two matrices A × B. The number of columns in A must equal the number of rows in B."""
    return matrix_factory.multiply_matrices(matrix_a, matrix_b)

@mcp.tool()
def square_root(x: float = Field(description="The number to find the square root of (must be non-negative)")
                ) -> float:
    """Calculate the square root of a non-negative number using Newton's method for high precision."""
    return matrix_factory.square_root(x)

@mcp.tool()
def solve_linear_system_general(matrix_a: list[list[float]] = Field(description="The coefficient matrix A (m×n)"),
                                vector_b: list[float] = Field(description="The right-hand side vector b (length m)")
                                ) -> dict:
    """Solve the linear system Ax = b for square and non-square matrices using the least squares or minimum norm solutions.
    Returns a dictionary with the solution and metadata."""
    return solve_linear_system_general(matrix_a, vector_b)

if __name__ == "__main__":

    mcp.run(transport="stdio")