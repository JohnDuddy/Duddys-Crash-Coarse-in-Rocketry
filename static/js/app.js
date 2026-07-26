(() => {
  const body = document.body;
  const railToggle = document.querySelector("[data-rail-toggle]");
  const railScrim = document.querySelector("[data-rail-scrim]");
  const searchInput = document.querySelector("#course-query");

  function closeRail() {
    body.classList.remove("rail-open");
  }

  railToggle?.addEventListener("click", () => body.classList.toggle("rail-open"));
  railScrim?.addEventListener("click", closeRail);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeRail();
    if (
      event.key === "/"
      && !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)
    ) {
      event.preventDefault();
      searchInput?.focus();
    }
  });

  document.querySelectorAll(".mission-rail a").forEach((link) => {
    link.addEventListener("click", closeRail);
  });

  const reveals = [...document.querySelectorAll(".reveal")];
  if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    reveals.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -7% 0px", threshold: 0.08 },
  );
  reveals.forEach((item, index) => {
    item.style.transitionDelay = `${Math.min(index % 4, 3) * 55}ms`;
    observer.observe(item);
  });
})();
