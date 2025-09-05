EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "extracted": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "company": {"type": ["string", "null"]},
                        "industry": {"type": ["string", "null"]},
                    },
                    "additionalProperties": True,
                },
                "terms": {
                    "type": "object",
                    "properties": {
                        "price_band": {"type": ["array", "null"], "items": {"type": "number"}},
                        "lot_size": {"type": ["integer", "null"]},
                        "open_date": {"type": ["string", "null"]},
                        "close_date": {"type": ["string", "null"]},
                    },
                    "additionalProperties": True,
                },
                "financials": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "fy": {"type": ["string", "null"]},
                            "revenue_cr": {"type": ["number", "null"]},
                            "ebitda_cr": {"type": ["number", "null"]},
                            "pat_cr": {"type": ["number", "null"]},
                            "networth_cr": {"type": ["number", "null"]},
                            "debt_cr": {"type": ["number", "null"]},
                            "cfo_cr": {"type": ["number", "null"]},
                        },
                        "required": ["fy"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["meta", "terms", "financials"],
            "additionalProperties": False,
        }
    },
    "required": ["extracted"],
    "additionalProperties": False,
} 