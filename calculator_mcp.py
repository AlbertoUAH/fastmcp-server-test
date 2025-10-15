from fastmcp import FastMCP

mcp = FastMCP("Calculadora")

@mcp.tool()
def sumar(a: float, b: float) -> float:
    return a + b

@mcp.tool()
def restar(a: float, b: float) -> float:
    return a - b

@mcp.tool()
def multiplicar(a: float, b: float) -> float:
    return a * b

@mcp.tool()
def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

if __name__ == "__main__":
    mcp.run()
