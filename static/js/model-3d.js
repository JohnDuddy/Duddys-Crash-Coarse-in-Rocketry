(() => {
  const root = document.querySelector("[data-engineering-model]");
  if (!root) return;

  const canvas = root.querySelector("[data-model-canvas]");
  const context = canvas.getContext("2d");
  const type = root.dataset.modelType;
  const status = root.querySelector("[data-model-status]");
  const yawInput = root.querySelector("[data-model-yaw]");
  const pitchInput = root.querySelector("[data-model-pitch]");
  const zoomInput = root.querySelector("[data-model-zoom]");
  const yawOutput = root.querySelector("[data-model-yaw-output]");
  const pitchOutput = root.querySelector("[data-model-pitch-output]");
  const zoomOutput = root.querySelector("[data-model-zoom-output]");
  const spinButton = root.querySelector("[data-model-spin]");
  const explodeButton = root.querySelector("[data-model-explode]");
  const resetButton = root.querySelector("[data-model-reset]");

  const C = {
    white: "#e9f3f2",
    muted: "#627984",
    grid: "rgba(128, 160, 172, .13)",
    orange: "#ff6038",
    amber: "#ffb454",
    signal: "#c8ed75",
    cyan: "#79d9e8",
    red: "#ff6b60",
    blue: "#4b83ff",
    fuel: "#f5c45d",
    oxidizer: "#72d5ff",
    structure: "#adc0c7",
  };

  const scene = { segments: [], points: [], labels: [] };
  const state = {
    yaw: Number(yawInput.value) * Math.PI / 180,
    pitch: Number(pitchInput.value) * Math.PI / 180,
    zoom: Number(zoomInput.value),
    spin: !window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    exploded: false,
    explode: 0,
    dragging: false,
    lastX: 0,
    lastY: 0,
    time: 0,
  };

  const point = (x, y, z) => ({ x, y, z });
  const add = (a, b) => point(a.x + b.x, a.y + b.y, a.z + b.z);
  const scale = (a, factor) => point(a.x * factor, a.y * factor, a.z * factor);

  function line(a, b, color = C.structure, width = 1, offset = point(0, 0, 0), dash = []) {
    scene.segments.push({ a, b, color, width, offset, dash });
  }

  function polyline(points, color = C.structure, width = 1, offset = point(0, 0, 0), dash = []) {
    for (let index = 1; index < points.length; index += 1) {
      line(points[index - 1], points[index], color, width, offset, dash);
    }
  }

  function dot(position, color = C.white, radius = 3, offset = point(0, 0, 0)) {
    scene.points.push({ position, color, radius, offset });
  }

  function label(text, position, color = C.white, offset = point(0, 0, 0)) {
    scene.labels.push({ text, position, color, offset });
  }

  function ring(center, radius, plane = "xz", color = C.structure, width = 1, offset = point(0, 0, 0), start = 0, end = Math.PI * 2) {
    const vertices = [];
    const steps = Math.max(12, Math.round(40 * Math.abs(end - start) / (Math.PI * 2)));
    for (let index = 0; index <= steps; index += 1) {
      const angle = start + (end - start) * index / steps;
      if (plane === "xz") vertices.push(point(center.x + Math.cos(angle) * radius, center.y, center.z + Math.sin(angle) * radius));
      if (plane === "xy") vertices.push(point(center.x + Math.cos(angle) * radius, center.y + Math.sin(angle) * radius, center.z));
      if (plane === "yz") vertices.push(point(center.x, center.y + Math.cos(angle) * radius, center.z + Math.sin(angle) * radius));
    }
    polyline(vertices, color, width, offset);
  }

  function orientedRing(center, radius, tiltX, tiltZ, color = C.structure, width = 1, offset = point(0, 0, 0), start = 0, end = Math.PI * 2) {
    const vertices = [];
    const steps = 52;
    for (let index = 0; index <= steps; index += 1) {
      const angle = start + (end - start) * index / steps;
      let p = point(Math.cos(angle) * radius, 0, Math.sin(angle) * radius);
      const cx = Math.cos(tiltX);
      const sx = Math.sin(tiltX);
      p = point(p.x, p.y * cx - p.z * sx, p.y * sx + p.z * cx);
      const cz = Math.cos(tiltZ);
      const sz = Math.sin(tiltZ);
      p = point(p.x * cz - p.y * sz, p.x * sz + p.y * cz, p.z);
      vertices.push(add(center, p));
    }
    polyline(vertices, color, width, offset);
  }

  function sphere(center, radius, color = C.cyan, offset = point(0, 0, 0)) {
    [-60, -30, 0, 30, 60].forEach((latitude) => {
      const radians = latitude * Math.PI / 180;
      ring(
        point(center.x, center.y + Math.sin(radians) * radius, center.z),
        Math.cos(radians) * radius,
        "xz",
        color,
        latitude === 0 ? 1.6 : 0.7,
        offset,
      );
    });
    for (let longitude = 0; longitude < 180; longitude += 30) {
      const radians = longitude * Math.PI / 180;
      const vertices = [];
      for (let latitude = -90; latitude <= 90; latitude += 6) {
        const lat = latitude * Math.PI / 180;
        vertices.push(point(
          center.x + radius * Math.cos(lat) * Math.cos(radians),
          center.y + radius * Math.sin(lat),
          center.z + radius * Math.cos(lat) * Math.sin(radians),
        ));
      }
      polyline(vertices, color, 0.65, offset);
    }
  }

  function cylinder(center, radius, height, color = C.structure, offset = point(0, 0, 0), ribs = 8) {
    const bottom = point(center.x, center.y - height / 2, center.z);
    const top = point(center.x, center.y + height / 2, center.z);
    ring(bottom, radius, "xz", color, 1.2, offset);
    ring(top, radius, "xz", color, 1.2, offset);
    for (let index = 0; index < ribs; index += 1) {
      const angle = Math.PI * 2 * index / ribs;
      line(
        point(bottom.x + Math.cos(angle) * radius, bottom.y, bottom.z + Math.sin(angle) * radius),
        point(top.x + Math.cos(angle) * radius, top.y, top.z + Math.sin(angle) * radius),
        color,
        0.8,
        offset,
      );
    }
  }

  function frustum(center, bottomRadius, topRadius, height, color = C.structure, offset = point(0, 0, 0), ribs = 10) {
    const bottom = point(center.x, center.y - height / 2, center.z);
    const top = point(center.x, center.y + height / 2, center.z);
    ring(bottom, bottomRadius, "xz", color, 1.2, offset);
    ring(top, topRadius, "xz", color, 1.2, offset);
    for (let index = 0; index < ribs; index += 1) {
      const angle = Math.PI * 2 * index / ribs;
      line(
        point(bottom.x + Math.cos(angle) * bottomRadius, bottom.y, bottom.z + Math.sin(angle) * bottomRadius),
        point(top.x + Math.cos(angle) * topRadius, top.y, top.z + Math.sin(angle) * topRadius),
        color,
        0.8,
        offset,
      );
    }
  }

  function box(center, size, color = C.structure, offset = point(0, 0, 0)) {
    const vertices = [
      point(-1, -1, -1), point(1, -1, -1), point(1, 1, -1), point(-1, 1, -1),
      point(-1, -1, 1), point(1, -1, 1), point(1, 1, 1), point(-1, 1, 1),
    ].map((p) => add(center, point(p.x * size.x / 2, p.y * size.y / 2, p.z * size.z / 2)));
    [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
      .forEach(([a, b]) => line(vertices[a], vertices[b], color, 1.1, offset));
  }

  function arrow(start, end, color = C.orange, text = "", offset = point(0, 0, 0)) {
    line(start, end, color, 2, offset);
    const direction = point(end.x - start.x, end.y - start.y, end.z - start.z);
    const length = Math.hypot(direction.x, direction.y, direction.z) || 1;
    const unit = scale(direction, 1 / length);
    const side = Math.abs(unit.y) < 0.8 ? point(-unit.z, 0, unit.x) : point(1, 0, 0);
    const base = add(end, scale(unit, -0.22));
    line(end, add(base, scale(side, 0.12)), color, 2, offset);
    line(end, add(base, scale(side, -0.12)), color, 2, offset);
    if (text) label(text, add(end, scale(side, 0.18)), color, offset);
  }

  function rocket(center, height = 3.3, radius = 0.42, color = C.structure, offset = point(0, 0, 0)) {
    cylinder(point(center.x, center.y, center.z), radius, height * 0.66, color, offset);
    frustum(point(center.x, center.y + height * 0.43, center.z), radius, 0, height * 0.20, C.white, offset);
    frustum(point(center.x, center.y - height * 0.42, center.z), radius * 0.72, radius * 0.30, height * 0.18, C.orange, offset);
    for (let index = 0; index < 4; index += 1) {
      const angle = index * Math.PI / 2;
      line(
        point(center.x + Math.cos(angle) * radius, center.y - height * 0.22, center.z + Math.sin(angle) * radius),
        point(center.x + Math.cos(angle) * radius * 1.55, center.y - height * 0.34, center.z + Math.sin(angle) * radius * 1.55),
        C.muted,
        1,
        offset,
      );
    }
  }

  function buildArchitecture() {
    sphere(point(-2.25, -1.15, 0), 0.72, C.cyan);
    rocket(point(-1.0, 0.05, 0), 2.5, 0.28, C.structure, point(-0.35, 0, 0));
    cylinder(point(0.45, 0.15, 0), 0.34, 1.3, C.signal, point(0.35, 0, 0));
    frustum(point(1.58, -0.05, 0), 0.58, 0.31, 0.82, C.amber, point(0.7, -0.1, 0));
    line(point(0.10, 0.15, 0), point(0.98, 0.02, 0), C.orange, 1.5, point(0.25, 0, 0), [7, 5]);
    orientedRing(point(-0.3, -0.55, 0), 2.35, 0.18, 0.22, C.muted, 1);
    label("LAUNCH", point(-1.3, 1.55, 0), C.white, point(-0.35, 0, 0));
    label("TRANSFER", point(0.05, 1.08, 0), C.signal, point(0.35, 0, 0));
    label("LANDER", point(1.20, 0.72, 0), C.amber, point(0.7, -0.1, 0));
  }

  function buildStaging() {
    cylinder(point(0, -1.05, 0), 0.62, 2.25, C.oxidizer, point(0, -0.65, 0));
    ring(point(0, -0.25, 0), 0.62, "xz", C.orange, 2, point(0, -0.65, 0));
    frustum(point(0, -2.35, 0), 0.48, 0.20, 0.55, C.orange, point(0, -0.65, 0));
    cylinder(point(0, 0.85, 0), 0.47, 1.48, C.fuel, point(0, 0.30, 0));
    frustum(point(0, 1.75, 0), 0.47, 0.22, 0.34, C.structure, point(0, 0.30, 0));
    frustum(point(0, 2.38, 0), 0.46, 0, 0.95, C.white, point(0, 0.72, 0));
    label("STAGE 01", point(0.78, -1.1, 0), C.oxidizer, point(0, -0.65, 0));
    label("STAGE 02", point(0.63, 0.95, 0), C.fuel, point(0, 0.30, 0));
    label("PAYLOAD", point(0.58, 2.4, 0), C.white, point(0, 0.72, 0));
  }

  function buildOrbit() {
    sphere(point(0, 0, 0), 1.25, C.cyan);
    orientedRing(point(0, 0, 0), 1.62, 0.35, 0.18, C.signal, 1.6);
    orientedRing(point(0, 0, 0), 2.65, -0.22, 0.40, C.muted, 1);
    orientedRing(point(0, 0, 0), 2.2, 0.05, 0.29, C.orange, 2, point(0, 0, 0), 0, Math.PI);
    box(point(1.32, 0.82, 0.35), point(0.28, 0.18, 0.18), C.white);
    line(point(1.18, 0.82, 0.35), point(0.72, 0.82, 0.35), C.blue, 2);
    line(point(1.46, 0.82, 0.35), point(1.92, 0.82, 0.35), C.blue, 2);
    arrow(point(0, 0, 0), point(2.05, 0, 0), C.red, "X");
    arrow(point(0, 0, 0), point(0, 2.05, 0), C.signal, "Z");
    label("TRANSFER", point(-2.10, 1.10, 0), C.orange);
  }

  function buildAscent() {
    sphere(point(0, -4.25, 0), 3.05, C.cyan);
    const path = [];
    for (let index = 0; index <= 32; index += 1) {
      const t = index / 32;
      path.push(point(0.15 + 2.6 * t ** 1.7, -1.18 + 4.4 * t, 0.35 * Math.sin(t * Math.PI)));
    }
    polyline(path, C.orange, 2.4);
    rocket(point(1.47, 1.42, 0.25), 0.95, 0.11, C.white);
    ring(point(0.74, 0.23, 0), 0.42, "xz", C.red, 1.2);
    arrow(point(1.47, 1.42, 0.25), point(2.15, 2.08, 0.25), C.signal, "THRUST");
    label("MAX-Q CORRIDOR", point(0.30, 0.65, 0), C.red);
    label("155 s HANDOFF", point(2.26, 3.22, 0), C.white);
  }

  function buildNozzle() {
    cylinder(point(0, 1.35, 0), 0.92, 1.15, C.structure, point(0, 0.3, 0));
    ring(point(0, 1.90, 0), 0.82, "xz", C.fuel, 1.4, point(0, 0.3, 0));
    frustum(point(0, 0.35, 0), 0.92, 0.30, 0.92, C.amber);
    frustum(point(0, -1.10, 0), 1.28, 0.30, 2.0, C.orange, point(0, -0.35, 0));
    ring(point(0, -0.12, 0), 0.30, "xz", C.signal, 2);
    for (let index = 0; index < 8; index += 1) {
      const angle = index * Math.PI * 2 / 8;
      polyline([
        point(Math.cos(angle) * 0.12, 1.75, Math.sin(angle) * 0.12),
        point(Math.cos(angle) * 0.25, -0.12, Math.sin(angle) * 0.25),
        point(Math.cos(angle) * 0.90, -2.30, Math.sin(angle) * 0.90),
      ], index % 2 ? C.cyan : C.signal, 0.75);
    }
    label("INJECTOR", point(1.02, 1.85, 0), C.fuel, point(0, 0.3, 0));
    label("M = 1", point(0.48, -0.12, 0), C.signal);
    label("SUPERSONIC EXPANSION", point(1.28, -1.65, 0), C.orange, point(0, -0.35, 0));
  }

  function buildCycle() {
    cylinder(point(-1.45, 0.85, 0), 0.46, 0.55, C.oxidizer, point(-0.35, 0, 0));
    cylinder(point(1.45, 0.85, 0), 0.46, 0.55, C.fuel, point(0.35, 0, 0));
    cylinder(point(0, 1.60, 0), 0.55, 0.48, C.amber, point(0, 0.35, 0));
    cylinder(point(0, -0.35, 0), 0.78, 1.20, C.structure);
    frustum(point(0, -1.42, 0), 1.02, 0.35, 0.95, C.orange);
    polyline([point(-1.45, 0.58, 0), point(-1.45, -0.05, 0), point(-0.72, -0.05, 0)], C.oxidizer, 3, point(-0.35, 0, 0));
    polyline([point(1.45, 0.58, 0), point(1.45, -0.05, 0), point(0.72, -0.05, 0)], C.fuel, 3, point(0.35, 0, 0));
    line(point(-1.45, 1.13, 0), point(-0.50, 1.60, 0), C.cyan, 2, point(-0.20, 0.18, 0));
    line(point(1.45, 1.13, 0), point(0.50, 1.60, 0), C.cyan, 2, point(0.20, 0.18, 0));
    arrow(point(-0.65, 1.60, 0), point(0.65, 1.60, 0), C.signal, "SHAFT");
    label("LOX PUMP", point(-2.05, 0.90, 0), C.oxidizer, point(-0.35, 0, 0));
    label("FUEL PUMP", point(1.72, 0.90, 0), C.fuel, point(0.35, 0, 0));
    label("TURBINE", point(0.66, 1.94, 0), C.amber, point(0, 0.35, 0));
  }

  function buildPropulsion() {
    rocket(point(-2.15, 0.45, 0), 2.05, 0.25, C.structure, point(-0.30, 0, 0));
    frustum(point(-0.70, -0.15, 0), 0.70, 0.28, 1.10, C.cyan, point(-0.10, 0, 0));
    cylinder(point(0.80, 0.42, 0), 0.52, 1.15, C.amber, point(0.12, 0, 0));
    ring(point(0.80, 0.42, 0), 0.34, "xz", C.red, 2, point(0.12, 0, 0));
    box(point(2.05, 0.35, 0), point(1.45, 1.45, 0.06), C.signal, point(0.35, 0, 0));
    for (let value = -0.45; value <= 0.45; value += 0.3) {
      line(point(1.33, 0.35 + value, 0), point(2.77, 0.35 + value, 0), C.signal, 0.5, point(0.35, 0, 0));
    }
    label("CHEMICAL", point(-2.70, 1.65, 0), C.orange, point(-0.30, 0, 0));
    label("ELECTRIC", point(-1.10, 1.00, 0), C.cyan, point(-0.10, 0, 0));
    label("NUCLEAR THERMAL", point(0.18, 1.55, 0), C.amber, point(0.12, 0, 0));
    label("SOLAR SAIL", point(1.62, 1.55, 0), C.signal, point(0.35, 0, 0));
  }

  function buildAero() {
    rocket(point(0, 0, 0), 3.7, 0.38, C.structure);
    frustum(point(0, 0.25, 0), 1.85, 0.10, 4.8, C.cyan);
    arrow(point(0, 0.20, 0), point(1.8, 0.20, 0), C.red, "NORMAL LOAD");
    arrow(point(0, -0.15, 0), point(0, 2.75, 0), C.signal, "VELOCITY");
    ring(point(0, 0.70, 0), 0.46, "xz", C.orange, 2);
    const bent = [];
    for (let index = 0; index <= 24; index += 1) {
      const y = -1.7 + index * 3.4 / 24;
      bent.push(point(0.16 * Math.sin((y + 1.7) / 3.4 * Math.PI), y, 0));
    }
    polyline(bent, C.amber, 2, point(0.65, 0, 0));
    label("CENTER OF PRESSURE", point(0.58, 0.72, 0), C.orange);
    label("FIRST BENDING MODE", point(0.92, -1.15, 0), C.amber, point(0.65, 0, 0));
  }

  function buildThermal() {
    frustum(point(0, 0.20, 0), 1.55, 0.45, 1.65, C.structure);
    ring(point(0, -0.63, 0), 1.55, "xz", C.orange, 4, point(0, -0.18, 0));
    ring(point(0, -0.57, 0), 1.28, "xz", C.amber, 2);
    ring(point(0, -0.48, 0), 0.95, "xz", C.signal, 1.5);
    for (let radius = 1.8; radius <= 2.35; radius += 0.18) {
      ring(point(0, -0.82, 0), radius, "xz", C.red, 0.8, point(0, -0.35 - (radius - 1.8) * 0.25, 0), -0.18, Math.PI + 0.18);
    }
    for (let index = 0; index < 6; index += 1) {
      dot(point(Math.cos(index) * 0.70, -0.43, Math.sin(index) * 0.70), C.cyan, 4);
    }
    label("SHOCK LAYER", point(1.85, -1.55, 0), C.red);
    label("ABLATOR", point(1.40, -0.82, 0), C.orange, point(0, -0.18, 0));
    label("BONDLINE", point(0.82, -0.40, 0), C.cyan);
  }

  function buildStructure() {
    cylinder(point(0, 0, 0), 1.25, 3.60, C.structure);
    for (let y = -1.45; y <= 1.45; y += 0.58) ring(point(0, y, 0), 1.29, "xz", C.orange, 1.3);
    for (let index = 0; index < 10; index += 1) {
      const angle = index * Math.PI * 2 / 10;
      line(point(Math.cos(angle) * 1.31, -1.72, Math.sin(angle) * 1.31), point(Math.cos(angle) * 1.31, 1.72, Math.sin(angle) * 1.31), C.muted, 0.8);
    }
    cylinder(point(0, -0.35, 0), 1.04, 2.75, C.oxidizer, point(0.45, 0, 0));
    ring(point(0, 0.58, 0), 1.04, "xz", C.cyan, 2, point(0.45, 0, 0));
    arrow(point(0, 0, 0), point(1.9, 0, 0), C.red, "p r / t");
    label("PRESSURE SHELL", point(-1.92, 1.12, 0), C.structure);
    label("CRYOGEN", point(1.15, -0.55, 0), C.oxidizer, point(0.45, 0, 0));
  }

  function buildGnc() {
    box(point(0, 0, 0), point(1.35, 2.10, 1.05), C.structure);
    arrow(point(0, 0, 0), point(2.2, 0, 0), C.red, "BODY X");
    arrow(point(0, 0, 0), point(0, 2.4, 0), C.signal, "BODY Z");
    arrow(point(0, 0, 0), point(0, 0, 2.0), C.cyan, "BODY Y");
    frustum(point(-0.55, 0.45, 0), 0.78, 0.10, 1.55, C.amber, point(-0.35, 0.5, 0));
    orientedRing(point(0.75, -0.55, 0.15), 0.72, 0.25, -0.18, C.orange, 1.2, point(0.35, -0.2, 0));
    orientedRing(point(0.75, -0.55, 0.15), 0.40, 1.55, 0.10, C.orange, 1.2, point(0.35, -0.2, 0));
    label("SENSOR FOV", point(-1.75, 1.45, 0), C.amber, point(-0.35, 0.5, 0));
    label("3-SIGMA COVARIANCE", point(1.15, -1.40, 0), C.orange, point(0.35, -0.2, 0));
  }

  function buildReliability() {
    [-1.35, 0, 1.35].forEach((x, index) => {
      box(point(x, 0.65, 0), point(0.82, 1.05, 0.72), [C.oxidizer, C.signal, C.fuel][index], point((index - 1) * 0.25, 0, 0));
      label(`LANE ${index + 1}`, point(x - 0.35, 1.35, 0), [C.oxidizer, C.signal, C.fuel][index], point((index - 1) * 0.25, 0, 0));
      line(point(x, 0.10, 0), point(0, -0.65, 0), C.muted, 1.5, point((index - 1) * 0.12, 0, 0));
    });
    box(point(0, -0.82, 0), point(1.35, 0.58, 0.58), C.orange);
    label("VOTER", point(0.72, -0.82, 0), C.orange);
    line(point(-2.2, -1.65, -0.7), point(2.2, -1.65, -0.7), C.red, 3);
    [-1.35, 0, 1.35].forEach((x) => line(point(x, 0.10, 0), point(x, -1.65, -0.7), C.red, 0.9, point(0, -0.2, 0)));
    label("SHARED POWER / COMMON CAUSE", point(-1.95, -2.05, -0.7), C.red);
  }

  function buildTest() {
    for (const x of [-1.35, 1.35]) {
      line(point(x, -2.1, -1), point(x, 2.15, -1), C.structure, 2);
      line(point(x, -2.1, 1), point(x, 2.15, 1), C.structure, 2);
      line(point(x, 2.15, -1), point(x, 2.15, 1), C.structure, 2);
    }
    line(point(-1.35, 1.65, 0), point(1.35, 1.65, 0), C.structure, 3);
    cylinder(point(0, 0.65, 0), 0.58, 1.15, C.structure);
    frustum(point(0, -0.55, 0), 0.92, 0.30, 1.25, C.orange);
    frustum(point(0, -1.80, 0), 1.45, 0.45, 1.25, C.red);
    [-1.8, -0.9, 0.9, 1.8].forEach((x, index) => {
      dot(point(x, -0.25 + (index % 2) * 0.7, 1.15), C.cyan, 5, point((x / 1.8) * 0.15, 0, 0));
      line(point(x, -0.25 + (index % 2) * 0.7, 1.15), point(0, -0.2, 0), C.cyan, 0.7, point((x / 1.8) * 0.15, 0, 0), [4, 4]);
    });
    label("THRUST FRAME", point(1.55, 1.72, 0), C.structure);
    label("OPTICAL + PRESSURE DIAGNOSTICS", point(-2.40, 0.95, 1.15), C.cyan);
  }

  function buildLanding() {
    for (let x = -2.8; x <= 2.8; x += 0.4) line(point(x, -2.1, -2.8), point(x, -2.1, 2.8), C.grid, 0.7);
    for (let z = -2.8; z <= 2.8; z += 0.4) line(point(-2.8, -2.1, z), point(2.8, -2.1, z), C.grid, 0.7);
    rocket(point(0, 0.55, 0), 3.2, 0.38, C.structure, point(0, 0.55, 0));
    frustum(point(0, -1.05, 0), 0.92, 0.20, 1.65, C.orange, point(0, -0.35, 0));
    orientedRing(point(0, -0.15, 0), 1.15, 0, 0, C.signal, 1.2);
    orientedRing(point(0, -0.65, 0), 1.75, 0, 0, C.signal, 1.0);
    ring(point(0, -2.08, 0), 0.72, "xz", C.cyan, 2);
    for (let index = 0; index < 4; index += 1) {
      const angle = index * Math.PI / 2;
      line(point(Math.cos(angle) * 0.34, -0.55, Math.sin(angle) * 0.34), point(Math.cos(angle) * 0.92, -1.75, Math.sin(angle) * 0.92), C.white, 2, point(0, 0.55, 0));
    }
    label("REACHABLE DIVERT", point(1.72, -0.10, 0), C.signal);
    label("TOUCHDOWN DISPERSION", point(0.82, -2.05, 0), C.cyan);
  }

  const builders = {
    architecture: buildArchitecture,
    staging: buildStaging,
    orbit: buildOrbit,
    ascent: buildAscent,
    nozzle: buildNozzle,
    cycle: buildCycle,
    propulsion: buildPropulsion,
    aero: buildAero,
    thermal: buildThermal,
    structure: buildStructure,
    gnc: buildGnc,
    reliability: buildReliability,
    test: buildTest,
    landing: buildLanding,
  };

  function transformed(position, offset) {
    const exploded = add(position, scale(offset, state.explode));
    const cosYaw = Math.cos(state.yaw);
    const sinYaw = Math.sin(state.yaw);
    const x1 = exploded.x * cosYaw - exploded.z * sinYaw;
    const z1 = exploded.x * sinYaw + exploded.z * cosYaw;
    const cosPitch = Math.cos(state.pitch);
    const sinPitch = Math.sin(state.pitch);
    return point(x1, exploded.y * cosPitch - z1 * sinPitch, exploded.y * sinPitch + z1 * cosPitch);
  }

  function project(position, offset) {
    const p = transformed(position, offset);
    const camera = 8.6;
    const perspective = camera / Math.max(2.8, camera - p.z);
    const unit = Math.min(canvas.width, canvas.height) * 0.115 * state.zoom;
    return {
      x: canvas.width / 2 + p.x * unit * perspective,
      y: canvas.height / 2 - p.y * unit * perspective,
      z: p.z,
      perspective,
    };
  }

  function drawBackground() {
    const gradient = context.createRadialGradient(canvas.width * 0.55, canvas.height * 0.44, 20, canvas.width * 0.55, canvas.height * 0.44, canvas.width * 0.70);
    gradient.addColorStop(0, "#102331");
    gradient.addColorStop(0.55, "#07131d");
    gradient.addColorStop(1, "#03070b");
    context.fillStyle = gradient;
    context.fillRect(0, 0, canvas.width, canvas.height);

    context.strokeStyle = "rgba(121, 217, 232, .07)";
    context.lineWidth = 1;
    for (let x = -canvas.height; x < canvas.width + canvas.height; x += 54) {
      context.beginPath();
      context.moveTo(x, canvas.height);
      context.lineTo(x + canvas.height, 0);
      context.stroke();
    }
    for (let x = 0; x < canvas.width + canvas.height; x += 54) {
      context.beginPath();
      context.moveTo(x, 0);
      context.lineTo(x - canvas.height, canvas.height);
      context.stroke();
    }
    context.fillStyle = "rgba(200, 237, 117, .65)";
    for (let index = 0; index < 42; index += 1) {
      const x = (index * 173 + 41) % canvas.width;
      const y = (index * 97 + 17) % canvas.height;
      context.fillRect(x, y, index % 4 === 0 ? 2 : 1, index % 4 === 0 ? 2 : 1);
    }
  }

  function render(time = 0) {
    state.time = time;
    if (state.spin && !state.dragging) {
      state.yaw += 0.00022 * Math.min(40, Math.max(0, time - (render.lastTime || time)));
      if (state.yaw > Math.PI) state.yaw -= Math.PI * 2;
      yawInput.value = String(Math.round(state.yaw * 180 / Math.PI));
    }
    render.lastTime = time;
    const targetExplode = state.exploded ? 1 : 0;
    state.explode += (targetExplode - state.explode) * 0.09;

    drawBackground();
    const segments = scene.segments.map((item) => {
      const a = project(item.a, item.offset);
      const b = project(item.b, item.offset);
      return { ...item, a2: a, b2: b, depth: (a.z + b.z) / 2 };
    }).sort((a, b) => a.depth - b.depth);

    for (const item of segments) {
      context.beginPath();
      context.moveTo(item.a2.x, item.a2.y);
      context.lineTo(item.b2.x, item.b2.y);
      context.strokeStyle = item.color;
      context.globalAlpha = Math.max(0.24, Math.min(1, 0.62 + item.depth * 0.08));
      context.lineWidth = item.width * Math.max(0.55, (item.a2.perspective + item.b2.perspective) / 2);
      context.setLineDash(item.dash);
      context.stroke();
    }
    context.setLineDash([]);
    context.globalAlpha = 1;

    const points = scene.points.map((item) => ({ ...item, p: project(item.position, item.offset) })).sort((a, b) => a.p.z - b.p.z);
    for (const item of points) {
      context.beginPath();
      context.arc(item.p.x, item.p.y, item.radius * item.p.perspective, 0, Math.PI * 2);
      context.fillStyle = item.color;
      context.shadowColor = item.color;
      context.shadowBlur = 14;
      context.fill();
      context.shadowBlur = 0;
    }

    context.font = "700 11px 'Courier New', monospace";
    context.textBaseline = "middle";
    for (const item of scene.labels) {
      const p = project(item.position, item.offset);
      const width = context.measureText(item.text).width + 18;
      context.fillStyle = "rgba(3, 8, 12, .80)";
      context.fillRect(p.x - 7, p.y - 10, width, 20);
      context.strokeStyle = item.color;
      context.lineWidth = 1;
      context.strokeRect(p.x - 7, p.y - 10, width, 20);
      context.fillStyle = item.color;
      context.fillText(item.text, p.x + 2, p.y);
    }

    context.fillStyle = "rgba(233, 243, 242, .42)";
    context.font = "700 9px 'Courier New', monospace";
    context.fillText(`MODEL / ${type.toUpperCase()} / CONCEPTUAL GEOMETRY`, 20, 24);
    context.textAlign = "right";
    context.fillText("DRAG TO ORBIT / WHEEL TO ZOOM", canvas.width - 20, 24);
    context.textAlign = "left";
    yawOutput.textContent = `${Math.round(state.yaw * 180 / Math.PI)} deg`;
    pitchOutput.textContent = `${Math.round(state.pitch * 180 / Math.PI)} deg`;
    zoomOutput.textContent = `${state.zoom.toFixed(2)} x`;
    canvas.dataset.rendered = "true";
    requestAnimationFrame(render);
  }

  function syncFromInputs() {
    state.yaw = Number(yawInput.value) * Math.PI / 180;
    state.pitch = Number(pitchInput.value) * Math.PI / 180;
    state.zoom = Number(zoomInput.value);
  }

  [yawInput, pitchInput, zoomInput].forEach((input) => input.addEventListener("input", syncFromInputs));
  spinButton.addEventListener("click", () => {
    state.spin = !state.spin;
    spinButton.textContent = state.spin ? "Pause rotation" : "Resume rotation";
    status.textContent = `${state.spin ? "AUTO ROTATE" : "MANUAL VIEW"} / ${state.exploded ? "EXPLODED CUTAWAY" : "NOMINAL ASSEMBLY"}`;
  });
  explodeButton.addEventListener("click", () => {
    state.exploded = !state.exploded;
    explodeButton.textContent = state.exploded ? "Close assembly" : "Explode / cutaway";
    status.textContent = `${state.spin ? "AUTO ROTATE" : "MANUAL VIEW"} / ${state.exploded ? "EXPLODED CUTAWAY" : "NOMINAL ASSEMBLY"}`;
  });
  resetButton.addEventListener("click", () => {
    yawInput.value = "28";
    pitchInput.value = "-12";
    zoomInput.value = "1";
    state.spin = true;
    state.exploded = false;
    spinButton.textContent = "Pause rotation";
    explodeButton.textContent = "Explode / cutaway";
    status.textContent = "AUTO ROTATE / NOMINAL ASSEMBLY";
    syncFromInputs();
  });

  canvas.addEventListener("pointerdown", (event) => {
    state.dragging = true;
    state.lastX = event.clientX;
    state.lastY = event.clientY;
    canvas.setPointerCapture(event.pointerId);
    status.textContent = `MANUAL ORBIT / ${state.exploded ? "EXPLODED CUTAWAY" : "NOMINAL ASSEMBLY"}`;
  });
  canvas.addEventListener("pointermove", (event) => {
    if (!state.dragging) return;
    state.yaw += (event.clientX - state.lastX) * 0.008;
    state.pitch = Math.max(-1.22, Math.min(1.22, state.pitch + (event.clientY - state.lastY) * 0.008));
    state.lastX = event.clientX;
    state.lastY = event.clientY;
    yawInput.value = String(Math.round(state.yaw * 180 / Math.PI));
    pitchInput.value = String(Math.round(state.pitch * 180 / Math.PI));
  });
  canvas.addEventListener("pointerup", (event) => {
    state.dragging = false;
    canvas.releasePointerCapture(event.pointerId);
  });
  canvas.addEventListener("wheel", (event) => {
    event.preventDefault();
    state.zoom = Math.max(0.65, Math.min(1.65, state.zoom - event.deltaY * 0.001));
    zoomInput.value = state.zoom.toFixed(2);
  }, { passive: false });

  builders[type]();
  syncFromInputs();
  requestAnimationFrame(render);
})();
