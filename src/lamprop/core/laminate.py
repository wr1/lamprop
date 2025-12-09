"""Laminate model and creation function."""
import math
import numpy as np
from typing import List, Union
from pydantic import BaseModel, Field, ConfigDict
from .lamina import Lamina
from .utils import clean

class Laminate(BaseModel):
    """Represents a laminate."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., min_length=1)
    layers: List[Union[Lamina, str]]
    thickness: float
    fiber_weight: float
    rho: float
    vf: float
    resin_weight: float
    ABD: np.ndarray
    abd: np.ndarray
    H: np.ndarray
    h: np.ndarray
    Ex: float
    Ey: float
    Ez: float
    Gxy: float
    Gyz: float
    Gxz: float
    nu_xy: float
    nu_yx: float
    alpha_x: float
    alpha_y: float
    wf: float
    C: np.ndarray
    S: np.ndarray
    tEx: float
    tEy: float
    tEz: float
    tGxy: float
    tGyz: float
    tGxz: float
    t_nu_xy: float
    t_nu_xz: float
    t_nu_yz: float

def laminate(name: str, layers: List[Union[Lamina, str]]) -> Laminate:
    """Create a Laminate."""
    orig_layers = layers
    layers = [la for la in layers if isinstance(la, Lamina)]
    thickness = sum(la.thickness for la in layers)
    fiber_weight = sum(la.fiber_weight for la in layers)
    rho = sum(la.rho * la.thickness for la in layers) / thickness
    vf = sum(la.vf * la.thickness for la in layers) / thickness
    resin_weight = sum(la.resin_weight for la in layers)
    wf = fiber_weight / (fiber_weight + resin_weight)
    zs = -thickness / 2
    lz2, lz3 = [], []
    C = np.zeros((6, 6))
    for la in layers:
        ze = zs + la.thickness
        lz2.append((ze * ze - zs * zs) / 2)
        lz3.append((ze * ze * ze - zs * zs * zs) / 3)
        zs = ze
        C = C + la.C * la.thickness / thickness
    C = clean(C)
    S = np.linalg.inv(C)
    Ntx, Nty, Ntxy = 0.0, 0.0, 0.0
    ABD = np.zeros((6, 6))
    H = np.zeros((2, 2))
    c3 = 0
    for la, z2, z3 in zip(layers, lz2, lz3):
        ABD[0, 0] += la.Q11_bar * la.thickness
        ABD[0, 1] += la.Q12_bar * la.thickness
        ABD[0, 2] += la.Q16_bar * la.thickness
        ABD[0, 3] += la.Q11_bar * z2
        ABD[0, 4] += la.Q12_bar * z2
        ABD[0, 5] += la.Q16_bar * z2
        ABD[1, 0] += la.Q12_bar * la.thickness
        ABD[1, 1] += la.Q22_bar * la.thickness
        ABD[1, 2] += la.Q26_bar * la.thickness
        ABD[1, 3] += la.Q12_bar * z2
        ABD[1, 4] += la.Q22_bar * z2
        ABD[1, 5] += la.Q26_bar * z2
        ABD[2, 0] += la.Q16_bar * la.thickness
        ABD[2, 1] += la.Q26_bar * la.thickness
        ABD[2, 2] += la.Q66_bar * la.thickness
        ABD[2, 3] += la.Q16_bar * z2
        ABD[2, 4] += la.Q26_bar * z2
        ABD[2, 5] += la.Q66_bar * z2
        ABD[3, 0] += la.Q11_bar * z2
        ABD[3, 1] += la.Q12_bar * z2
        ABD[3, 2] += la.Q16_bar * z2
        ABD[3, 3] += la.Q11_bar * z3
        ABD[3, 4] += la.Q12_bar * z3
        ABD[3, 5] += la.Q16_bar * z3
        ABD[4, 0] += la.Q12_bar * z2
        ABD[4, 1] += la.Q22_bar * z2
        ABD[4, 2] += la.Q26_bar * z2
        ABD[4, 3] += la.Q12_bar * z3
        ABD[4, 4] += la.Q22_bar * z3
        ABD[4, 5] += la.Q26_bar * z3
        ABD[5, 0] += la.Q16_bar * z2
        ABD[5, 1] += la.Q26_bar * z2
        ABD[5, 2] += la.Q66_bar * z2
        ABD[5, 3] += la.Q16_bar * z3
        ABD[5, 4] += la.Q26_bar * z3
        ABD[5, 5] += la.Q66_bar * z3
        Ntx += (la.Q11_bar * la.alpha_x + la.Q12_bar * la.alpha_y + la.Q16_bar * la.alpha_xy) * la.thickness
        Nty += (la.Q12_bar * la.alpha_x + la.Q22_bar * la.alpha_y + la.Q26_bar * la.alpha_xy) * la.thickness
        Ntxy += (la.Q16_bar * la.alpha_x + la.Q26_bar * la.alpha_y + la.Q66_bar * la.alpha_xy) * la.thickness
        sb = 5 / 4 * (la.thickness - 4 * z3 / thickness**2)
        H[0, 0] += la.Q44_bar_s * sb
        H[0, 1] += la.Q45_bar_s * sb
        H[1, 0] += la.Q45_bar_s * sb
        H[1, 1] += la.Q55_bar_s * sb
        c3 += la.thickness / la.E3
    ABD = clean(ABD)
    H = clean(H)
    abd = np.linalg.inv(ABD)
    h = np.linalg.inv(H)
    dABD = np.linalg.det(ABD)
    dt1 = np.linalg.det(np.delete(np.delete(ABD, 0, 0), 0, 1))
    Ex = dABD / (dt1 * thickness)
    dt2 = np.linalg.det(np.delete(np.delete(ABD, 1, 0), 1, 1))
    Ey = dABD / (dt2 * thickness)
    dt3 = np.linalg.det(np.delete(np.delete(ABD, 2, 0), 2, 1))
    Gxy = dABD / (dt3 * thickness)
    dt4 = np.linalg.det(np.delete(np.delete(ABD, 0, 1), 1, 0))
    dt5 = np.linalg.det(np.delete(np.delete(ABD, 1, 1), 0, 0))
    nu_xy = dt4 / dt1
    nu_yx = dt5 / dt2
    Gyz = H[0, 0] / thickness
    Gxz = H[1, 1] / thickness
    Ez = thickness / c3
    alpha_x = abd[0, 0] * Ntx + abd[0, 1] * Nty + abd[0, 2] * Ntxy
    alpha_y = abd[1, 0] * Ntx + abd[1, 1] * Nty + abd[1, 2] * Ntxy
    tEx, tEy, tEz = 1 / S[0, 0], 1 / S[1, 1], 1 / S[2, 2]
    tGxy, tGxz, tGyz = 1 / S[5, 5], 1 / S[4, 4], 1 / S[3, 3]
    t_nu_xy, t_nu_xz, t_nu_yz = -S[1, 0] / S[0, 0], -S[2, 0] / S[0, 0], -S[2, 1] / S[1, 1]
    return Laminate(
        name=name,
        layers=orig_layers,
        thickness=thickness,
        fiber_weight=fiber_weight,
        rho=rho,
        vf=vf,
        resin_weight=resin_weight,
        ABD=ABD,
        abd=abd,
        H=H,
        h=h,
        Ex=Ex,
        Ey=Ey,
        Ez=Ez,
        Gxy=Gxy,
        Gyz=Gyz,
        Gxz=Gxz,
        nu_xy=nu_xy,
        nu_yx=nu_yx,
        alpha_x=alpha_x,
        alpha_y=alpha_y,
        wf=wf,
        C=C,
        S=S,
        tEx=tEx,
        tEy=tEy,
        tEz=tEz,
        tGxy=tGxy,
        tGyz=tGyz,
        tGxz=tGxz,
        t_nu_xy=t_nu_xy,
        t_nu_xz=t_nu_xz,
        t_nu_yz=t_nu_yz,
    )
