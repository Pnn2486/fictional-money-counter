import re
from datetime import datetime, timezone, timedelta

# ----------------- CONFIG -----------------
ICT = timezone(timedelta(hours=7))
DEFAULT_YEAR = 2025

CONFIG_TEMPLATE = {
    "name": Player Name",
    "START_MONEY": 0,
    "RATE_PHASES": [
       ("1/1/2026 12:00", 15.0),
   ],
    "TRANSACTIONS": [],
}

# ----------------- REGEX -----------------
PAT = re.compile(
    r"^\s*([+-]?\d[\d,]*)\s*-\s*"
    r"(\d{1,2}):(\d{2})\s*-\s*"
    r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\s*$"
)

# ----------------- FUNCTIONS -----------------
print("—" * 70)


def parse_entry(s):
    m = PAT.match(s)
    if not m:
        raise ValueError(
            "❌ Invalid format. Use amount-HH:MM-DD/MM or amount-HH:MM-DD/MM/YYYY"
        )

    raw_amount = m.group(1)
    hh, mm = int(m.group(2)), int(m.group(3))
    day, month = int(m.group(4)), int(m.group(5))
    year_str = m.group(6)

    year = (
        int(year_str) + 2000
        if year_str and len(year_str) == 2
        else int(year_str) if year_str else DEFAULT_YEAR
    )
    amount_val = int(raw_amount.replace(",", "").replace("+", "").replace("-", ""))

    if raw_amount.startswith("+"):
        sign = 1
    elif raw_amount.startswith("-"):
        sign = -1
    else:
        sign = -1

    amount_signed = sign * amount_val
    dt = datetime(year, month, day, hh, mm, tzinfo=ICT)
    ts = dt.timestamp()

    return {"ts": ts, "amount": amount_signed, "dt": dt, "raw": s}


def get_rate_at(ts, rate_phases):
    current_rate = rate_phases[0][1]
    for start_str, rate in rate_phases:
        start_dt = datetime.strptime(start_str, "%d/%m/%Y %H:%M").replace(tzinfo=ICT)
        if ts >= start_dt.timestamp():
            current_rate = rate
        else:
            break
    return current_rate


def calculate_balance(config, now_ts=None):
    START_MONEY = config["START_MONEY"]
    RATE_PHASES = config["RATE_PHASES"]
    TRANSACTIONS = [parse_entry(e) for e in config["TRANSACTIONS"]]

    now_dt = (
        datetime.now(ICT) if now_ts is None else datetime.fromtimestamp(now_ts, ICT)
    )
    now_ts = now_dt.timestamp()
    balance = START_MONEY

    prev_ts = None
    for i, (start_str, rate) in enumerate(RATE_PHASES):
        start_dt = datetime.strptime(start_str, "%d/%m/%Y %H:%M").replace(tzinfo=ICT)
        start_ts = start_dt.timestamp()

        if prev_ts is None:
            prev_ts = start_ts

        if now_ts > start_ts:
            if i + 1 < len(RATE_PHASES):
                next_dt = datetime.strptime(
                    RATE_PHASES[i + 1][0], "%d/%m/%Y %H:%M"
                ).replace(tzinfo=ICT)
                next_ts = next_dt.timestamp()
            else:
                next_ts = now_ts

            time_span = min(now_ts, next_ts) - start_ts
            balance += (time_span / 60) * rate

        prev_ts = start_ts

    applied, pending = [], []
