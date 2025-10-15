from fastmcp import FastMCP

mcp = FastMCP("Catálogo BBVA")

CATALOGO_PRODUCTOS = {
    "cuentas": [
        {
            "nombre": "Cuenta Online",
            "descripcion": "Cuenta sin comisiones con gestión 100% digital. Incluye tarjeta de débito gratuita y acceso a banca online y móvil."
        },
        {
            "nombre": "Cuenta Nómina",
            "descripcion": "Cuenta sin comisiones domiciliando tu nómina o pensión. Incluye tarjeta de débito y ventajas exclusivas."
        },
        {
            "nombre": "Cuenta Joven",
            "descripcion": "Cuenta sin comisiones para menores de 30 años. Incluye tarjeta de débito y servicios digitales."
        }
    ],
    "tarjetas": [
        {
            "nombre": "Tarjeta Débito Aqua",
            "descripcion": "Tarjeta de débito ecológica fabricada con materiales reciclados. Sin comisiones de mantenimiento."
        },
        {
            "nombre": "Tarjeta Crédito",
            "descripcion": "Tarjeta de crédito con pago aplazado y facilidad de financiación. Aceptada mundialmente."
        },
        {
            "nombre": "Tarjeta After Pay",
            "descripcion": "Tarjeta de crédito que permite aplazar compras sin intereses en comercios adheridos."
        }
    ],
    "prestamos": [
        {
            "nombre": "Préstamo Personal",
            "descripcion": "Financiación flexible hasta 60.000€ para cualquier proyecto personal. Respuesta inmediata online."
        },
        {
            "nombre": "Préstamo Coche",
            "descripcion": "Financiación específica para la compra de vehículos nuevos y usados con condiciones especiales."
        }
    ],
    "hipotecas": [
        {
            "nombre": "Hipoteca Fija",
            "descripcion": "Hipoteca con tipo de interés fijo durante toda la vida del préstamo. Cuotas constantes y previsibles."
        },
        {
            "nombre": "Hipoteca Variable",
            "descripcion": "Hipoteca con tipo de interés variable referenciado al Euríbor. Mayor flexibilidad inicial."
        },
        {
            "nombre": "Hipoteca Mixta",
            "descripcion": "Combina un periodo inicial de tipo fijo y posteriormente pasa a tipo variable."
        }
    ],
    "inversiones": [
        {
            "nombre": "Fondos de Inversión",
            "descripcion": "Amplia gama de fondos de inversión para diferentes perfiles de riesgo y objetivos financieros."
        },
        {
            "nombre": "Planes de Pensiones",
            "descripcion": "Ahorro a largo plazo con ventajas fiscales para complementar tu jubilación."
        },
        {
            "nombre": "Depósitos",
            "descripcion": "Productos de ahorro con rentabilidad garantizada y diferentes plazos de vencimiento."
        }
    ],
    "seguros": [
        {
            "nombre": "Seguro de Hogar",
            "descripcion": "Protección completa para tu vivienda, contenido y responsabilidad civil."
        },
        {
            "nombre": "Seguro de Vida",
            "descripcion": "Protección financiera para tu familia con diferentes coberturas y capitales asegurados."
        },
        {
            "nombre": "Seguro de Salud",
            "descripcion": "Asistencia médica completa con acceso a amplio cuadro médico y hospitales."
        }
    ]
}

@mcp.tool()
def obtener_catalogo_completo() -> dict:
    return CATALOGO_PRODUCTOS

@mcp.tool()
def obtener_productos_por_categoria(categoria: str) -> list:
    categoria_lower = categoria.lower()
    if categoria_lower in CATALOGO_PRODUCTOS:
        return CATALOGO_PRODUCTOS[categoria_lower]
    else:
        categorias_disponibles = list(CATALOGO_PRODUCTOS.keys())
        raise ValueError(f"Categoría no encontrada. Categorías disponibles: {', '.join(categorias_disponibles)}")

@mcp.tool()
def buscar_producto(nombre: str) -> dict:
    nombre_lower = nombre.lower()
    for categoria, productos in CATALOGO_PRODUCTOS.items():
        for producto in productos:
            if nombre_lower in producto["nombre"].lower():
                return {
                    "categoria": categoria,
                    "producto": producto
                }
    raise ValueError(f"Producto '{nombre}' no encontrado en el catálogo")

@mcp.tool()
def listar_categorias() -> list:
    return list(CATALOGO_PRODUCTOS.keys())

if __name__ == "__main__":
    mcp.run()
