# Token Optimization & Iteration Control

## Overview

Token limits are critical for cost control and API rate limits. This document covers how the parallel orchestration handles iterations and strategies to optimize token usage.

## Iteration Control Mechanisms

### 1. max_rounds Parameter

**Location**: `src/agentic/flow.py` in `parallel_orchestration_flow()`

```python
async def parallel_orchestration_flow(max_rounds: int = 10, batch_size: int = 5):
    """
    Args:
        max_rounds: Maximum orchestration rounds (prevents infinite loops)
        batch_size: Number of tasks per agent per round
    """
```

**What it does**: Limits orchestration rounds, not individual agent invocations.

- One **round** = get ready tasks → dispatch researchers + writers in parallel → save results
- Multiple **agent invocations** per round (parallel dispatch)
- Multiple **API calls** per agent (may need multiple calls per research task)

**Example**:
```
max_rounds=10, batch_size=5
│
├─ Round 1: 5 researchers + up to 5 writers (potentially 10 API calls)
├─ Round 2: 5 researchers + up to 5 writers (potentially 10 API calls)
├─ ...
└─ Round 10: remaining tasks or early exit if complete

Total API calls: up to 10 rounds × 10 agents = ~100 agent invocations
Each invocation may consume 100K-500K tokens
```

### 2. batch_size Parameter

Controls tasks dispatched per agent per round:

```python
max_rounds=10, batch_size=5

Per Round:
- Researcher dispatch: min(5 ready research tasks, batch_size=5) → up to 5 parallel agents
- Writer dispatch: min(5 ready blog_post tasks, batch_size=5) → up to 5 parallel agents
```

**Parallelism vs Cost Trade-off**:
- ↑ `batch_size` → ↑ parallelism, ↓ rounds needed, ↑ tokens per round
- ↓ `batch_size` → ↓ parallelism, ↑ rounds needed, ↓ tokens per round

### 3. Early Exit Condition

```python
while round_num < max_rounds:
    researcher_tasks = await get_ready_tasks_batch("researcher", batch_size)
    writer_tasks = await get_ready_tasks_batch("writer", batch_size)
    
    if not researcher_tasks and not writer_tasks:
        logger.info("No more ready tasks. Orchestration complete.")
        break  # ← Exit before max_rounds if all work done
```

**Benefit**: If all 26 weeks complete early, no waste of remaining rounds.

## Token Cost Per Orchestration

### Cost Breakdown

```
Per Agent Invocation:
├─ Context (system prompt + tools + instructions): ~1-2K tokens
├─ Input (project metadata, research results):     ~1-10K tokens
│  └─ Writer gets ALL research results for week    (can be large)
├─ Agent reasoning:                                 ~2-5K tokens
└─ Output (research summary or blog draft):         ~5-20K tokens

Total per agent call: ~9-37K tokens (avg ~15K)

Per Round with batch_size=5:
├─ 5 researchers × 15K = 75K tokens
├─ 5 writers × 20K = 100K tokens (writers use more due to research context)
└─ Round total: ~175K tokens

Full Orchestration:
max_rounds=10, avg 8 rounds to complete = ~1.4M tokens
```

### High Token Usage Scenarios

1. **Large batch_size**: More agents per round
2. **Many weeks**: More rounds to process all
3. **Large research results**: Writer context bloat
4. **Long web searches**: Researcher tool calls

### Low Token Usage Scenarios

1. **Small batch_size** (1-2): Sequential-like processing
2. **Few weeks**: Quick completion
3. **Context optimization**: Reduced research summaries
4. **Limited tool calls**: Cached or pre-fetched data

## Optimization Strategies

### Strategy 1: Tune batch_size

```python
# Conservative (low token cost)
await parallel_orchestration_flow(max_rounds=26, batch_size=1)
# → ~1 task per agent per round
# → ~26 rounds
# → ~400K tokens total

# Balanced (moderate token cost, good parallelism)
await parallel_orchestration_flow(max_rounds=15, batch_size=3)
# → ~3 tasks per agent per round
# → ~8-10 rounds average
# → ~1.2-1.5M tokens total

# Aggressive (high token cost, max parallelism)
await parallel_orchestration_flow(max_rounds=5, batch_size=10)
# → ~10 tasks per agent per round
# → forces completion in few rounds or fails
# → ~2-3M tokens total
```

**Recommendation**: Start with `batch_size=3` for balanced throughput/cost.

### Strategy 2: Limit Weeks

Not all 26 weeks needed for testing. Use sequential flow with limit:

```python
# Test with just Week A
await weekly_content_flow(limit=50)  # ~50 items
# → ~500K tokens

# Full production run
await weekly_content_flow(limit=None)  # All 26 weeks
# → ~3-5M tokens
```

### Strategy 3: Research Context Optimization

Current implementation already does this:
- `read_week_summary()` with `summary_only=True` (20 lines instead of 500+)
- `get_all_weeks_status()` returns only incomplete weeks

**Writer receives**: Research results list → Already optimized

**Optimization opportunities**:
1. Compress research results for writer input
2. Cache research results to avoid re-generation
3. Use summaries instead of full research

### Strategy 4: Token Budget Tracking

**Manual estimation**:
```python
# Before running orchestration
batch_size = 3
max_rounds = 10
estimated_tokens = batch_size * 2 * 15_000 * max_rounds
# batch_size × (researchers + writers) × avg_tokens × max_rounds
# 3 × 2 × 15K × 10 = 900K tokens

# Actual usage will vary based on:
# - Early exit (completes faster)
# - Research depth (more searches = more tokens)
# - Model efficiency (varies by model)
```

**Logging integration**:
```python
# Add to flow for monitoring
logger.info(f"Estimated tokens for this run: ~{estimated_tokens:,.0f}")
logger.info(f"batch_size={batch_size}, max_rounds={max_rounds}")
```

### Strategy 5: Progressive Execution

Run in phases rather than all at once:

```python
# Phase 1: Test weeks A-C with conservative settings
await weekly_content_flow(limit=150)  # ~3 weeks × 50 items

# Phase 2: Run weeks D-Z
await weekly_content_flow(limit=1150)  # Remaining ~23 weeks
```

## Token Limits by Model

### Google Gemini Models
- Input: 1M tokens (models available)
- Output: 50K tokens
- **Single agent call**: ~15-20K tokens (safe)
- **Safe batch_size**: 5-10 per round

### OpenAI GPT-4/4o
- Input: 128K tokens
- Output: 4K tokens
- **Single agent call**: ~15-20K tokens (safe)
- **Safe batch_size**: 3-5 per round
- **Cost**: ~$0.03 per 1M input tokens

### Anthropic Claude
- Input: 200K tokens
- Output: 4K tokens
- **Single agent call**: ~15-20K tokens (safe)
- **Safe batch_size**: 5-10 per round

### Gateway/Vertex AI
- Depends on underlying model
- Typically same as base model

## Configuration Recommendations

### Development/Testing
```python
# Quick testing: ~100-200K tokens
await weekly_content_flow(limit=10)  # 1 week partial
```

### Staging/Validation
```python
# Full coverage testing: ~500K-1M tokens
await weekly_content_flow(limit=None)  # All weeks, sequential
```

### Production
```python
# Option A: Sequential (predictable, safer)
await weekly_content_flow(limit=None)
# ~3-5M tokens, stable token usage per week

# Option B: Parallel batched (faster, higher peak token usage)
await parallel_orchestration_flow(max_rounds=15, batch_size=3)
# ~1-2M tokens, completion in ~8-10 rounds
```

## Monitoring & Limits

### Add Token Tracking

```python
# In src/agentic/flow.py
@task
async def log_round_stats(round_num: int, batch_size: int):
    logger = get_run_logger()
    estimated_round_tokens = batch_size * 2 * 15_000  # 2 agent types
    logger.info(
        f"Round {round_num}: est. {estimated_round_tokens:,.0f} tokens "
        f"({batch_size} tasks × 2 agents)"
    )
```

### Environment Variable Limits

```bash
# In .env or config
MAX_ROUNDS=10
BATCH_SIZE=3
ESTIMATED_TOKEN_BUDGET=1500000  # 1.5M tokens
```

### API Rate Limits

Different from token limits - also important:

```python
# Add delays to respect rate limits
import asyncio

async def research_item_with_rate_limit(item, week_letter, delay=0.5):
    await asyncio.sleep(delay)  # Wait between API calls
    return await research.research_item(item, week_letter)
```

## Cost Calculation

### Per-Week Costs

```
Week: ~50 items
├─ Research: 50 items × 1 invocation × 10K tokens = 500K tokens
├─ Writing: 1 blog post × 50K tokens (includes all research) = 50K tokens
├─ Overhead: tools, retries, ~20K tokens
└─ Total per week: ~570K tokens

All 26 weeks: ~14.8M tokens
```

**Cost by model**:
- Gemini (free tier): 2M tokens/month free, then pay
- GPT-4o: 1M tokens ≈ $3 (input), ~$0.30 (output) → 26 weeks ≈ $45
- Claude 3.5 Sonnet: 1M tokens ≈ $3 (input), ~$0.15 (output) → 26 weeks ≈ $45

### Cost Optimization

1. **Use smaller batch_size** (1-2): 50% fewer rounds, 50% cost reduction
2. **Cache research results**: Reuse summaries between writing attempts
3. **Limit weeks initially**: Test with 5 weeks before full 26
4. **Batch processing**: Process weeks in phases to avoid API spikes

## Best Practices

### ✅ Do
- Set `max_rounds` to prevent runaway loops
- Monitor early exit (logs when no more ready tasks)
- Use `batch_size=3` as default (balanced)
- Track estimated vs actual tokens per run
- Test with limited weeks first
- Use sequential flow for predictable budgeting

### ❌ Don't
- Set `max_rounds=1000` (uncontrolled)
- Use `batch_size=50` without testing (token spike)
- Run all 26 weeks on first try
- Ignore early exit condition (can waste rounds)
- Stack multiple orchestrations without monitoring
- Use aggressive settings without cost estimates

## Example: Full Production Run

```python
# Recommended production configuration
async def run_production_workflow():
    logger = get_run_logger()
    
    # Phase 1: Validate with subset
    logger.info("Phase 1: Validating with 3 weeks...")
    await weekly_content_flow(limit=150)  # ~1.7M tokens
    logger.info("✓ Phase 1 complete")
    
    # Phase 2: Run remaining weeks in parallel batches
    logger.info("Phase 2: Processing remaining 23 weeks...")
    await parallel_orchestration_flow(
        max_rounds=12,      # ~12 rounds for 23 weeks × 50 items
        batch_size=3        # 3 per agent = ~90K tokens/round
    )
    logger.info("✓ Production run complete")
    logger.info("Total estimated tokens: ~2.5-3M")

if __name__ == "__main__":
    asyncio.run(run_production_workflow())
```

## Troubleshooting High Token Usage

### Symptom: Token usage higher than expected

**Causes**:
1. `batch_size` too large
2. Research results very long (many tool calls)
3. Many retries (failures + re-attempts)
4. Inefficient system prompts

**Debug**:
```python
# Check orchestration logs
# Look for: "est. X tokens per round"

# Monitor model usage:
# - Google Cloud Console for Vertex AI
# - OpenAI Usage Dashboard
# - Anthropic usage API

# Reduce batch_size and retry
await parallel_orchestration_flow(max_rounds=20, batch_size=1)
```

### Symptom: Runs out of tokens before completion

**Solution**:
```python
# Option A: Run in multiple sessions
await weekly_content_flow(limit=500)  # First 10 weeks
# ... later ...
await weekly_content_flow(limit=500)  # Next 10 weeks

# Option B: More aggressive batching
await parallel_orchestration_flow(max_rounds=8, batch_size=2)
```

## Related Documentation

- [Graph-Driven Orchestration](graph-driven-orchestration.md) - Architecture details
- [Agentic Workflow](agentic-workflow.md) - Agent behaviors
- [Architecture](architecture.md) - System design
