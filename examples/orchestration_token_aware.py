#!/usr/bin/env python3
"""
Example: Running orchestration with token awareness

This script demonstrates how to run the parallel orchestration
with proper token tracking and configuration.
"""

import asyncio
import os
from src.agentic.flow import parallel_orchestration_flow, weekly_content_flow

def calculate_estimated_tokens(max_rounds: int, batch_size: int) -> int:
    """Calculate estimated tokens for an orchestration run.
    
    Formula: max_rounds × batch_size × 2_agent_types × 15K_tokens_per_agent
    """
    tokens_per_round = batch_size * 2 * 15_000
    total_tokens = tokens_per_round * max_rounds
    return total_tokens


def get_token_budget() -> int | None:
    """Get token budget from environment or user input.
    
    Returns:
        Token budget as int, or None for unlimited
    """
    budget_str = os.getenv("TOKEN_BUDGET")
    if budget_str and budget_str.lower() != "unlimited":
        try:
            return int(budget_str)
        except ValueError:
            print(f"Warning: Invalid TOKEN_BUDGET='{budget_str}', ignoring")
    return None


def recommend_config(budget: int | None) -> tuple[int, int]:
    """Recommend max_rounds and batch_size based on token budget.
    
    Args:
        budget: Token budget, or None for no limit
        
    Returns:
        Tuple of (max_rounds, batch_size)
    """
    if budget is None:
        # No budget constraint, use fast parallel
        return (10, 5)
    
    # Calculate configurations to fit within budget
    # Test different batch_size values (smaller = cheaper)
    for batch_size in [1, 2, 3, 5]:
        tokens_per_round = batch_size * 2 * 15_000
        max_rounds = budget // tokens_per_round
        
        if max_rounds >= 8:  # At least 8 rounds for 26 weeks
            print(f"Recommended: max_rounds={max_rounds}, batch_size={batch_size}")
            print(f"  (uses ~{tokens_per_round * max_rounds:,.0f} of {budget:,.0f} tokens)")
            return (max_rounds, batch_size)
    
    # If budget very tight, use conservative sequential
    print("Budget very tight, using conservative mode")
    print("  (sequential-like processing, low token usage)")
    return (26, 1)


async def run_orchestration_with_tokens():
    """Main example: Run orchestration with token awareness."""
    
    print("=" * 60)
    print("CNCF Landscape Orchestration - Token-Aware Example")
    print("=" * 60)
    
    # Option 1: Budget-based configuration
    print("\n[1] Budget-based configuration:")
    budget = get_token_budget()
    if budget:
        print(f"Token budget: {budget:,.0f} tokens")
        max_rounds, batch_size = recommend_config(budget)
    else:
        print("No token budget limit set")
        max_rounds, batch_size = (10, 5)  # Default fast config
    
    # Option 2: Manual configuration
    print("\n[2] Manual configuration:")
    print("(Set environment variables to override)")
    print(f"  MAX_ROUNDS={os.getenv('MAX_ROUNDS', max_rounds)}")
    print(f"  BATCH_SIZE={os.getenv('BATCH_SIZE', batch_size)}")
    
    # Allow override from environment
    max_rounds = int(os.getenv("MAX_ROUNDS", max_rounds))
    batch_size = int(os.getenv("BATCH_SIZE", batch_size))
    
    # Calculate estimated cost
    print("\n[3] Estimated cost:")
    estimated_tokens = calculate_estimated_tokens(max_rounds, batch_size)
    estimated_cost_gpt4 = (estimated_tokens / 1_000_000) * 3  # ~$3 per 1M tokens
    estimated_cost_claude = (estimated_tokens / 1_000_000) * 3
    
    print(f"Configuration: max_rounds={max_rounds}, batch_size={batch_size}")
    print(f"Estimated tokens: {estimated_tokens:,.0f}")
    print(f"Estimated cost (GPT-4o): ${estimated_cost_gpt4:.2f}")
    print(f"Estimated cost (Claude): ${estimated_cost_claude:.2f}")
    print(f"Note: Actual may vary based on early exit and tool usage")
    
    # Confirmation
    print("\n[4] Proceed?")
    response = input("Run orchestration? [y/N]: ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    # Run orchestration
    print("\n[5] Starting orchestration...\n")
    print("-" * 60)
    await parallel_orchestration_flow(max_rounds=max_rounds, batch_size=batch_size)
    print("-" * 60)
    print("\n✓ Orchestration complete!")


async def run_development_test():
    """Quick development test: Single week, small token usage."""
    print("\n=== Development Test (Week A only) ===")
    print("Configuration: weekly_content_flow(limit=50)")
    print("Estimated tokens: ~500K")
    print("Estimated cost: ~$1.50 (GPT-4o)")
    
    response = input("Run? [y/N]: ").strip().lower()
    if response != 'y':
        return
    
    await weekly_content_flow(limit=50)
    print("✓ Test complete")


async def run_phased_orchestration():
    """Run orchestration in phases to stay within budget."""
    print("\n=== Phased Orchestration (Budget-aware) ===")
    
    # Phase 1: Weeks A-M (13 weeks)
    print("Phase 1: Processing weeks A-M (13 weeks)")
    max_rounds_1 = 8
    batch_size_1 = 3
    tokens_1 = calculate_estimated_tokens(max_rounds_1, batch_size_1)
    print(f"  Config: max_rounds={max_rounds_1}, batch_size={batch_size_1}")
    print(f"  Estimated tokens: {tokens_1:,.0f}")
    
    response = input("Start Phase 1? [y/N]: ").strip().lower()
    if response == 'y':
        await parallel_orchestration_flow(max_rounds=max_rounds_1, batch_size=batch_size_1)
        print("✓ Phase 1 complete\n")
    
    # Phase 2: Weeks N-Z (13 weeks)
    print("Phase 2: Processing weeks N-Z (13 weeks)")
    max_rounds_2 = 8
    batch_size_2 = 3
    tokens_2 = calculate_estimated_tokens(max_rounds_2, batch_size_2)
    print(f"  Config: max_rounds={max_rounds_2}, batch_size={batch_size_2}")
    print(f"  Estimated tokens: {tokens_2:,.0f}")
    print(f"  Phase 1 + Phase 2 total: {tokens_1 + tokens_2:,.0f} tokens")
    
    response = input("Start Phase 2? [y/N]: ").strip().lower()
    if response == 'y':
        await parallel_orchestration_flow(max_rounds=max_rounds_2, batch_size=batch_size_2)
        print("✓ Phase 2 complete")
        print(f"✓ All phases complete - Total: {tokens_1 + tokens_2:,.0f} tokens")


async def main():
    """Main entry point with menu."""
    print("\n" + "=" * 60)
    print("CNCF Landscape - Orchestration Examples")
    print("=" * 60)
    print("\nChoose an option:")
    print("  1. Full orchestration (token-aware)")
    print("  2. Development test (Week A only)")
    print("  3. Phased execution (budget-aware)")
    print("  4. Exit")
    
    choice = input("\nSelect [1-4]: ").strip()
    
    if choice == "1":
        await run_orchestration_with_tokens()
    elif choice == "2":
        await run_development_test()
    elif choice == "3":
        await run_phased_orchestration()
    elif choice == "4":
        print("Exiting.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    # Environment variable examples:
    # TOKEN_BUDGET=1000000 - Set token budget to 1M
    # MAX_ROUNDS=10        - Override max_rounds
    # BATCH_SIZE=3         - Override batch_size
    
    # Example usage:
    # TOKEN_BUDGET=1000000 python examples/orchestration_token_aware.py
    
    asyncio.run(main())
