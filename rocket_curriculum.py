"""Graduate-to-research rocketry curriculum and seminar generator."""

from rocket_sources import source_list


def equation(name, expression, meaning, validity):
    return {
        "name": name,
        "expression": expression,
        "meaning": meaning,
        "validity": validity,
    }


def seminar(title, question, method, case, frontier, failure):
    return {
        "title": title,
        "question": question,
        "method": method,
        "case": case,
        "frontier": frontier,
        "failure": failure,
    }


def module(
    number,
    slug,
    title,
    domain,
    summary,
    outcomes,
    equations,
    seminars,
    research_questions,
    lab,
    sources,
):
    return {
        "number": number,
        "slug": slug,
        "title": title,
        "domain": domain,
        "summary": summary,
        "outcomes": outcomes,
        "equations": equations,
        "seminar_specs": seminars,
        "research_questions": research_questions,
        "lab": lab,
        "source_keys": sources,
    }


MODULES = [
    module(
        1,
        "mission-architecture-and-systems-engineering",
        "Mission Architecture and Systems Engineering",
        "The mission is the system",
        "Translate an exploration objective into measures of effectiveness, architecture trades, requirements, interfaces, verification evidence, and decision gates.",
        [
            "Build a traceable objective-to-requirement hierarchy without confusing a design choice for a requirement.",
            "Formulate architecture trades with cost, schedule, performance, safety, and uncertainty on commensurate scales.",
            "Separate verification from validation and connect each requirement to credible evidence.",
            "Audit technical decisions for hidden coupling, irreversibility, and organizational risk.",
        ],
        [
            equation("Value model", "J(x) = sum(w_i u_i(x)) - lambda R(x)", "Combines stakeholder utility with an explicit risk penalty.", "Weights and utility functions must be elicited, normalized, and sensitivity-tested."),
            equation("Mass margin", "M_margin = (M_limit - M_current) / M_current", "Tracks design maturity against an allocated mass limit.", "Margin policy depends on project phase and uncertainty classification."),
            equation("Reliability allocation", "R_system = product(R_i) for independent series elements", "Shows how serial critical functions compound unreliability.", "Independence is a modeling assumption that must be challenged for common-cause failures."),
            equation("Decision robustness", "rho = min_theta [J(x*,theta) - J(x_alt,theta)]", "Measures whether a preferred architecture survives uncertain futures.", "Only meaningful over a defensible uncertainty set theta."),
        ],
        [
            seminar("From Purpose to Verifiable Mission Need", "How can a broad ambition such as lunar cargo delivery become a falsifiable mission need?", "Construct stakeholder needs, measures of effectiveness, operational scenarios, and success thresholds before proposing hardware.", "Decompose a notional 5,000 kg lunar-surface cargo objective into delivered mass, landing ellipse, cadence, reliability, and lifecycle constraints.", "Digital mission threads increasingly join requirements, models, test evidence, and operations data.", "Writing a preferred vehicle configuration into the mission need and suppressing alternatives."),
            seminar("Architecture Enumeration and Trade Space", "What is a defensible way to compare direct ascent, staging, depots, and reusable elements?", "Use morphological matrices, constraints, Pareto dominance, utility theory, and global sensitivity rather than a single weighted score.", "Compare expendable direct delivery with a reusable cislunar tug under uncertain launch price and propellant transfer reliability.", "Set-based design and model-based systems engineering can defer premature point-design commitment.", "Reporting a crisp winner while the result reverses under plausible weights."),
            seminar("Requirements, Interfaces, and Closure", "How do requirements remain necessary, sufficient, feasible, and verifiable as the design evolves?", "Derive requirements from scenarios, assign owners, define interfaces, and maintain bidirectional traceability to verification methods.", "Close a propulsion-to-structure interface for thrust, gimbal envelope, thermal soakback, plumbing loads, and fault response.", "Machine-readable requirements and executable interface contracts can expose inconsistencies earlier.", "Treating interface control documents as static paperwork rather than active technical models."),
            seminar("Margins, Reserves, and Technical Performance", "How should mass, power, data, thermal, and delta-v margin change with design maturity?", "Distinguish uncertainty, growth allowance, reserve, and contingency; aggregate correlated contributors with Monte Carlo analysis.", "Build a mass properties ledger whose stage-level margins reconcile to vehicle center-of-mass and performance models.", "Probabilistic technical-performance measures can replace disconnected deterministic margin tables.", "Adding margin independently to every subsystem and then double-counting it at system level."),
            seminar("Verification, Validation, and Evidence", "What evidence demonstrates that the product was built right and that the right product was built?", "Map each requirement to analysis, inspection, demonstration, or test; then validate end-to-end mission scenarios with stakeholders.", "Create a verification cross-reference matrix for an autonomous upper stage including off-nominal modes.", "Continuous assurance cases can link claims, evidence, model pedigree, and unresolved risk.", "Using successful component tests as proof that integrated mission behavior is valid."),
            seminar("Technical Authority and Decision Integrity", "Why do technically correct local decisions still produce unsafe systems?", "Examine dissent channels, independent review, risk acceptance, schedule pressure, and the distinction between programmatic and technical authority.", "Reconstruct a launch-commit decision from sensor evidence, model uncertainty, consequence, and decision rights.", "Structured argumentation and counterfactual review can make organizational assumptions inspectable.", "Converting absence of evidence into evidence of safety."),
        ],
        [
            "When does added architectural flexibility justify its interface and operations burden?",
            "How should uncertainty correlations be represented before component data exist?",
            "Which technical decisions are reversible, and what option value does reversibility create?",
            "How can an assurance case remain synchronized with continuously changing models and tests?",
        ],
        {"type": "architecture", "title": "Architecture Trade Observatory", "description": "Explore mass, reliability, reuse, schedule, and uncertainty across competing lunar cargo architectures."},
        ["seh", "caib", "faa450"],
    ),
    module(
        2,
        "variable-mass-flight-and-staging",
        "Variable-Mass Flight and Staging",
        "Performance emerges from coupled mass flow",
        "Derive variable-mass dynamics, finite-burn losses, staging optima, reserves, and sensitivity without treating the ideal rocket equation as a complete launch model.",
        [
            "Derive the rocket equation from a control-volume momentum balance with explicit sign conventions.",
            "Quantify gravity, drag, steering, residual, and finite-burn losses.",
            "Optimize multistage mass distribution subject to structural and engine constraints.",
            "Propagate performance uncertainty into payload capability and mission reserve.",
        ],
        [
            equation("Tsiolkovsky", "Delta-v = Isp g0 ln(m0 / mf)", "Relates ideal velocity increment to effective exhaust velocity and mass ratio.", "Assumes constant effective exhaust velocity and excludes external-force losses."),
            equation("Variable-mass acceleration", "m dv/dt = T - D - m g_parallel", "Powered-flight force balance along the velocity direction.", "Requires consistent inertial frame, sign convention, and thrust definition."),
            equation("Staging velocity", "Delta-v_total = sum(c_i ln(m0_i / mf_i))", "Adds ideal stage velocity increments at staging events.", "Ignores staging impulse, coast losses, and engine transients unless separately modeled."),
            equation("Payload sensitivity", "d m_payload / d Delta-v_req", "Measures how small mission-demand changes alter deliverable payload.", "Must be evaluated on the closed mass model, not an isolated stage."),
        ],
        [
            seminar("Control-Volume Derivation", "Where does the logarithm in the rocket equation come from?", "Apply momentum conservation to a translating control volume, retain pressure thrust, and integrate with changing mass.", "Derive ideal delta-v for a stage while distinguishing dry mass, residual propellant, payload, and jettisoned hardware.", "Variable exhaust velocity and throttling turn the analytic integral into an optimal-control problem.", "Using F = ma with constant mass and adding propellant flow as an afterthought."),
            seminar("Loss Taxonomy and Ascent Bookkeeping", "How much ideal performance disappears into gravity, drag, steering, backpressure, and transients?", "Integrate each loss along a simulated trajectory and avoid assigning coupled effects to arbitrary buckets.", "Compare short high-thrust and long low-thrust ascent profiles with the same ideal stage delta-v.", "Adjoint sensitivity can identify which trajectory intervals dominate performance loss.", "Applying a fixed textbook loss allowance outside the vehicle and trajectory class from which it came."),
            seminar("Optimal Staging", "How should total ideal delta-v be distributed across stages with different exhaust velocity and inert fraction?", "Formulate payload fraction maximization with Lagrange multipliers and then add thrust-to-weight and geometry constraints.", "Optimize a two-stage LOX/RP-1 plus LOX/LH2 launcher for a fixed orbital insertion condition.", "Mixed-integer optimization can select stage count, engine count, and recovery mode together.", "Optimizing delta-v split while holding structural fractions independent of tank size and engine count."),
            seminar("Residuals, Reserves, and Unusable Propellant", "Why is loaded propellant not equal to usable impulse?", "Model trapped volume, settling, mixture-ratio bias, shutdown dispersions, chilldown, and mission reserve as distinct quantities.", "Close an upper-stage propellant budget through restart, coast, and disposal requirements.", "Autonomous propellant gauging and covariance-aware reserve policies can recover payload.", "Treating all residual propellant as statistical margin available to every contingency."),
            seminar("Finite Burns and Oberth Coupling", "When does burn duration change orbital outcome even if delivered impulse is constant?", "Integrate thrust through the rotating local orbital frame and compare impulsive and finite-burn state transitions.", "Analyze a high-thrust and low-thrust perigee burn with equal integrated delta-v.", "Hybrid impulsive-continuous optimization is central to chemical-electric mission architectures.", "Applying an impulsive burn at its midpoint without checking gravity and direction losses."),
            seminar("Performance Uncertainty and Payload Risk", "How should Isp, dry mass, mixture ratio, atmosphere, and guidance dispersions map into payload confidence?", "Use correlated Monte Carlo sampling, response surfaces, and percentile payload metrics.", "Estimate P95 delivered mass for a vehicle with common dry-mass growth drivers across both stages.", "Polynomial chaos and multifidelity surrogates can reduce expensive high-fidelity campaign cost.", "Varying one uncertain input at a time and summing worst cases that cannot occur together."),
        ],
        [
            "How does engine-out capability alter the optimal number and placement of engines?",
            "When is an additional stage worth its separation and reliability penalty?",
            "How should performance reserve be allocated across coupled ascent and on-orbit phases?",
            "Can adaptive guidance safely monetize favorable real-time propulsion performance?",
        ],
        {"type": "staging", "title": "Multistage Performance Workbench", "description": "Vary specific impulse, inert fraction, staging split, reserve, and loss terms to expose payload sensitivity."},
        ["rocket_equation", "thrust", "sp125"],
    ),
    module(
        3,
        "orbital-mechanics-and-perturbations",
        "Orbital Mechanics and Perturbations",
        "State evolves in modeled gravity",
        "Move from two-body conics to high-fidelity propagation, coordinate and time conventions, perturbations, covariance, cislunar dynamics, and operationally meaningful orbit design.",
        [
            "Transform between Cartesian states, orbital elements, frames, and time systems without convention ambiguity.",
            "Derive and use variational equations and state transition matrices.",
            "Select perturbation fidelity appropriate to mission phase and decision risk.",
            "Analyze cislunar and libration-region trajectories beyond patched conics.",
        ],
        [
            equation("Two-body dynamics", "r_ddot = -mu r / |r|^3", "Defines ideal point-mass central gravity.", "Valid when other bodies, nonspherical gravity, drag, and radiation pressure are negligible."),
            equation("Specific orbital energy", "epsilon = v^2/2 - mu/r = -mu/(2a)", "Connects state magnitude to conic semimajor axis.", "Two-body osculating interpretation; perturbations cause element evolution."),
            equation("State transition", "delta-x(t) = Phi(t,t0) delta-x(t0)", "Propagates first-order state perturbations and covariance.", "Linearization is local and must be monitored over long or chaotic arcs."),
            equation("CR3BP integral", "C = 2U(x,y,z) - |v|^2", "Jacobi constant constrains accessible regions in the circular restricted three-body problem.", "Applies only within the rotating-frame CR3BP assumptions."),
        ],
        [
            seminar("State, Elements, Frames, and Time", "Why can two correct orbit states disagree numerically?", "Define inertial and rotating frames, epochs, time scales, central bodies, and element singularities before conversion.", "Convert a cislunar state between Earth-centered inertial, Earth-Moon rotating, and local orbital frames.", "Standardized conventions are essential for multi-agency cislunar navigation interoperability.", "Publishing position and velocity without a frame, epoch, time scale, or units."),
            seminar("Two-Body Geometry and Maneuvers", "How do energy and angular momentum organize conic motion?", "Derive conic invariants, apsides, time of flight, plane changes, and combined impulsive maneuvers.", "Compare Hohmann, bi-elliptic, and constrained plane-change transfers for a high-altitude target.", "Primer-vector theory generalizes local maneuver optimality beyond named transfers.", "Optimizing delta-v while ignoring transfer time, eclipse, communications, or collision constraints."),
            seminar("Perturbations and Fidelity Selection", "Which neglected forces can reverse a mission decision?", "Model nonspherical gravity, third bodies, drag, solar radiation pressure, tides, and relativistic terms by scale.", "Build a force-model ladder for LEO deployment, translunar coast, and NRHO operations.", "Automated fidelity management can focus computational effort where sensitivities are largest.", "Calling the highest-fidelity model the most credible without validating its inputs."),
            seminar("Variational Dynamics and Covariance", "How does uncertainty stretch, rotate, and couple under nonlinear dynamics?", "Integrate variational equations, state transition matrices, process noise, and covariance in consistent coordinates.", "Propagate launch injection covariance to a lunar targeting correction and compare linear and Monte Carlo results.", "Non-Gaussian uncertainty transport is increasingly important near resonances and close approaches.", "Interpreting a covariance ellipsoid as a hard boundary containing all possible states."),
            seminar("Cislunar Three-Body Dynamics", "Why do libration-point families not behave like Keplerian ellipses?", "Use the circular restricted three-body problem, manifolds, periodic orbits, differential correction, and continuation.", "Generate a near-rectilinear halo-orbit seed and inspect stable and unstable directions.", "Ephemeris transition and low-energy manifold design remain active mission-design research areas.", "Treating a CR3BP periodic orbit as an exact ephemeris trajectory requiring no stationkeeping."),
            seminar("Orbit Determination and Operational Design", "How should trajectory design interact with measurement geometry and navigation performance?", "Join dynamics, measurement partials, filtering, maneuver execution error, and contact schedules.", "Design a tracking arc and correction sequence that meets a lunar flyby B-plane requirement.", "Autonomous optical navigation can shift architecture trades in deep-space operations.", "Designing a mathematically reachable trajectory that cannot be navigated or reconstructed."),
        ],
        [
            "How should model-form uncertainty enter cislunar covariance?",
            "Which coordinate representations best preserve uncertainty geometry near libration orbits?",
            "When should a mission transition from analytic seeds to ephemeris optimization?",
            "How can onboard autonomy exploit invariant structures without losing certifiability?",
        ],
        {"type": "orbit", "title": "Perturbed Orbit Laboratory", "description": "Propagate a planar orbit while varying J2, drag, third-body forcing, and integration step."},
        ["trajectory", "trajectory_method", "cislunar", "copernicus"],
    ),
    module(
        4,
        "ascent-trajectory-optimization",
        "Ascent Trajectory Optimization",
        "Fly through constraints, not around them",
        "Formulate ascent as a constrained optimal-control problem coupling atmosphere, propulsion, aerodynamics, staging, path limits, dispersions, and guidance implementability.",
        [
            "Write ascent equations of motion and path constraints in an appropriate state representation.",
            "Distinguish direct, indirect, shooting, collocation, and pseudospectral optimization methods.",
            "Interpret costates, active constraints, and sensitivities rather than accepting a solver trace.",
            "Convert an open-loop optimum into robust onboard guidance.",
        ],
        [
            equation("Translational dynamics", "r_dot = v; v_dot = T/m u_T + g(r) + a_aero", "Propagates position and velocity under thrust, gravity, and aerodynamic acceleration.", "Requires atmosphere, force, attitude, and mass models consistent with the optimization state."),
            equation("Dynamic pressure", "q = 0.5 rho V_rel^2", "Provides a primary ascent structural and aerodynamic path metric.", "Density and air-relative velocity must include atmosphere and winds."),
            equation("Heating proxy", "q_dot_conv proportional to sqrt(rho/R_n) V^3", "Captures strong velocity sensitivity of stagnation heating.", "A correlation for preliminary screening, not a substitute for validated aerothermodynamics."),
            equation("Optimal control", "min J = Phi(x_f) + integral L(x,u,t) dt", "Defines terminal and running objectives subject to dynamics and constraints.", "The chosen objective and constraints encode the mission decision; solver convergence is not physical validity."),
        ],
        [
            seminar("Ascent Dynamics and Coordinates", "Which state and independent variable produce a numerically stable ascent model?", "Derive 3-DOF and 6-DOF equations in inertial, rotating, and local frames with Earth rotation and winds.", "Compare time, energy, and normalized path length as independent variables for orbital ascent.", "Lie-group state representations can improve attitude propagation and optimization consistency.", "Mixing inertial velocity with atmosphere-relative aerodynamic forces."),
            seminar("Optimal-Control Formulation", "How does payload maximization become a constrained boundary-value problem?", "Define states, controls, phases, linkage conditions, terminal orbit constraints, and path inequalities.", "Formulate a two-stage ascent with throttle, angle of attack, q, axial acceleration, and heating constraints.", "Multiphase automatic differentiation enables larger integrated vehicle-trajectory design spaces.", "Optimizing an objective whose sign or terminal mass definition is inconsistent across stages."),
            seminar("Direct and Indirect Numerical Methods", "What does each optimization method reveal and hide?", "Compare costate shooting, direct collocation, pseudospectral transcription, mesh refinement, and scaling.", "Solve the same pitch program with shooting and collocation, then compare active constraints and residuals.", "Structure-exploiting sparse solvers and differentiable simulators are changing practical problem size.", "Trusting convergence status without independently evaluating defects and constraints."),
            seminar("Constraint Physics", "Why do max-q, bending load, heating, and acceleration constraints create nonintuitive steering?", "Relate path constraints to atmosphere, angle of attack, thrust, structural modes, and engine throttling.", "Interpret a throttle bucket that rides a q-alpha or bending-moment boundary.", "Online constraint adaptation may recover performance from measured winds while protecting loads.", "Constraining q alone when load depends on q times angle of attack and vehicle flexibility."),
            seminar("Robustness and Dispersions", "How does an optimal trajectory survive atmosphere, wind, engine, and navigation uncertainty?", "Use chance constraints, covariance steering, scenario optimization, and Monte Carlo verification.", "Compare nominal payload optimum with a design meeting a 99.7 percent structural-load probability target.", "Distributionally robust optimization can protect against uncertain uncertainty models.", "Adding independent three-sigma dispersions to create a physically impossible worst case."),
            seminar("From Optimum to Guidance Law", "How can an onboard algorithm approximate an offline optimum under real-time uncertainty?", "Derive reference guidance, predictor-corrector targeting, feedback gains, and update logic.", "Convert an optimized ascent into a guidance table and evaluate engine-out retargeting.", "Real-time successive convexification is moving sophisticated optimization onboard.", "Calling an open-loop trajectory a guidance algorithm."),
        ],
        [
            "How should structural flexibility enter ascent optimization before a final finite-element model exists?",
            "Can real-time wind estimation safely reduce load conservatism?",
            "Which uncertainty descriptions justify chance constraints?",
            "How should abort capability be co-optimized with nominal performance?",
        ],
        {"type": "ascent", "title": "Ascent Constraint Console", "description": "Vary thrust-to-weight, pitch schedule, atmosphere, and path limits while observing altitude, velocity, q, and heating."},
        ["trajectory", "trajectory_method", "copernicus", "gnc"],
    ),
    module(
        5,
        "combustion-thermochemistry-and-nozzles",
        "Combustion Thermochemistry and Nozzles",
        "Convert chemical potential into directed momentum",
        "Connect equilibrium and finite-rate chemistry to chamber state, choked flow, nozzle expansion, thrust coefficient, performance loss, stability, and altitude adaptation.",
        [
            "Formulate equilibrium-chemistry rocket performance and identify frozen versus shifting assumptions.",
            "Derive choked mass flow and isentropic nozzle relations.",
            "Separate momentum, pressure, kinetic, divergence, boundary-layer, and chemistry losses.",
            "Interpret combustion-instability mechanisms and validation evidence.",
        ],
        [
            equation("Rocket thrust", "F = m_dot V_e + (p_e - p_a) A_e", "Adds exhaust momentum and exit-plane pressure thrust.", "Steady one-dimensional control-volume form with representative exit-plane properties."),
            equation("Characteristic velocity", "c* = p_c A_t / m_dot", "Measures chamber and propellant performance largely independent of nozzle expansion.", "Depends on chamber state, throat definition, and measured mass flow."),
            equation("Thrust coefficient", "C_F = F / (p_c A_t)", "Captures nozzle expansion and ambient-pressure effects.", "Must state ambient condition and whether losses are included."),
            equation("Area-Mach relation", "A/A* = f(M,gamma)", "Links nozzle area ratio to isentropic Mach number.", "Calorically perfect, quasi-one-dimensional, isentropic gas approximation."),
        ],
        [
            seminar("Equilibrium Chemistry and Adiabatic Flame State", "How do propellant choice, mixture ratio, pressure, and dissociation set theoretical performance?", "Minimize Gibbs free energy or apply equilibrium constants, then enforce energy and element conservation.", "Compare LOX/LH2 and LOX/CH4 chamber products across mixture ratio using NASA CEA concepts.", "Reduced-order chemistry for optimization must preserve performance and thermal predictions.", "Using a single constant gamma and molecular weight across chamber and nozzle."),
            seminar("Choking and Characteristic Velocity", "Why does the throat set mass flow?", "Derive sonic choking from compressible conservation equations and connect c-star to chamber quality.", "Estimate throat area from chamber pressure, mass flow, and c-star efficiency.", "Real-gas, multiphase, and reacting throat flow challenge classical correlations.", "Treating c-star as an exhaust velocity or nozzle efficiency."),
            seminar("Nozzle Expansion and Altitude", "How does fixed geometry trade sea-level separation risk against vacuum performance?", "Use isentropic relations, pressure thrust, area ratio, and ambient pressure to map expansion.", "Compare sea-level, vacuum, and altitude-compensating nozzle performance for one chamber state.", "Aerospikes, dual-bell nozzles, and extendable nozzles target wider operating envelopes.", "Assuming p_e = p_a at every altitude because ideal expansion is desirable."),
            seminar("Real Nozzle Losses", "Where does theoretical impulse disappear inside a real nozzle?", "Quantify divergence, boundary-layer, two-phase, kinetic, chemistry, leakage, and erosion losses.", "Build a thrust-coefficient efficiency budget and identify which loss scales with chamber pressure.", "Additively manufactured channels and non-axisymmetric nozzles require richer loss models.", "Multiplying independently calibrated efficiency factors that already contain overlapping losses."),
            seminar("Heat Transfer and Regenerative Cooling", "How can a wall survive gas temperatures above its material limit?", "Couple gas-side convection, wall conduction, coolant heat pickup, pressure drop, and material stress.", "Size a methane regenerative channel at throat heat-flux peak and inspect boiling margin.", "Conjugate heat transfer, roughness evolution, and supercritical coolant behavior remain active research.", "Using average chamber heat flux to size the throat region."),
            seminar("Combustion Stability and Injector Coupling", "How do chamber acoustics couple to unsteady heat release and feed dynamics?", "Analyze acoustic modes, Rayleigh coupling, injector response, damping devices, and hot-fire evidence.", "Interpret a high-frequency pressure spectrum and distinguish instrumentation artifact from instability.", "High-fidelity reacting simulations are improving but still require carefully designed test validation.", "Calling any pressure oscillation combustion instability without modal and energy-coupling evidence."),
        ],
        [
            "How can uncertainty in chemical kinetics be mapped into design margin?",
            "Which altitude-compensation concepts remain compelling after mass and cooling penalties?",
            "How should additive-manufacturing roughness enter boundary-layer and heat-transfer predictions?",
            "Can instability risk be screened reliably before full-scale hot fire?",
        ],
        {"type": "nozzle", "title": "Nozzle and Chemistry Observatory", "description": "Explore chamber pressure, mixture ratio, area ratio, ambient pressure, and efficiency effects on thrust and specific impulse."},
        ["sp125", "thrust", "nozzle", "cea"],
    ),
    module(
        6,
        "liquid-engine-cycles-and-turbomachinery",
        "Liquid Engine Cycles and Turbomachinery",
        "Close every pressure, power, and thermal balance",
        "Analyze pressure-fed, gas-generator, staged-combustion, expander, and electric-pump cycles together with cavitation, turbopump maps, rotordynamics, controls, start transients, and health monitoring.",
        [
            "Close steady engine-cycle mass, species, pressure, power, and energy balances.",
            "Read pump and turbine maps with corrected variables, efficiency, and stability limits.",
            "Model ignition, chilldown, start, throttle, and shutdown as coupled transients.",
            "Design instrumentation and fault detection around physically observable failure precursors.",
        ],
        [
            equation("Pump power", "P_p = m_dot Delta-p / (rho eta_p)", "Relates pressure rise to hydraulic power and efficiency.", "Incompressible approximation with representative density and efficiency."),
            equation("Turbine power", "P_t = m_dot_t Delta-h_t eta_t", "Extracts shaft power from turbine enthalpy drop.", "Requires a consistent definition of isentropic versus actual enthalpy drop."),
            equation("Cavitation margin", "NPSH_available > NPSH_required", "Protects pump inlet from unacceptable vapor formation and performance loss.", "NPSH is test- and configuration-dependent and not a universal fluid property."),
            equation("Shaft dynamics", "I omega_dot = tau_t - tau_p - tau_loss", "Describes spool acceleration during start and transients.", "Lumped rotor model; flexible modes and fluid-structure coupling may dominate."),
        ],
        [
            seminar("Cycle Topology and Closure", "What is gained and lost by each liquid-engine cycle?", "Close mass, energy, species, pressure, shaft power, and cooling branches for major cycle families.", "Compare gas-generator, oxygen-rich staged combustion, and full-flow staged combustion for a methane engine.", "Integrated cycle and vehicle optimization can overturn engine-only efficiency rankings.", "Comparing cycles by specific impulse while ignoring mass, operability, development risk, and throttling."),
            seminar("Pumps, Cavitation, and Inducers", "How does a compact pump raise propellant pressure without destructive cavitation?", "Use Euler turbomachinery, velocity triangles, specific speed, suction performance, and inducer design.", "Map inlet pressure and flow coefficient against cavitation head breakdown during throttle.", "Cryogenic cavitation thermodynamics and unsteady blade loading remain difficult prediction problems.", "Treating vapor-pressure margin as sufficient evidence of stable pump operation."),
            seminar("Turbines and Power Balance", "How do turbine pressure ratio, temperature, flow, and efficiency close the shaft balance?", "Analyze velocity triangles, reaction, cooling, leakage, and map matching to pump torque.", "Close a two-shaft preburner-driven engine at nominal and deep-throttle points.", "Ceramic composites and additive cooling may expand turbine operating envelopes.", "Balancing nominal powers while ignoring transient rotor acceleration and accessory loads."),
            seminar("Rotordynamics, Seals, and Bearings", "Which coupled modes threaten high-speed turbomachinery?", "Build critical-speed maps and consider cross-coupled seal forces, bearing stiffness, damping, imbalance, and thermal growth.", "Assess whether a spool crosses a critical speed during start and with what dwell time.", "Active magnetic bearings and model-based monitoring create new control-certification questions.", "Using a rigid-rotor balance calculation as proof of rotordynamic stability."),
            seminar("Start, Shutdown, and Throttle Transients", "Why are engine transients often more hazardous than steady operation?", "Model valve sequencing, line fill, chilldown, ignition, mixture-ratio excursions, shaft acceleration, and thermal shock.", "Construct a start sequence that avoids hard start, pump overspeed, and thrust overshoot.", "Real-time transient optimization may improve reusable-engine life and operability.", "Validating a start sequence only at nominal initial temperature and tank pressure."),
            seminar("Engine Health Management", "Which measurements can detect faults early enough to act?", "Use physics residuals, spectral features, change detection, sensor validation, and fault isolation matrices.", "Design a detector for injector restriction versus pump degradation using pressure and speed channels.", "Hybrid physics and machine-learning diagnostics must quantify out-of-distribution behavior.", "Training a classifier on nominal and seeded faults without proving coverage of realistic failure evolution."),
        ],
        [
            "How can cycle optimization include life consumption and maintenance cost?",
            "Which transient measurements best identify cavitation onset before head breakdown?",
            "How should fault detection trade false shutdowns against catastrophic continuation?",
            "Can digital twins remain calibrated across an engine fleet?",
        ],
        {"type": "cycle", "title": "Engine Cycle Closure Lab", "description": "Balance pump power, turbine work, chamber pressure, bypass flow, efficiency, and cavitation margin."},
        ["sp125", "materials", "engine_test"],
    ),
    module(
        7,
        "advanced-propulsion-families",
        "Advanced Propulsion Families",
        "Match propulsion physics to mission timescale",
        "Compare solid, hybrid, electric, solar-sail, nuclear thermal, and nuclear electric propulsion using common mission metrics, operability constraints, technology readiness, and integrated architecture effects.",
        [
            "Compare propulsion options using thrust, specific impulse, power, burn duration, storage, and mission geometry.",
            "Analyze solid and hybrid internal ballistics and regression behavior.",
            "Formulate power-limited electric-propulsion trajectories.",
            "Evaluate nuclear and propellantless concepts without ignoring safety, infrastructure, and integration.",
        ],
        [
            equation("Electric thrust", "T = 2 eta P / v_e", "Shows the thrust penalty of high exhaust velocity at fixed input power.", "Assumes steady conversion efficiency and neglects plume and power-processing limits."),
            equation("Solid chamber balance", "m_dot_generation = m_dot_nozzle at quasi-steady pressure", "Links burn area and regression to choked nozzle flow.", "Quasi-steady internal ballistics; erosive burning and transients require added models."),
            equation("Hybrid regression", "r_dot = a G_ox^n", "Empirical fuel regression relation versus oxidizer mass flux.", "Geometry, scale, fuel formulation, and flow regime affect coefficients."),
            equation("Light-sail acceleration", "a = C_R S A / (m c)", "Relates radiation pressure to area-to-mass ratio.", "Depends on reflectivity, attitude, distance from the Sun, and degradation."),
        ],
        [
            seminar("Solid Motor Internal Ballistics", "How do grain geometry, burn law, nozzle erosion, and pressure couple?", "Close generation and discharge rates, track burning area, erosive effects, insulation, and thrust history.", "Design a neutral-thrust grain and examine sensitivity to throat erosion and burn-rate exponent.", "Additive grains and embedded diagnostics expand design space while complicating qualification.", "Assuming chamber pressure remains fixed when burn area or throat area evolves."),
            seminar("Hybrid Combustion and Scale", "Why is hybrid performance limited by mixing and regression rather than stoichiometry alone?", "Model boundary-layer regression, oxidizer distribution, port evolution, combustion efficiency, and instabilities.", "Compare single- and multiport hybrid designs under equal envelope and thrust targets.", "Liquefying fuels and swirl injection seek higher regression with controllable behavior.", "Extrapolating small-motor empirical regression coefficients directly to flight scale."),
            seminar("Electric Propulsion and Power", "How should exhaust velocity be selected when thrust is power-limited?", "Couple thruster efficiency, power system mass, duty cycle, plume, lifetime, and trajectory duration.", "Trade Hall and gridded-ion propulsion for a cargo spiral from high Earth orbit to lunar orbit.", "High-power solar electric and nuclear electric systems enable different logistics architectures.", "Selecting the highest specific impulse while ignoring transfer time and power-system mass."),
            seminar("Low-Thrust Optimal Control", "Why does continuous thrust alter the geometry of mission design?", "Use averaged elements, direct transcription, switching structure, eclipse constraints, and continuation.", "Optimize a low-thrust Earth escape with constrained thrust direction and coast arcs.", "Onboard autonomous low-thrust replanning is becoming more feasible.", "Approximating months of low thrust as one impulsive maneuver at departure."),
            seminar("Nuclear Thermal and Electric Systems", "What performance and integration changes follow from using a reactor?", "Analyze reactor power, propellant heating, shielding, decay heat, startup, specific mass, and mission operations.", "Compare chemical and nuclear-thermal stages for a crewed Mars departure under equal payload assumptions.", "Advanced fuels, reactor materials, and high-temperature testing dominate feasibility.", "Quoting reactor-level specific impulse without vehicle-level shielding, tank, and disposal mass."),
            seminar("Solar Sails and Momentum Exchange", "When can propellantless thrust produce mission-level advantage?", "Model radiation pressure, attitude authority, degradation, characteristic acceleration, and resonant orbit changes.", "Design a solar-sail spiral and compare it with low-power electric propulsion.", "Diffractive sails and beamed propulsion introduce new materials and control problems.", "Calling a system propellantless and therefore massless or operationally free."),
        ],
        [
            "What common metric fairly compares high-thrust and power-limited propulsion?",
            "How should lifetime uncertainty enter electric-propulsion trajectory optimization?",
            "Which nuclear-system constraints should be architectural requirements rather than late safety additions?",
            "Can hybrid propulsion gain throttling without unacceptable regression nonuniformity?",
        ],
        {"type": "propulsion", "title": "Propulsion Architecture Comparator", "description": "Compare chemical, electric, nuclear thermal, and sail options across power, thrust, Isp, transfer time, and system mass."},
        ["sp125", "cea", "trajectory_method"],
    ),
    module(
        8,
        "aerodynamics-loads-and-aeroelasticity",
        "Aerodynamics, Loads, and Aeroelasticity",
        "The atmosphere couples shape, control, and structure",
        "Treat launch and entry aerodynamics as unsteady, compressible, uncertain loads that interact with winds, propulsion, flexible modes, control, acoustics, and vehicle configuration.",
        [
            "Select aerodynamic fidelity using Mach, Knudsen, Reynolds, angle, and uncertainty regimes.",
            "Construct force and moment databases with interpolation and uncertainty.",
            "Translate distributed pressure and buffet into structural and control loads.",
            "Assess static and dynamic aeroelastic stability.",
        ],
        [
            equation("Aerodynamic force", "F_aero = q S C(M,Re,alpha,beta,...)", "Maps dynamic pressure and coefficients into resultant loads.", "Coefficient database must cover configuration, flow regime, and uncertainty."),
            equation("Bending metric", "M_bend = integral r x dF_aero + thrust and inertial terms", "Accumulates distributed loading about a structural station.", "Requires consistent distributed loads and accelerating-frame treatment."),
            equation("Flutter eigenproblem", "det[-omega^2 M + i omega C + K - Q_aero] = 0", "Couples structural modes with unsteady aerodynamic forces.", "Linearized stability model around a defined flight condition."),
            equation("Knudsen number", "Kn = lambda_mfp / L", "Classifies continuum versus rarefied flow behavior.", "Characteristic length and local mean free path must match the phenomenon."),
        ],
        [
            seminar("Flow-Regime Map", "Which physical effects control from liftoff through hypersonic ascent?", "Use Mach, Reynolds, Knudsen, chemistry, and boundary-layer state to select models and tests.", "Build a fidelity map for a reusable booster from pad winds to exoatmospheric flight.", "Adaptive multifidelity CFD can target uncertainty rather than uniformly increasing mesh cost.", "Using Mach number alone to select an aerodynamic model."),
            seminar("Aerodynamic Databases and Uncertainty", "How is a continuous flight database built from sparse CFD, tunnel, and flight evidence?", "Design samples, reconcile coordinate conventions, interpolate smoothly, quantify discrepancy, and track configuration changes.", "Fuse wind-tunnel and CFD pitching-moment data with a model-form uncertainty term.", "Gaussian-process and physics-informed surrogates can expose poorly supported regions.", "Treating interpolated values as measured truth with zero uncertainty."),
            seminar("Transonic Buffet and Unsteady Loads", "Why can a short transonic interval dominate fatigue or control risk?", "Analyze shock motion, separation, spectral content, spatial correlation, and modal forcing.", "Map unsteady pressure spectra into first-bending-mode generalized force.", "Scale-resolving simulations are improving buffet prediction but remain validation-intensive.", "Applying a steady peak coefficient as a substitute for unsteady correlated loading."),
            seminar("Base Flow, Plumes, and Proximity", "How do multiple plumes and separated wakes change vehicle forces and heating?", "Couple external flow, nozzle plumes, recirculation, stage geometry, and altitude.", "Assess booster-base heating and separation impulse during a clustered-engine staging event.", "Reusable vehicles drive interest in plume-surface and plume-plume interaction across broad envelopes.", "Using isolated-engine plume data for a clustered integrated base region."),
            seminar("Aeroelasticity and Control Interaction", "When do flexible structures reshape the aerodynamic and control problem?", "Build modal models, generalized aerodynamic forces, gain and phase margins, and flutter boundaries.", "Evaluate a bending-filter design against winds, sensor placement, and actuator bandwidth.", "Integrated controls-structures optimization can reduce mass but increases model-dependence.", "Notching a structural mode without checking uncertainty, delay, and neighboring modes."),
            seminar("Flight Reconstruction and Model Update", "How should flight data update aerodynamic knowledge?", "Estimate winds, states, biases, and coefficient corrections with covariance and identifiability analysis.", "Reconstruct axial force and pitching moment from inertial and pressure measurements.", "Bayesian model updating can carry flight learning into fleet operations.", "Assigning every model-data residual to aerodynamics while ignoring sensor and propulsion bias."),
        ],
        [
            "How should CFD model-form uncertainty be correlated across the flight envelope?",
            "Which flight instrumentation most improves aeroelastic model validation?",
            "Can onboard load estimation support less conservative guidance?",
            "How should plume-induced environments enter reusable-stage life models?",
        ],
        {"type": "aero", "title": "Aero-Loads Flight Tunnel", "description": "Sweep Mach, angle of attack, density, flexibility, and wind while tracking q, bending, heating proxy, and stability margin."},
        ["trajectory", "gnc", "caib"],
    ),
    module(
        9,
        "aerothermodynamics-and-thermal-protection",
        "Aerothermodynamics and Thermal Protection",
        "Survive energy deposition across scales",
        "Connect shock-layer physics, high-temperature chemistry, convective and radiative heating, catalytic surfaces, ablation, conduction, uncertainty, and test correlation to TPS architecture.",
        [
            "Distinguish equilibrium, nonequilibrium, continuum, transitional, and rarefied entry regimes.",
            "Construct preliminary heating and heat-load estimates with explicit validity limits.",
            "Model ablative and reusable TPS response and bondline constraints.",
            "Design an aerothermal validation and uncertainty-quantification campaign.",
        ],
        [
            equation("Stagnation heating correlation", "q_dot_s = k sqrt(rho/R_n) V^3", "Screens convective heating sensitivity to density, nose radius, and velocity.", "Correlation coefficient and exponent depend on gas, regime, and calibration."),
            equation("Surface energy balance", "q_conv + q_rad,in = epsilon sigma T_w^4 + q_cond + q_abl", "Balances incident heating against reradiation, conduction, and material response.", "Requires consistent sign, area, temperature, and material-response definitions."),
            equation("Transient conduction", "rho c_p dT/dt = div(k grad T) + q_vol", "Propagates temperature through TPS and structure.", "Properties may vary strongly with temperature, phase, and damage."),
            equation("Biot number", "Bi = h L_c / k_s", "Compares internal conduction resistance with surface convection.", "Characteristic length and effective h must reflect the thermal path."),
        ],
        [
            seminar("Shock Layers and High-Temperature Gas", "When do vibrational excitation, dissociation, ionization, and nonequilibrium matter?", "Map kinetic, internal, and chemical energy modes through the shock layer and select chemistry models.", "Compare equilibrium and nonequilibrium predictions for a lunar-return stagnation streamline.", "Radiation coupling and high-enthalpy kinetics remain significant uncertainty sources.", "Using perfect-gas normal-shock tables at orbital-entry enthalpy."),
            seminar("Convective and Radiative Heating", "How do trajectory, shape, boundary layer, and gas state set surface heating?", "Combine stagnation correlations, surface distributions, transition, turbulence, and shock-layer radiation.", "Build a peak-heating and integrated-heat-load envelope for two entry flight-path angles.", "Data-driven transition models must preserve physical extrapolation limits.", "Optimizing only peak heat flux while ignoring total heat load and soak time."),
            seminar("Ablation and Material Response", "How does sacrificial material protect underlying structure?", "Model pyrolysis, blowing, recession, char, moving boundaries, gas transport, and property uncertainty.", "Size an ablative layer to a bondline-temperature requirement with recession margin.", "Multiscale material models seek to connect microstructure with system response.", "Subtracting predicted recession from thickness without coupling changing geometry and heating."),
            seminar("Reusable TPS and Damage Tolerance", "What changes when the shield must survive many flights?", "Analyze coatings, oxidation, impact, gaps, seals, strain isolation, inspections, and life consumption.", "Construct a reuse disposition rule from damage size, location, thermal response, and uncertainty.", "Integrated sensing may enable condition-based TPS maintenance.", "Using intact coupon performance to justify damaged acreage behavior."),
            seminar("Arc-Jet, Tunnel, and Flight Correlation", "How can ground tests reproduce the relevant flight environment?", "Match heat flux, pressure, enthalpy, shear, chemistry, duration, and configuration as a vector, not one scalar.", "Design an arc-jet matrix that anchors a material-response model across expected entry conditions.", "Model-based test design can maximize information gained per specimen.", "Calling a test flight-like because one headline heat-flux value matches."),
            seminar("Aerothermal Uncertainty and Margin", "How should trajectory, transition, chemistry, material, and manufacturing uncertainty become TPS thickness?", "Propagate aleatory and epistemic uncertainty, calibrate discrepancy, and allocate thermal margin.", "Compare deterministic knockups with probabilistic bondline-temperature risk.", "Reliability-based TPS sizing can expose where testing has highest value.", "Applying one global heating multiplier to unrelated uncertainty mechanisms."),
        ],
        [
            "How should transition uncertainty be conditioned on surface damage and roughness?",
            "Which ground-test similarity parameters dominate flight extrapolation?",
            "Can reusable TPS health be inferred reliably from embedded sensing?",
            "How should epistemic model discrepancy enter certification margin?",
        ],
        {"type": "thermal", "title": "Entry Heating and TPS Lab", "description": "Vary velocity, density, nose radius, emissivity, conductivity, and thickness to inspect heat flux and bondline temperature."},
        ["tps", "thermal", "materials"],
    ),
    module(
        10,
        "structures-materials-and-cryogenic-systems",
        "Structures, Materials, and Cryogenic Systems",
        "Mass efficiency must survive the environment",
        "Integrate load paths, shell buckling, composites, fracture, fatigue, acoustic loads, cryogenic tanks, insulation, slosh, pressurization, manufacturing variability, and life management.",
        [
            "Build coupled load cases from propulsion, aerodynamics, inertia, acoustics, thermal gradients, and ground operations.",
            "Distinguish material allowables, structural margins, knockdown factors, and reliability.",
            "Analyze cryogenic storage, pressurization, boiloff, slosh, and feed-system interactions.",
            "Connect manufacturing and inspection evidence to damage tolerance and reuse life.",
        ],
        [
            equation("Margin of safety", "MS = allowable / applied - 1", "Expresses reserve against a defined failure mode and load case.", "Allowable and applied values must use compatible factors, statistics, and environments."),
            equation("Thin-wall hoop stress", "sigma_h = p r / t", "Screens membrane stress in a cylindrical pressure vessel.", "Thin, axisymmetric, membrane approximation without local discontinuities."),
            equation("Buckling form", "P_cr = k pi^2 E I / L^2", "Shows stiffness, length, and boundary sensitivity of elastic instability.", "Real shells require imperfection-sensitive knockdowns and combined loading."),
            equation("Pressurant balance", "p V = n R T", "Relates ullage pressure, volume, temperature, and gas inventory.", "Ideal-gas approximation; heat transfer, dissolution, and transient flow may matter."),
        ],
        [
            seminar("Integrated Loads and Load Paths", "How do local component forces become vehicle-level limit and ultimate loads?", "Combine trajectory cases, flexible-body dynamics, pressure, thrust, acoustics, thermal stress, and ground events.", "Trace an engine gimbal transient through thrust structure, tank shell, interstage, and payload interface.", "Probabilistic load combination may replace overly conservative independent envelopes.", "Applying component maxima from different times as one simultaneous vehicle load case."),
            seminar("Shell Buckling and Imperfections", "Why do thin launch-vehicle shells fail below classical predictions?", "Study nonlinear stability, geometric imperfections, combined compression and bending, orthotropy, and knockdown factors.", "Compare classical and imperfection-informed buckling predictions for an isogrid tank barrel.", "Validated high-fidelity analysis can support less conservative shell knockdowns.", "Treating an eigenvalue buckling load as a certified collapse load."),
            seminar("Composites and Joints", "How do anisotropy, defects, joints, and cryogenic cycling govern composite structures?", "Use laminate theory, failure criteria, cohesive interfaces, bearing/bypass loads, and process variability.", "Design a composite overwrapped tank region around a metallic boss.", "Cryogenic composite liners and permeation barriers remain active development areas.", "Optimizing pristine laminate strength while ignoring joints, impact, and manufacturing defects."),
            seminar("Fracture, Fatigue, and Reuse Life", "How should cracks and cumulative damage be managed across repeated missions?", "Apply stress intensity, crack growth, low- and high-cycle fatigue, inspection probability, and safe-life versus damage-tolerance logic.", "Build a retirement-for-cause rule for a reusable thrust structure.", "Digital thread and fleet data may support individualized life prediction.", "Using average S-N life as a deterministic allowable for a safety-critical fleet."),
            seminar("Cryogenic Tanks, Boiloff, and Pressurization", "How do heat leak, phase change, ullage dynamics, and withdrawal couple?", "Model stratification, autogenous or stored-gas pressurization, venting, boiloff, and feed transients.", "Estimate pressure evolution during a long coast with engine chilldown and restart.", "Zero-boiloff and in-space transfer architectures demand coupled fluid-thermal control.", "Using a uniform tank temperature and equilibrium vapor pressure during dynamic operations."),
            seminar("Slosh and Propellant Management", "When does free-surface motion become a guidance, loads, or feed problem?", "Use equivalent mechanical models, CFD, baffles, settling thrust, surface tension, and acquisition devices.", "Assess a lateral guidance maneuver against slosh mode and engine inlet requirements.", "Microgravity propellant transfer drives new multiphase sensing and control research.", "Treating slosh mass as rigidly attached or as one mode over the full fill range."),
        ],
        [
            "How can shell-buckling uncertainty be reduced most efficiently by tests?",
            "What inspection architecture supports economical reusable damage tolerance?",
            "How should cryogenic composite permeability be represented over life?",
            "Can propellant state estimation replace large settling and reserve penalties?",
        ],
        {"type": "structure", "title": "Cryogenic Structure Workbench", "description": "Trade tank pressure, radius, wall thickness, material, imperfection, heat leak, and pressurant conditions."},
        ["materials", "thermal", "seh"],
    ),
    module(
        11,
        "guidance-navigation-control-and-estimation",
        "Guidance, Navigation, Control, and Estimation",
        "Estimate the state, command the future, stabilize the vehicle",
        "Unify nonlinear dynamics, sensors, filtering, guidance, control allocation, flexible modes, navigation observability, fault accommodation, Monte Carlo verification, and real-time constraints.",
        [
            "Derive estimation and control models from consistent nonlinear dynamics.",
            "Analyze observability, controllability, covariance, and robustness.",
            "Design guidance and control that respect actuator, structural, and mission constraints.",
            "Verify GN&C through deterministic cases, Monte Carlo, hardware-in-the-loop, and flight reconstruction.",
        ],
        [
            equation("State estimation", "x_dot = f(x,u,w); y = h(x) + v", "Defines nonlinear process and measurement models with disturbances and noise.", "Noise assumptions and unmodeled biases must be stated and tested."),
            equation("Kalman update", "K = P H^T (H P H^T + R)^-1", "Weights predicted state against new measurement information.", "Linear-Gaussian form or local linearization; consistency must be monitored."),
            equation("Attitude dynamics", "I omega_dot + omega x (I omega) = tau", "Rigid-body rotational equation for torque-driven angular motion.", "Flexible modes, slosh, and moving mass require augmentation."),
            equation("Closed-loop robustness", "S = 1/(1+L); T = L/(1+L)", "Sensitivity functions expose disturbance rejection and model uncertainty tradeoffs.", "Linear frequency-domain interpretation about a defined operating point."),
        ],
        [
            seminar("Nonlinear State and Sensor Models", "What state is actually needed to fly the mission?", "Define translational, rotational, mass, bias, flexible, and environmental states with sensor geometry and timing.", "Build IMU, GPS, star-tracker, radar-altimeter, and engine models for a reusable booster.", "Factor-graph and smoothing methods increasingly complement recursive filters.", "Adding unobservable states because a model can represent them."),
            seminar("Navigation, Observability, and Consistency", "When do measurements contain enough independent information to estimate the state?", "Use linearized observability, information matrices, innovations, covariance consistency, and bias modeling.", "Assess yaw and lateral-velocity observability during vertical flight with intermittent GPS.", "Autonomous cislunar navigation combines weak, delayed, and nontraditional measurements.", "Reporting filter covariance as truth without innovation consistency tests."),
            seminar("Powered-Flight Guidance", "How does guidance convert mission targets into feasible thrust commands?", "Derive linear-tangent, polynomial, predictor-corrector, and optimal guidance forms with constraints.", "Target orbital insertion while adapting to measured engine performance.", "Successive convexification can support onboard constrained retargeting.", "Feeding an unreachable target to a guidance law without feasibility management."),
            seminar("Attitude Control and Allocation", "How should commanded torque be distributed among gimbals, thrusters, fins, and differential throttle?", "Design nonlinear attitude error, feedback, feedforward, allocation, saturation, and anti-windup.", "Allocate booster landing torque across center engine gimbal and aerodynamic surfaces.", "Control allocation under failures is a rich constrained optimization problem.", "Designing axes independently when actuators and inertia are strongly coupled."),
            seminar("Flexible-Body and Slosh Interaction", "How can control stabilize rigid motion without exciting flexible dynamics?", "Augment models with modes, sensor/actuator placement, filters, robustness, and time-varying frequency.", "Evaluate bending-mode gain and phase through propellant depletion.", "Adaptive notch and model-predictive methods must balance performance with certification.", "Testing structural filters only against the nominal modal model."),
            seminar("GN&C Verification and Monte Carlo", "What evidence demonstrates acceptable closed-loop performance across uncertainty?", "Construct dispersion models, coverage matrices, rare-event methods, HIL tests, and flight-reconstruction checks.", "Define pass/fail metrics for 10,000 ascent and landing simulations.", "Adaptive sampling can find failure regions missed by random Monte Carlo.", "Using a large run count as a substitute for a credible uncertainty model."),
        ],
        [
            "How can filter consistency be maintained with learned measurement models?",
            "Which rare-event methods best expose landing-guidance tail risk?",
            "How should onboard optimization be bounded for certification?",
            "Can flexible and slosh state estimation reduce structural conservatism?",
        ],
        {"type": "gnc", "title": "Closed-Loop Guidance Laboratory", "description": "Tune estimator noise, guidance gain, actuator authority, delay, wind, and sensor bias while tracking error and stability."},
        ["gnc", "cislunar", "software"],
    ),
    module(
        12,
        "avionics-software-reliability-and-fault-management",
        "Avionics, Software, Reliability, and Fault Management",
        "Make correct decisions under faults and incomplete evidence",
        "Engineer flight computers, networks, power, timing, software, redundancy, reliability, cybersecurity, fault detection isolation and recovery, and assurance cases as one safety-critical system.",
        [
            "Allocate reliability and fault tolerance without assuming independence.",
            "Design deterministic real-time software and dataflow with bounded failure behavior.",
            "Construct FMEA, fault trees, common-cause analysis, and recovery logic.",
            "Connect software and avionics verification evidence to system hazards.",
        ],
        [
            equation("Series reliability", "R = product(R_i)", "Shows reliability multiplication across independent required functions.", "Independence and mission-time failure distributions must be justified."),
            equation("Fault-tree OR gate", "P_union approx sum(P_i) for rare independent events", "Screens top-event probability from alternate causes.", "Approximation fails with dependence, nonrare events, and shared initiators."),
            equation("Availability", "A = MTBF / (MTBF + MTTR)", "Relates reliability and repair time for repairable systems.", "Not a substitute for mission reliability in a nonrepairable flight phase."),
            equation("Schedulability", "sum(C_i/T_i) <= U_bound", "Screens CPU utilization for periodic real-time tasks.", "Bound depends on scheduler, deadlines, blocking, jitter, and architecture."),
        ],
        [
            seminar("Flight-Computer and Network Architecture", "How should computation, data, time, and power be partitioned?", "Trade centralized and distributed architectures, redundancy, buses, deterministic timing, and graceful degradation.", "Design command and telemetry paths for a two-stage vehicle with reusable first stage.", "Time-sensitive networking and heterogeneous computing create new assurance questions.", "Adding redundant boxes that share power, clock, software, or environmental vulnerabilities."),
            seminar("Safety-Critical Software Engineering", "How is executable behavior traced from hazard to tested code?", "Use software requirements, architecture, coding standards, static analysis, unit and integration tests, configuration control, and independence.", "Trace an engine-shutdown hazard control through requirement, implementation, test, and evidence.", "Formal methods and proof-carrying components can strengthen selected high-consequence functions.", "Equating statement coverage with evidence that requirements and hazards are correct."),
            seminar("Reliability Modeling and Common Cause", "How should reliability models represent dependence and operational modes?", "Combine reliability blocks, fault trees, Markov states, Bayesian updates, and common-cause factors.", "Compare dual- and triple-redundant flight computers under shared software and power faults.", "Fleet evidence can update priors if configuration and exposure are controlled.", "Multiplying component reliabilities while omitting shared initiators."),
            seminar("FDIR Logic and Fault Accommodation", "Which faults should be detected, isolated, tolerated, or made safe?", "Map fault signatures to sensors, thresholds, persistence, voting, recovery, and authority.", "Design engine-sensor validation that avoids both false shutdown and unsafe continuation.", "Runtime assurance architectures can supervise advanced adaptive components.", "Creating recovery actions that are more hazardous than the fault they address."),
            seminar("Cyber-Physical Assurance", "How can cybersecurity be integrated without degrading real-time safety?", "Model trust boundaries, authenticated command, supply chain, update control, denial of service, and safety interactions.", "Threat-model a ground-to-vehicle command path during countdown and flight.", "Post-quantum and autonomous operations will change key-management and update strategies.", "Treating an isolated flight network as invulnerable across its full lifecycle."),
            seminar("Assurance Cases and Evidence Quality", "How can a reviewer decide whether the system is acceptably safe?", "Structure claims, arguments, evidence, defeaters, model pedigree, and unresolved uncertainty.", "Build an assurance fragment for autonomous stage safing after navigation loss.", "Executable assurance cases may detect stale evidence as configurations change.", "Counting documents instead of evaluating whether evidence supports the safety claim."),
        ],
        [
            "How should common software cause be quantified in redundant architectures?",
            "Which formal methods provide the highest assurance return for flight code?",
            "How can FDIR thresholds adapt without becoming unverifiable?",
            "What evidence is required before learned components enter safety-critical control paths?",
        ],
        {"type": "reliability", "title": "Fault-Tolerant Avionics Lab", "description": "Vary component reliability, common cause, voting, detection coverage, latency, and recovery success."},
        ["software", "seh", "caib", "faa450"],
    ),
    module(
        13,
        "testing-verification-range-safety-and-operations",
        "Testing, Verification, Range Safety, and Operations",
        "Evidence is engineered",
        "Design development, qualification, acceptance, integrated, hot-fire, environmental, software, range-safety, and operational evidence while protecting the public and preserving configuration integrity.",
        [
            "Build a verification strategy that connects model uncertainty to test objectives.",
            "Design instrumentation, calibration, sampling, and data reduction for propulsion and vehicle tests.",
            "Understand public-risk, system-safety, flight-safety, and licensing concepts.",
            "Integrate countdown, launch commit, anomaly response, and learning across operations.",
        ],
        [
            equation("Measurement uncertainty", "u_y^2 = J Sigma_x J^T + u_model^2", "Propagates correlated measurement and model uncertainty into a derived result.", "Local linearization unless nonlinear propagation is used."),
            equation("Sampling criterion", "f_s > 2 f_max with anti-alias filtering", "Sets a minimum sampling logic for band-limited signals.", "Practical systems require transition-band, phase, dynamic-range, and transient margin."),
            equation("Expected casualties", "E_c = sum_i P_i N_i", "Represents population-weighted expected consequence across hazard outcomes.", "Regulatory implementation requires prescribed models, areas, and conditional probabilities."),
            equation("Test information", "I(theta) = E[(d log L / d theta)^2]", "Measures how strongly a test can inform an uncertain parameter.", "Depends on likelihood model and assumed experiment conditions."),
        ],
        [
            seminar("Verification Architecture and Test Like You Fly", "Which claims require test, and which can credible analysis verify?", "Map requirements to evidence, similarity, model validation, qualification logic, and configuration.", "Plan verification for an engine restart after long cryogenic coast.", "Optimal experimental design can target the uncertainties that control mission risk.", "Repeating heritage tests without showing relevance to the new design and environment."),
            seminar("Instrumentation and Data Acquisition", "How can sensors and acquisition preserve the physics being measured?", "Specify bandwidth, range, mounting, calibration, timing, anti-aliasing, uncertainty, and failure behavior.", "Design thrust, pressure, flow, temperature, vibration, and plume measurements for a hot fire.", "Distributed fiber, optical, and high-temperature sensors expand observability.", "Selecting sample rate from event duration while ignoring high-frequency content and filtering."),
            seminar("Hot-Fire Test and Performance Reduction", "How do raw measurements become defensible thrust, impulse, mixture ratio, c-star, and efficiency?", "Correct tare, alignment, ambient pressure, timing, flow calibration, transients, and uncertainty.", "Reduce a synthetic engine test and close mass and impulse balances.", "Automated data-quality monitoring can prevent invalid tests from appearing successful.", "Averaging only the smoothest interval and discarding adverse dynamics without justification."),
            seminar("Environmental and Integrated Testing", "How should vibration, acoustics, shock, thermal vacuum, EMI, and end-to-end tests be sequenced?", "Connect workmanship, qualification, acceptance, protoflight, combined environments, and model correlation.", "Build an integrated test flow for launch vehicle avionics and upper-stage propulsion.", "Virtual testing can reduce hardware campaigns only when uncertainty and pedigree remain visible.", "Testing each environment separately when interactions or sequence drive failure."),
            seminar("Range Safety and Public Risk", "How do vehicle hazards become flight-safety rules and licensing evidence?", "Study hazard areas, debris, toxic release, blast, reliability, trajectory dispersions, containment, and flight termination.", "Construct a conceptual public-risk analysis for an orbital launch corridor.", "Autonomous flight safety systems shift validation toward software, navigation, and decision logic.", "Treating regulatory thresholds as design targets rather than upper safety bounds."),
            seminar("Launch Operations and Anomaly Learning", "How should countdown decisions integrate evidence, uncertainty, authority, and reversibility?", "Design launch commit criteria, hold logic, redlines, waiver process, configuration control, and post-test learning.", "Run a tabletop decision on a drifting engine-temperature sensor during terminal count.", "Digital operations twins can improve procedure validation and fleet learning.", "Normalizing repeated anomalies because previous missions succeeded."),
        ],
        [
            "How can tests maximize information rather than simply satisfy a matrix?",
            "Which model discrepancies should block extrapolation to flight?",
            "How should autonomous flight-safety evidence differ from crewed decision logic?",
            "Can fleet operations update risk without eroding qualification baselines?",
        ],
        {"type": "test", "title": "Test Evidence and Public-Risk Lab", "description": "Explore sensor uncertainty, sample rate, test information, failure probability, footprint, and population exposure."},
        ["engine_test", "faa450", "seh", "caib"],
    ),
    module(
        14,
        "reentry-landing-reuse-and-research-capstone",
        "Reentry, Landing, Reuse, and Research Capstone",
        "Close the mission and defend the evidence",
        "Integrate entry guidance, hypersonic and transonic flight, propulsion relight, landing, reusability, operability, economics, life consumption, and a publishable capstone research argument.",
        [
            "Design entry-to-landing trajectories across thermal, load, propellant, control, and range constraints.",
            "Analyze propulsive landing guidance, divert, engine-out, and touchdown robustness.",
            "Model reuse as a reliability, inspection, refurbishment, and economics problem.",
            "Produce a technically reviewable research package with reproducible evidence and explicit limitations.",
        ],
        [
            equation("Entry energy rate", "d epsilon/dt = v dot a_nonconservative", "Tracks how drag and propulsion change specific mechanical energy.", "Requires a consistent rotating or inertial energy definition."),
            equation("Landing divert", "Delta-v_budget >= Delta-v_brake + Delta-v_divert + reserves", "Closes propellant against braking, translation, hover, and uncertainty.", "Finite thrust, throttle, engine response, and gravity loss must be represented."),
            equation("Fleet lifecycle cost", "C_flight = C_ops + C_refurb + C_loss P_loss + C_capital/N", "Connects operations, refurbishment, risk, and amortization.", "Economic model depends on cadence, learning, financing, and consequence assumptions."),
            equation("Research reproducibility", "Result = f(code, data, configuration, assumptions)", "Makes every finding dependent on controlled artifacts and declared assumptions.", "Requires versioned code, data provenance, environment, and executable procedure."),
        ],
        [
            seminar("Entry Guidance and Energy Management", "How can a reusable stage dissipate energy while satisfying heat, load, footprint, and control constraints?", "Use bank, angle of attack, lift-to-drag, drag modulation, targeting, and predictor-corrector logic.", "Design a boostback and entry sequence for a returning first stage under crossrange uncertainty.", "Real-time footprint optimization can improve abort and weather robustness.", "Targeting a point without tracking the reachable set under constraints."),
            seminar("Transonic Return and Relight", "Why is the transition from hypersonic entry to powered descent operationally difficult?", "Couple unsteady aerodynamics, attitude authority, propellant settling, inlet state, ignition, and plume interaction.", "Construct relight conditions and timing for an entry burn with engine-start dispersions.", "Supersonic retropropulsion remains a key coupled fluid-control research problem.", "Assuming a qualified vacuum or sea-level start sequence is automatically valid in high-speed external flow."),
            seminar("Powered Descent Guidance", "How does a vehicle find a feasible landing trajectory under thrust and state constraints?", "Formulate convexified landing guidance with glide-slope, tilt, thrust, rate, and terminal constraints.", "Compare nominal and engine-out landing reachable sets with divert reserve.", "Successive convexification and runtime assurance are central to autonomous landing.", "Solving an infeasible problem repeatedly without a safe fallback policy."),
            seminar("Touchdown, Terrain, and Terminal Sensing", "Which sensor and control errors dominate the final seconds?", "Integrate radar, lidar, vision, terrain maps, leg dynamics, slosh, thrust transients, and surface uncertainty.", "Build a terminal-error budget from navigation covariance to leg load.", "Vision-based hazard avoidance needs transparent confidence and off-nominal behavior.", "Validating terminal sensing on visually clean sites unlike operational terrain."),
            seminar("Reusability, Inspection, and Economics", "When does hardware reuse create system-level value?", "Model life consumption, inspection probability, refurbishment flow, fleet size, reliability growth, cadence, and loss consequence.", "Compare expendable and reusable stages under uncertain flight rate and turnaround.", "Condition-based maintenance and digital fleet evidence may reduce unnecessary work.", "Quoting marginal propellant cost as the cost of a reusable launch."),
            seminar("Research Capstone and Expert Defense", "What would convince an independent rocket scientist that a conclusion is technically credible?", "State a falsifiable question, literature basis, model hierarchy, verification, validation, uncertainty, limitations, and reproducible artifacts.", "Prepare a review package comparing two architectures with one high-fidelity risk retired by targeted evidence.", "Open, executable technical arguments can improve education, review, and funding diligence.", "Using polished visualization to conceal unsupported assumptions or an unreproducible result."),
        ],
        [
            "How should reachable-set uncertainty drive landing reserve?",
            "What evidence supports extending reusable hardware life?",
            "How can cost models avoid optimistic cadence circularity?",
            "Which capstone claim is both consequential and falsifiable with available evidence?",
        ],
        {"type": "landing", "title": "Reusable Landing and Funding Case Lab", "description": "Trade entry energy, thrust, reserve, divert, reliability, refurbishment, cadence, and lifecycle cost."},
        ["gnc", "tps", "faa450", "seh", "caib"],
    ),
]


def _build_seminar(module_item, number, spec):
    equation_item = module_item["equations"][(number - 1) % len(module_item["equations"])]
    sections = [
        {
            "title": "Research frame",
            "body": (
                f"{spec['question']} This seminar treats the question as a falsifiable engineering "
                f"claim inside {module_item['title']}, not as a request for a memorized formula. "
                f"Begin by naming the system boundary, mission phase, decision to be supported, "
                f"observables, controlled variables, and consequences of error. State which effects "
                f"are intentionally omitted and identify evidence that would force the model to change."
            ),
        },
        {
            "title": "Mathematical spine",
            "body": (
                f"{spec['method']} The anchor relationship is {equation_item['name']}: "
                f"{equation_item['expression']}. {equation_item['meaning']} Derive or justify each "
                f"term, preserve units and signs, and nondimensionalize where scaling matters. "
                f"Validity boundary: {equation_item['validity']} A postdoctoral-quality analysis "
                f"must show numerical conditioning, convergence, and sensitivity rather than only a result."
            ),
        },
        {
            "title": "Worked engineering case",
            "body": (
                f"{spec['case']} Build the case in layers: a transparent analytic estimate, a numerical "
                f"baseline, and at least one higher-fidelity correction. Close conserved quantities and "
                f"interfaces, compare against an independent method, and report the decision metric with "
                f"units. Preserve enough intermediate state that another analyst can reproduce the result "
                f"and locate the first disagreement."
            ),
        },
        {
            "title": "Verification, validation, and uncertainty",
            "body": (
                "Verify implementation with limiting cases, manufactured solutions where possible, "
                "step-size or mesh refinement, conservation residuals, and regression tests. Validate "
                "the model only against evidence relevant to the intended use. Separate input variability, "
                "measurement uncertainty, parameter uncertainty, and model-form discrepancy; retain "
                "correlations. Report how uncertainty changes the decision, not merely the plotted curve."
            ),
        },
        {
            "title": "Research edge and red team",
            "body": (
                f"{spec['frontier']} The red-team failure to challenge is: {spec['failure']} Close the "
                f"seminar by proposing the smallest analysis, experiment, or flight measurement that "
                f"could disprove the favored explanation. Record unresolved assumptions and rank them by "
                f"decision sensitivity, consequence, and cost of acquiring better evidence."
            ),
        },
        {
            "title": "Reproducible computational protocol",
            "body": (
                "Implement the analysis as a versioned experiment. Define the state vector, parameters, "
                "units, reference frames, initial and boundary conditions, solver tolerances, event logic, "
                "and random seed in machine-readable configuration. Create unit tests from analytic limits "
                "and regression tests from reviewed baselines. Record software version, source-data hashes, "
                "runtime environment, and convergence evidence with every result. Plot residuals and conserved "
                "quantities, not only the desired performance metric. A second analyst should be able to rerun "
                "the case, perturb one assumption, and explain any changed conclusion without private knowledge."
            ),
        },
        {
            "title": "Expert defense",
            "body": (
                f"Defend one concise claim about {spec['title']} with a claim-evidence-limit table. Present "
                "the strongest alternative explanation, the evidence that discriminates between explanations, "
                "and the conditions under which no decision should be made. Quantify at least one sensitivity "
                "that can reverse the recommendation. Distinguish verified code, validated model behavior, and "
                "unvalidated extrapolation. End with a stop rule for additional analysis and a prioritized plan "
                "for retiring the remaining technical risk. The objective is not to appear certain; it is to "
                "make the exact boundary of justified confidence inspectable to an independent specialist. "
                "Answer challenges with traceable calculations, source lineage, and explicit model limitations "
                "rather than appeals to authority, heritage, or solver sophistication."
            ),
        },
    ]
    word_count = sum(len(section["body"].split()) for section in sections)
    return {
        "number": number,
        "slug": f"{module_item['slug']}-{number:02d}",
        "title": spec["title"],
        "question": spec["question"],
        "sections": sections,
        "failure": spec["failure"],
        "equation": equation_item,
        "word_count": word_count,
        "minutes": max(6, round(word_count / 125)),
    }


for _module in MODULES:
    _module["seminars"] = [
        _build_seminar(_module, number, spec)
        for number, spec in enumerate(_module["seminar_specs"], start=1)
    ]
    _module["sources"] = source_list(_module["source_keys"])


def all_modules():
    return MODULES


def module_by_slug(slug):
    return next((item for item in MODULES if item["slug"] == slug), None)


def seminar_by_number(module_item, number):
    if not module_item or number < 1 or number > len(module_item["seminars"]):
        return None
    return module_item["seminars"][number - 1]


def search_curriculum(query):
    terms = [term.lower() for term in query.split() if term.strip()]
    if not terms:
        return []
    results = []
    for item in MODULES:
        module_text = " ".join(
            [
                item["title"],
                item["domain"],
                item["summary"],
                *item["outcomes"],
                *item["research_questions"],
                *(f"{eq['name']} {eq['expression']} {eq['meaning']}" for eq in item["equations"]),
            ]
        ).lower()
        if all(term in module_text for term in terms):
            results.append(
                {
                    "kind": "Module",
                    "module": item,
                    "title": item["title"],
                    "summary": item["summary"],
                    "url_suffix": "",
                }
            )
        for lecture in item["seminars"]:
            lecture_text = " ".join(
                [
                    lecture["title"],
                    lecture["question"],
                    lecture["failure"],
                    *(section["body"] for section in lecture["sections"]),
                ]
            ).lower()
            if all(term in lecture_text for term in terms):
                results.append(
                    {
                        "kind": "Research seminar",
                        "module": item,
                        "title": lecture["title"],
                        "summary": lecture["question"],
                        "url_suffix": f"/seminar/{lecture['number']}",
                    }
                )
    return results[:80]


def validate_curriculum():
    errors = []
    if len(MODULES) != 14:
        errors.append("The curriculum must contain fourteen modules")
    for expected, item in enumerate(MODULES, start=1):
        if item["number"] != expected:
            errors.append(f"Module numbering breaks at {item['slug']}")
        if len(item["outcomes"]) != 4:
            errors.append(f"{item['slug']} needs four outcomes")
        if len(item["equations"]) != 4:
            errors.append(f"{item['slug']} needs four governing equations")
        if len(item["seminars"]) != 6:
            errors.append(f"{item['slug']} needs six research seminars")
        if len(item["research_questions"]) != 4:
            errors.append(f"{item['slug']} needs four research questions")
        if len(item["sources"]) < 3:
            errors.append(f"{item['slug']} needs at least three primary sources")
        if not item["lab"].get("type"):
            errors.append(f"{item['slug']} needs an interactive laboratory")
        for seminar_item in item["seminars"]:
            if len(seminar_item["sections"]) != 7:
                errors.append(f"{seminar_item['slug']} needs seven seminar sections")
            if seminar_item["word_count"] < 500:
                errors.append(f"{seminar_item['slug']} is too shallow")
    return errors
