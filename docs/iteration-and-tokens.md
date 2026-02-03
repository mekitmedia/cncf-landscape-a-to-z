# Iteration & Token Limit Quick Reference

## TL;DR - Token Control

The number of iterations is controlled by **two parameters**:

| Parameter | Controls | Default | Range |
|-----------|----------|---------|-------|
| `max_rounds` | Max orchestration rounds (prevents infinite loops) | 10 | 1-100 |
| `batch_size` | Tasks per agent per round | 5 | 1-20 |

```python
# Token estimate per run:
tokens = max_rounds × batch_size × 2 agent_types × 15K tokens/agent
# = max_rounds × batch_size × 30K

# Examples:
# max_rounds=10, batch_size=5 → 1.5M tokens
# max_rounds=10, batch_size=3 → 900K tokens  ← recommended
# max_rounds=26, batch_size=1 → 780K tokens
```

## Choose Your Configuration

### If you want: **Fast completion (parallel)**
```python
await parallel_orchestration_flow(max_rounds=10, batch_size=5)
# → ~8 actual rounds (early exit)
# → ~1.2M tokens
# → ✓ Process all 26 weeks in hours
```

### If you want: **Low token usage**
```python
await parallel_orchestration_flow(max_rounds=26, batch_size=1)
# → Sequential-like, ~26 rounds
# → ~780K tokens
# → ✓ Budget friendly
```

### If you want: **Balanced (recommended)**
```python
await parallel_orchestration_flow(max_rounds=15, batch_size=3)
# → ~8-10 actual rounds
# → ~900K-1.2M tokens
# → ✓ Good parallelism + reasonable cost
```

### If you want: **Testing/validation**
```python
await weekly_content_flow(limit=150)  # ~3 weeks
# → Sequential per-week
# → ~1.7M tokens
# → ✓ Verify pipeline works
```

## How Early Exit Works

```
max_rounds=10 means UP TO 10 rounds, not always 10:

Round 1: 5 research tasks → complete
Round 2: 5 research tasks → complete
Round 3: 3 research + 2 blog_post → complete
Round 4: 2 blog_post → complete
Round 5: [NO READY TASKS] → EXIT EARLY ✓

Actual: 5 rounds used (not 10)
Tokens: 5 × (3 + 3) × 15K = ~450K (not 1.5M)
```

**Key**: Set `max_rounds` high enough, early exit handles completion.

## Iteration Examples

### Scenario: Processing all 26 weeks

```
26 weeks × ~50 items/week = 1,300 items

Configuration: max_rounds=15, batch_size=3

Round 1: [5 research tasks, 0 blog_post] → process
Round 2: [5 research tasks, 0 blog_post] → process
Round 3: [5 research tasks, 2 blog_post] → process  ← First blog ready!
Round 4: [5 research tasks, 3 blog_post] → process
...
Round ~10: [2 research tasks, 3 blog_post] → process
Round ~11: [0 research tasks, 0 blog_post] → EARLY EXIT ✓

Total: ~11 actual rounds
Tokens: 11 × (3 + 3) × 15K = ~990K tokens ✓
```

### Scenario: Testing phase (Week A only)

```
1 week × ~50 items = ~50 items

Configuration: await weekly_content_flow(limit=50)

Week A: Get 50 items → research all 50 → write blog post → done

Total: 1 "round"
Tokens: ~500K-700K tokens ✓
```

## Token Budget by Phase

### Development
```
Phase: Testing pipeline
Config: weekly_content_flow(limit=50)
Tokens: ~500K
Cost: ~$1.50 (GPT-4) / $1.50 (Claude)
```

### Staging
```
Phase: Full validation
Config: weekly_content_flow(limit=None)  # All 26 weeks
Tokens: ~3-5M
Cost: ~$150 (GPT-4) / $150 (Claude)
```

### Production
```
Phase: Real-time updates
Config: parallel_orchestration_flow(max_rounds=15, batch_size=3)
Tokens: ~900K per full run
Cost: ~$27 (GPT-4) / $27 (Claude)
Can run ~3 times/month within typical API budgets
```

## How to Stay Within Token Limits

### Method 1: Reduce batch_size
```python
# Original
await parallel_orchestration_flow(max_rounds=10, batch_size=5)  # 1.5M tokens

# Reduced
await parallel_orchestration_flow(max_rounds=10, batch_size=2)  # 600K tokens
# → Takes more rounds but lower per-round cost
```

### Method 2: Reduce max_rounds
```python
# Original
await parallel_orchestration_flow(max_rounds=15, batch_size=3)  # 1.2M tokens

# Reduced
await parallel_orchestration_flow(max_rounds=8, batch_size=3)  # 720K tokens
# → May not complete all weeks, needs manual continuation
```

### Method 3: Sequential with limit
```python
# Original
await parallel_orchestration_flow(max_rounds=15, batch_size=5)  # 1.5M tokens

# Sequential in phases
await weekly_content_flow(limit=650)  # Weeks A-M: ~3.9M tokens
await weekly_content_flow(limit=650)  # Weeks N-Z: ~3.9M tokens
# Split across different sessions/days
```

### Method 4: Skip completed weeks
```python
# Don't reprocess - orchestrator does early exit if:
# - Week blog_post already completed
# - All items in week already completed
# → Automatically reduces tokens on re-runs
```

## Monitoring Token Usage

### Before Running
```python
max_rounds = 10
batch_size = 3
estimated = max_rounds * batch_size * 2 * 15_000
print(f"Estimated tokens: {estimated:,.0f}")  # Output: 900,000
```

### During Running
```
Logs will show:
  Estimated ~450,000 tokens/round
  Estimated total: ~4,500,000 tokens (actual varies by early exit)
  Round 1: est. 450,000 tokens
  ...
  ✓ No more ready tasks. Early exit after 8 rounds.
  Actual estimated tokens: ~3,600,000
```

### After Running
Check model usage dashboard:
- **Google Cloud Console** → Vertex AI → Usage
- **OpenAI** → Usage dashboard
- **Anthropic** → API Usage

## Recommended Starting Point

For your CNCF landscape project:

```python
# Start here for balanced performance/cost
await parallel_orchestration_flow(max_rounds=15, batch_size=3)

# Expected results:
# - Completion: ~8-10 rounds (1-2 hours)
# - Token usage: ~900K-1.2M
# - All 26 weeks processed ✓
# - Cost: ~$27-36 (GPT-4o)
```

If too expensive, reduce `batch_size` to 1-2.  
If too slow, increase `batch_size` to 5-10.

## See Also
- [Graph-Driven Orchestration](graph-driven-orchestration.md) - Architecture details
- [Token Optimization](token-optimization.md) - Detailed token analysis
- [Agentic Workflow](agentic-workflow.md) - Agent behaviors
