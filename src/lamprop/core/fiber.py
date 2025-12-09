"""Fiber model and creation function."""
from pydantic import BaseModel, Field

class Fiber(BaseModel):
    """Represents a fiber material."""
    E1: float = Field(..., gt=0, description="Young's modulus in MPa")
    nu12: float = Field(..., description="Poisson's constant")
    alpha1: float = Field(..., description="Coefficient of thermal expansion in K^-1")
    rho: float = Field(..., gt=0, description="Fiber density in g/cm^3")
    name: str = Field(..., min_length=1, description="Name of the fiber")

def fiber(E1: float, nu12: float, alpha1: float, rho: float, name: str) -> Fiber:
    """Create a Fiber instance."""
    return Fiber(E1=E1, nu12=nu12, alpha1=alpha1, rho=rho, name=name)
