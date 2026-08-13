# Source registry contract

Keep executable source metadata in a versioned JSON registry. A source is eligible for normal discovery only when its status is `enabled` and its contract/fixture check is current.

Each entry must contain:

```json
{
  "id": "institution-example",
  "name": "Example University vacancies",
  "regions": ["Example country"],
  "entry_url": "https://university.example/jobs",
  "access_method": "api|rss|static_pagination|browser_assisted|discovery_only",
  "capabilities": ["advertised_position", "funded_program_route"],
  "pagination": {"kind": "page", "parameter": "page", "max_pages": 5},
  "stable_id": "official vacancy ID or canonical URL",
  "status": "enabled|testing|blocked|disabled",
  "last_health_check": "YYYY-MM-DD",
  "fixture": "tests/fixtures/example.json",
  "contract_test": "tests/test_example.py"
}
```

Discovery-only sources may produce leads but never direct formal results. A newly added source remains `testing` until its fixture and contract test pass. Record selected, skipped, blocked, failed, and zero-result states per run.
