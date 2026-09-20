import streamlit as st
import random
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="The Analyst's Ledger",
    page_icon="📊",
    layout="wide"
)

DATA = {
    "1 · Foundations": [
        {"term": "Time Value of Money (TVM)", "star": True,
         "definition": "A rupee today is worth more than a rupee tomorrow, because today's rupee can be invested.",
         "example": "₹1,00,000 today beats ₹1,00,000 in 3 years — invested at 6%, it becomes ~₹1,19,100.",
         "formula": "FV = PV × (1 + r)^n\nPV = FV / (1 + r)^n",
         "worked": "PV=₹1,00,000, r=6%, n=3 → FV = 1,00,000×(1.06)³ = ₹1,19,102",
         "hi": "High discount rate → future cash flows worth much less today; penalizes long-duration/growth assets.",
         "lo": "Low discount rate → future cash flows retain value; favors long-duration/growth assets.",
         "strategy": "Rising-rate cycles compress growth-stock valuations hardest (long duration); falling-rate cycles re-rate them up.",
         "interview": "Time value of money means a rupee today is worth more than a rupee later, purely due to opportunity cost. Every valuation method I use — DCF, bond pricing, NPV — is just an application of discounting future cash flows back to today's terms."},
        {"term": "Future Value (FV) & Present Value (PV)", "star": False,
         "definition": "FV is what a sum grows to over time; PV is what a future sum is worth today, discounted back.",
         "example": "A VC offered ₹5cr in 5 years for a ₹50L investment — the real question is the PV of that ₹5cr at their 25% hurdle rate.",
         "formula": "FV = PV(1+r)^n        PV = FV / (1+r)^n",
         "worked": "PV of ₹5cr in 5yrs @25% = 5,00,00,000/(1.25)^5 = ₹1,63,84,000 — clears the ₹50L hurdle comfortably.",
         "hi": "High required return → PV shrinks fast for distant cash flows.",
         "lo": "Low required return → PV stays closer to face value.",
         "strategy": "Use PV to compare any two cash flows occurring at different times on an apples-to-apples basis.",
         "interview": "FV tells me what a cash flow becomes; PV tells me what a future cash flow is worth today. I spend most of my time discounting — projected FCFs, terminal values, bond coupons — back to PV to compare against a price I'd pay now."},
        {"term": "Annuities & Perpetuities", "star": False,
         "definition": "An annuity is a fixed cash flow series over a set period; a perpetuity is the same, continuing forever.",
         "example": "A car EMI is an annuity. A stable, growing dividend forever (Coca-Cola) is modeled as a growing perpetuity — exactly how DCF terminal value works.",
         "formula": "Annuity PV = C×[1−(1+r)^−n]/r\nPerpetuity PV = C/r\nGrowing Perpetuity PV = C/(r−g)",
         "worked": "Year-5 FCF=₹120cr, g=4%, WACC=11% → TV = 120×1.04/(0.11−0.04) = ₹1,782.9cr",
         "hi": "Higher g relative to r → PV explodes (be skeptical of g close to r).",
         "lo": "Lower g relative to r → PV is conservative and more defensible.",
         "strategy": "Cap g at long-run GDP growth (~3-4%) to keep terminal value assumptions credible.",
         "interview": "The growing perpetuity formula is exactly what I use for terminal value at the end of a DCF's explicit forecast — a mature company's cash flows are modeled as growing indefinitely at a conservative long-run rate."},
    ],
    "2 · Statements & Ratios (FAFSA/FRA)": [
        {"term": "The Three Financial Statements", "star": True,
         "definition": "Income Statement (profitability), Balance Sheet (position at a point in time), Cash Flow Statement (actual cash movement).",
         "example": "Amazon showed net income growth for years while burning cash on capex — only the Cash Flow Statement revealed the real capital intensity.",
         "formula": "Assets = Liabilities + Equity",
         "worked": "A $10 depreciation expense: reduces net income (IS), is added back as non-cash (CFS), reduces PP&E (BS).",
         "hi": "—", "lo": "—",
         "strategy": "Always reconcile net income to operating cash flow before trusting reported earnings.",
         "interview": "The three statements are linked, not standalone. Net income flows into retained earnings on the balance sheet and is the CFS's starting point — that interconnection is what I'd walk through for the classic 'walk me through the statements' question."},
        {"term": "Liquidity Ratios (Current & Quick)", "star": False,
         "definition": "Measure a company's ability to pay short-term obligations using short-term assets.",
         "example": "Walmart runs a thin current ratio (~0.8-0.9) due to fast inventory turnover — low isn't automatically dangerous, context matters.",
         "formula": "Current Ratio = Current Assets / Current Liabilities\nQuick Ratio = (Current Assets − Inventory) / Current Liabilities",
         "worked": "CA=₹450cr, Inv=₹150cr, CL=₹300cr → Current=1.5x, Quick=1.0x",
         "hi": ">2x → strong safety but possibly idle cash.",
         "lo": "<1x → liquidity stress risk, unless high-turnover retail/FMCG model.",
         "strategy": "Always benchmark against industry norms, never in isolation.",
         "interview": "Quick ratio is the more conservative liquidity test since it strips out inventory. I'd never judge these without benchmarking to the industry."},
        {"term": "Profitability Ratios (Margins & Returns)", "star": False,
         "definition": "Gross/Operating/Net margins measure how much of revenue converts to profit at each stage; ROE/ROA measure capital efficiency.",
         "example": "Nvidia's gross margin expanded past 70%+ during the AI GPU boom — a signal of pricing power flagged before the stock re-rated.",
         "formula": "Gross Margin = Gross Profit/Revenue\nROE = Net Income/Equity\nROA = Net Income/Total Assets",
         "worked": "Net Income=₹200cr, Equity=₹1,000cr → ROE = 20%",
         "hi": "High ROE → efficient capital use, but check if leverage-driven.",
         "lo": "Low ROE → weak returns on shareholder capital.",
         "strategy": "Always decompose ROE via DuPont before concluding — leverage-driven ROE is a different risk story than margin-driven ROE.",
         "interview": "I look at margins top-down — gross for pricing power, operating for cost control, net for the full picture — and I'd always decompose ROE via DuPont analysis before drawing conclusions."},
        {"term": "Debt-to-Equity (D/E)", "star": True,
         "definition": "Measures how much debt a company uses relative to equity to finance its assets — a core solvency signal.",
         "example": "Adani Group drew scrutiny in 2023 partly over elevated D/E ratios across group entities.",
         "formula": "D/E = Total Debt / Total Shareholders' Equity",
         "worked": "Debt=₹600cr, Equity=₹400cr → D/E = 1.5x",
         "hi": ">2x → higher financial risk, but potentially higher ROE via leverage.",
         "lo": "<0.5x → conservative balance sheet, possibly under-levered.",
         "strategy": "Rising rates: highly levered names underperform as refinancing costs jump. Slowdowns: low D/E 'fortress' balance sheets are favored.",
         "interview": "D/E tells me the debt-equity funding mix and the financial risk layered on top of business risk. I'd always compare it to industry norms and pair it with interest coverage before forming a view."},
        {"term": "Interest Coverage Ratio (ICR)", "star": True,
         "definition": "Measures how many times operating earnings cover interest expense — the direct near-term solvency test.",
         "example": "\"Zombie companies\" post-2022 rate hikes had ICR near or below 1x.",
         "formula": "ICR = EBIT / Interest Expense",
         "worked": "EBIT=₹180cr, Interest=₹40cr → ICR = 4.5x",
         "hi": ">5x → comfortable debt servicing capacity.",
         "lo": "<1.5x → distress signal, a small EBIT dip could trigger default.",
         "strategy": "Pair ICR with the debt maturity schedule — a low ICR with near-term maturities is far riskier than the same ratio with distant maturities.",
         "interview": "ICR directly answers 'can this company afford its debt from operations alone.' Below 1.5x is a flashing warning, especially heading into a rate-hiking cycle."},
        {"term": "Efficiency Ratios (Turnover & DSO)", "star": False,
         "definition": "Measure how effectively assets, inventory, and receivables convert into sales and cash.",
         "example": "Zara's parent Inditex runs ~4-5x inventory turnover — a huge fast-fashion supply chain advantage.",
         "formula": "Inventory Turnover = COGS/Avg Inventory\nDSO = 365/Receivables Turnover",
         "worked": "Revenue=₹900cr, Avg AR=₹90cr → Turnover=10x → DSO = 36.5 days",
         "hi": "Rising DSO → early red flag for weakening demand or looser credit terms.",
         "lo": "Falling/stable DSO → healthy collections discipline.",
         "strategy": "Watch DSO trend before it shows up in the cash flow statement.",
         "interview": "I'd flag rising DSO as an early earnings-quality red flag even before it appears in the cash flow statement."},
    ],
    "3 · Corporate Finance": [
        {"term": "Net Present Value (NPV)", "star": True,
         "definition": "Sum of all future cash flows discounted to today, minus the initial investment — the dollar value a project adds.",
         "example": "Tesla only greenlights a new Gigafactory if its NPV, discounted at Tesla's cost of capital, is positive.",
         "formula": "NPV = Σ [CFt/(1+r)^t] − Initial Investment",
         "worked": "Investment=-₹1,000cr, CF=₹400cr/yr for 3yrs @10% → PV=994.7cr → NPV=-₹5.3cr → Reject",
         "hi": "NPV > 0 → accept, value-creating.",
         "lo": "NPV < 0 → reject, value-destroying.",
         "strategy": "Rising rates: fewer projects clear the NPV bar, capex budgets tighten. Falling rates: more projects clear, driving capex booms.",
         "interview": "NPV discounts all future cash flows at the firm's cost of capital and nets out the initial investment. Positive NPV means the project earns above what capital would earn elsewhere at that risk level — that's why NPV is the superior capital budgeting rule versus IRR or payback."},
        {"term": "Internal Rate of Return (IRR)", "star": True,
         "definition": "The discount rate at which a project's NPV equals zero — the project's own break-even return.",
         "example": "PE funds like Blackstone quote target IRRs (~20-25%) to compare deals with very different cash flow patterns.",
         "formula": "0 = Σ [CFt/(1+IRR)^t] − Initial Investment",
         "worked": "Same cash flows as NPV example → IRR ≈ 9.7% (below 10% hurdle → reject, matches NPV conclusion)",
         "hi": "IRR > hurdle rate → accept.",
         "lo": "IRR < hurdle rate → reject.",
         "strategy": "Non-conventional cash flows (sign changes more than once) can produce multiple IRRs — always sanity-check against NPV, especially for mutually exclusive projects of different scale.",
         "interview": "IRR can give multiple answers with non-conventional cash flows, and it implicitly assumes reinvestment at the IRR itself, which overstates returns for very high-IRR projects. When NPV and IRR disagree, I'd always defer to NPV."},
        {"term": "Payback Period", "star": False,
         "definition": "Time for a project's cumulative cash flows to recover the initial investment — a liquidity/risk screen, not a value measure.",
         "example": "A capital-constrained startup might pick a 2-year-payback project over a 5-year-payback project with a similar NPV, just to preserve cash runway.",
         "formula": "Payback = Years until Cumulative CF ≥ Initial Investment",
         "worked": "Investment=₹300cr, CF=₹100cr/yr → Payback = 3 years",
         "hi": "—", "lo": "—",
         "strategy": "Use as a secondary sanity check alongside NPV/IRR, never as the sole rule — it ignores TVM and post-payback cash flows.",
         "interview": "Payback tells me how fast I get capital back — useful as a liquidity/risk screen for capital-constrained businesses, but I'd never use it as a sole decision rule."},
        {"term": "Beta (β)", "star": True,
         "definition": "A stock's volatility relative to the overall market — sensitivity of stock returns to market moves.",
         "example": "Nvidia's beta often runs 1.6-2.0; a utility like NTPC runs closer to 0.5-0.7.",
         "formula": "β = Cov(Rstock, Rmarket) / Var(Rmarket)",
         "worked": "Cov=0.0048, Var=0.0032 → β = 1.5 (1% market move → ~1.5% stock move)",
         "hi": "β>1 → amplifies gains in bull markets, amplifies losses in bear markets; higher required return.",
         "lo": "β<1 → defensive, dampens both up and down moves; lower required return.",
         "strategy": "Bull markets favor high-beta rotation (tech, small caps). Bear/high-vol markets favor low-beta defensives (utilities, staples, healthcare).",
         "interview": "Beta captures systematic risk — the only risk factor CAPM compensates, since idiosyncratic risk can be diversified away. Higher beta means higher cost of equity, higher WACC, and lower DCF valuation, all else equal."},
        {"term": "CAPM & Cost of Equity", "star": False,
         "definition": "Calculates the return investors require to hold a stock, given its systematic risk (beta).",
         "example": "Analysts valuing Reliance use the 10Y G-Sec yield as risk-free rate plus an Indian equity risk premium.",
         "formula": "Re = Rf + β×(Rm − Rf)",
         "worked": "Rf=7%, Rm=12%, β=1.3 → Re = 7+1.3×(12−7) = 13.5%",
         "hi": "—", "lo": "—",
         "strategy": "Sanity-check CAPM output against comps' observed cost of equity — it's a single-factor model with strong assumptions.",
         "interview": "CAPM says required return equals the risk-free rate plus a beta-adjusted equity risk premium — the standard way to derive cost of equity for a DCF or WACC."},
        {"term": "WACC", "star": True,
         "definition": "The blended rate a company pays across debt and equity — the standard DCF discount rate.",
         "example": "Amazon discounts new fulfillment-center cash flows at its blended WACC (~8-9%), not just cost of debt or equity alone.",
         "formula": "WACC = (E/V)×Re + (D/V)×Rd×(1−Tax)",
         "worked": "E=₹700cr, D=₹300cr, Re=13.5%, Rd=9%, Tax=25% → WACC = 0.7×13.5% + 0.3×9%×0.75 = 11.5%",
         "hi": "High WACC → steeper discounting, lower valuation, signals expensive/riskier capital.",
         "lo": "Low WACC → gentler discounting, higher valuation, signals cheap/stable financing.",
         "strategy": "Use market values (not book values) for weights; reconsider a static WACC if capital structure will change materially.",
         "interview": "WACC is the blended, tax-adjusted cost of a company's capital, weighted by market values — the minimum return the company must earn to satisfy both debt and equity holders."},
        {"term": "Capital Structure & Modigliani-Miller (MM)", "star": False,
         "definition": "How a firm finances assets through debt vs equity, and MM theory explains whether that mix affects firm value.",
         "example": "Apple issues bonds to fund buybacks despite huge cash reserves — exploiting the interest tax shield (MM with taxes).",
         "formula": "Vlevered = Vunlevered + (Tax Rate × Debt)",
         "worked": "—",
         "hi": "—", "lo": "—",
         "strategy": "Trade-off theory: firms target an optimal capital structure balancing the tax shield of debt against rising distress costs.",
         "interview": "MM's original proposition says capital structure is irrelevant with no taxes/bankruptcy costs. With taxes, debt adds value via the interest tax shield — but that benefit is capped by rising distress costs as leverage increases."},
    ],
    "4 · Financial Markets": [
        {"term": "Bond Valuation", "star": True,
         "definition": "A bond's price equals the PV of all future coupons plus the PV of face value at maturity, discounted at the market yield.",
         "example": "SVB's 2023 collapse was driven by mark-to-market losses on long-dated bonds as rates rose sharply.",
         "formula": "Price = Σ [C/(1+y)^t] + F/(1+y)^n",
         "worked": "3yr, 8% coupon, ₹1,000 face, yield 10% → Price = 72.7+66.1+811.4 = ₹950.2 (trades at discount)",
         "hi": "Yield rises → bond price falls (longer duration falls more).",
         "lo": "Yield falls → bond price rises.",
         "strategy": "Expecting rate cuts: extend duration. Expecting hikes: shorten duration or hold floating-rate instruments.",
         "interview": "A bond's price is the PV of its coupon annuity plus the PV of face value. The inverse price-yield relationship is why rising rates hurt bondholders even without selling — the mechanism behind SVB's collapse."},
        {"term": "Yield Curve", "star": False,
         "definition": "A plot of bond yields across maturities — its shape reflects market expectations on growth and inflation.",
         "example": "The US 2s10s curve inverted in 2022-23 — every US recession since the 1970s was preceded by such an inversion.",
         "formula": "—", "worked": "—",
         "hi": "Normal/upward-sloping → healthy growth expectations.",
         "lo": "Inverted (short>long) → market expects cuts, usually pricing in a slowdown.",
         "strategy": "Watch the re-steepening after an inversion — it has historically preceded actual recession onset by several months.",
         "interview": "An inversion signals the market expects the central bank to cut rates in response to a slowdown — one of the most closely watched recession indicators."},
        {"term": "Duration & Convexity", "star": False,
         "definition": "Duration measures a bond's price sensitivity to rate changes (in years); convexity measures how that sensitivity itself changes.",
         "example": "Long-duration bond funds fell far more than short-duration funds during 2022's hiking cycle.",
         "formula": "%ΔPrice ≈ −ModDuration×Δy + 0.5×Convexity×(Δy)²",
         "worked": "ModDuration=7yrs, Δy=+1% → Approx price change = −7%",
         "hi": "—", "lo": "—",
         "strategy": "Positive convexity is desirable — gains more on rallies than it loses on selloffs of equal size.",
         "interview": "Duration is a first-order interest rate risk measure; convexity is the second-order correction since the price-yield relationship is curved, not linear."},
    ],
    "5 · Valuation & PE (BVPE)": [
        {"term": "DCF Valuation", "star": True,
         "definition": "Values a company as the present value of all its projected future free cash flows.",
         "example": "Sell-side analysts build Reliance DCFs across retail, telecom, and energy segments, discounting at a blended WACC.",
         "formula": "EV = Σ [FCFt/(1+WACC)^t] + TV/(1+WACC)^n\nFCF = EBIT(1−Tax) + D&A − CapEx − ΔNWC",
         "worked": "FCF Yr1-3=100/115/130cr, WACC=11%, TV(g=4%)=1,931.4cr → EV = 278.4+1,412.0 = ₹1,690.4cr",
         "hi": "Higher growth/lower WACC → higher valuation (very sensitive — TV is often 60-80% of value).",
         "lo": "Lower growth/higher WACC → lower valuation.",
         "strategy": "Always present a sensitivity table across WACC and terminal growth, not a single-point estimate.",
         "interview": "I'd forecast unlevered FCF over an explicit horizon, discount at WACC, then add a terminal value via Gordon Growth or exit multiple as a cross-check. The biggest weakness to flag proactively is sensitivity to the discount rate and long-run growth assumptions."},
        {"term": "Comparable Company Analysis (Comps)", "star": True,
         "definition": "Values a company by applying multiples observed from similar publicly traded peers.",
         "example": "Zomato was benchmarked against listed food-delivery platforms like DoorDash on EV/Revenue pre-IPO.",
         "formula": "Target EV = Peer Median Multiple × Target's Metric",
         "worked": "Peer median EV/EBITDA=12.0x, Target EBITDA=₹150cr → Implied EV = ₹1,800cr",
         "hi": "—", "lo": "—",
         "strategy": "Use the median (not mean) to avoid outlier distortion; screen peers on business model, growth, margins, and geography.",
         "interview": "Comps are market-based/relative, versus DCF's intrinsic approach. The tradeoff: comps inherit whatever mispricing exists in the sector at that moment."},
        {"term": "Precedent Transactions", "star": False,
         "definition": "Applies multiples paid in past M&A deals for similar companies — captures the control premium actually paid.",
         "example": "Bankers benchmark recent Indian IT/pharma M&A multiples to price a realistic takeover for a new target.",
         "formula": "—", "worked": "—",
         "hi": "—", "lo": "—",
         "strategy": "Use for M&A pricing/LBO entry-exit assumptions; comps for public trading value; both feed the 'football field' valuation range.",
         "interview": "Precedent transactions reflect actual M&A deal pricing including a control premium — the extra amount paid for control plus expected synergies."},
        {"term": "Valuation Multiples", "star": False,
         "definition": "Ratios expressing a company's value relative to a financial metric — the shorthand language of relative valuation.",
         "example": "EV/EBITDA for capital-structure-neutral comparisons; EV/Revenue for unprofitable growth companies; P/E for stable mature businesses.",
         "formula": "EV/EBITDA = EV/EBITDA\nP/E = Price/EPS\nEV/Revenue = EV/Revenue",
         "worked": "—",
         "hi": "—", "lo": "—",
         "strategy": "Match the multiple to the company's profitability stage and capital structure comparability.",
         "interview": "EV/EBITDA is my default for comparing companies with different leverage or tax structures; EV/Revenue for pre-profitability growth companies; P/E for stable, mature, similarly-structured peers."},
    ],
    "6 · SAPM": [
        {"term": "Sharpe Ratio", "star": True,
         "definition": "Excess return per unit of total risk (volatility) — the most widely quoted risk-adjusted performance metric.",
         "example": "Renaissance's Medallion Fund reportedly posted Sharpe ratios well above 2, versus ~0.5-1.0 for typical long-only strategies.",
         "formula": "Sharpe = (Rp − Rf) / σp",
         "worked": "Rp=14%, Rf=6%, σp=16% → Sharpe = (14−6)/16 = 0.50",
         "hi": ">1 is good; >2 is excellent/rare for long-only strategies.",
         "lo": "<0.5 → weak risk-adjusted return.",
         "strategy": "High-vol regimes compress Sharpe across the board — only compare within the same volatility regime.",
         "interview": "Sharpe treats upside and downside volatility identically, which is why I'd pair it with Sortino when I specifically care about downside risk — what most investors actually worry about."},
        {"term": "Sortino Ratio", "star": True,
         "definition": "Like Sharpe, but only penalizes downside volatility.",
         "example": "Trend-following/options-selling funds with positively skewed returns market Sortino alongside Sharpe.",
         "formula": "Sortino = (Rp − Rf) / σ_downside",
         "worked": "Rp−Rf=8%, downside dev=10% → Sortino = 0.80",
         "hi": "Sortino >> Sharpe → positive skew, attractive risk profile.",
         "lo": "Sortino ≈ Sharpe → roughly symmetric volatility, no skew benefit.",
         "strategy": "—",
         "interview": "A strategy with a much higher Sortino than Sharpe tells me its volatility is skewed positively — genuinely attractive, since investors dislike losses, not upside swings."},
        {"term": "Treynor Ratio", "star": True,
         "definition": "Excess return per unit of systematic (market) risk, using beta — best for well-diversified portfolios.",
         "example": "A large diversified mutual fund, with idiosyncratic risk already eliminated, is evaluated on Treynor rather than Sharpe.",
         "formula": "Treynor = (Rp − Rf) / βp",
         "worked": "Rp−Rf=9%, β=1.2 → Treynor = 7.5",
         "hi": "—", "lo": "—",
         "strategy": "—",
         "interview": "I'd use Treynor over Sharpe for a well-diversified portfolio, since idiosyncratic risk is already eliminated and beta is the relevant remaining risk measure."},
        {"term": "Information Ratio (IR)", "star": True,
         "definition": "Excess return over a benchmark, per unit of tracking error — the key metric for active manager skill.",
         "example": "Active mutual fund managers are judged on IR vs. their stated benchmark (Nifty 50/S&P 500) — a consistent IR above ~0.5 signals genuine alpha.",
         "formula": "IR = (Rp − Rbenchmark) / Tracking Error",
         "worked": "Rp=15%, Rbench=12%, TE=5% → IR = (15−12)/5 = 0.60",
         "hi": ">0.5 → strong, consistent active skill.",
         "lo": "Near 0 or negative → not adding value beyond benchmark.",
         "strategy": "—",
         "interview": "A high, consistent IR over time suggests genuine, repeatable alpha, versus a manager who beat the benchmark once with huge tracking error — this is the metric LPs actually use to judge if active management is worth the fee."},
        {"term": "Fundamental Analysis", "star": False,
         "definition": "Evaluates a security's intrinsic value using financial statements, business quality, industry position, and macro factors.",
         "example": "Buffett's 1988 Coca-Cola buy: durable moat, consistent ROE, pricing power, price below intrinsic value.",
         "formula": "—", "worked": "—",
         "hi": "—", "lo": "—",
         "strategy": "Red flags: margin deterioration with rising revenue, aggressive revenue recognition, rising receivables/inventory vs. sales, frequent auditor changes.",
         "interview": "I'd combine top-down macro/industry screening with bottom-up company analysis, looking closely at earnings quality — red flags often show up before a stock price reaction does."},
        {"term": "Technical Analysis", "star": False,
         "definition": "Studies historical price/volume patterns to forecast future price movement.",
         "example": "Trend-following CTAs manage billions using moving-average crossovers with no reference to fundamentals.",
         "formula": "—", "worked": "—",
         "hi": "—", "lo": "—",
         "strategy": "Use fundamentals to decide what to buy, technicals to decide when to enter/exit — complementary, not competing approaches.",
         "interview": "Technical analysis assumes price already reflects all available information. I see it as complementary to fundamentals — useful for timing and risk management."},
        {"term": "Industry Analysis (Porter's Five Forces)", "star": False,
         "definition": "A framework for assessing an industry's competitive intensity and long-run profitability potential.",
         "example": "Indian telecom post-Jio (2016): intense rivalry and new-entrant threat crushed industry profitability, consolidating ~10 players to 3.",
         "formula": "New entrants, Supplier power, Buyer power, Substitutes, Competitive rivalry",
         "worked": "—", "hi": "—", "lo": "—",
         "strategy": "—",
         "interview": "Before evaluating an individual company, I want to understand the structural attractiveness of its industry using Porter's Five Forces — this shapes durable margin potential regardless of how well any one company is run."},
    ],
    "7 · Derivatives": [
        {"term": "Forwards, Futures & Swaps", "star": True,
         "definition": "Agreements to buy/sell an asset at a set future price; swaps exchange one cash flow stream for another. Futures are standardized/exchange-traded; forwards are OTC.",
         "example": "Infosys uses USD/INR forwards to hedge future dollar revenue; commodity traders use exchange-traded crude futures for the same economic purpose.",
         "formula": "F = S0 × e^(r×T)",
         "worked": "A company swaps a floating-rate loan (MIBOR+2%) into fixed 8% to eliminate rate uncertainty.",
         "hi": "—", "lo": "—",
         "strategy": "—",
         "interview": "Futures are standardized, exchange-traded, and marked to market daily, virtually eliminating counterparty risk. Forwards are private OTC contracts settled only at maturity. Swaps extend the idea to ongoing cash flow streams, like converting floating debt into fixed."},
        {"term": "Options Basics: Calls & Puts", "star": True,
         "definition": "A call gives the right to buy at a strike price; a put gives the right to sell — the buyer pays a premium for this optionality.",
         "example": "Retail traders buy Nifty calls ahead of earnings for capped, known downside (the premium).",
         "formula": "Long Call payoff = max(S−K, 0) − Premium\nLong Put payoff = max(K−S, 0) − Premium",
         "worked": "K=₹2,500, Premium=₹50, S=₹2,600 → Payoff = max(2600-2500,0)-50 = ₹50 profit",
         "hi": "—", "lo": "—",
         "strategy": "—",
         "interview": "The buyer's downside is always capped at the premium; the seller takes on the obligation and correspondingly larger, potentially unlimited risk for collecting that premium upfront."},
        {"term": "The Greeks", "star": True,
         "definition": "Measure an option's sensitivity to price (Delta), Delta's own change (Gamma), volatility (Vega), time (Theta), and rates (Rho).",
         "example": "Market makers run delta-neutral books, so P&L comes from gamma/vega/theta exposure rather than direction.",
         "formula": "Delta=N(d1)  Gamma=N'(d1)/(Sσ√T)  Vega=SN'(d1)√T  Theta≈−[SN'(d1)σ/(2√T)]−rKe^(−rT)N(d2)  Rho=KTe^(−rT)N(d2)",
         "worked": "Delta=0.60 (moves like 60 shares/100-lot); Gamma=0.05 (Delta rises toward 0.65 per ₹1 up-move); Theta=−₹8/day; Vega=₹12 per 1-pt IV rise",
         "hi": "High Gamma → Delta changes fast, needs frequent rehedging, risky near expiry on ATM strikes.",
         "lo": "High Theta decay (short-dated ATM) → rapid value erosion, favors sellers.",
         "strategy": "High IV (pre-earnings): favors selling volatility. Low IV (calm markets): better to buy optionality ahead of catalysts. Near expiry: Gamma/Theta spike, exaggerating intraday moves.",
         "interview": "Delta is directional exposure. Gamma is the rate of change of that delta — highest ATM near expiry. Vega is volatility sensitivity. Theta is time decay, accelerating into expiration. Rho is usually least important except for longer-dated options."},
        {"term": "Black-Scholes (& Binomial) Models", "star": False,
         "definition": "Black-Scholes prices European options in closed form; binomial prices via a discrete lattice, better for American/early-exercise options.",
         "example": "Every options desk still quotes off Black-Scholes despite the empirically observed 'volatility smile' violating its constant-vol assumption.",
         "formula": "C = S0N(d1) − Ke^(−rT)N(d2)\nd1 = [ln(S0/K)+(r+σ²/2)T]/(σ√T)\nd2 = d1 − σ√T",
         "worked": "—", "hi": "—", "lo": "—",
         "strategy": "—",
         "interview": "I'd use the binomial model for American-style options since it can explicitly value early exercise at each tree node, which Black-Scholes can't natively handle."},
        {"term": "Put-Call Parity", "star": True,
         "definition": "A no-arbitrage relationship linking call and put prices with the same strike/expiry to the underlying and a risk-free bond.",
         "example": "If parity is ever violated on a liquid name like Reliance, HFT arbitrage desks close the gap within seconds via conversion/reversal trades.",
         "formula": "C − P = S0 − Ke^(−rT)",
         "worked": "S0=₹2,500, K=₹2,500, r=6%, T=1yr → Ke^(−rT)=2,354.4 → Implied C−P = ₹145.6",
         "hi": "—", "lo": "—",
         "strategy": "—",
         "interview": "Long call plus short put replicates a synthetic long stock position, financed at the risk-free rate. Any deviation after adjusting for dividends/financing creates a genuine riskless arbitrage — which is why it holds tightly in liquid markets."},
        {"term": "Option Strategies: Covered Call vs. Long Straddle", "star": True,
         "definition": "Covered call = own stock + sell OTM call (income, range-bound view). Long straddle = buy ATM call + put (volatility bet, direction-agnostic).",
         "example": "Covered call on a large-cap at ₹2,500, sell ₹2,650 call for ₹40 premium. Straddle on a mid-cap ahead of earnings, combined premium ₹110.",
         "formula": "Covered Call breakeven ≈ cost − premium\nStraddle breakevens = K ± combined premium",
         "worked": "Covered call: flat months earn the premium consistently; rally months cap upside at strike; selloffs cushioned slightly but not prevented.\nStraddle: big moves profit either direction; small moves lose to theta decay; post-event IV crush can offset directional gains.",
         "hi": "—", "lo": "—",
         "strategy": "Covered calls suit mildly bullish-to-neutral, range-bound markets. Straddles suit anticipated high realized volatility exceeding what's priced into the premium — watch for IV crush after known catalysts.",
         "interview": "Covered call is mildly bullish/neutral and income-generating, capping upside for premium. Long straddle bets purely on realized volatility exceeding priced-in premium — the key risk is IV crush after events like earnings, where the stock moves but implied vol collapses faster than intrinsic value builds."},
    ],
    "8 · Risk Management (FRM)": [
        {"term": "Value at Risk (VaR)", "star": True,
         "definition": "Estimates the maximum expected loss on a portfolio over a horizon, at a given confidence level.",
         "example": "Goldman Sachs and JPMorgan report daily VaR in quarterly filings as a standard regulatory risk disclosure.",
         "formula": "VaR = Portfolio Value × z-score × σ_daily × √t\n(z=1.65 for 95%, z=2.33 for 99%)",
         "worked": "Portfolio=₹10cr, σ_daily=1.5%, 95% conf → VaR = 10,00,00,000×1.65×0.015 = ₹24,75,000",
         "hi": "High VaR → significant loss exposure, may need hedging or position cuts.",
         "lo": "Low VaR → lower near-term exposure, but says nothing about severity beyond the threshold.",
         "strategy": "High-vol/crisis regimes: VaR spikes reactively, not predictively. Regulatory context: Basel III/IV increasingly require Expected Shortfall (CVaR) alongside VaR to address the tail-risk blindspot.",
         "interview": "VaR estimates max expected loss at a confidence level — e.g., a 95% 1-day VaR of ₹25L means only a 5% chance of exceeding that loss. The limitation I'd always flag: it says nothing about how severe losses get in that remaining 5% tail, which is why Expected Shortfall has become the preferred regulatory complement."},
    ],
}

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #16233a;
}
.subtitle {
    color: #555;
    margin-bottom: 1.5rem;
}
.card {
    border: 1px solid #d8d4c8;
    border-radius: 10px;
    padding: 22px;
    margin: 12px 0 20px 0;
    background: #fdfcf9;
}
.formula {
    background: #16233a;
    color: #f5f7fa;
    padding: 14px;
    border-radius: 6px;
    white-space: pre-wrap;
    font-family: Consolas, monospace;
}
.example {
    background: #f0efe9;
    border-left: 4px solid #0e6e6b;
    padding: 12px;
    margin: 12px 0;
}
.interview {
    background: #dceaf3;
    border-left: 5px solid #8fb6cc;
    padding: 14px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)


def all_terms():
    return [(course, term) for course, terms in DATA.items() for term in terms]


def render_term(term):
    star = " ⭐" if term.get("star") else ""

    st.markdown(
        f'<div class="card"><h2>{term["term"]}{star}</h2>'
        f'<p><b>{term["definition"]}</b></p>'
        f'<div class="example"><b>Example:</b><br>{term["example"]}</div></div>',
        unsafe_allow_html=True
    )

    if term.get("formula", "—") != "—":
        st.markdown(
            f'<div class="formula"><b>Formula</b><br><br>{term["formula"]}</div>',
            unsafe_allow_html=True
        )

    if term.get("worked", "—") != "—":
        st.markdown("### Worked Example")
        st.write(term["worked"])

    if term.get("hi", "—") != "—":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**High / Higher:**")
            st.write(term["hi"])
        with c2:
            st.markdown("**Low / Lower:**")
            st.write(term["lo"])

    if term.get("strategy", "—") != "—":
        st.markdown("### Strategy / Interpretation")
        st.write(term["strategy"])

    st.markdown(
        f'<div class="interview"><b>💬 INTERVIEW SCRIPT</b><br><br>'
        f'"{term["interview"]}"</div>',
        unsafe_allow_html=True
    )


# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="title">📊 The Analyst\'s Ledger</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Interactive Finance Interview Revision Guide</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Course Revision", "Search", "Random ⭐ Quiz"]
)

# -----------------------------
# Course Revision
# -----------------------------
if page == "Course Revision":
    st.header("📚 Course Revision")

    course = st.selectbox(
        "Select Course",
        list(DATA.keys())
    )

    terms = DATA[course]
    term_names = [t["term"] for t in terms]

    selected_name = st.selectbox(
        "Select Concept",
        term_names
    )

    selected = next(t for t in terms if t["term"] == selected_name)

    render_term(selected)

# -----------------------------
# Search
# -----------------------------
elif page == "Search":
    st.header("🔍 Search Across All Courses")

    query = st.text_input(
        "Search for a concept",
        placeholder="Try: WACC, DCF, Beta, Sharpe, VaR..."
    ).strip().lower()

    if query:
        matches = []

        for course, term in all_terms():
            searchable = " ".join([
                term.get("term", ""),
                term.get("definition", ""),
                term.get("example", ""),
                term.get("strategy", "")
            ]).lower()

            if query in searchable:
                matches.append((course, term))

        if matches:
            st.success(f"Found {len(matches)} matching concept(s).")

            for course, term in matches:
                st.caption(course)
                render_term(term)
        else:
            st.warning("No matches found. Try another keyword.")

# -----------------------------
# Random Quiz
# -----------------------------
else:
    st.header("🎲 Random ⭐ Quiz")

    st.write(
        "Click the button to get a randomly selected must-know finance concept."
    )

    if st.button("🎲 Give Me a Random Concept", type="primary"):
        stars = [(c, t) for c, t in all_terms() if t.get("star")]

        if stars:
            course, term = random.choice(stars)
            st.info(f"From: {course}")
            render_term(term)
        else:
            st.warning("No starred concepts were found.")

# ============================================================
# AI CHATBOT
# ============================================================

st.sidebar.markdown("---")
st.sidebar.header("🤖 AI Finance Assistant")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask any finance question...")

if question:

    st.session_state.chat_messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        response = client.responses.create(
            model="gpt-5-mini",
            input=f"""
You are the AI Finance Assistant inside The Analyst's Ledger.

Answer the user's finance question clearly and accurately.

Structure your answer using:

1. Definition
2. Formula (if applicable)
3. Simple Example
4. Key Insight
5. Interview Answer

User's question:
{question}
"""
        )

        answer = response.output_text

        st.markdown(answer)

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": answer
        })
