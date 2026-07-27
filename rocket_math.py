"""Detailed theoretical and practical mathematics for every course module."""


def _studio(title, principle, derivation, scenario, inputs, calculation, result, checks):
    return {
        "title": title,
        "principle": principle,
        "derivation": derivation,
        "practical": {
            "scenario": scenario,
            "inputs": inputs,
            "calculation": calculation,
            "result": result,
            "checks": checks,
        },
    }


MATH_STUDIOS = {
    "architecture": _studio(
        "Robust multi-attribute architecture selection",
        (
            "Architecture selection is a decision under uncertainty, not a beauty contest between "
            "point estimates. Utility theory maps unlike attributes onto dimensionless preference, "
            "while risk and robustness tests expose decisions that reverse under plausible assumptions."
        ),
        [
            "Define each physical outcome y_i(x, theta) for architecture x and uncertain state theta. Never apply a weight directly to dimensional quantities such as kilograms and dollars.",
            "Map each outcome through an elicited utility u_i(y_i) in [0, 1]. A linear map is defensible only when equal physical increments have equal decision value over the stated range.",
            "Form J(x, theta) = sum_i w_i u_i(y_i) - lambda R(x, theta), with w_i >= 0 and sum_i w_i = 1. The risk term must not duplicate a consequence already embedded in utility.",
            "Compute expected utility E_theta[J], percentile performance, and regret L(x, theta) = max_z J(z, theta) - J(x, theta). A robust choice controls regret across the uncertainty set instead of winning only at its center.",
            "Differentiate or resample J with respect to weights, correlations, and uncertain inputs. The decision is fragile when a plausible perturbation changes the preferred architecture.",
        ],
        "Compare two cislunar cargo architectures after all three attributes have been mapped to defensible utilities.",
        [
            "Weights: delivered utility 0.45, reliability utility 0.35, lifecycle-cost utility 0.20.",
            "Architecture A utilities: delivery 0.80, reliability 0.96, cost 0.60.",
            "Architecture B utilities: delivery 0.70, reliability 0.985, cost 0.85.",
        ],
        [
            "J_A = 0.45(0.80) + 0.35(0.96) + 0.20(0.60) = 0.8160.",
            "J_B = 0.45(0.70) + 0.35(0.985) + 0.20(0.85) = 0.82975.",
            "Nominal advantage: J_B - J_A = 0.01375, only 1.7 percent of J_A.",
            "Because the margin is small, sweep weights over the elicitation intervals and carry correlated cost/reliability uncertainty before selecting B.",
        ],
        "Architecture B is the nominal leader, but the correct engineering decision is WATCH: the utility margin is too small to claim robust dominance without sensitivity and regret analysis.",
        [
            "Weights sum to one and utilities are dimensionless.",
            "No consequence is counted in both a utility and the risk penalty.",
            "The preferred architecture survives plausible weight and correlation changes.",
        ],
    ),
    "staging": _studio(
        "Variable-mass dynamics and staging closure",
        (
            "The logarithm in the rocket equation follows from momentum conservation as vehicle mass "
            "changes. Staging then becomes a constrained allocation problem because exhaust velocity, "
            "inert fraction, thrust, geometry, and operational losses differ by stage."
        ),
        [
            "For a vehicle of instantaneous mass m that ejects mass at effective speed c relative to the vehicle, momentum balance gives m dv = -c dm when external impulse is neglected.",
            "Integrate from m_0 to m_f: Delta-v = integral[-c dm/m]. For constant c this becomes Delta-v = c ln(m_0/m_f) = Isp g_0 ln(m_0/m_f).",
            "Restore external forces with m dv/dt = T - D - m g_parallel. The ideal integral and the time integral of gravity, drag, steering, backpressure, and transient effects must close to the simulated state change.",
            "For stage i, define mass ratio R_i = exp(Delta-v_i/c_i) and inert fraction epsilon_i. The ideal payload fraction passed through that stage is lambda_i = (1/R_i - epsilon_i)/(1 - epsilon_i).",
            "Maximize product(lambda_i) subject to sum(Delta-v_i) = Delta-v_required and constraints on thrust-to-weight, acceleration, tankage, residuals, restart, and engine count.",
        ],
        "Estimate the ideal payload fraction of a two-stage vehicle before applying reserves and external losses.",
        [
            "Stage 1: Isp = 330 s, inert fraction = 0.07, allocated Delta-v = 4.20 km/s.",
            "Stage 2: Isp = 450 s, inert fraction = 0.10, allocated Delta-v = 5.20 km/s.",
            "Standard gravity g_0 = 9.80665 m/s^2.",
        ],
        [
            "R_1 = exp[4200/(330 x 9.80665)] = 3.66; R_2 = exp[5200/(450 x 9.80665)] = 3.25.",
            "lambda_1 = (1/3.66 - 0.07)/(1 - 0.07) = 0.218.",
            "lambda_2 = (1/3.25 - 0.10)/(1 - 0.10) = 0.231.",
            "Overall ideal payload fraction = lambda_1 lambda_2 = 0.0504, or about 5.0 percent.",
        ],
        "The 5.0 percent result is an ideal screening value. Residuals, fairing and interstage jettison logic, finite burns, ascent losses, reserves, and structural scaling must be closed before it becomes a payload claim.",
        [
            "Every logarithm receives a dimensionless mass ratio.",
            "Delta-v and Isp g_0 use the same velocity units.",
            "Stage mass ledgers reconcile at ignition, cutoff, and separation.",
        ],
    ),
    "orbit": _studio(
        "Energy, angular momentum, and transfer geometry",
        (
            "Two-body motion is organized by conserved specific energy and angular momentum. Named "
            "maneuvers are useful analytic baselines; operational trajectory design restores finite burns, "
            "perturbations, navigation covariance, timing, eclipse, and targeting constraints."
        ),
        [
            "Begin with r_ddot = -mu r/|r|^3. Dot with velocity and integrate to obtain specific energy epsilon = v^2/2 - mu/r.",
            "For a bound conic, epsilon = -mu/(2a). Cross the equation of motion with r to show h = r x v is constant and the motion is planar.",
            "At an apsis, velocity is transverse. Combining energy with r gives the vis-viva equation v^2 = mu(2/r - 1/a).",
            "A Hohmann transfer uses an ellipse with a_t = (r_1 + r_2)/2. Subtract circular and transfer velocities at each apsis to obtain the two impulses.",
            "Transfer time is half the ellipse period: t_H = pi sqrt(a_t^3/mu). Propagate state and covariance at higher fidelity before treating this baseline as an operational design.",
        ],
        "Compute an ideal coplanar transfer from a 200 km circular Earth orbit to geostationary radius.",
        [
            "Earth mu = 398600 km^3/s^2; r_1 = 6578 km; r_2 = 42164 km.",
            "Transfer semimajor axis a_t = (r_1 + r_2)/2 = 24371 km.",
            "Impulses are tangential and instantaneous in the two-body model.",
        ],
        [
            "Delta-v_1 = sqrt(mu/r_1)[sqrt(2r_2/(r_1+r_2)) - 1] = 2.455 km/s.",
            "Delta-v_2 = sqrt(mu/r_2)[1 - sqrt(2r_1/(r_1+r_2))] = 1.478 km/s.",
            "Total ideal Delta-v = 3.933 km/s.",
            "t_H = pi sqrt(a_t^3/mu) = 5.26 h.",
        ],
        "This is a reference solution, not a mission plan. Launch-site inclination, plane change, injection error, finite burn duration, disposal, and perturbations can materially alter the result.",
        [
            "Specific energy computed before and after each impulse matches the intended conic.",
            "Position is continuous across an impulsive burn and velocity changes by the commanded vector.",
            "A numerical propagator converges toward the analytic conic as step size decreases.",
        ],
    ),
    "ascent": _studio(
        "Constrained ascent dynamics and path control",
        (
            "Ascent is a nonlinear optimal-control problem. Thrust direction and magnitude must build "
            "orbital energy while respecting atmospheric loads, heating, controllability, propellant, "
            "engine, range, and terminal-state constraints."
        ),
        [
            "Propagate r_dot = v and v_dot = (T/m)u_T + g(r) + a_aero in one declared frame. Atmosphere-relative velocity, not inertial velocity, drives aerodynamic force.",
            "Dynamic pressure is q = rho V_rel^2/2. If aerodynamic coefficients are locally constant, force and bending scale approximately with q.",
            "A preliminary stagnation-heating proxy scales as q_dot proportional to sqrt(rho/R_n)V_rel^3, exposing its much stronger velocity sensitivity.",
            "State the optimization as min Phi(x_f) + integral L(x,u,t)dt subject to dynamics, boundary conditions, and path constraints g(x,u,t) <= 0.",
            "After transcription, independently integrate the returned control, report defect norms and constraint margins, and test dispersions. Solver success alone is not physical feasibility.",
        ],
        "Screen a trajectory point for a 45 kPa dynamic-pressure constraint and estimate the velocity reduction needed at fixed density.",
        [
            "Local density rho = 0.18 kg/m^3 and air-relative speed V = 900 m/s.",
            "Dynamic-pressure limit q_lim = 45 kPa.",
            "Use constant density only for this local sensitivity calculation.",
        ],
        [
            "q = 0.5(0.18)(900^2) = 72.9 kPa, so the point violates the limit by 27.9 kPa.",
            "At fixed density, q scales with V^2. Required speed ratio = sqrt(45/72.9) = 0.786.",
            "The corresponding local speed is about 707 m/s, a reduction of 193 m/s.",
            "A real controller changes future altitude, density, gravity loss, angle of attack, and terminal energy; re-optimize rather than applying this ratio as a throttle command.",
        ],
        "The local calculation identifies severity and scaling, not a guidance law. The interactive ascent laboratory reveals the trajectory-level consequences of changing thrust and pitch timing.",
        [
            "Aerodynamic calculations use air-relative velocity and consistent density units.",
            "Maximum q is located by event refinement, not only coarse output samples.",
            "Terminal state, integrated losses, and all active constraints close independently.",
        ],
    ),
    "nozzle": _studio(
        "Control-volume thrust and nozzle expansion",
        (
            "Rocket thrust is the net axial momentum and pressure force across a control volume. Chamber "
            "chemistry sets available thermodynamic performance; the nozzle converts enthalpy into directed "
            "kinetic energy while losses and ambient pressure determine delivered thrust."
        ),
        [
            "Apply steady axial momentum conservation around the engine: F = m_dot V_e + (p_e - p_a)A_e when inlet momentum is negligible in the vehicle frame.",
            "Define characteristic velocity c_star = p_c A_t/m_dot. It isolates chamber and propellant performance from most expansion effects.",
            "Define thrust coefficient C_F = F/(p_c A_t). Then F = C_F p_c A_t and effective exhaust velocity c = C_F c_star.",
            "Specific impulse follows as Isp = F/(m_dot g_0) = C_F c_star/g_0.",
            "Use isentropic area-Mach relations only inside their calorically perfect, quasi-one-dimensional validity domain; compare against equilibrium/frozen chemistry and measured loss factors.",
        ],
        "Close a preliminary thrust and specific-impulse estimate from chamber measurements and a modeled thrust coefficient.",
        [
            "Chamber pressure p_c = 7.0 MPa; throat area A_t = 0.060 m^2.",
            "Propellant mass flow m_dot = 240 kg/s; modeled C_F = 1.70.",
            "Sea-level or vacuum condition must match the C_F calculation.",
        ],
        [
            "c_star = p_c A_t/m_dot = (7.0e6)(0.060)/240 = 1750 m/s.",
            "F = C_F p_c A_t = 1.70(7.0e6)(0.060) = 714 kN.",
            "Isp = F/(m_dot g_0) = 714000/(240 x 9.80665) = 303.4 s.",
            "The identity C_F c_star = Isp g_0 closes: 1.70(1750) = 2975 m/s.",
        ],
        "The estimate is internally consistent but inherits the ambient condition and every loss embedded in C_F. Compare c_star and C_F separately with test data to localize chamber versus nozzle discrepancy.",
        [
            "Pressure is absolute and every area refers to the same throat definition.",
            "Mass flow includes all streams crossing the selected control volume.",
            "Momentum, pressure thrust, measured force, c_star, and C_F reconcile.",
        ],
    ),
    "cycle": _studio(
        "Power balance, cavitation, and transient shaft dynamics",
        (
            "A liquid engine cycle closes only when pump demand, turbine or motor supply, pressure losses, "
            "thermal states, mixture ratio, cavitation margin, and transient shaft dynamics are mutually "
            "consistent at every required operating point."
        ),
        [
            "For an incompressible pump, hydraulic power is m_dot Delta-p/rho. Shaft demand is P_p = m_dot Delta-p/(rho eta_p).",
            "A turbine supplies P_t = m_dot_t Delta-h_is eta_t under the stated efficiency convention. Mechanical and accessory losses consume the margin P_t - P_p.",
            "Pump inlet pressure determines NPSH_available = (p_total,in - p_vapor)/(rho g). Compare with configuration-specific NPSH_required at flow and speed.",
            "During start, I domega/dt = tau_t - tau_p - tau_loss. A steady power balance cannot prove a feasible transient because torque, pressure, and flow evolve together.",
            "Close every node in pressure, mass flow, enthalpy, species, and shaft work. A cycle code should report residuals rather than silently forcing inconsistent inputs.",
        ],
        "Check whether a turbine can power a fuel pump with useful steady-state margin.",
        [
            "Pump: m_dot = 220 kg/s, Delta-p = 12 MPa, density = 1140 kg/m^3, eta_p = 0.72.",
            "Turbine: m_dot_t = 10 kg/s, isentropic enthalpy drop = 450 kJ/kg, eta_t = 0.78.",
            "Accessory and bearing losses are not yet included.",
        ],
        [
            "P_p = 220(12e6)/(1140 x 0.72) = 3.216 MW.",
            "P_t = 10(450000)(0.78) = 3.510 MW.",
            "Gross margin = 0.294 MW, or 9.1 percent of pump demand.",
            "Subtract mechanical losses and repeat over throttle, inlet temperature, startup, and degraded efficiency before accepting closure.",
        ],
        "A positive 9.1 percent gross margin is necessary but not sufficient. Cavitation, turbine temperature, overspeed, start torque, controls, and off-design maps can still make the cycle infeasible.",
        [
            "Pump and turbine efficiencies use declared input/output conventions.",
            "All branch mass flows close and pressure losses have one sign convention.",
            "Steady operating points lie on compatible pump and turbine maps.",
        ],
    ),
    "propulsion": _studio(
        "Energy-limited propulsion and mission coupling",
        (
            "Propulsion comparisons must conserve momentum, energy, and total system mass. High exhaust "
            "velocity reduces propellant but demands power and time; high thrust shortens maneuvers but "
            "usually carries lower specific impulse or greater engine mass."
        ),
        [
            "Jet kinetic power is P_jet = m_dot v_e^2/2 and thrust is T = m_dot v_e. Eliminating m_dot gives T = 2 P_jet/v_e.",
            "With total input power P and conversion efficiency eta, T = 2 eta P/v_e = 2 eta P/(Isp g_0).",
            "Vehicle acceleration is a = T/m, so burn time for a small velocity change is approximately Delta-v/a. For large propellant changes, integrate variable mass and orbital dynamics.",
            "The ideal propellant fraction for prescribed Delta-v is 1 - exp[-Delta-v/(Isp g_0)]. This says nothing about power-system, tank, radiator, thruster, or trip-time mass.",
            "Compare propulsion families at the mission-system level using delivered mass, time, operations, environments, reliability, and technology readiness, not Isp alone.",
        ],
        "Estimate thrust, ideal burn time, and propellant for a solar-electric transfer.",
        [
            "Input power P = 100 kW, efficiency eta = 0.65, Isp = 3000 s.",
            "Initial spacecraft mass m_0 = 2000 kg; target ideal Delta-v = 3.0 km/s.",
            "Use constant power and ignore eclipse and thrust-direction loss for the analytic baseline.",
        ],
        [
            "v_e = Isp g_0 = 29.42 km/s; T = 2(0.65)(100000)/29420 = 4.42 N.",
            "Initial acceleration = 4.42/2000 = 2.21e-3 m/s^2.",
            "Constant-mass time estimate = 3000/(2.21e-3) = 1.36e6 s = 15.7 days.",
            "Ideal propellant = 2000[1 - exp(-3000/29420)] = 194 kg.",
        ],
        "The analytic result exposes scale but understates mission complexity. Power variation, eclipses, steering, tankage, power processing, radiator mass, duty cycle, and orbital geometry belong in the comparison.",
        [
            "Electrical input, jet power, and efficiency are not conflated.",
            "Burn duration is integrated with changing mass and available power.",
            "Every propulsion option carries its full support-system mass.",
        ],
    ),
    "aero": _studio(
        "Aerodynamic loads and aeroelastic stability",
        (
            "Aerodynamic coefficients turn local flow state into distributed forces and moments. Structural "
            "response feeds back into geometry and angle of attack, making loads, control, and flutter a "
            "coupled problem rather than independent lookup tables."
        ),
        [
            "Dynamic pressure q = rho V_rel^2/2 provides the force scale. Resultant force is F = q S C(M, Re, alpha, beta, configuration).",
            "Distributed load dF(x) produces shear and bending; about a station x_0, M = integral[(x-x_0) x dF] plus thrust and inertial contributions.",
            "Represent elastic displacement with modes eta: M_s eta_ddot + C_s eta_dot + K_s eta = Q_aero(eta, eta_dot, Mach, q).",
            "Linear flutter occurs when an eigenvalue of the coupled system crosses into positive real part. The prediction depends on mode set, unsteady aerodynamics, damping, and flight condition.",
            "Build a loads envelope over trajectory and uncertainty, then verify structural response and control interaction at critical combinations rather than isolated maxima.",
        ],
        "Screen normal force and root bending moment at a high-dynamic-pressure ascent condition.",
        [
            "Density rho = 0.40 kg/m^3, air-relative speed = 600 m/s, reference area S = 10 m^2.",
            "Normal-force slope C_N_alpha = 0.10 per degree and angle of attack alpha = 3 degrees.",
            "Effective center-of-pressure lever arm from the root station = 15 m.",
        ],
        [
            "q = 0.5(0.40)(600^2) = 72 kPa.",
            "C_N = C_N_alpha alpha = 0.30.",
            "Normal force N = q S C_N = 72000(10)(0.30) = 216 kN.",
            "Root bending estimate M = N(15) = 3.24 MN m.",
        ],
        "The estimate identifies an important load scale but not a structural design load. Distributed aerodynamics, inertia relief, thrust, gusts, flexibility, coefficient uncertainty, and dynamic amplification must be restored.",
        [
            "Velocity is relative to the atmosphere and coefficient conventions are declared.",
            "Distributed loads integrate to the reported forces and moments.",
            "Aeroelastic modes and control laws are tested together near stability boundaries.",
        ],
    ),
    "thermal": _studio(
        "Entry heating and material energy balance",
        (
            "Aerothermal design couples shock-layer flow, catalytic chemistry, radiation, surface response, "
            "conduction, pyrolysis, ablation, and structural temperature limits. Preliminary correlations "
            "reveal scaling but require explicit calibration and validity limits."
        ),
        [
            "A Sutton-Graves-form convective proxy is q_dot_s = k sqrt(rho/R_n)V^3. Its purpose is scaling; k and even the velocity exponent depend on regime and units.",
            "At the surface, q_conv + q_rad,in = epsilon sigma T_w^4 + q_cond + q_abl. Every term is a signed heat rate per area on the same surface.",
            "Inside a non-ablating solid, rho_s c_p dT/dt = div(k_s grad T). Temperature-dependent properties make the equation nonlinear.",
            "Nondimensional Bi = hL_c/k_s and Fo = alpha t/L_c^2 indicate whether lumped temperature or resolved transient conduction is appropriate.",
            "Size TPS against integrated temperature, recession, bondline, and structural constraints across trajectory and uncertainty, not peak heat flux alone.",
        ],
        "Estimate radiative-equilibrium temperature and the effect of doubling nose radius at one entry condition.",
        [
            "Incident convective heat flux = 1.20 MW/m^2; emissivity epsilon = 0.85.",
            "Neglect conduction, ablation, and incoming radiation for the equilibrium upper-bound exercise.",
            "Compare nose radii 0.50 m and 1.00 m at identical density and velocity.",
        ],
        [
            "T_eq = [q_dot/(epsilon sigma)]^(1/4) = [1.20e6/(0.85 x 5.670e-8)]^(1/4) = about 2234 K.",
            "Because q_dot scales as R_n^(-1/2), doubling R_n multiplies heat flux by sqrt(0.50/1.00) = 0.707.",
            "New screening heat flux = 0.849 MW/m^2.",
            "The corresponding radiative-equilibrium temperature scales as q_dot^(1/4), giving about 2048 K.",
        ],
        "Bluntness reduces stagnation convective flux in the correlation but changes drag, shock standoff, integrated exposure, mass, stability, and downstream heating. The full vehicle trade remains coupled.",
        [
            "Correlation constants match the selected units and gas regime.",
            "Surface fluxes and internal energy close over the full transient.",
            "Grid, time step, material properties, and recession predictions are convergence-tested.",
        ],
    ),
    "structure": _studio(
        "Pressure-vessel stress, stability, and cryogenic coupling",
        (
            "Launch structures carry pressure, thrust, inertia, bending, acoustic, thermal, and handling "
            "loads while mass and imperfection sensitivity are severe. Membrane formulas are screening "
            "tools; local discontinuities and shell buckling demand higher-fidelity evidence."
        ),
        [
            "Cut a thin cylindrical shell longitudinally. Pressure resultant 2prL is balanced by two wall forces 2 sigma_h tL, giving hoop stress sigma_h = pr/t.",
            "An axial cut gives closed-end longitudinal membrane stress sigma_l = pr/(2t). Add axial vehicle load and bending with consistent load factors.",
            "Define margin of safety MS = allowable/applied - 1 using compatible statistical allowables, environments, knockdowns, and factors.",
            "Elastic column scaling P_cr = k pi^2 EI/L^2 illustrates stiffness sensitivity, but thin shells require imperfection-sensitive buckling analysis and test correlation.",
            "Couple pressure and structural calculations to cryogenic temperature, weld efficiency, slosh, pressurization transients, heat leak, and material compatibility.",
        ],
        "Screen hoop stress and margin for a thin cryogenic tank barrel.",
        [
            "Internal gauge pressure p = 0.35 MPa, radius r = 2.5 m, wall thickness t = 4.0 mm.",
            "Temperature- and weld-adjusted allowable = 250 MPa.",
            "A 1.20 combined uncertainty/load factor is examined separately.",
        ],
        [
            "Nominal hoop stress = pr/t = 0.35e6(2.5)/0.004 = 218.75 MPa.",
            "Nominal MS = 250/218.75 - 1 = 0.143.",
            "Factored applied stress = 1.20(218.75) = 262.5 MPa.",
            "Factored MS = 250/262.5 - 1 = -0.048, so the screening case fails.",
        ],
        "The negative factored margin requires design change or better evidence. A shell model must then address welds, cutouts, local bending, proof pressure, combined axial load, buckling, fatigue, and fracture.",
        [
            "Pressure uses the correct gauge/absolute convention for each equation.",
            "Geometry satisfies the thin-wall assumption before membrane formulas are used.",
            "Loads, allowables, factors, and environmental reductions come from one consistent design basis.",
        ],
    ),
    "gnc": _studio(
        "State estimation, feedback, and covariance consistency",
        (
            "Guidance selects feasible objectives, navigation estimates the state and uncertainty, and "
            "control rejects disturbances while respecting actuator and structural limits. Their models "
            "must share frames, timing, conventions, and uncertainty assumptions."
        ),
        [
            "Write nonlinear process and measurement models x_dot = f(x,u,w) and y = h(x) + v. Linearize only about a declared trajectory and coordinate error definition.",
            "For a linear measurement, innovation is r = y - H x_minus and innovation covariance is S = H P_minus H^T + R.",
            "The Kalman gain K = P_minus H^T S^-1 minimizes posterior covariance under linear-Gaussian assumptions.",
            "Update x_plus = x_minus + Kr and use a numerically stable covariance form such as Joseph: P_plus = (I-KH)P_minus(I-KH)^T + KRK^T.",
            "Test filter consistency with normalized innovations and estimation error, then analyze closed-loop sensitivity S_c = 1/(1+L) and complementary sensitivity T_c = L/(1+L).",
        ],
        "Perform a scalar navigation update for one position measurement.",
        [
            "Prior position estimate = 100.0 m with variance P_minus = 25 m^2.",
            "Measurement = 106.0 m with noise variance R = 9 m^2.",
            "Measurement sensitivity H = 1 and no bias is modeled.",
        ],
        [
            "Innovation r = 106 - 100 = 6 m; S = 25 + 9 = 34 m^2.",
            "K = 25/34 = 0.7353.",
            "Posterior estimate = 100 + 0.7353(6) = 104.41 m.",
            "Posterior variance = (1-K)25 = 6.62 m^2, so one-sigma uncertainty falls from 5.00 m to 2.57 m.",
        ],
        "The update is mathematically consistent for the stated model. Repeated biased measurements, timing error, frame mismatch, or underestimated R can make the filter confidently wrong.",
        [
            "Covariance matrices remain symmetric positive semidefinite.",
            "Innovation statistics match predicted S over representative Monte Carlo trials.",
            "Estimator latency and uncertainty are included in closed-loop stability analysis.",
        ],
    ),
    "reliability": _studio(
        "Redundancy, dependence, and fault containment",
        (
            "Redundancy improves reliability only when failures are sufficiently independent and the voting, "
            "detection, isolation, recovery, power, timing, and software infrastructure do not introduce a "
            "larger common vulnerability."
        ),
        [
            "For independent identical components of reliability R, a two-out-of-three voter succeeds when exactly two or all three channels succeed.",
            "Therefore R_TMR = 3R^2(1-R) + R^3 = 3R^2 - 2R^3, before voter and infrastructure failures.",
            "Introduce common-cause probability q_c explicitly. A simple upper model is R_system = (1-q_c)R_TMR when common cause defeats all channels.",
            "Coverage C separates detected/recovered faults from dangerous undetected faults. Add voter, power, data bus, timing, software, and repair-state logic with a fault tree or state model.",
            "Use sensitivity and importance measures to find contributors whose uncertainty dominates the top event; numerical precision does not compensate for missing failure modes.",
        ],
        "Compare ideal triple modular redundancy with a small common-cause probability.",
        [
            "Each channel reliability for the mission phase R = 0.995.",
            "Common-cause probability q_c = 0.002.",
            "Assume a perfect voter only for the first calculation.",
        ],
        [
            "R_TMR = 3(0.995^2) - 2(0.995^3) = 0.999925.",
            "Independent-channel unreliability falls from 0.005 to 0.000075.",
            "With common cause, R_system = (1-0.002)(0.999925) = 0.997925.",
            "The common-cause term erases most of the ideal redundancy benefit and now dominates the risk.",
        ],
        "The practical priority is not adding a fourth identical channel. It is identifying and breaking shared causes, then modeling voter, coverage, power, timing, and software behavior.",
        [
            "Independence claims have architectural and test evidence.",
            "Mission time and failure/repair states match the operational phase.",
            "Fault injection exercises detection, isolation, recovery, and hazardous transitions.",
        ],
    ),
    "test": _studio(
        "Measurement uncertainty and test information",
        (
            "A test is valuable when it discriminates among models or retires a decision-relevant uncertainty. "
            "Instrumentation, sampling, calibration, synchronization, environment, and model discrepancy must "
            "be designed together rather than appended after the article is built."
        ),
        [
            "For derived y = f(x), linearized uncertainty is u_y^2 = J Sigma_x J^T + u_model^2, where J contains partial derivatives at the operating point.",
            "For a product y = ab with independent small errors, relative variance is approximately (u_y/y)^2 = (u_a/a)^2 + (u_b/b)^2.",
            "Sampling above twice the highest signal frequency is only the mathematical lower bound. Anti-alias filtering, transition band, phase, dynamic range, trigger uncertainty, and transients require margin.",
            "Use a likelihood p(data|theta) to compute parameter information and posterior uncertainty. Optimize the test condition for the decision, not simply for maximum sensor response.",
            "Separate repeatability, calibration bias, facility effects, configuration differences, and model-form discrepancy before extrapolating test evidence to flight.",
        ],
        "Propagate measurement uncertainty through a thrust estimate dominated by momentum flux.",
        [
            "Mass flow m_dot = 250 kg/s with 1.0 percent standard uncertainty.",
            "Effective exit velocity V_e = 2800 m/s with 0.5 percent standard uncertainty.",
            "Pressure-thrust estimate = 14 kN with independent 2 kN standard uncertainty.",
        ],
        [
            "Momentum thrust = m_dot V_e = 700 kN.",
            "Relative momentum uncertainty = sqrt(0.010^2 + 0.005^2) = 0.01118.",
            "Standard momentum uncertainty = 7.83 kN; total standard uncertainty = sqrt(7.83^2 + 2^2) = 8.08 kN.",
            "Total thrust = 714 kN with approximate 95 percent expanded uncertainty of +/-15.8 kN for coverage factor k = 1.96.",
        ],
        "Report 714 +/- 16 kN only with the stated confidence convention and assumptions. Correlated calibration, unsteady flow, alignment, facility correction, and model discrepancy can enlarge or bias the interval.",
        [
            "Every uncertainty component has units, distribution, correlation, and traceable basis.",
            "Sample rate and filters preserve the bandwidth needed for the stated claim.",
            "The test configuration and environment support the intended extrapolation.",
        ],
    ),
    "landing": _studio(
        "Powered-descent reachability and reserve",
        (
            "Reusable landing is a constrained reachability problem. Vehicle energy, thrust vector, throttle, "
            "engine response, attitude, propellant, terrain, navigation uncertainty, winds, and failure modes "
            "must remain inside a feasible corridor from entry interface through touchdown."
        ),
        [
            "For a vertical screening case with constant mass and maximum thrust-to-weight beta = T/(mg), upward net deceleration during a downward burn is a_net = (beta-1)g.",
            "Constant-acceleration kinematics give minimum altitude h_brake = V_d^2/[2(beta-1)g] when beta > 1. If beta <= 1, stopping is infeasible.",
            "Burn time is t = V_d/[(beta-1)g]. A first propellant estimate uses m_dot = T/(Isp g_0), but changing mass and throttle require integration.",
            "Add divert, attitude, ignition, engine buildup, landing-gear, sensor, terrain, and dispersions. The reserve constraint is Delta-v_available >= Delta-v_brake + Delta-v_divert + losses + protected reserve.",
            "Compute a reachable set under uncertainty and failures. A nominal trajectory is insufficient if the state estimate or engine response can leave the feasible set before the next guidance update.",
        ],
        "Estimate minimum braking altitude and propellant scale for a vertical booster descent.",
        [
            "Mass at ignition = 25,000 kg; downward speed = 260 m/s; thrust-to-weight beta = 1.80.",
            "Specific impulse = 282 s; use g = g_0 = 9.80665 m/s^2.",
            "Assume constant mass and thrust for the kinematic baseline.",
        ],
        [
            "Net deceleration = (1.80-1)9.80665 = 7.845 m/s^2.",
            "Minimum braking altitude = 260^2/[2(7.845)] = 4.31 km.",
            "Burn time = 260/7.845 = 33.1 s.",
            "Thrust = 1.80(25000)(9.80665) = 441 kN; m_dot = 441000/(282 x 9.80665) = 159.5 kg/s; constant-mass propellant scale = 5.28 t.",
        ],
        "Ignition at 4.31 km would have zero margin in an unrealistic model. Operational design must ignite higher and integrate changing mass, throttle, drag, attitude, engine transients, navigation error, divert, and protected reserves.",
        [
            "The model declares sign convention and rejects beta <= 1 as infeasible.",
            "Mass, thrust, and propellant integrate consistently through touchdown.",
            "Monte Carlo trajectories remain inside terrain, attitude, load, and reserve constraints.",
        ],
    ),
}


def math_studio_for(lab_type):
    """Return the mathematics studio for a module's laboratory domain."""
    return MATH_STUDIOS[lab_type]
