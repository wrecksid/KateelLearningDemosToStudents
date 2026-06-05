# Public Policy Resource Allocation Lab

A browser-based policy simulation demonstrating AI-driven resource allocation decisions in public governance.

## Live Demo

Open `index.html` in your browser to start the policy simulation.

## Learning Objectives

1. **Trade-off Analysis**: Understand how budget allocations affect different policy outcomes
2. **Equity Metrics**: Learn to evaluate policy impact across demographic groups
3. **Ethical AI**: Practice making governance decisions with incomplete information
4. **Scenario Planning**: Test "what-if" scenarios for public policy

## Lab Exercises

### Exercise 1: Baseline Analysis
- Run the default simulation
- Record the impact scores for each sector
- Note the equity score

### Exercise 2: Education Investment
- Increase education budget to 60%
- Decrease infrastructure to 5%
- Run simulation and analyze outcomes
- **Question**: What trade-offs do you observe?

### Exercise 3: Health Emergency
- Simulate a health crisis requiring 50% healthcare budget
- Adjust other sectors accordingly
- **Question**: How does this affect equity?

### Exercise 4: Balanced Budget
- Find an allocation that maximizes overall welfare
- Document your reasoning
- **Question**: What constraints did you consider?

## Methodology

The simulation uses simplified welfare functions:

- **Education Impact**: Diminishing returns model (first dollars have highest impact)
- **Health Outcomes**: Population-weighted benefit function
- **Infrastructure**: Linear benefit with threshold effects
- **Social Welfare**: Direct transfer benefit
- **Equity Score**: Balance × 0.7 + Social Spending × 0.3

## File Structure

```
PublicPolicyGovernance/
├── index.html    # Main application
├── style.css     # Policy-themed styling
├── app.js        # Simulation logic
└── README.md     # This file
```

## Educational Use

Designed for:
- Public Policy courses
- Urban Planning programs
- Public Administration
- AI for Social Good workshops
- Ethics in Governance modules

## Further Reading

- OECD Principles on AI for Democracy
- World Bank Development Impact Evaluation
- ACM Conference on Fairness, Accountability, and Transparency (FAccT)