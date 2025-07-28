# Evaluating-LLM-Agents-in-Android-World



📁 Repo Structure

```bash
├── src/
│   ├── agent.py          # Code for prompt generation, agent action loop
│   ├── evaluator.py      # Evaluation logic and retry handling
│   ├── prompt.py       # prompt
│
├── prompts/
│   ├── fewshot.txt       # Few-shot examples used in each experiment
│
├── results/
│   ├── full_eval.csv     # Full step-by-step logs
│   ├── plots/            # Accuracy bar charts, heatmaps
│
├── report.md             # This report
```

📋 Agent Evaluation Report

🧠 Goal

This project investigates the effectiveness of LLM-only agents in mobile UI control tasks using the android_world benchmark. We explored how prompting strategies, retry logic, and semantic enrichments impact agent performance across structured environments.

# Notes

🧪 Synthetic Data Generation

The datasets for episodes in andriod_world was deleted thats why synthetic data is generated
To simulate real-world mobile UI interactions, we generated 10 advanced synthetic episodes using Google Gemini . These episodes were designed to be:

❗️ Extremely challenging: including ambiguity, multi-hop reasoning, and hallucination traps.

🧠 Rich in reasoning: with natural typos, contradictions, and steps requiring world knowledge.\

📲 Diverse in task type: covering settings configuration, app navigation, text input, and search.

# 🔍 Why Gemini?

We used Gemini  for episode generation instead of OpenAI models for the following reasons:

Gemini is better at generating long, structured outputs with step-by-step task trees.

It allowed more controllable hallucination injection and goal complexity variation.

We wanted to avoid model bias by not training and evaluating on the same model family (OpenAI GPT).

This helps benchmark generalization of agents under LLM-generated scenarios that are different from the inference model.



# Agent Model: OpenAI GPT-4o(API)

We used OpenAI GPT-4o to implement and evaluate the LLM-based control agent.

Why GPT-4o?

🧠 We already had access to GPT-4o via our previous SecureGPT/NIST research projects.

💸 Claude 3 and Gemini cost constraints made it infeasible to run large-scale inference with them.

🔁 GPT-4o allowed fast retries, reflection, and CoT loops at scale with manageable latency.


# 🧪 Experiments Summary for advanced episode

Experiment	Strategy Used	Step Accuracy	Hallucinations	Retries	Episode Success

Exp 1	Basic few-shot prompting + retries	61.0%	11	54	0%
Exp 2	+ Chain-of-Thought prompting	62.7%	6	51	0%
Exp 3	+ Goal cleanup, + Step type, + 2-level retries	66.3%	7	90	0%

🔬 Detailed Findings & Analysis

# ✅ Experiment 1: Baseline (Few-shot Prompting + Retry)

Prompting Style: 2 few-shot examples followed by flat observations and a direct action query.
Retry Logic: If incorrect, reflect and retry once.

Outcome:
Decent start with 61% step accuracy.
High hallucinations (11) indicate poor grounding in UI elements.
Retry logic helped, but hallucinations still penalized success.

Limitation:
Lack of contextual reasoning (no memory of goal type or action history).
Prompt was too “static”, treating every step in isolation.


# 🧠 Experiment 2: Adding Chain-of-Thought (CoT) Reasoning

What Changed:

Introduced explicit "Reasoning:" line in the prompt.
Added structured reflection before action selection.

Outcome:

Improved grounding: hallucinations dropped to 6.
Slight improvement in accuracy to 62.7%.
Agent made more semantically valid decisions but was still brittle on ambiguous UI layouts.

Insight:

CoT helps filter out implausible actions.
However, no awareness of step type limits targeted reasoning (e.g., typing vs clicking).

# 🔎 Experiment 3: Goal Cleanup + Step-Type Awareness + Multi-Retry

Enhancements:

Used GPT to clean/clarify the goal into a precise sentence.
Tagged each step as one of: Selection, Typing, Navigation, etc.
Added 2-level retry with deeper reflection.

Outcome:

Best performance so far: 66.3% step accuracy
Hallucinations stayed low (7) despite more complex logic.
Retry count increased to 90, indicating agent is thinking harder before locking in an answer.

Analysis:

Cleaning the goal helps focus the agent on correct intent.
Step type lets the agent tailor reasoning (e.g., what to TYPE vs what to CLICK).
Multi-retry allowed the agent to self-correct more efficiently, reducing blind guesses.

# 📈 Key Takeaways

Prompt quality directly correlates with hallucination control and accuracy. Richer reasoning improves trustworthiness.
Structured metadata (like step type) acts as inductive bias, letting LLMs anchor their reasoning better.
More retries ≠ worse agents — it's about guided retrying with reflective prompts that reduces hallucination and overconfidence.

On experimenting with normal and advanced episode , the normal episodes perform 100% accuracy without any technique but on advanced_episode three experimentation done to improve it
Despite improvements, no advanced_episode reached full success (100% step accuracy), highlighting the limits of current LLMs in long-horizon, multi-step control.

# 🛠 Future Directions

Introduce memory-aware agents (e.g., state tracking + learned constraints).
Add ReAct-style tools (like UI validator) to reduce invalid actions.
Fine-tune a small agent on successful samples from these runs.
Combine OpenAI + heuristic fallback hybrid to enforce safe defaults when hallucinations are likely.
