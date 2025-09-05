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

if __name__ == "__main__":

    mcp.run(transport="stdio")