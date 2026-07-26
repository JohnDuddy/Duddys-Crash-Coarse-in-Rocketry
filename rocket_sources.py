"""Authoritative primary references used by the rocketry curriculum."""

ACCESSED = "2026-07-26"

SOURCES = {
    "seh": {
        "title": "NASA Systems Engineering Handbook, Revision 2",
        "agency": "NASA Office of the Chief Engineer",
        "publication": "NASA/SP-2016-6105 Rev2; web edition updated 2024-03-27",
        "url": "https://www.nasa.gov/reference/systems-engineering-handbook/",
        "note": "NASA's framework for system design, product realization, verification, validation, and technical management.",
    },
    "sp125": {
        "title": "Design of Liquid Propellant Rocket Engines, Second Edition",
        "agency": "NASA Technical Reports Server",
        "publication": "NASA SP-125; 1967-01-01",
        "url": "https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19710019929.pdf",
        "note": "Detailed engine-system design reference spanning thrust chambers, feed systems, cycles, controls, development, and flight application.",
    },
    "thrust": {
        "title": "General Thrust Equation for Rocket Engines",
        "agency": "NASA Glenn Research Center",
        "publication": f"Current NASA web reference; accessed {ACCESSED}",
        "url": "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/thrust-force/",
        "note": "Primary NASA explanation of momentum thrust, pressure thrust, equivalent exhaust velocity, and specific impulse.",
    },
    "rocket_equation": {
        "title": "Ideal Rocket Equation",
        "agency": "NASA Glenn Research Center",
        "publication": f"Current NASA web reference; accessed {ACCESSED}",
        "url": "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/",
        "note": "NASA derivation and interpretation of the variable-mass rocket equation and mass ratio.",
    },
    "nozzle": {
        "title": "Nozzle Design",
        "agency": "NASA Glenn Research Center",
        "publication": f"Current NASA web reference; accessed {ACCESSED}",
        "url": "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/nozzle-design/",
        "note": "Convergent-divergent nozzle behavior, choking, area ratio, exit state, and thrust consequences.",
    },
    "cea": {
        "title": "Chemical Equilibrium with Applications (CEA)",
        "agency": "NASA Software Catalog",
        "publication": f"LEW-20586-1 current release listing; accessed {ACCESSED}",
        "url": "https://software.nasa.gov/software/LEW-20586-1",
        "note": "NASA equilibrium chemistry and theoretical rocket-performance software for product composition and thermodynamic properties.",
    },
    "trajectory": {
        "title": "Trajectory Design",
        "agency": "NASA Ames Research Center",
        "publication": f"Current NASA engineering reference; accessed {ACCESSED}",
        "url": "https://www.nasa.gov/ames-engineering/spaceflight-division/flight-dynamics/trajectory-design/",
        "note": "NASA description of high-fidelity trajectory design with perturbations, constraints, and statistical uncertainty analysis.",
    },
    "trajectory_method": {
        "title": "General Methodology for Designing Spacecraft Trajectories",
        "agency": "NASA Technical Reports Server",
        "publication": "NASA Tech Brief MSC-23671-1/4209-1/4586-1; 2012-08-01",
        "url": "https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20120013239.pdf",
        "note": "Constrained nonlinear-equation and optimization formulation for broad classes of mission-design problems.",
    },
    "cislunar": {
        "title": "Astrodynamics Convention and Modeling Reference for Lunar, Cislunar, and Libration Point Orbits",
        "agency": "NASA Technical Reports Server",
        "publication": "NASA technical report; 2022",
        "url": "https://ntrs.nasa.gov/citations/20220014814",
        "note": "Coordinate systems, time systems, numerical integration, three-body approximations, and higher-fidelity cislunar modeling.",
    },
    "copernicus": {
        "title": "Copernicus Trajectory Design and Optimization System",
        "agency": "NASA Johnson Space Center",
        "publication": f"Version 5.4.1 page updated 2026-06-03; accessed {ACCESSED}",
        "url": "https://www.nasa.gov/general/copernicus/",
        "note": "NASA generalized trajectory optimization environment for planet, moon, libration-point, and interplanetary missions.",
    },
    "gnc": {
        "title": "Guidance, Navigation and Control Subsystems",
        "agency": "NASA Johnson Space Center",
        "publication": f"Current NASA engineering reference; accessed {ACCESSED}",
        "url": "https://www.nasa.gov/reference/jsc-guidance-navigation-control-subsystems/",
        "note": "NASA flight mechanics, trajectory, navigation, guidance, control, simulation, and mission-analysis capabilities.",
    },
    "materials": {
        "title": "Materials for Liquid Propulsion Systems",
        "agency": "NASA Technical Reports Server",
        "publication": "Book chapter M16-5345; 2018-08-01",
        "url": "https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20160008869.pdf",
        "note": "Materials response to cryogenic fluids, hot gas, thermal shock, reactive propellants, acoustics, and turbomachinery loads.",
    },
    "tps": {
        "title": "Pterodactyl: Thermal Protection System Design Methodology for a Flap Control System",
        "agency": "NASA Technical Reports Server",
        "publication": "NASA technical paper; 2021",
        "url": "https://ntrs.nasa.gov/citations/20210025489",
        "note": "Aerothermal anchoring and surface-resolved one-dimensional heat-transfer methodology for TPS sizing.",
    },
    "thermal": {
        "title": "NASA Passive Thermal Control Engineering Guidebook",
        "agency": "NASA Technical Reports Server",
        "publication": "NASA technical report, version 4; 2023",
        "url": "https://ntrs.nasa.gov/citations/20230013900",
        "note": "Thermal analysis, model correlation, hardware, materials, testing, and flight-operations practices.",
    },
    "engine_test": {
        "title": "Liquid Rocket Engine Test Data Acquisition and Performance Determination",
        "agency": "NASA Technical Reports Server",
        "publication": "AFRPL-TR-79-24; 1979",
        "url": "https://ntrs.nasa.gov/api/citations/19790022112/downloads/19790022112.pdf",
        "note": "Measurement and reduction methods for thrust, impulse, propellant flow, pressure, temperature, and exhaust composition.",
    },
    "faa450": {
        "title": "14 CFR Part 450: Launch and Reentry License Requirements",
        "agency": "Electronic Code of Federal Regulations",
        "publication": f"Current federal regulation; accessed {ACCESSED}",
        "url": "https://www.ecfr.gov/current/title-14/chapter-III/subchapter-C/part-450",
        "note": "Current U.S. licensing, system-safety, flight-safety, and public-risk requirements for commercial launch and reentry.",
    },
    "software": {
        "title": "NASA Software Engineering Requirements",
        "agency": "NASA Online Directives Information System",
        "publication": f"NPR 7150.2 current directive; accessed {ACCESSED}",
        "url": "https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7150&s=2",
        "note": "NASA software assurance, planning, implementation, testing, configuration, and safety-critical engineering requirements.",
    },
    "caib": {
        "title": "Columbia Accident Investigation Board Report, Volume I",
        "agency": "NASA Safety and Mission Assurance",
        "publication": "CAIB report; 2003-08",
        "url": "https://sma.nasa.gov/SignificantIncidents/assets/caib-report-vol1.pdf",
        "note": "Primary mishap investigation record connecting technical failure, organizational causes, decision processes, and safety culture.",
    },
}


def source_list(keys):
    return [{"id": key, **SOURCES[key]} for key in keys]

