"""Metadata for the module-specific interactive 3D engineering models."""


MODELS = {
    "architecture": {
        "title": "Exploded cislunar mission architecture",
        "description": "Rotate and separate the launch, transfer, and landing elements to inspect physical interfaces and mission handoffs.",
        "features": ["Launch stack", "Transfer stage", "Cargo lander", "Interface planes"],
    },
    "staging": {
        "title": "Multistage launch vehicle anatomy",
        "description": "Inspect the propellant volumes, dry structure, interstage, engines, payload, and changing centerline as stages separate.",
        "features": ["Stage volumes", "Interstage", "Engine clusters", "Payload fairing"],
    },
    "orbit": {
        "title": "Orbital geometry and transfer plane",
        "description": "Orbit a three-dimensional Earth model with reference axes, an inclined parking orbit, a transfer arc, and target orbit.",
        "features": ["Earth-fixed axes", "Inclined orbit", "Transfer arc", "Target orbit"],
    },
    "ascent": {
        "title": "Ascent corridor and attitude geometry",
        "description": "Follow the vehicle from vertical rise through pitch-over while inspecting velocity, thrust, atmosphere, and the max-q corridor.",
        "features": ["Earth curvature", "Pitch program", "Thrust axis", "Max-q corridor"],
    },
    "nozzle": {
        "title": "Cutaway thrust chamber and nozzle flow",
        "description": "Rotate a cutaway chamber, converging throat, expansion bell, injector face, and representative supersonic stream tubes.",
        "features": ["Injector face", "Chamber", "Sonic throat", "Expansion plume"],
    },
    "cycle": {
        "title": "Three-dimensional engine-cycle closure",
        "description": "Trace oxidizer and fuel paths through pumps, turbine, injector, chamber, and shafts while exposing power-transfer interfaces.",
        "features": ["Propellant pumps", "Turbine shaft", "Feed circuits", "Main chamber"],
    },
    "propulsion": {
        "title": "Propulsion family comparison bay",
        "description": "Compare chemical, electric, nuclear-thermal, and solar-sail hardware at a common visual scale with their energy paths exposed.",
        "features": ["Chemical nozzle", "Ion plume", "Reactor core", "Solar sail"],
    },
    "aero": {
        "title": "Aerodynamic load and shock geometry",
        "description": "Rotate the ascent vehicle inside a Mach cone with angle-of-attack, normal-force, bending, and flexible-mode overlays.",
        "features": ["Mach cone", "Load vectors", "Center of pressure", "Bending mode"],
    },
    "thermal": {
        "title": "Entry capsule thermal cutaway",
        "description": "Inspect shock layer, heat shield, insulation, pressure vessel, and bondline measurement locations during atmospheric entry.",
        "features": ["Shock layer", "Ablator", "Insulation", "Bondline sensors"],
    },
    "structure": {
        "title": "Cryogenic tank structural cutaway",
        "description": "Separate tank wall, insulation, domes, rings, stringers, ullage, and liquid volume to reveal competing structural and thermal paths.",
        "features": ["Pressure shell", "Ring frames", "Cryogenic volume", "Insulation"],
    },
    "gnc": {
        "title": "Guidance, navigation, and control frames",
        "description": "Rotate the rigid body with inertial, body, sensor, thrust, covariance, and control-authority geometry shown together.",
        "features": ["Body axes", "Sensor cones", "Covariance ellipsoid", "Control vectors"],
    },
    "reliability": {
        "title": "Fault-containment architecture",
        "description": "Inspect three redundant compute lanes, voter, power domains, sensors, actuators, and the shared paths that create common cause.",
        "features": ["Compute lanes", "Voting plane", "Power domains", "Shared interfaces"],
    },
    "test": {
        "title": "Propulsion test article and instrumentation",
        "description": "Rotate the test stand, engine, thrust structure, plume, transducers, optical paths, and data-acquisition boundaries.",
        "features": ["Thrust stand", "Engine article", "Sensor stations", "Plume diagnostics"],
    },
    "landing": {
        "title": "Powered-landing reachable corridor",
        "description": "Inspect the descending booster, thrust cone, divert envelope, landing legs, terrain plane, and touchdown dispersion volume.",
        "features": ["Braking corridor", "Thrust cone", "Divert envelope", "Touchdown zone"],
    },
}


def model_for(lab_type):
    """Return the 3D model metadata for a module's laboratory domain."""
    return MODELS[lab_type]
