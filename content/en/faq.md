# FAQ

### Can I turn thinking off?
No. This model always thinks; `none` and `thinking.type=disabled` are ignored.

### Which effort should I start with?
Use `low` for latency-sensitive short work, `high` for the default balance, and `max` only when the extra reasoning is justified.

### Does a timeout mean the call failed?
No. A network timeout leaves completion state uncertain. Keep the request ID when available and query your own transport logs before deciding whether a new call is safe.
