(() => {
  const canvas = document.querySelector("[data-hero-orbit]");
  if (!canvas) return;
  const context = canvas.getContext("2d");
  const stars = Array.from({ length: 95 }, (_, index) => ({
    x: ((index * 157) % canvas.width) / canvas.width,
    y: ((index * 83 + 31) % canvas.height) / canvas.height,
    radius: 0.4 + (index % 4) * 0.35,
    alpha: 0.15 + (index % 7) * 0.08,
  }));
  let phase = 0;

  function draw() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    stars.forEach((star) => {
      context.fillStyle = `rgba(220,240,241,${star.alpha})`;
      context.beginPath();
      context.arc(star.x * canvas.width, star.y * canvas.height, star.radius, 0, Math.PI * 2);
      context.fill();
    });

    const centerX = canvas.width * 0.72;
    const centerY = canvas.height * 0.52;
    context.save();
    context.translate(centerX, centerY);
    context.rotate(-0.22);
    [180, 265, 355].forEach((radius, index) => {
      context.strokeStyle = index === 1 ? "rgba(255,96,56,.25)" : "rgba(121,217,232,.12)";
      context.lineWidth = index === 1 ? 2 : 1;
      context.setLineDash(index === 2 ? [9, 11] : []);
      context.beginPath();
      context.ellipse(0, 0, radius * 1.55, radius * 0.62, 0, 0, Math.PI * 2);
      context.stroke();
    });
    context.setLineDash([]);
    const angle = phase * 0.24;
    const vehicleX = Math.cos(angle) * 265 * 1.55;
    const vehicleY = Math.sin(angle) * 265 * 0.62;
    context.fillStyle = "#ff6038";
    context.shadowColor = "#ff6038";
    context.shadowBlur = 18;
    context.beginPath();
    context.arc(vehicleX, vehicleY, 5, 0, Math.PI * 2);
    context.fill();
    context.restore();
  }

  if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
    draw();
    return;
  }
  let previous = performance.now();
  function frame(now) {
    phase += Math.min(0.05, (now - previous) / 1000);
    previous = now;
    draw();
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
