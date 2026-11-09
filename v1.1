from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

ICT = timezone(timedelta(hours=7))
DEFAULT_YEAR = 2025

CONFIG_TEMPLATE = {
    "name": "Entity Name",
    "START_MONEY": 0,
    "RATE_PHASES": [
        ("1/1/2026 12:00", 15.0),
    ],
    "TRANSACTIONS": [],
}

PAT = re.compile(
    r"^\s*([+-]?\d[\d,]*)\s*-\s*"
    r"(\d{1,2}):(\d{2})\s*-\s*"
    r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\s*$"
)

def parse_entry(s: str):
    match = PAT.match(s)
    if not match:
        raise ValueError(
            "Invalid format. Use: amount-HH:MM-DD/MM or amount-HH:MM-DD-DD/MM/YYYY"
        )

    raw_amount = match.group(1)
    hh = int(match.group(2))
    mm = int(match.group(3))
    day = int(match.group(4))
    month = int(match.group(5))
    year_str = match.group(6)

    if year_str is None:
        year = DEFAULT_YEAR
    elif len(year_str) == 2:
        year = 2000 + int(year_str)
    else:
        year = int(year_str)

    # better default: implicit sign is positive
    if raw_amount.startswith("-"):
        sign = -1
    else:
        sign = 1

    amount_value = int(raw_amount.replace(",", "").replace("+", "").replace("-", ""))
    amount = Decimal(sign * amount_value)

    dt = datetime(year, month, day, hh, mm, tzinfo=ICT)
    return {
        "ts": dt.timestamp(),
        "amount": amount,
        "dt": dt,
        "raw": s,
    }

def normalize_rate_phases(rate_phases):
    normalized = []
    for start_str, rate in rate_phases:
        start_dt = datetime.strptime(start_str, "%d/%m/%Y %H:%M").replace(tzinfo=ICT)
        normalized.append((start_dt, Decimal(str(rate))))
    normalized.sort(key=lambda x: x[0])
    return normalized

def get_rate_at(ts: float, rate_phases):
    normalized = normalize_rate_phases(rate_phases)
    current_rate = normalized[0][1]
    for start_dt, rate in normalized:
        if ts >= start_dt.timestamp():
            current_rate = rate
        else:
            break
    return current_rate

def calculate_balance(config, now_ts=None):
    start_money = Decimal(str(config["START_MONEY"]))
    rate_phases = normalize_rate_phases(config["RATE_PHASES"])
    transactions = [parse_entry(e) for e in config["TRANSACTIONS"]]

    now_dt = datetime.now(ICT) if now_ts is None else datetime.fromtimestamp(now_ts, ICT)
    now_ts = now_dt.timestamp()

    balance = start_money

    # apply rate accrual
    for i, (start_dt, rate) in enumerate(rate_phases):
        start_ts = start_dt.timestamp()
        if now_ts <= start_ts:
            continue

        if i + 1 < len(rate_phases):
            next_ts = rate_phases[i + 1][0].timestamp()
        else:
            next_ts = now_ts

        time_span_seconds = max(0, min(now_ts, next_ts) - start_ts)
        balance += (Decimal(time_span_seconds) / Decimal(60)) * rate

    for tx in sorted(transactions, key=lambda x: x["ts"]):
        if tx["ts"] <= now_ts:
            balance += tx["amount"]

    return balance, now_dt

def pretty_amt(value: Decimal | float | int) -> str:
    d = Decimal(str(value))
    q = d.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if q == q.to_integral_value():
        return f"{q.quantize(Decimal('1')):,.0f}".replace(",", ".")
    return f"{q:,.1f}".replace(",", ".")

# Example
if __name__ == "__main__":
    bal, now_dt = calculate_balance(CONFIG_TEMPLATE)
    print(f"Balance: {pretty_amt(bal)}$")
