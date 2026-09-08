# Temporal routing audit

Run

```bash
python examples/audit_temporal_routing.py
```

Expected qualitative pattern:

```text
rho=0.00 -> alternation routing, gain 0.25
rho=0.25 -> alternation routing, gain 0.125
rho=0.50 -> indifferent, gain 0
rho=0.75 -> persistence routing, gain 0.125
rho=1.00 -> persistence routing, gain 0.25
```

The symmetry around `rho=1/2` is the key result: predictable persistence and predictable alternation both create routing value, whereas temporal independence destroys it.
