"""Small cross-app utilities."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


class PriceTierError(ValueError):
    """Raised when a pool's price_tiers payload is malformed."""


def validate_price_tiers(tiers: Any) -> list[dict[str, int | str]]:
    """Validate and normalise a pool's ``price_tiers`` JSON payload."""
    if not isinstance(tiers, list) or not tiers:
        raise PriceTierError("price_tiers must be a non-empty list")

    seen: set[int] = set()
    normalised: list[dict[str, int | str]] = []

    for i, tier in enumerate(tiers):
        if not isinstance(tier, dict):
            raise PriceTierError(f"tier {i}: must be an object")

        min_units = tier.get("min_units")
        price = tier.get("price_per_unit")

        if not isinstance(min_units, int) or min_units < 1:
            raise PriceTierError(f"tier {i}: min_units must be a positive int")
        if min_units in seen:
            raise PriceTierError(f"tier {i}: duplicate min_units {min_units}")
        seen.add(min_units)

        try:
            price_dec = Decimal(str(price))
        except (InvalidOperation, TypeError) as exc:
            raise PriceTierError(f"tier {i}: invalid price_per_unit") from exc
        if price_dec <= 0:
            raise PriceTierError(f"tier {i}: price_per_unit must be > 0")

        normalised.append(
            {
                "min_units": min_units,
                "price_per_unit": f"{price_dec:.2f}",
            }
        )

    normalised.sort(key=lambda t: t["min_units"])
    return normalised


def price_for_units(unit_count: int, tiers: list[dict[str, Any]]) -> Decimal:
    """Return the per-unit price applicable at ``unit_count``."""
    if not tiers:
        raise PriceTierError("no tiers configured")

    applicable = sorted(tiers, key=lambda t: t["min_units"])
    chosen = applicable[0]
    for tier in applicable:
        if unit_count >= tier["min_units"]:
            chosen = tier
        else:
            break
    return Decimal(str(chosen["price_per_unit"]))
