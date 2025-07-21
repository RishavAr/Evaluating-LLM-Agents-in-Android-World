def evaluate_agent(episodes, model="gpt-4o", retry=True):
    logs = []
    for ep in tqdm(episodes, desc="Episodes"):
        cleaned_goal = clean_goal(ep["goal"])
        memory_buffer = []
        correct = 0
        retry_count = 0
        for step in ep["steps"]:
            obs = step["observation"]
            gt = step["action"]
            step_type = detect_step_type(gt)

            prompt = build_prompt(cleaned_goal, obs["current_activity"], obs["ui_elements"], memory_buffer, step_type)
            pred, raw = gpt_action(prompt, model)

            if pred != gt and retry:
                retry_prompt = f"{prompt}\n\nFirst attempt: {pred}\nThat was incorrect. Try again.\nAction:"
                pred_retry, raw_retry = gpt_action(retry_prompt)
                retry_count += 1
                if pred_retry != gt:
                    retry_prompt_2 = f"{retry_prompt}\nSecond attempt: {pred_retry}\nStill wrong. One more try.\nAction:"
                    pred_final, raw_final = gpt_action(retry_prompt_2)
                    retry_count += 1
                    pred, raw = pred_final, raw_final
                else:
                    pred, raw = pred_retry, raw_retry

            hallucinated = pred.startswith("CLICK") and pred[7:-2] not in obs["ui_elements"]
            logs.append({
                "episode": ep["id"],
                "goal": cleaned_goal,
                "activity": obs["current_activity"],
                "ui_elements": obs["ui_elements"],
                "ground_truth": gt,
                "predicted": pred,
                "raw": raw,
                "correct": pred == gt,
                "hallucinated": hallucinated,
                "retried": retry_count,
                "levenshtein": fuzz.ratio(pred, gt),
                "step_type": step_type
            })

            if pred == gt:
                correct += 1
            memory_buffer.append((obs["current_activity"], pred))

        ep["step_accuracy"] = correct / len(ep["steps"])
        ep["success"] = ep["step_accuracy"] == 1.0
        ep["hallucinations"] = sum(1 for log in logs if log["episode"] == ep["id"] and log["hallucinated"])
        ep["retries_used"] = retry_count
    return episodes, pd.DataFrame(logs)


def plot_accuracy(episodes):
    ep_names = [ep["id"] for ep in episodes]
    acc = [ep["step_accuracy"] * 100 for ep in episodes]
    plt.figure(figsize=(10, 4))
    bars = plt.bar(ep_names, acc)
    for bar, val in zip(bars, acc):
        plt.text(bar.get_x() + bar.get_width() / 2, val + 1, f"{val:.1f}%", ha='center')
    plt.xticks(rotation=45)
    plt.ylabel("Step Accuracy (%)")
    plt.title("Per-Episode Step Accuracy")
    plt.tight_layout()
    plt.show()

def plot_hallucination_heatmap(df):
    halluc = df.groupby("episode")["hallucinated"].sum()
    plt.figure(figsize=(10, 1.5))
    sns.heatmap([halluc.values], annot=True, cbar=False, xticklabels=halluc.index, yticklabels=["Hallucinations"])
    plt.title("Hallucinations per Episode")
    plt.tight_layout()
    plt.show()


