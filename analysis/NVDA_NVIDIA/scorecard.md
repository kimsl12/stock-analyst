# NVIDIA (NVDA) Scorecard and Strategy
[Lead direct] Date: 2026-04-17

## Scorecard (10 Items, Weighted 100 Points)

Stock Type: Growth Stock
Criteria: Revenue CAGR 33%+, FY26 growth 60.5%, Fwd PER 30.7x

| # | Item | Weight | Score/10 | Weighted | Key Basis |
|---|------|--------|---------|----------|-----------|
| 1 | Moat | 15% | 9.5 | 14.25 | Wide Moat: CUDA ecosystem 400M+ devs, 80-85% share |
| 2 | Profitability | 12% | 9.5 | 11.40 | OPM 63.8%, ROE 108%, NPM 55.3% - #1 globally |
| 3 | Growth | 12% | 8.5 | 10.20 | Rev +60.5% FY26, +33.7% FY27E. Decelerating but strong |
| 4 | Financial Health | 10% | 9.0 | 9.00 | Net cash, debt ratio 22%, AA- rating, FCF 5B |
| 5 | Valuation | 10% | 7.0 | 7.00 | Fwd PER 30.7x, PEG 0.82. Reasonable for growth but high absolute |
| 6 | Momentum | 10% | 6.5 | 6.50 | Short-term correction (-5.8% 3M), LT uptrend. RSI 48 neutral |
| 7 | Flow/Supply | 8% | 6.0 | 4.80 | Institutional neutral, consolidation. No strong signal |
| 8 | Risk | 10% | 6.5 | 6.50 | AI CapEx cycle + export controls + ASIC = medium aggregate risk |
| 9 | Industry | 8% | 9.0 | 7.20 | AI chip market CAGR 30-35%, growth phase, Porter 14/25 |
| 10 | Management | 5% | 9.5 | 4.75 | Jensen Huang 30yr CEO, visionary, aligned via stock ownership |
| | **Total** | **100%** | | **81.60** | |

## Rating
Score: 81.6 / 100
Grade: A (Strong Buy)
Expected Return: +21% (Base Case to 40)

## ATR Stop Loss and Target

### Calculation (per stop-loss-rules.md)
Entry Price: 98.35 (current)
ATR(14): .08

STEP 1: Initial Stop Loss
- Fixed stop (8%): 198.35 x 0.92 = 82.48
- ATR stop (2x): 198.35 - (5.08 x 2) = 88.19
- Initial Stop = MAX(182.48, 188.19) = 88.19 (ATR method, tighter)
- Risk = 198.35 - 188.19 = 0.16 (-5.1%)

STEP 2: Trailing Threshold
- Trail trigger: 198.35 x 1.10 = 18.19
- At 18.19+, switch to trailing stop mode

STEP 3: Trailing Stop (when triggered)
- Trailing stop = current_high - (5.08 x 2)
- Ratchet: never decreases

STEP 4: Target Price
- Risk = 0.16
- Target = 198.35 + (10.16 x 2) = 18.67 (R:R 2:1 minimum)
- Extended target (R:R 3:1) = 198.35 + (10.16 x 3) = 28.83

### Summary
| Level | Price | vs Current |
|-------|-------|------------|
| Stop Loss | 88.19 | -5.1% |
| Entry | 98.35 | - |
| Trail Trigger | 18.19 | +10.0% |
| Target (2:1) | 18.67 | +10.2% |
| Target (3:1) | 28.83 | +15.4% |
| Consensus Target | 39.00 | +20.5% |
| Bull Target | 80.00 | +41.2% |

## Investment Strategy

### Buy Strategy
Type: Staggered Buy (3 tranches)
- Tranche 1 (40%): Current price 98 zone (immediate)
- Tranche 2 (30%): 90-192 (50MA support zone)
- Tranche 3 (30%): 85-188 (strong support / 2xATR zone)
Max position: 5-8% of portfolio (high conviction, growth stock)

### Sell Strategy
- Partial exit (50%): At 30-240 (consensus zone)
- Trail remaining: Switch to trailing stop at 18+
- Full exit trigger: Stop loss at 88.19 or fundamental deterioration

### Monthly Monitoring
1. Hyperscaler CapEx guidance (quarterly earnings)
2. ASIC share of AI inference market
3. China export control policy developments

## Scenarios
| Scenario | Target | EPS | PER | Probability |
|----------|--------|-----|-----|-------------|
| Bull (+41%) | 80 | .00 | 40x | 25% |
| Base (+21%) | 40 | .45 | 37x | 50% |
| Bear (-22%) | 55 | .50 | 28x | 25% |

Expected value: 0.25x280 + 0.50x240 + 0.25x155 = 28.75 (+15.3%)

## Key Insights (3 lines)
1. NVIDIA is the undisputed AI infrastructure leader with Wide Moat (CUDA), exceptional profitability (OPM 64%), and 2-year growth visibility (Blackwell/Rubin). Score 81.6 = Strong Buy.
2. Current Fwd PER 30.7x with PEG 0.82 is reasonable for 37%+ EPS growth. The 88-198 zone offers attractive entry for 20%+ upside to consensus 39.
3. Primary risks are AI CapEx cycle peak-out and ASIC competition in inference. Monthly monitoring of hyperscaler CapEx and ASIC adoption rates is essential. Stop loss at 88.19 (-5.1%).

## Moat vs Risk Consistency Check
Moat: Wide (9.5/10) | Risk: Medium (6.5/10)
No contradiction: Wide Moat with medium risk is consistent because
risks are external (CapEx cycle, regulation) not internal (Moat erosion).
Moat trend remains Positive.

## KB Feedback Loop
[Condition D met] Score >= 70: YES (81.6)
Saving to wiki/analysis/ for permanent archive.
[Condition A] Consensus dates within KB range: OK, no KB update needed
[Condition B] New risk items: None beyond KB
[Condition C] Target vs KB consensus: 40 within 80-300 range: OK