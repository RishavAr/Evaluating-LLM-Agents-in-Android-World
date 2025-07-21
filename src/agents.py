def build_prompt(goal, activity, ui_elements, history=None, fewshot=True, cot=True):
    ui = ", ".join(ui_elements)
    mem = ""
    if history:
        mem = "History:\n" + "\n".join([f"- Step {i+1}: {a}" for i, a in enumerate(history)]) + "\n\n"
    reasoning = "Reasoning: Decide on the most direct next step." if cot else ""
    template = f"""{FEWSHOT if fewshot else ""}
Goal: {goal}
{mem}Observation:
- App: {activity}
- UI Elements: {ui}
{reasoning}
Action:"""
    return template.strip()


ACTION_RE = r'(CLICK\(\".*?\"\)|SCROLL_DOWN\(\)|SCROLL_UP\(\)|BACK\(\)|TYPE\(\".*?\"\))'

def extract_action(text):
    m = re.search(ACTION_RE, text)
    return m.group(1) if m else text.strip()

def gpt_action(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a mobile UI control agent. Respond with ONE valid action only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,`
        max_tokens=64,
    )
    raw = response.choices[0].message.content
    return extract_action(raw), raw.strip()

