## Sample requests

```bash
curl -d '{"request":{"command":"test"}}' -H "Content-Type: application/json" -X POST http://localhost:5000/alice/
curl -d '{"request":{"command":"test"}}' -H "Content-Type: application/json" -X POST https://alice.sandbox.rezvov.com/alice/ | jq
```