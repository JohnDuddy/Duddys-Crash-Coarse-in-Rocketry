(() => {
  const lab = document.querySelector("[data-rocket-lab]");
  if (!lab) return;
  const canvas = lab.querySelector("[data-lab-canvas]");
  const context = canvas.getContext("2d");
  const controlsHost = lab.querySelector("[data-lab-controls]");
  const readoutsHost = lab.querySelector("[data-lab-readouts]");
  const resetButton = lab.querySelector("[data-lab-reset]");
  const type = lab.dataset.labType;
  const G0 = 9.80665;
  const RE = 6_378_137;
  const MU = 3.986004418e14;
  const SIGMA = 5.670374419e-8;
  const COLORS = {
    void: "#05080c",
    deep: "#08111b",
    grid: "rgba(181, 211, 219, .10)",
    white: "#eef5f3",
    muted: "rgba(202, 220, 225, .50)",
    orange: "#ff6038",
    amber: "#ffb454",
    signal: "#c8ed75",
    cyan: "#79d9e8",
    red: "#ff6b60",
  };

  function clamp(value, minimum, maximum) {
    return Math.min(maximum, Math.max(minimum, value));
  }

  function machFromArea(areaRatio, gamma) {
    if (areaRatio <= 1) return 1;
    let low = 1.0001;
    let high = 12;
    const areaAtMach = (mach) => (
      (1 / mach)
      * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * mach ** 2))
        ** ((gamma + 1) / (2 * (gamma - 1)))
    );
    for (let index = 0; index < 70; index += 1) {
      const middle = (low + high) / 2;
      if (areaAtMach(middle) > areaRatio) high = middle;
      else low = middle;
    }
    return (low + high) / 2;
  }

  function simulateAscent(values) {
    const dt = 0.5;
    const trajectory = [];
    let x = 0;
    let h = 0;
    let vx = 0;
    let vy = 0;
    let massFraction = 1;
    let maxQ = 0;
    let maxHeat = 0;
    for (let time = 0; time <= 155 && h >= 0; time += dt) {
      const pitchFraction = clamp((time - 8) / Math.max(25, values.pitchTime), 0, 1);
      const angle = (90 - pitchFraction * 64) * Math.PI / 180;
      const density = 1.225 * values.atmosphere * Math.exp(-h / 8_500);
      const speed = Math.hypot(vx, vy);
      const q = 0.5 * density * speed ** 2;
      const heat = 1.83e-4 * Math.sqrt(Math.max(density, 0) / 0.8) * speed ** 3;
      maxQ = Math.max(maxQ, q);
      maxHeat = Math.max(maxHeat, heat);
      const throttle = q > values.qLimit * 1_000 ? clamp(values.qLimit * 1_000 / q, 0.55, 1) : 1;
      const thrustAcceleration = values.twr * G0 * throttle / Math.max(0.36, massFraction);
      const dragAcceleration = q / Math.max(180, values.ballistic);
      const dragX = speed > 1 ? dragAcceleration * vx / speed : 0;
      const dragY = speed > 1 ? dragAcceleration * vy / speed : 0;
      vx += (thrustAcceleration * Math.cos(angle) - dragX) * dt;
      vy += (thrustAcceleration * Math.sin(angle) - dragY - G0 * (RE / (RE + h)) ** 2) * dt;
      x += vx * dt;
      h += vy * dt;
      massFraction = Math.max(0.34, massFraction - values.burnRate * dt / 1000);
      if (Math.round(time * 2) % 4 === 0) trajectory.push({ time, x, h, vx, vy, q, heat });
    }
    const final = trajectory.at(-1);
    return { trajectory, final, maxQ, maxHeat };
  }

  const CONFIGS = {
    architecture: {
      controls: [
        ["mass", "Initial mass", 100, 1500, 10, 620, "t"],
        ["reliability", "Mission reliability", 0.75, 0.999, 0.001, 0.965, ""],
        ["reuse", "Design reuse flights", 1, 50, 1, 12, "flights"],
        ["uncertainty", "Architecture uncertainty", 0, 0.5, 0.01, 0.18, "fraction"],
        ["complexity", "Interface complexity", 1, 20, 1, 9, "index"],
      ],
      calculate: (v) => {
        const delivered = v.mass * 0.045 * v.reliability * (1 - 0.42 * v.uncertainty);
        const lifecycle = 100 * (1 + v.complexity / 12) / Math.sqrt(v.reuse);
        const robustness = 100 * v.reliability * (1 - v.uncertainty) / (1 + v.complexity / 30);
        return {
          readouts: [`Expected delivery ${delivered.toFixed(1)} t`, `Lifecycle index ${lifecycle.toFixed(1)}`, `Robustness ${robustness.toFixed(1)} / 100`],
          data: { delivered, lifecycle, robustness },
        };
      },
    },
    staging: {
      controls: [
        ["isp1", "Stage 1 Isp", 250, 390, 1, 330, "s"],
        ["isp2", "Stage 2 Isp", 300, 480, 1, 450, "s"],
        ["inert1", "Stage 1 inert fraction", 0.03, 0.16, 0.005, 0.07, ""],
        ["inert2", "Stage 2 inert fraction", 0.04, 0.20, 0.005, 0.10, ""],
        ["split", "Delta-v to stage 1", 0.25, 0.72, 0.01, 0.48, "fraction"],
        ["losses", "External losses", 800, 2600, 25, 1600, "m/s"],
      ],
      calculate: (v) => {
        const ideal = 7_800 + v.losses;
        const dv1 = ideal * v.split;
        const dv2 = ideal - dv1;
        const r1 = Math.exp(dv1 / (v.isp1 * G0));
        const r2 = Math.exp(dv2 / (v.isp2 * G0));
        const lambda1 = Math.max(0, (1 / r1 - v.inert1) / (1 - v.inert1));
        const lambda2 = Math.max(0, (1 / r2 - v.inert2) / (1 - v.inert2));
        const payload = lambda1 * lambda2 * 100;
        return {
          readouts: [`Ideal demand ${ideal.toFixed(0)} m/s`, `Stage split ${dv1.toFixed(0)} / ${dv2.toFixed(0)} m/s`, `Ideal payload fraction ${payload.toFixed(2)}%`],
          data: { dv1, dv2, payload, lambda1, lambda2 },
        };
      },
    },
    orbit: {
      controls: [
        ["altitude", "Mean altitude", 180, 60_000, 20, 400, "km"],
        ["eccentricity", "Eccentricity", 0, 0.7, 0.01, 0.05, ""],
        ["inclination", "Inclination", 0, 100, 0.5, 51.6, "deg"],
        ["j2", "J2 model scale", 0, 2, 0.05, 1, "x"],
        ["drag", "Drag model scale", 0, 5, 0.1, 1, "x"],
        ["thirdBody", "Third-body scale", 0, 2, 0.05, 0.3, "x"],
      ],
      calculate: (v) => {
        const a = RE + v.altitude * 1000;
        const period = 2 * Math.PI * Math.sqrt(a ** 3 / MU);
        const velocity = Math.sqrt(MU / a);
        const p = a * (1 - v.eccentricity ** 2);
        const j2 = 1.08262668e-3 * v.j2;
        const n = Math.sqrt(MU / a ** 3);
        const raanRate = -1.5 * j2 * (RE / p) ** 2 * n * Math.cos(v.inclination * Math.PI / 180);
        const degDay = raanRate * 86400 * 180 / Math.PI;
        const fidelity = 1 + v.j2 + v.drag + v.thirdBody;
        return {
          readouts: [`Period ${(period / 60).toFixed(1)} min`, `Circular-speed scale ${(velocity / 1000).toFixed(2)} km/s`, `J2 RAAN drift ${degDay.toFixed(2)} deg/day`, `Force-model index ${fidelity.toFixed(1)}`],
          data: { period, velocity, degDay, a, e: v.eccentricity },
        };
      },
    },
    ascent: {
      controls: [
        ["twr", "Initial thrust / weight", 1.05, 2.4, 0.01, 1.45, ""],
        ["pitchTime", "Pitch program duration", 35, 150, 1, 88, "s"],
        ["atmosphere", "Density scale", 0.65, 1.35, 0.01, 1, "x"],
        ["qLimit", "Dynamic-pressure limit", 20, 75, 1, 45, "kPa"],
        ["ballistic", "Ballistic coefficient", 1000, 20_000, 100, 8000, "kg/m2"],
        ["burnRate", "Normalized burn rate", 1.5, 5.0, 0.05, 3.3, "/ks"],
      ],
      calculate: (v) => {
        const simulation = simulateAscent(v);
        const final = simulation.final || { h: 0, vx: 0, vy: 0 };
        return {
          readouts: [
            `155 s handoff altitude ${(final.h / 1000).toFixed(1)} km`,
            `155 s handoff speed ${(Math.hypot(final.vx, final.vy) / 1000).toFixed(2)} km/s`,
            `Max q ${(simulation.maxQ / 1000).toFixed(1)} kPa`,
            simulation.maxQ / 1000 <= v.qLimit
              ? "q constraint satisfied"
              : `q constraint VIOLATED by ${(simulation.maxQ / 1000 - v.qLimit).toFixed(1)} kPa`,
            `Peak heat ${(simulation.maxHeat / 1e6).toFixed(2)} MW/m2`,
          ],
          data: simulation,
        };
      },
    },
    nozzle: {
      controls: [
        ["pc", "Chamber pressure", 2, 35, 0.1, 15, "MPa"],
        ["temperature", "Chamber temperature", 2200, 3900, 10, 3550, "K"],
        ["gamma", "Specific-heat ratio", 1.12, 1.34, 0.005, 1.22, ""],
        ["molecularMass", "Molecular mass", 12, 32, 0.2, 22, "kg/kmol"],
        ["areaRatio", "Nozzle area ratio", 3, 180, 1, 40, ""],
        ["throatArea", "Throat area", 0.01, 0.5, 0.005, 0.12, "m2"],
        ["ambient", "Ambient pressure", 0, 101, 1, 20, "kPa"],
      ],
      calculate: (v) => {
        const gamma = v.gamma;
        const gasR = 8314.4626 / v.molecularMass;
        const mach = machFromArea(v.areaRatio, gamma);
        const pressureRatio = (1 + (gamma - 1) / 2 * mach ** 2) ** (-gamma / (gamma - 1));
        const exitPressure = v.pc * 1e6 * pressureRatio;
        const exitTemperature = v.temperature / (1 + (gamma - 1) / 2 * mach ** 2);
        const exitVelocity = mach * Math.sqrt(gamma * gasR * exitTemperature);
        const massFlow = v.pc * 1e6 * v.throatArea * Math.sqrt(gamma / (gasR * v.temperature))
          * (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1)));
        const exitArea = v.throatArea * v.areaRatio;
        const thrust = massFlow * exitVelocity + (exitPressure - v.ambient * 1000) * exitArea;
        const isp = thrust / (massFlow * G0);
        return {
          readouts: [`Exit Mach ${mach.toFixed(2)}`, `Exit pressure ${(exitPressure / 1000).toFixed(1)} kPa`, `Mass flow ${massFlow.toFixed(1)} kg/s`, `Thrust ${(thrust / 1000).toFixed(0)} kN`, `Ideal Isp ${isp.toFixed(1)} s`],
          data: { mach, exitPressure, massFlow, thrust, isp, areaRatio: v.areaRatio, ambient: v.ambient },
        };
      },
    },
    cycle: {
      controls: [
        ["pc", "Chamber pressure", 3, 35, 0.1, 18, "MPa"],
        ["flow", "Main propellant flow", 40, 1200, 5, 420, "kg/s"],
        ["density", "Mean pump inlet density", 70, 1150, 5, 640, "kg/m3"],
        ["pumpEff", "Pump efficiency", 0.45, 0.88, 0.01, 0.72, ""],
        ["turbineDh", "Turbine enthalpy drop", 100, 950, 5, 430, "kJ/kg"],
        ["turbineEff", "Turbine efficiency", 0.45, 0.92, 0.01, 0.76, ""],
        ["turbineFraction", "Turbine flow fraction", 0.02, 0.35, 0.005, 0.12, ""],
      ],
      calculate: (v) => {
        const deltaP = v.pc * 1e6 * 1.22;
        const pumpPower = v.flow * deltaP / (v.density * v.pumpEff);
        const turbinePower = v.flow * v.turbineFraction * v.turbineDh * 1000 * v.turbineEff;
        const balance = turbinePower / pumpPower;
        const shaftMargin = (turbinePower - pumpPower) / 1e6;
        return {
          readouts: [`Pump power ${(pumpPower / 1e6).toFixed(1)} MW`, `Turbine power ${(turbinePower / 1e6).toFixed(1)} MW`, `Power ratio ${balance.toFixed(2)}`, `Shaft margin ${shaftMargin.toFixed(1)} MW`],
          data: { pumpPower, turbinePower, balance, shaftMargin },
        };
      },
    },
    propulsion: {
      controls: [
        ["power", "Input power", 0.05, 20, 0.05, 2, "MW"],
        ["efficiency", "Conversion efficiency", 0.25, 0.85, 0.01, 0.62, ""],
        ["isp", "Specific impulse", 500, 12_000, 50, 2800, "s"],
        ["initialMass", "Spacecraft mass", 1, 100, 0.5, 22, "t"],
        ["systemMass", "Power + propulsion mass", 0.5, 30, 0.25, 6, "t"],
        ["duration", "Thrust duration", 1, 500, 1, 120, "days"],
      ],
      calculate: (v) => {
        const exhaust = v.isp * G0;
        const thrust = 2 * v.efficiency * v.power * 1e6 / exhaust;
        const flow = thrust / exhaust;
        const propellant = Math.min(v.initialMass * 1000 * 0.75, flow * v.duration * 86400);
        const dryFinal = Math.max(1, v.initialMass * 1000 - propellant);
        const deltaV = exhaust * Math.log(v.initialMass * 1000 / dryFinal);
        const acceleration = thrust / (v.initialMass * 1000);
        const specificMass = v.systemMass * 1000 / (v.power * 1000);
        return {
          readouts: [`Thrust ${thrust.toFixed(1)} N`, `Initial acceleration ${(acceleration * 1e3).toFixed(3)} mm/s2`, `Propellant ${(propellant / 1000).toFixed(2)} t`, `Ideal delta-v ${(deltaV / 1000).toFixed(2)} km/s`, `System specific mass ${specificMass.toFixed(2)} kg/kW`],
          data: { thrust, propellant, deltaV, acceleration, specificMass },
        };
      },
    },
    aero: {
      controls: [
        ["mach", "Mach number", 0.2, 12, 0.05, 1.2, ""],
        ["density", "Density", 0.001, 1.225, 0.005, 0.55, "kg/m3"],
        ["temperature", "Air temperature", 180, 320, 1, 245, "K"],
        ["alpha", "Angle of attack", -8, 12, 0.1, 2, "deg"],
        ["area", "Reference area", 5, 200, 1, 48, "m2"],
        ["cnAlpha", "Normal-force slope", 0.5, 8, 0.1, 3.6, "/rad"],
        ["flexibility", "Flexibility index", 0, 1, 0.01, 0.35, ""],
      ],
      calculate: (v) => {
        const sound = Math.sqrt(1.4 * 287.05 * v.temperature);
        const speed = v.mach * sound;
        const q = 0.5 * v.density * speed ** 2;
        const normal = q * v.area * v.cnAlpha * v.alpha * Math.PI / 180;
        const bending = normal * 18;
        const flutterQ = 92_000 * (1 - 0.55 * v.flexibility);
        const margin = flutterQ / Math.max(q, 1) - 1;
        return {
          readouts: [`Speed ${speed.toFixed(0)} m/s`, `Dynamic pressure ${(q / 1000).toFixed(1)} kPa`, `Normal force ${(normal / 1000).toFixed(1)} kN`, `Bending ${(bending / 1e6).toFixed(2)} MN m`, `Flutter screen MS ${margin.toFixed(2)}`],
          data: { speed, q, normal, bending, margin, alpha: v.alpha },
        };
      },
    },
    thermal: {
      controls: [
        ["velocity", "Entry velocity", 3, 13, 0.05, 7.8, "km/s"],
        ["density", "Local density", 0.00001, 0.08, 0.0001, 0.008, "kg/m3"],
        ["noseRadius", "Nose radius", 0.1, 8, 0.05, 1.2, "m"],
        ["emissivity", "Surface emissivity", 0.35, 0.95, 0.01, 0.82, ""],
        ["thickness", "TPS thickness", 5, 180, 1, 45, "mm"],
        ["conductivity", "TPS conductivity", 0.03, 1.5, 0.01, 0.16, "W/mK"],
      ],
      calculate: (v) => {
        const velocity = v.velocity * 1000;
        const heatFlux = 1.83e-4 * Math.sqrt(v.density / v.noseRadius) * velocity ** 3;
        const radiationTemp = (heatFlux / (v.emissivity * SIGMA)) ** 0.25;
        const resistance = v.thickness / 1000 / v.conductivity;
        const conductionScreen = heatFlux / Math.max(resistance * 1500, 1);
        const bondline = 293 + 900 * Math.exp(-v.thickness / (18 + 30 * v.conductivity)) * (v.velocity / 7.8) ** 1.7;
        return {
          readouts: [`Convective screen ${(heatFlux / 1e6).toFixed(2)} MW/m2`, `Radiative equilibrium ${radiationTemp.toFixed(0)} K`, `Thermal resistance ${resistance.toFixed(3)} m2K/W`, `Bondline screen ${bondline.toFixed(0)} K`, `Conduction index ${conductionScreen.toFixed(0)}`],
          data: { heatFlux, radiationTemp, bondline, thickness: v.thickness },
        };
      },
    },
    structure: {
      controls: [
        ["pressure", "Tank pressure", 0.1, 6, 0.05, 0.45, "MPa"],
        ["radius", "Tank radius", 0.5, 6, 0.05, 2.4, "m"],
        ["thickness", "Wall thickness", 1, 45, 0.5, 7.5, "mm"],
        ["yield", "Cryogenic allowable", 120, 1400, 10, 520, "MPa"],
        ["knockdown", "Buckling knockdown", 0.15, 0.95, 0.01, 0.55, ""],
        ["heatLeak", "Heat leak", 50, 8000, 25, 950, "W"],
        ["coast", "Coast duration", 0.1, 72, 0.1, 8, "h"],
      ],
      calculate: (v) => {
        const hoop = v.pressure * 1e6 * v.radius / (v.thickness / 1000);
        const margin = v.yield * 1e6 / hoop - 1;
        const bucklingAllowable = v.knockdown * 0.6 * v.yield;
        const boiloff = v.heatLeak * v.coast * 3600 / 445_000;
        const stored = 4 * Math.PI * v.radius ** 2 * v.thickness / 1000 * 2700;
        return {
          readouts: [`Hoop stress ${(hoop / 1e6).toFixed(0)} MPa`, `Pressure MS ${margin.toFixed(2)}`, `Buckling screen ${bucklingAllowable.toFixed(0)} MPa`, `LH2-equivalent boiloff ${boiloff.toFixed(1)} kg`, `Shell mass screen ${stored.toFixed(0)} kg`],
          data: { hoop, margin, bucklingAllowable, boiloff, stored },
        };
      },
    },
    gnc: {
      controls: [
        ["wind", "Disturbance acceleration", 0, 8, 0.1, 2.4, "m/s2"],
        ["noise", "Sensor noise", 0, 2, 0.01, 0.25, "units"],
        ["bias", "Sensor bias", -2, 2, 0.01, 0.12, "units"],
        ["gain", "Closed-loop gain", 0.2, 8, 0.05, 2.2, ""],
        ["delay", "Loop delay", 0, 0.5, 0.005, 0.08, "s"],
        ["authority", "Actuator authority", 0.2, 3, 0.05, 1.4, "x"],
        ["flexHz", "First flexible mode", 0.5, 12, 0.1, 4.2, "Hz"],
      ],
      calculate: (v) => {
        const residual = v.wind / (1 + v.gain * v.authority) + Math.abs(v.bias) + v.noise;
        const crossover = v.gain * 0.7;
        const phaseMargin = 72 - crossover * v.delay * 180 / Math.PI - 15 * crossover / v.flexHz;
        const covariance = v.noise ** 2 / Math.max(v.gain, 0.1) + v.bias ** 2;
        const robustness = clamp(phaseMargin / 60, 0, 1.5);
        return {
          readouts: [`Tracking-error screen ${residual.toFixed(2)}`, `Crossover ${crossover.toFixed(2)} rad/s`, `Phase-margin screen ${phaseMargin.toFixed(1)} deg`, `Covariance index ${covariance.toFixed(3)}`, `Robustness ${robustness.toFixed(2)}`],
          data: { residual, crossover, phaseMargin, covariance, robustness },
        };
      },
    },
    reliability: {
      controls: [
        ["componentR", "Component reliability", 0.90, 0.99999, 0.00001, 0.998, ""],
        ["seriesCount", "Required series functions", 1, 80, 1, 24, ""],
        ["redundancy", "Redundant channels", 1, 4, 1, 3, ""],
        ["commonCause", "Common-cause probability", 0, 0.08, 0.0005, 0.008, ""],
        ["detection", "Fault detection coverage", 0.5, 1, 0.005, 0.96, ""],
        ["recovery", "Recovery success", 0.3, 1, 0.01, 0.88, ""],
      ],
      calculate: (v) => {
        const channelSuccess = 1 - (1 - v.componentR) ** Math.round(v.redundancy);
        const functionSuccess = (1 - v.commonCause) * channelSuccess;
        const rawSystem = functionSuccess ** Math.round(v.seriesCount);
        const coveredFailure = (1 - rawSystem) * v.detection * v.recovery;
        const mission = clamp(rawSystem + coveredFailure, 0, 1);
        const failurePpm = (1 - mission) * 1e6;
        return {
          readouts: [`Channel success ${(channelSuccess * 100).toFixed(4)}%`, `Raw system ${(rawSystem * 100).toFixed(3)}%`, `Recovered mission ${(mission * 100).toFixed(3)}%`, `Failure ${failurePpm.toFixed(0)} ppm`],
          data: { channelSuccess, rawSystem, mission, failurePpm },
        };
      },
    },
    test: {
      controls: [
        ["bandwidth", "Signal bandwidth", 50, 20_000, 50, 2500, "Hz"],
        ["sampleRate", "Sample rate", 100, 100_000, 100, 20_000, "Hz"],
        ["uncertainty", "Sensor uncertainty", 0.1, 10, 0.1, 1.2, "%"],
        ["failureP", "Vehicle failure probability", 0.00001, 0.1, 0.00001, 0.002, ""],
        ["footprint", "Hazard footprint", 1, 2500, 1, 180, "km2"],
        ["population", "Population density", 0, 1000, 1, 12, "/km2"],
        ["casualty", "Conditional casualty fraction", 0, 0.1, 0.001, 0.012, ""],
      ],
      calculate: (v) => {
        const nyquistMargin = v.sampleRate / (2 * v.bandwidth);
        const people = v.footprint * v.population;
        const expectedCasualties = v.failureP * people * v.casualty;
        const information = 1 / (v.uncertainty / 100) ** 2;
        return {
          readouts: [`Nyquist margin ${nyquistMargin.toFixed(2)}x`, `Measurement information ${information.toFixed(0)}`, `Exposed population ${people.toFixed(0)}`, `Illustrative E_c ${expectedCasualties.toExponential(2)}`, nyquistMargin < 1 ? "ALIASING RISK" : "Sampling screen passed"],
          data: { nyquistMargin, people, expectedCasualties, information },
        };
      },
    },
    landing: {
      controls: [
        ["mass", "Landing mass", 10, 300, 1, 65, "t"],
        ["thrust", "Available thrust", 200, 5000, 10, 1400, "kN"],
        ["velocity", "Initial descent speed", 50, 900, 5, 360, "m/s"],
        ["altitude", "Ignition altitude", 0.5, 30, 0.1, 8, "km"],
        ["isp", "Landing Isp", 220, 380, 1, 310, "s"],
        ["reserve", "Propellant reserve", 0, 0.4, 0.01, 0.16, "fraction"],
        ["reliability", "Landing reliability", 0.8, 0.9999, 0.0001, 0.985, ""],
        ["cadence", "Annual flight cadence", 1, 100, 1, 18, "flights"],
      ],
      calculate: (v) => {
        const mass = v.mass * 1000;
        const acceleration = v.thrust * 1000 / mass - G0;
        const brakingDistance = acceleration > 0 ? v.velocity ** 2 / (2 * acceleration) : Infinity;
        const gravityLoss = 0.35 * G0 * v.velocity / Math.max(acceleration, 0.5);
        const deltaV = v.velocity + gravityLoss;
        const propellant = mass * (1 - Math.exp(-deltaV / (v.isp * G0))) * (1 + v.reserve);
        const altitudeMargin = v.altitude * 1000 - brakingDistance;
        const lifecycleIndex = 100 / Math.sqrt(v.cadence) + (1 - v.reliability) * 1500;
        const brakingText = Number.isFinite(brakingDistance)
          ? `Brake distance ${(brakingDistance / 1000).toFixed(2)} km`
          : "Brake distance infeasible: thrust / weight <= 1";
        const marginText = Number.isFinite(altitudeMargin)
          ? `Altitude margin ${(altitudeMargin / 1000).toFixed(2)} km`
          : "Altitude margin unavailable";
        return {
          readouts: [`Net deceleration ${acceleration.toFixed(2)} m/s2`, brakingText, marginText, `Landing propellant ${(propellant / 1000).toFixed(1)} t`, `Lifecycle index ${lifecycleIndex.toFixed(1)}`],
          data: { acceleration, brakingDistance, altitudeMargin, propellant, lifecycleIndex },
        };
      },
    },
  };

  const config = CONFIGS[type] || CONFIGS.architecture;
  const state = Object.fromEntries(
    config.controls.map(([key, _label, _min, _max, _step, value]) => [key, value]),
  );

  function buildControls() {
    controlsHost.replaceChildren();
    config.controls.forEach(([key, label, min, max, step, value, unit]) => {
      const wrapper = document.createElement("label");
      const header = document.createElement("span");
      const labelText = document.createElement("b");
      const output = document.createElement("output");
      labelText.textContent = label;
      output.textContent = `${value} ${unit}`;
      header.append(labelText, output);
      const input = document.createElement("input");
      input.type = "range";
      input.min = String(min);
      input.max = String(max);
      input.step = String(step);
      input.value = String(value);
      input.dataset.key = key;
      input.addEventListener("input", () => {
        state[key] = Number.parseFloat(input.value);
        output.textContent = `${input.value} ${unit}`;
        render();
      });
      wrapper.append(header, input);
      controlsHost.append(wrapper);
    });
  }

  function background(title) {
    const gradient = context.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, COLORS.void);
    gradient.addColorStop(1, "#0a1d2b");
    context.fillStyle = gradient;
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.strokeStyle = COLORS.grid;
    context.lineWidth = 1;
    for (let x = 0; x <= canvas.width; x += 49) {
      context.beginPath(); context.moveTo(x, 0); context.lineTo(x, canvas.height); context.stroke();
    }
    for (let y = 0; y <= canvas.height; y += 40) {
      context.beginPath(); context.moveTo(0, y); context.lineTo(canvas.width, y); context.stroke();
    }
    context.fillStyle = COLORS.muted;
    context.font = "700 11px 'Cascadia Mono', monospace";
    context.fillText(`MODEL / ${title.toUpperCase()}`, 22, 29);
    context.fillStyle = COLORS.signal;
    context.fillText("SCREENING ANALYSIS / NOT FLIGHT CERTIFIED", canvas.width - 290, 29);
  }

  function line(x1, y1, x2, y2, color = COLORS.white, width = 2, dash = []) {
    context.save();
    context.strokeStyle = color;
    context.lineWidth = width;
    context.setLineDash(dash);
    context.beginPath();
    context.moveTo(x1, y1);
    context.lineTo(x2, y2);
    context.stroke();
    context.restore();
  }

  function arrow(x1, y1, x2, y2, color = COLORS.orange, label = "") {
    line(x1, y1, x2, y2, color, 4);
    const angle = Math.atan2(y2 - y1, x2 - x1);
    context.fillStyle = color;
    context.beginPath();
    context.moveTo(x2, y2);
    context.lineTo(x2 - 13 * Math.cos(angle - 0.5), y2 - 13 * Math.sin(angle - 0.5));
    context.lineTo(x2 - 13 * Math.cos(angle + 0.5), y2 - 13 * Math.sin(angle + 0.5));
    context.fill();
    if (label) {
      context.font = "700 12px 'Cascadia Mono', monospace";
      context.fillText(label, x2 + 8, y2 - 8);
    }
  }

  function bar(x, y, width, height, fraction, color, label) {
    context.fillStyle = "rgba(255,255,255,.055)";
    context.fillRect(x, y, width, height);
    context.fillStyle = color;
    context.fillRect(x, y + height * (1 - clamp(fraction, 0, 1)), width, height * clamp(fraction, 0, 1));
    context.fillStyle = COLORS.white;
    context.font = "700 11px 'Cascadia Mono', monospace";
    context.textAlign = "center";
    context.fillText(label, x + width / 2, y + height + 23);
    context.textAlign = "left";
  }

  function plot(points, bounds, color, width = 3) {
    if (!points.length) return;
    const { x, y, width: w, height: h, xMax, yMax } = bounds;
    context.strokeStyle = color;
    context.lineWidth = width;
    context.beginPath();
    points.forEach((point, index) => {
      const px = x + clamp(point[0] / Math.max(xMax, 1), 0, 1) * w;
      const py = y + h - clamp(point[1] / Math.max(yMax, 1), 0, 1) * h;
      if (index === 0) context.moveTo(px, py);
      else context.lineTo(px, py);
    });
    context.stroke();
  }

  function rocket(x, y, scale = 1, color = COLORS.white) {
    context.save();
    context.translate(x, y);
    context.scale(scale, scale);
    context.fillStyle = color;
    context.beginPath();
    context.moveTo(0, -75);
    context.quadraticCurveTo(28, -42, 23, 35);
    context.lineTo(14, 63);
    context.lineTo(-14, 63);
    context.lineTo(-23, 35);
    context.quadraticCurveTo(-28, -42, 0, -75);
    context.fill();
    context.fillStyle = COLORS.deep;
    context.beginPath();
    context.arc(0, -25, 8, 0, Math.PI * 2);
    context.fill();
    context.fillStyle = COLORS.orange;
    context.beginPath();
    context.moveTo(-11, 64); context.lineTo(0, 92); context.lineTo(11, 64); context.fill();
    context.restore();
  }

  function drawArchitecture(data) {
    const cx = 450;
    const cy = 285;
    const radius = 175;
    const metrics = [
      clamp(data.delivered / 40, 0, 1),
      clamp(1 - data.lifecycle / 200, 0, 1),
      clamp(data.robustness / 100, 0, 1),
      clamp(state.reliability, 0, 1),
      clamp(1 - state.uncertainty, 0, 1),
    ];
    for (let ring = 1; ring <= 4; ring += 1) {
      context.strokeStyle = COLORS.grid;
      context.beginPath();
      for (let i = 0; i < 5; i += 1) {
        const angle = -Math.PI / 2 + i * Math.PI * 2 / 5;
        const x = cx + radius * ring / 4 * Math.cos(angle);
        const y = cy + radius * ring / 4 * Math.sin(angle);
        if (i === 0) context.moveTo(x, y); else context.lineTo(x, y);
      }
      context.closePath();
      context.stroke();
    }
    context.fillStyle = "rgba(255,96,56,.26)";
    context.strokeStyle = COLORS.orange;
    context.lineWidth = 3;
    context.beginPath();
    metrics.forEach((metric, i) => {
      const angle = -Math.PI / 2 + i * Math.PI * 2 / 5;
      const x = cx + radius * metric * Math.cos(angle);
      const y = cy + radius * metric * Math.sin(angle);
      if (i === 0) context.moveTo(x, y); else context.lineTo(x, y);
    });
    context.closePath(); context.fill(); context.stroke();
    ["DELIVERY", "LIFECYCLE", "ROBUST", "RELIABLE", "CERTAINTY"].forEach((label, i) => {
      const angle = -Math.PI / 2 + i * Math.PI * 2 / 5;
      context.fillStyle = COLORS.muted;
      context.font = "700 10px 'Cascadia Mono', monospace";
      context.textAlign = "center";
      context.fillText(label, cx + (radius + 34) * Math.cos(angle), cy + (radius + 24) * Math.sin(angle));
    });
    context.textAlign = "left";
  }

  function drawStaging(data) {
    rocket(250, 300, 1.25);
    line(175, 325, 325, 325, COLORS.orange, 2, [7, 6]);
    context.fillStyle = COLORS.orange;
    context.font = "700 11px 'Cascadia Mono', monospace";
    context.fillText("STAGING INTERFACE", 174, 348);
    const total = data.dv1 + data.dv2;
    bar(520, 110, 95, 300, data.dv1 / total, COLORS.orange, "STAGE 1 DV");
    bar(650, 110, 95, 300, data.dv2 / total, COLORS.cyan, "STAGE 2 DV");
    bar(780, 110, 95, 300, data.payload / 10, COLORS.signal, "PAYLOAD %");
  }

  function drawOrbit(data) {
    const cx = 480;
    const cy = 290;
    const earthRadius = 62;
    const orbitA = 285;
    const orbitB = orbitA * Math.sqrt(1 - data.e ** 2);
    const gradient = context.createRadialGradient(cx - 18, cy - 18, 5, cx, cy, earthRadius);
    gradient.addColorStop(0, "#b7fff2"); gradient.addColorStop(.42, "#2f92a6"); gradient.addColorStop(1, "#05111b");
    context.fillStyle = gradient;
    context.beginPath(); context.arc(cx, cy, earthRadius, 0, Math.PI * 2); context.fill();
    context.strokeStyle = COLORS.orange; context.lineWidth = 3;
    context.beginPath(); context.ellipse(cx + orbitA * data.e * .45, cy, orbitA, orbitB * .55, -.15, 0, Math.PI * 2); context.stroke();
    context.strokeStyle = "rgba(121,217,232,.3)"; context.setLineDash([8, 8]);
    context.beginPath(); context.ellipse(cx, cy, orbitA * .88, orbitB * .68, .25, 0, Math.PI * 2); context.stroke(); context.setLineDash([]);
    context.fillStyle = COLORS.signal; context.beginPath(); context.arc(cx + orbitA, cy - 35, 8, 0, Math.PI * 2); context.fill();
    arrow(cx + 210, cy - 110, cx + 300, cy - 150, COLORS.cyan, "v");
  }

  function drawAscent(data) {
    const trajectory = data.trajectory;
    const maxX = Math.max(...trajectory.map((item) => item.x), 1);
    const maxH = Math.max(...trajectory.map((item) => item.h), 1);
    plot(trajectory.map((item) => [item.x, item.h]), { x: 70, y: 75, width: 560, height: 390, xMax: maxX, yMax: maxH }, COLORS.orange, 4);
    line(70, 465, 630, 465, COLORS.muted, 1);
    line(70, 75, 70, 465, COLORS.muted, 1);
    const qMax = Math.max(...trajectory.map((item) => item.q), 1);
    plot(trajectory.map((item) => [item.time, item.q]), { x: 700, y: 100, width: 220, height: 130, xMax: 190, yMax: qMax }, COLORS.cyan, 3);
    const heatMax = Math.max(...trajectory.map((item) => item.heat), 1);
    plot(trajectory.map((item) => [item.time, item.heat]), { x: 700, y: 315, width: 220, height: 130, xMax: 190, yMax: heatMax }, COLORS.red, 3);
    context.fillStyle = COLORS.muted; context.font = "700 10px 'Cascadia Mono', monospace";
    context.fillText("ASCENT TRAJECTORY", 70, 495); context.fillText("DYNAMIC PRESSURE", 700, 88); context.fillText("HEATING PROXY", 700, 303);
  }

  function drawNozzle(data) {
    context.fillStyle = "#263b47";
    context.fillRect(90, 190, 200, 180);
    context.fillStyle = COLORS.orange;
    context.beginPath();
    context.moveTo(290, 215); context.lineTo(405, 255); context.lineTo(780, 100);
    context.lineTo(780, 460); context.lineTo(405, 305); context.lineTo(290, 345); context.closePath(); context.fill();
    context.fillStyle = COLORS.void;
    context.beginPath();
    context.moveTo(110, 215); context.lineTo(285, 215); context.lineTo(405, 263); context.lineTo(760, 130);
    context.lineTo(760, 430); context.lineTo(405, 297); context.lineTo(285, 345); context.lineTo(110, 345); context.closePath(); context.fill();
    for (let i = 0; i < 8; i += 1) {
      arrow(420 + i * 38, 280, 455 + i * 43, 280, i < 3 ? COLORS.amber : COLORS.cyan);
    }
    line(405, 90, 405, 470, COLORS.signal, 2, [7, 7]);
    context.fillStyle = COLORS.signal; context.font = "700 10px 'Cascadia Mono', monospace";
    context.fillText("CHOKED THROAT / M = 1", 324, 82);
    context.fillText(`EXIT M ${data.mach.toFixed(2)} / AR ${data.areaRatio.toFixed(0)}`, 650, 495);
  }

  function drawCycle(data) {
    const nodes = [
      [140, 280, "TANK", COLORS.cyan],
      [340, 160, "PUMP", COLORS.orange],
      [560, 160, "CHAMBER", COLORS.red],
      [560, 390, "TURBINE", COLORS.amber],
      [800, 280, "NOZZLE", COLORS.signal],
    ];
    [[0,1],[1,2],[2,4],[2,3],[3,1]].forEach(([a,b]) => arrow(nodes[a][0],nodes[a][1],nodes[b][0],nodes[b][1],COLORS.muted));
    nodes.forEach(([x,y,label,color]) => {
      context.fillStyle = color; context.fillRect(x - 55, y - 30, 110, 60);
      context.fillStyle = COLORS.void; context.font = "800 11px 'Cascadia Mono', monospace"; context.textAlign = "center"; context.fillText(label, x, y + 4);
    });
    context.textAlign = "left";
    const fraction = clamp(data.balance / 1.4, 0, 1);
    context.fillStyle = "rgba(255,255,255,.08)"; context.fillRect(300, 500, 380, 13);
    context.fillStyle = data.balance >= 1 ? COLORS.signal : COLORS.red; context.fillRect(300, 500, 380 * fraction, 13);
  }

  function drawPropulsion(data) {
    const ratios = [
      clamp(data.thrust / 500, 0, 1),
      clamp(data.deltaV / 20_000, 0, 1),
      clamp(1 - data.specificMass / 10, 0, 1),
      clamp(1 - data.propellant / (state.initialMass * 1000), 0, 1),
    ];
    ["THRUST", "DELTA-V", "POWER MASS", "MASS LEFT"].forEach((label, index) => {
      bar(150 + index * 175, 120, 90, 300, ratios[index], [COLORS.orange,COLORS.cyan,COLORS.signal,COLORS.amber][index], label);
    });
    arrow(90, 485, 875, 485, COLORS.muted, "MISSION TIMESCALE");
  }

  function drawAero(data) {
    rocket(450, 290, 1.45);
    for (let i = -3; i <= 3; i += 1) {
      const y = 180 + (i + 3) * 38;
      arrow(75, y, 330 + Math.abs(i) * 12, y, i === 0 ? COLORS.orange : COLORS.cyan);
    }
    const bend = clamp(Math.abs(data.bending) / 25e6, 0, 1);
    context.strokeStyle = data.margin < 0 ? COLORS.red : COLORS.signal;
    context.lineWidth = 6;
    context.beginPath();
    context.moveTo(585, 420);
    context.bezierCurveTo(650, 360 - bend * 80, 725, 220 + bend * 55, 825, 145);
    context.stroke();
    context.fillStyle = COLORS.muted; context.font = "700 10px 'Cascadia Mono', monospace";
    context.fillText(`BENDING RESPONSE / MS ${data.margin.toFixed(2)}`, 640, 455);
  }

  function drawThermal(data) {
    context.fillStyle = "rgba(255,96,56,.16)";
    context.beginPath(); context.arc(480, 290, 220, Math.PI * .72, Math.PI * 1.28); context.lineTo(480, 290); context.fill();
    context.fillStyle = COLORS.orange; context.beginPath(); context.arc(480, 290, 132, Math.PI * .68, Math.PI * 1.32); context.fill();
    context.fillStyle = COLORS.deep; context.beginPath(); context.arc(510, 290, 126, Math.PI * .68, Math.PI * 1.32); context.fill();
    context.strokeStyle = COLORS.signal; context.lineWidth = 12;
    context.beginPath(); context.arc(510, 290, 105, Math.PI * .68, Math.PI * 1.32); context.stroke();
    for (let i = -3; i <= 3; i += 1) arrow(70, 290 + i * 42, 250, 290 + i * 28, i === 0 ? COLORS.red : COLORS.orange);
    const temperature = clamp((data.bondline - 293) / 1000, 0, 1);
    bar(760, 130, 85, 300, temperature, data.bondline > 650 ? COLORS.red : COLORS.signal, "BONDLINE T");
  }

  function drawStructure(data) {
    context.strokeStyle = COLORS.cyan; context.lineWidth = 16;
    context.beginPath(); context.ellipse(430, 290, 210, 145, 0, 0, Math.PI * 2); context.stroke();
    context.strokeStyle = COLORS.signal; context.lineWidth = 5;
    context.beginPath(); context.ellipse(430, 290, 170, 112, 0, 0, Math.PI * 2); context.stroke();
    for (let i = 0; i < 8; i += 1) {
      const angle = i * Math.PI / 4;
      arrow(430 + 100 * Math.cos(angle), 290 + 70 * Math.sin(angle), 430 + 230 * Math.cos(angle), 290 + 160 * Math.sin(angle), COLORS.orange);
    }
    bar(760, 120, 90, 300, clamp(data.hoop / (state.yield * 1e6), 0, 1), data.margin < 0 ? COLORS.red : COLORS.signal, "STRESS / ALLOW");
  }

  function drawGnc(data) {
    const targetX = 800;
    const targetY = 175;
    line(90, 445, targetX, targetY, COLORS.muted, 2, [8, 7]);
    const error = clamp(data.residual / 5, 0, 1);
    context.strokeStyle = COLORS.orange; context.lineWidth = 4;
    context.beginPath();
    context.moveTo(90, 445);
    context.bezierCurveTo(280, 300 + error * 100, 550, 150 - error * 80, targetX - error * 95, targetY + error * 55);
    context.stroke();
    rocket(500, 260, .65);
    context.strokeStyle = data.phaseMargin < 30 ? COLORS.red : COLORS.signal; context.lineWidth = 3;
    context.beginPath(); context.ellipse(targetX, targetY, 45 + data.covariance * 30, 24 + data.covariance * 18, -.35, 0, Math.PI * 2); context.stroke();
    context.fillStyle = COLORS.signal; context.fillRect(targetX - 5, targetY - 5, 10, 10);
    context.fillStyle = COLORS.muted; context.font = "700 10px 'Cascadia Mono', monospace";
    context.fillText(`PHASE MARGIN ${data.phaseMargin.toFixed(1)} DEG`, 700, 475);
  }

  function drawReliability(data) {
    const y = 250;
    const count = Math.min(8, Math.round(state.seriesCount / 4));
    for (let i = 0; i < count; i += 1) {
      const x = 90 + i * 100;
      context.fillStyle = i === count - 1 && data.mission < .99 ? COLORS.red : COLORS.cyan;
      context.fillRect(x, y - 30, 70, 60);
      if (i < count - 1) arrow(x + 70, y, x + 98, y, COLORS.muted);
      context.fillStyle = COLORS.void; context.font = "800 9px 'Cascadia Mono', monospace"; context.fillText(`F${i + 1}`, x + 25, y + 4);
    }
    arrow(430, 160, 430, 215, COLORS.orange, "COMMON CAUSE");
    bar(760, 120, 90, 300, data.mission, data.mission > .99 ? COLORS.signal : COLORS.orange, "MISSION R");
  }

  function drawTest(data) {
    const points = [];
    for (let index = 0; index <= 180; index += 1) {
      const time = index / 180;
      const signal = .5 + .24 * Math.sin(time * 16 * Math.PI) + .08 * Math.sin(time * 52 * Math.PI);
      points.push([time, signal]);
    }
    plot(points, { x: 70, y: 90, width: 580, height: 260, xMax: 1, yMax: 1 }, data.nyquistMargin < 1 ? COLORS.red : COLORS.cyan, 3);
    line(70, 350, 650, 350, COLORS.muted, 1);
    context.fillStyle = COLORS.muted; context.font = "700 10px 'Cascadia Mono', monospace";
    context.fillText("MEASURED TRANSIENT / BAND-LIMITED VIEW", 70, 380);
    const risk = clamp(-Math.log10(Math.max(data.expectedCasualties, 1e-12)) / 10, 0, 1);
    bar(770, 100, 90, 300, risk, data.expectedCasualties < 1e-6 ? COLORS.signal : COLORS.red, "RISK HEADROOM");
  }

  function drawLanding(data) {
    line(80, 455, 900, 455, COLORS.muted, 2);
    rocket(500, 260, 1.05);
    arrow(500, 360, 500, 440, COLORS.orange, "THRUST");
    arrow(500, 150, 500, 235, COLORS.cyan, "VELOCITY");
    const distanceFraction = clamp(data.brakingDistance / Math.max(state.altitude * 1000, 1), 0, 1.4);
    context.strokeStyle = data.altitudeMargin < 0 ? COLORS.red : COLORS.signal;
    context.lineWidth = 4;
    context.setLineDash([9, 7]);
    context.beginPath(); context.ellipse(500, 455, 130 + distanceFraction * 90, 25 + distanceFraction * 25, 0, Math.PI, Math.PI * 2); context.stroke();
    context.setLineDash([]);
    bar(760, 120, 90, 280, clamp(data.propellant / (state.mass * 1000), 0, 1), COLORS.orange, "PROP FRACTION");
  }

  const DRAWERS = {
    architecture: drawArchitecture,
    staging: drawStaging,
    orbit: drawOrbit,
    ascent: drawAscent,
    nozzle: drawNozzle,
    cycle: drawCycle,
    propulsion: drawPropulsion,
    aero: drawAero,
    thermal: drawThermal,
    structure: drawStructure,
    gnc: drawGnc,
    reliability: drawReliability,
    test: drawTest,
    landing: drawLanding,
  };

  function render() {
    const result = config.calculate(state);
    readoutsHost.innerHTML = result.readouts.map((item) => `<span>${item}</span>`).join("");
    background(type);
    (DRAWERS[type] || drawArchitecture)(result.data);
    canvas.dataset.rendered = "true";
  }

  resetButton.addEventListener("click", () => {
    config.controls.forEach(([key, _label, _min, _max, _step, value]) => {
      state[key] = value;
    });
    buildControls();
    render();
  });

  buildControls();
  render();
})();
