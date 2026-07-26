(() => {
  const workspace = document.querySelector("[data-review-workspace]");
  if (!workspace) return;
  const storageKey = "duddyRocketryExpertReview:v1";
  const criteria = [...workspace.querySelectorAll("[data-review-criterion]")];
  const totalOutput = workspace.querySelector("[data-review-score]");
  const dateInput = workspace.querySelector("[data-review-date]");
  const fields = {
    reviewer: workspace.querySelector("[data-reviewer-name]"),
    role: workspace.querySelector("[data-reviewer-role]"),
    date: dateInput,
    build: workspace.querySelector("[data-review-build]"),
    strengths: workspace.querySelector("[data-review-strengths]"),
    defects: workspace.querySelector("[data-review-defects]"),
    recommendation: workspace.querySelector("[data-review-recommendation]"),
    statement: workspace.querySelector("[data-review-statement]"),
  };

  if (!dateInput.value) dateInput.value = new Date().toISOString().slice(0, 10);

  function calculate() {
    let weighted = 0;
    let weightTotal = 0;
    criteria.forEach((item) => {
      const input = item.querySelector("[data-score-input]");
      const value = Number.parseFloat(input.value);
      const weight = Number.parseFloat(item.dataset.weight);
      item.querySelector("[data-score-output]").value = value.toFixed(1).replace(".0", "");
      weighted += value * weight;
      weightTotal += weight;
    });
    const score = weightTotal ? weighted / weightTotal : 0;
    totalOutput.textContent = score.toFixed(1);
    return score;
  }

  function reviewData() {
    return {
      schema: "duddy-rocketry-review-v1",
      project: "Duddy's Crash Coarse in Rocketry",
      disclaimer: "A saved reviewer name does not imply affiliation or endorsement.",
      exported_at: new Date().toISOString(),
      reviewer: Object.fromEntries(Object.entries(fields).map(([key, field]) => [key, field.value])),
      weighted_score: calculate(),
      criteria: criteria.map((item, index) => ({
        number: index + 1,
        title: item.querySelector("h2").textContent.trim(),
        weight: Number.parseFloat(item.dataset.weight),
        score: Number.parseFloat(item.querySelector("[data-score-input]").value),
        evidence_or_action: item.querySelector("[data-score-note]").value,
      })),
    };
  }

  function save() {
    localStorage.setItem(storageKey, JSON.stringify(reviewData()));
  }

  function restore() {
    const raw = localStorage.getItem(storageKey);
    if (!raw) return;
    try {
      const data = JSON.parse(raw);
      Object.entries(fields).forEach(([key, field]) => {
        if (data.reviewer?.[key] !== undefined) field.value = data.reviewer[key];
      });
      data.criteria?.forEach((saved, index) => {
        const item = criteria[index];
        if (!item) return;
        item.querySelector("[data-score-input]").value = String(saved.score ?? 0);
        item.querySelector("[data-score-note]").value = saved.evidence_or_action || "";
      });
    } catch {
      localStorage.removeItem(storageKey);
    }
  }

  workspace.addEventListener("input", () => {
    calculate();
    save();
  });
  workspace.addEventListener("change", save);
  workspace.querySelector("[data-review-export]").addEventListener("click", () => {
    const data = JSON.stringify(reviewData(), null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `duddy-rocketry-review-${dateInput.value || "undated"}.json`;
    link.click();
    URL.revokeObjectURL(url);
  });
  restore();
  calculate();
})();
