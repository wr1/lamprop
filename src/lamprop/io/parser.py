"""Parser for YAML lamprop files."""
from __future__ import annotations

from typing import Any

import yaml

from lamprop.core.fiber import Fiber
from lamprop.core.lamina import lamina
from lamprop.core.laminate import laminate
from lamprop.core.resin import Resin
from lamprop.generic import fibers as generic_fibers
from lamprop.generic import resins as generic_resins

info: list[str] = []
warn: list[str] = []

def parse(filename: str) -> list[laminate]:
    """Parse a YAML lamprop file."""
    info.clear()
    warn.clear()
    try:
        info.append(f'Reading file "{filename}".')
        from pathlib import Path
        data = yaml.safe_load(Path(filename).read_text(encoding="utf-8")) or {}
    except Exception as e:
        warn.append(f'Cannot read "{filename}": {e}')
        return []
    fdict = _get_components(data.get("fibers", []), Fiber)
    info.append(f"Found {len(fdict)} fibers, including {len(generic_fibers)} generic fibers.")
    rdict = _get_components(data.get("resins", []), Resin)
    info.append(f"Found {len(rdict)} resins, including {len(generic_resins)} generic resins.")
    laminates = []
    for lam_data in data.get("laminates", []):
        lam = _laminate(lam_data, rdict, fdict)
        if lam:
            laminates.append(lam)
    info.append(f"Found {len(laminates)} laminates")
    return laminates

def _get_components(items: list[dict[str, Any]], model) -> dict[str, Any]:
    """Parse components from list of dicts."""
    rv = {}
    for item in items:
        try:
            comp = model(**item)
            rv[comp.name] = comp
        except (ValueError, TypeError) as e:
            warn.append(f"Error parsing {model.__name__}: {e}")
    return rv

def _laminate(lam_data: dict[str, Any], resins: dict[str, Resin], fibers: dict[str, Fiber]) -> laminate:
    """Parse a laminate definition."""
    name = lam_data.get("name", "")
    if not name:
        warn.append("No laminate name")
        return None
    resin_name = lam_data.get("resin", "")
    if resin_name not in resins:
        warn.append(f'Unknown resin "{resin_name}"')
        return None
    vf = lam_data.get("vf", 0.5)
    layers = []
    for layer_data in lam_data.get("layers", []):
        if isinstance(layer_data, str):
            layers.append(layer_data)
        else:
            fiber_name = layer_data.get("fiber", "")
            if fiber_name not in fibers:
                warn.append(f'Unknown fiber "{fiber_name}"')
                continue
            la = lamina(fibers[fiber_name], resins[resin_name], layer_data["weight"], layer_data["angle"], vf)
            layers.append(la)
    if not layers:
        warn.append(f'Empty laminate "{name}"')
        return None
    if lam_data.get("symmetric", False):
        layers = _extend_symmetric(layers)
    return laminate(name, layers)

def _extend_symmetric(original: list) -> list:
    """Create symmetric extension."""
    # Simplified symmetric extension
    return original + original[::-1]
