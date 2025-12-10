"""Lamina model and creation function."""

import math

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from .fiber import Fiber
from .resin import Resin
from .utils import tbar


class Lamina(BaseModel):
    """Represents a lamina layer."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    fiber: Fiber
    resin: Resin
    fiber_weight: float = Field(..., gt=0)
    angle: float
    vf: float = Field(..., ge=0, le=1)
    thickness: float
    resin_weight: float
    E1: float
    E2: float
    E3: float
    G12: float
    G13: float
    G23: float
    nu12: float
    nu13: float
    nu23: float
    alpha_x: float
    alpha_y: float
    alpha_xy: float
    Q11_bar: float
    Q12_bar: float
    Q16_bar: float
    Q22_bar: float
    Q26_bar: float
    Q66_bar: float
    Q44_bar_s: float
    Q55_bar_s: float
    Q45_bar_s: float
    rho: float
    C: np.ndarray


def lamina(
    fiber: Fiber, resin: Resin, fiber_weight: float, angle: float, vf: float
) -> Lamina:
    """Create a Lamina of unidirectional fibers in resin."""
    vm = 1.0 - vf
    fiber_thickness = fiber_weight / (fiber.rho * 1000)
    thickness = fiber_thickness * (1 + vm / vf)
    resin_weight = thickness * vm * resin.rho * 1000
    E1 = vf * fiber.E1 + resin.E * vm
    xi = 1.5
    eta = (fiber.E1 / resin.E - 1) / (fiber.E1 / resin.E + xi)
    E2 = resin.E * ((1 + xi * eta * vf) / (1 - eta * vf))
    E3 = E2
    nu12 = fiber.nu12 * vf + resin.nu * vm
    nu13 = nu12
    Gm = resin.E / (2 * (1 + resin.nu))
    G12 = Gm * (1 + vf) / (1 - vf)
    G13 = G12
    nu21 = nu12 * E2 / E1
    Kf = fiber.E1 / (3 * (1 - 2 * fiber.nu12))
    Km = resin.E / (3 * (1 - 2 * resin.nu))
    K = 1 / (vf / Kf + vm / Km)
    nu23 = 1 - nu21 - E2 / (3 * K)
    G23 = E2 / (2 * (1 + nu23))
    a = math.radians(float(angle))
    m, n = math.cos(a), math.sin(a)
    Sp = [
        [1 / E1, -nu12 / E1, -nu13 / E1, 0, 0, 0],
        [-nu12 / E1, 1 / E2, -nu23 / E2, 0, 0, 0],
        [-nu13 / E1, -nu23 / E2, 1 / E3, 0, 0, 0],
        [0, 0, 0, 1 / G23, 0, 0],
        [0, 0, 0, 0, 1 / G13, 0],
        [0, 0, 0, 0, 0, 1 / G12],
    ]
    Cp = np.linalg.inv(Sp)
    Tbar = tbar(angle)
    C = np.matmul(np.matmul(np.transpose(Tbar), Cp), Tbar)
    m2 = m * m
    m3, m4 = m2 * m, m2 * m2
    n2 = n * n
    n3, n4 = n2 * n, n2 * n2
    alpha1 = (fiber.alpha1 * fiber.E1 * vf + resin.alpha * resin.E * vm) / E1
    alpha2 = vf * resin.alpha
    alpha_x = alpha1 * m2 + alpha2 * n2
    alpha_y = alpha1 * n2 + alpha2 * m2
    alpha_xy = 2 * (alpha1 - alpha2) * m * n
    denum = 1 - nu12 * nu21
    Q11, Q12 = E1 / denum, nu12 * E2 / denum
    Q22, Q66 = E2 / denum, G12
    Q44_s = G23
    Q55_s = G12
    Q11_bar = Q11 * m4 + 2 * (Q12 + 2 * Q66) * n2 * m2 + Q22 * n4
    QA = Q11 - Q12 - 2 * Q66
    QB = Q12 - Q22 + 2 * Q66
    Q12_bar = (Q11 + Q22 - 4 * Q66) * n2 * m2 + Q12 * (n4 + m4)
    Q16_bar = QA * n * m3 + QB * n3 * m
    Q22_bar = Q11 * n4 + 2 * (Q12 + 2 * Q66) * n2 * m2 + Q22 * m4
    Q26_bar = QA * n3 * m + QB * n * m3
    Q66_bar = (Q11 + Q22 - 2 * Q12 - 2 * Q66) * n2 * m2 + Q66 * (n4 + m4)
    Q44_bar_s = Q44_s * m2 + Q55_s * n2
    Q55_bar_s = Q44_s * n2 + Q55_s * m2
    Q45_bar_s = (Q55_bar_s - Q44_bar_s) * n * m
    rho = fiber.rho * vf + resin.rho * vm
    return Lamina(
        fiber=fiber,
        resin=resin,
        fiber_weight=fiber_weight,
        angle=angle,
        vf=vf,
        thickness=thickness,
        resin_weight=resin_weight,
        E1=E1,
        E2=E2,
        E3=E3,
        G12=G12,
        G13=G13,
        G23=G23,
        nu12=nu12,
        nu13=nu13,
        nu23=nu23,
        alpha_x=alpha_x,
        alpha_y=alpha_y,
        alpha_xy=alpha_xy,
        Q11_bar=Q11_bar,
        Q12_bar=Q12_bar,
        Q16_bar=Q16_bar,
        Q22_bar=Q22_bar,
        Q26_bar=Q26_bar,
        Q66_bar=Q66_bar,
        Q44_bar_s=Q44_bar_s,
        Q55_bar_s=Q55_bar_s,
        Q45_bar_s=Q45_bar_s,
        rho=rho,
        C=C,
    )
