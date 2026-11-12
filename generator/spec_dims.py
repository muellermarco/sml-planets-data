"""Dimensions and queryable attributes for the planets_data model."""

F_PLANET = "Planet Record"
F_ORBIT = "Orbital Properties"
F_PHYS = "Physical Properties"
F_DERIVED = "Derived Planet Quantities"
F_HOST = "Host Star Snapshot"
F_QUAL = "Measurement Quality"
F_PCLASS = "Planet Classifications"
F_OBS = "Survey Observations"
F_STAR = "Star Record"
F_SYSTEM = "Star System Summary"
F_SFORM = "Stellar Formula Measures"
F_COORD = "Sky Coordinates"
F_SURVEY = "Survey Facility"

ASK = ("")  # no-cheat: closed-question / re-ask boilerplate removed

CONSTANTS = ("Physical constants are the standard published values, written out "
             "and composed inside the formula rather than pre-multiplied: G = "
             "6.67430E-11, solar mass 1.98847E30 kg, solar radius 6.957E8 m, "
             "astronomical unit 1.496E11 m, Jupiter mass 1.898E27 kg, Jupiter "
             "radius 7.1492E7 m, 109.2 Earth radii per solar radius.")

FLAG = ("'Yes' when the flag is 1, 'No' when the flag is recorded and not 1 "
        "(0 or -1), null when no flag is recorded - so filtering on 'No' keeps "
        "exactly the planets whose flag is present and differs from 1, and "
        "excludes the unknown ones.")

PD = "Planet Detail"
SD = "Star Detail"
OD = "Planet Observation"
FD = "Survey Facility Detail"


def prof(unique_name, folder, dataset, key, description, secondaries):
    return {
        "unique_name": unique_name, "label": unique_name, "folder": folder,
        "dataset": dataset, "is_degenerate": True, "description": description,
        "levels": [{
            "unique_name": f"{unique_name} Key", "label": f"{unique_name} Key",
            "key_columns": [key], "name_column": key, "is_hidden": True,
            "secondaries": secondaries,
        }],
    }


DIMENSIONS = [
    {
        "unique_name": "Planet Record",
        "label": "Planet Record",
        "folder": F_PLANET,
        "dataset": PD,
        "description": (
            "A confirmed exoplanet - the grain of this model's fact, 3372 rows. "
            "This is a clean star schema: the orbital record covers 3371 "
            "planets, the physical record 3359 and the data-quality record all "
            "3372, and each is exactly 1:1 with a planet, so all three fold "
            "onto this row. Every planet names a host star and every host "
            "resolves; 2509 distinct stars carry 1 to 7 planets each. "
            "COVERAGE IS THE FIRST THING TO CHECK because the physical "
            "measurements are far sparser than the orbital ones: a period "
            "exists for 3305 planets, a radius for 2694, a semi-major axis for "
            "1897, a mass for 1174, an eccentricity for 974, an inclination for "
            "502 and a density for only 388. Every derived quantity inherits "
            "the scarcest input it needs, so the surface gravity and the escape "
            "velocity exist for 509 planets and the equilibrium temperature for "
            "1533."),
        "levels": [
            {
                "unique_name": "Discovery Method",
                "label": "Discovery Method",
                "key_columns": ["discovery_method"],
                "name_column": "discovery_method",
                "description": (
                    "The knowledge base defines the Transit Timing Variation (TTV) method as a planet whose observation record is linked to the 'ttv' facility - that is TTV Observation (1 on 225 planets), not this column's 'TTV' category (15 planets); a planet found or discovered via timing variations or the TTV method reads TTV Observation = 1. "
                    "Standardised discovery method - how the planet was found. "
                    "Six categories on all 3372 planets: Transit "
                    "2664, Radial Velocity 591, Imaging 42, Microlensing 39, "
                    "Other 21 and TTV 15. The RAW column holds 38 different "
                    "spellings of these six, so grouping by the stored text "
                    "splits Transit across five buckets - 'Photometric' 578, "
                    "'TR' 536, 'Transit Method' 523, 'Photometry' 516 and "
                    "'Transit' 511. Membership is EXACT, matching the label "
                    "lists the knowledge base gives: Radial Velocity covers "
                    "RadVel, RV, RV Method, Radial Velocity and Doppler; "
                    "Transit covers Transit, TR, Transit Method, Photometry and "
                    "Photometric; Imaging covers Direct Imaging, DI, Imaging, "
                    "IMG and Direct; TTV covers TTV, TTV Method, Transit "
                    "Timing, Transit Timing Variations and Timing Var; and "
                    "Microlensing covers Microlensing, ML, Lensing, "
                    "Gravitational and a Greek-mu abbreviation. A substring "
                    "reading would pull other timing labels into TTV, which "
                    "those lists do not. Anything "
                    "outside the five named groups is 'Other'."),
                "secondaries": [],
            },
            {
                "unique_name": "Planet",
                "label": "Planet",
                "key_columns": ["planet"],
                "name_column": "planet_name",
                "is_unique_key": True,
                "description": (
                    "A planet, keyed on its record number and displayed as the "
                    "host star name followed by its companion letter - planet "
                    "name, planet ID. THREE printable identifications of a "
                    "planet exist here and they are DIFFERENT strings: this "
                    "combined name (3372 distinct values, e.g. Kepler-57 b, "
                    "HD 209458 b, 55 Cnc e), Planet Host Star Name on its own "
                    "(2509 distinct values, shared by the 1433 planets whose "
                    "host carries more than one planet row), and Companion "
                    "Letter on its own ('b' on 2504 of the 3372). The "
                    "warehouse stores only the last two and never the "
                    "combination, which is built here. If the question's wording does not settle which, ask the user which they mean by a planet's name: this combined host-star-and-letter name (3372 distinct), Planet Host Star Name alone (2509 distinct) or Companion Letter alone ('b' on 2504 of 3372). Whether the star's name prints before or after it is likewise the caller's. A list of planets has no inherent row order either; which column orders it is the caller's whenever that is unstated. If the caller declines to "
                    "choose a name form and the star's name is asked for as its "
                    "own column, the planet's name is Companion Letter beside "
                    "Planet Host Star Name, since this combined name would repeat "
                    "the star's name."),
                "secondaries": [
                    ("Planet Host Star Name", "host_star_name", F_PLANET,
                     "Name of the planet's host star, carried onto the planet "
                     "row. 2509 distinct values over 3372 planets, e.g. 11 Com, "
                     "14 Her, 55 Cnc. It names the STAR, not the planet: 1433 "
                     "planets share theirs with a sibling. It is one of the "
                     "two name columns the warehouse itself stores, and Planet "
                     "Name is this one with Companion Letter appended."),
                    ("Companion Letter", "companion_letter", F_PLANET,
                     "Letter distinguishing the planet within its system - "
                     "companion letter. Seven values on all 3372 planets: 'b' "
                     "on 2504, 'c' on 572, 'd' on 192, 'e' on 71, 'f' on 24, "
                     "'g' on 6 and 'h' on 3. Lower case, so a filter written as "
                     "'B' matches nothing. With Planet Host Star Name it is "
                     "the other of the two name columns the warehouse stores, "
                     "and printed beside a host star's name it identifies the "
                     "planet exactly, without the combined Planet Name. When the "
                     "caller declines to choose a name form and the question asks "
                     "for the planet's name AND its star's name as separate "
                     "columns, print this letter as the planet's name beside "
                     "Planet Host Star Name as the star - the combined Planet "
                     "Name would repeat the star's name in the planet column."),
                    ("Note Count", "note_count", F_PLANET,
                     "How many notes are attached to the planet record. 0 to 3 "
                     "on all 3372 planets, averaging 0.705."),
                    ("Discovery Method Stored", "discovery_method_stored",
                     F_PLANET,
                     "The discovery method exactly as stored, in one of 38 "
                     "spellings. Published for a question explicitly about the "
                     "raw label; for analysis group by Discovery Method."),
                    ("Record Update Date", "record_update_date", F_PLANET,
                     "Date the planet's record was last updated. Present on all "
                     "3372 planets with 82 distinct dates from 2014-05-14 to "
                     "2016-08-12. The column meaning says the range ends "
                     "2016-07-07; the stored data runs five weeks later. It is a "
                     "real date column, not text."),
                    ("Record Update Year", "record_update_year", F_PLANET,
                     "Calendar year of the last update. 2014, 2015 or 2016 on "
                     "all 3372 planets."),
                ],
            },
        ],
    },
    {
        "unique_name": "Star Record",
        "label": "Star Record",
        "folder": F_STAR,
        "dataset": SD,
        "description": (
            "A host star - 2509 rows, every one of them hosting at least one "
            "planet. Coverage again decides the answers: a distance exists for "
            "1996 stars, a temperature for 2379, a mass for 2357, a magnitude "
            "and a photometric band for 2400, a radius for 2228, and therefore a "
            "luminosity for 2207 and a density for 2117. The star's own "
            "companion count and the number of planet rows it actually carries "
            "agree on all but ONE star, so the two readings of 'multi-planetary' "
            "differ by a single row."),
        "levels": [
            {
                "unique_name": "Star",
                "label": "Star",
                "key_columns": ["star"],
                "name_column": "star_name",
                "is_unique_key": True,
                "description": (
                    "Host star, keyed on its record number and displayed by "
                    "name - star, host, catalogue name. 2509 distinct names, "
                    "e.g. 11 Com, 55 Cnc, alf Tau, PSR J1719-1438. Names are "
                    "stored in catalogue form, so 'alf Tau' rather than "
                    "'Aldebaran'."),
                "secondaries": [
                    ("Stellar Distance Parsecs", "stellar_distance_pc", F_STAR,
                     "Distance to the star in parsecs - distance, how far away. "
                     "3.21 to 8500 pc on the 1996 stars that record one, "
                     "averaging 660.4. One parsec is about 3.26 light-years."),
                    ("Stellar Distance Light Years", "stellar_distance_ly",
                     F_STAR,
                     "The Distance in Light-Years - the parsec figure multiplied "
                     "by 3.26156. 10.47 to 27723 ly on 1996 stars, averaging "
                     "2153.8."),
                    ("Star Companion Count", "companion_count", F_STAR,
                     "Number of confirmed planetary companions the star record "
                     "declares - companion count. 1 to 7 on all 2509 stars, "
                     "averaging 1.344. More than 1 is the multi-planetary "
                     "condition, met by 569 stars."),
                    ("Stellar Mass", "stellar_mass", F_STAR,
                     "Mass of the star in solar masses. 0.02 to 3.9 on the 2357 "
                     "stars that record one, averaging 1.000 - so the typical "
                     "host is Sun-like."),
                    ("Stellar Radius", "stellar_radius", F_STAR,
                     "Radius of the star in solar radii. 0.04 to 51.1 on 2228 "
                     "stars, averaging 1.610."),
                    ("Stellar Temperature", "stellar_temperature", F_STAR,
                     "Effective surface temperature in Kelvin. 575 to 57000 K "
                     "on 2379 stars, averaging 5545 - just below the Sun's "
                     "5778 K, which is the reference this model uses for the "
                     "luminosity formula."),
                    ("Optical Magnitude", "optical_magnitude", F_STAR,
                     "Apparent visual magnitude of the star as seen from Earth - an observed magnitude, not a luminosity. 0.85 to 20.15 on 2400 stars, averaging 12.89. The scale is INVERTED and logarithmic, so the smallest number is the star that looks brightest, and 'the brightest star' means the MINIMUM of this column, not the maximum. A star's intrinsic output relative to the Sun is "
                     "Stellar Luminosity (Intrinsic Brightness, Solar Units)."),
                    ("Photometric Band", "photometric_band", F_STAR,
                     "Photometric band the magnitude was measured through, folded "
                     "to one spelling per band. The labels 'Johnson V', "
                     "'Kepler' and 'K-band' are THIS MODEL'S OWN spellings, so "
                     "a question that prints band names has its own wording to "
                     "supply. Three labels here: Kepler (1306 stars), Johnson V (779) and K-band (315, stored one way only); Photometric Band (Folded Groups Only) is the two-group reading that nulls K-band and the 109 stars with no band. "
                     "The raw column holds 10 spellings. "
                     "This reading folds 'V-band' into "
                     "Johnson V; the column meaning lists 'V-band' AFTER the "
                     "Johnson group rather than inside it, and the stricter "
                     "reading that keeps it separate is published beside this "
                     "one - it moves a block of stars. Photometric Band (Folded Groups "
                     "Only) keeps just the two folded groups, labelled 'V-Band' "
                     "and 'Kepler-Band', with K-band null."),
                    ("Photometric Band Strict", "photometric_band_strict",
                     F_STAR,
                     "The same folding but with 'V-band' kept as its own "
                     "category."),
                    ("Photometric Band (Folded Groups Only)",
                     "photometric_band_group", F_STAR,
                     "Only the two bands the warehouse spells several ways, each "
                     "folded to one label: 'V-Band' for the Johnson/V spellings, "
                     "V-band included, and 'Kepler-Band' for the Kepler "
                     "spellings. K-band, stored one way only, and the stars "
                     "with no band are null here, so a count of stars by this "
                     "column has exactly two groups. Use it when a question asks "
                     "to consolidate the spellings into groups and count the "
                     "stars in each; Photometric Band keeps K-band as a third "
                     "label and Photometric Band Strict keeps 'V-band' apart."),
                    ("Photometric Band Stored", "photometric_band_stored",
                     F_STAR,
                     "The photometric band exactly as stored, in one of 10 "
                     "spellings: Kepler, Kep-b, Kepler-band, K-band, Kep, V, "
                     "V (Johnson), V-band, Johnson, Johnson V (in descending "
                     "order of frequency). Folding these by hand in a CASE "
                     "reproduces what the folded attributes already publish - "
                     "prefer Photometric Band (Folded Groups Only), Photometric "
                     "Band or Photometric Band Strict, and note their shared "
                     "fork: whether K-band, which has nothing to fold, appears "
                     "in a consolidated report is a choice to put to the user "
                     "explicitly."),
                ],
            },
        ],
    },
    {
        "unique_name": "Survey Facility",
        "label": "Survey Facility",
        "folder": F_SURVEY,
        "dataset": FD,
        "description": (
            "An observing survey or mission - only THREE rows. They are the "
            "three flags the source catalogue carried: 'kep' for the Kepler "
            "mission, 'k2' for the K2 mission and 'ttv' for the transit-timing "
            "survey. The observation bridge holds 2683 rows over 2460 "
            "planets, so 912 of the 3372 planets were observed by none of the "
            "three and no planet was observed by more than two. By facility: 'kep' on 2329 observations over 1644 stars, 'ttv' on 225 observations and 'k2' on 129 over 94 stars."),
        "levels": [
            {
                "unique_name": "Facility Name",
                "label": "Facility Name",
                "key_columns": ["facility"],
                "name_column": "facility",
                "is_unique_key": True,
                "description": (
                    "Survey or mission that made the observation - facility, "
                    "survey, telescope, mission. Exactly three stored values, "
                    "all lower case: 'kep', 'k2' and 'ttv'. A filter written as "
                    "'Kepler' or 'K2' matches nothing - use the stored codes, or "
                    "read Facility Description for the expansion."),
                "secondaries": [
                    ("Facility Description", "facility_description", F_SURVEY,
                     "What the facility code stands for: 'kep' is the Kepler "
                     "mission, 'k2' is the K2 mission and 'ttv' is the transit-timing "
                     "survey. Published because the stored codes are "
                     "opaque abbreviations."),
                    ("Facility Key", "facility_key", F_SURVEY,
                     "Numeric identifier of the facility - 1, 2 or 3."),
                ],
            },
        ],
    },
]

# --------------------------------------------------------------------------- #
# planet profiles
# --------------------------------------------------------------------------- #
DIMENSIONS.append(prof(
    "Orbital Profile", F_ORBIT, PD, "planet",
    "The planet's orbit, from the orbital record that covers 3371 of the 3372 "
    "planets - though its individual columns are much sparser than that.",
    [
        ("Orbital Period", "orbital_period_days", F_ORBIT,
         "Time to complete one orbit, in DAYS as the warehouse records it - "
         "orbital period, year length, length of a year. 0.0907 to 7,300,000 "
         "days on the 3305 planets that record one, averaging 2726. The range "
         "spans eight orders of magnitude, so an unweighted mean is dominated "
         "by a handful of very wide orbits. Below 10 days is the short-period "
         "condition, met by 1445 planets. A twin, Orbital Period (Years), "
         "divides by 365.25; the recorded days are what a plain reading of the "
         "warehouse reports, and the twin is the input Kepler's third law "
         "needs."),
        ("Orbital Period (Years)", "orbital_period_years", F_ORBIT,
         "The recorded period divided by 365.25, in years. 0.000248 to 19986 "
         "years, averaging 7.463. It is the denominator in the Kepler's-law mass "
         "check, which needs years rather than days; for the period itself use "
         "Orbital Period, which carries the recorded days."),
        ("Semi Major Axis AU", "semi_major_axis_au", F_ORBIT,
         "Mean orbital distance in astronomical units - semi-major axis, "
         "orbital distance. 0.0044 to 2500 AU on only 1897 planets, averaging "
         "7.70. Its sparseness is the binding constraint on the equilibrium "
         "temperature, the orbital velocity, the habitable-zone test and the "
         "Kepler's-law check."),
        ("Eccentricity", "eccentricity", F_ORBIT,
         "How far the orbit departs from a circle - eccentricity, how weird the "
         "orbit is. 0 to 0.956 on 974 planets, averaging 0.171. Zero is a "
         "perfect circle; above 0.25 is the high-eccentricity condition, met by "
         "249 planets."),
        ("Inclination Degrees", "inclination_degrees", F_ORBIT,
         "Orbital inclination in degrees - inclination, orbital tilt. 17.6 to "
         "90.76 degrees on only 502 planets, averaging 85.9. The maximum is "
         "90.76, barely above the 90-degree retrograde threshold, so only 8 "
         "planets in the whole catalogue orbit retrograde on the strict "
         "reading - and 21 more sit at exactly 90.0 degrees, edge-on, which "
         "is why Retrograde Orbit (90 Degrees Or More) ships beside "
         "Retrograde Orbit."),
        ("Next Planet Period Days", "next_planet_period_days", F_ORBIT,
         "Orbital period of the next planet outward in the same system, in "
         "days. Present for 861 planets - those with at least one longer-period "
         "sibling. Null for the outermost planet of every system and for every "
         "single-planet system."),
        ("Next Planet Period Ratio", "next_planet_period_ratio", F_ORBIT,
         "The next planet's period divided by this one's - the Orbital Period "
         "Ratio for this adjacent pair. 1.006 to 4482 on 861 planets, averaging "
         "20.36. Adjacent pairs are taken in order of period within each host "
         "star."),
    ]))

DIMENSIONS.append(prof(
    "Physical Profile", F_PHYS, PD, "planet",
    "The planet's mass, size and density, from the physical record that covers "
    "3359 planets - but a mass exists for only 1174 and a density for 388, and "
    "those two numbers bound most of the classifications in this model.",
    [
        ("Planet Mass Jupiter", "planet_mass_jupiter", F_PHYS,
         "Mass in Jupiter masses - mass, planet mass. 0.00006 to 28.5 on only "
         "1174 of the 3372 planets, averaging 2.628. Above 0.1 is the gas-giant "
         "condition, met by 929 planets. Earth is about 0.003 Jupiter masses."),
        ("Planet Mass Earth", "planet_mass_earth", F_PHYS,
         "The Planet Mass in Earth Units - the Jupiter figure "
         "multiplied by 317.83. 0.0191 to 9058 "
         "on 1174 planets, averaging 835.4. Between 1 and 10 is half the "
         "super-Earth condition."),
        ("Planet Radius Jupiter", "planet_radius_jupiter", F_PHYS,
         "Radius in Jupiter radii - radius, size. 0.027 to 6.9 on 2694 planets, "
         "averaging 0.342. Earth is about 0.09 Jupiter radii."),
        ("Planet Radius Earth", "planet_radius_earth", F_PHYS,
         "The Planet Radius in Earth Units - the Jupiter figure "
         "multiplied by 11.209. 0.303 to 77.3 "
         "on 2694 planets, averaging 3.833."),
        ("Planet Density", "planet_density", F_PHYS,
         "Bulk density in grams per cubic centimetre - density. 0.03 to 77.7 on "
         "only 388 of the 3372 planets, averaging 2.559. Above 3 is the rocky "
         "condition, met by 74 planets; below 0.5 with a giant mass is the "
         "inflated condition, met by 103. Earth is about 5.5. Because a density "
         "exists for so few planets, EVERY rocky, super-Earth, inflated-giant "
         "and potentially-habitable answer is bounded by 388 rows."),
    ]))

DIMENSIONS.append(prof(
    "Derived Quantity Profile", F_DERIVED, PD, "planet",
    "Every knowledge-base formula that lands on a planet, as a queryable "
    "attribute, each evaluated in consistent SI units from the standard "
    "physical constants written out in full. Velocities carry kilometres per "
    "second under the bare name with a metres-per-second twin; the transit "
    "depth is a fraction with a percent twin.",
    [
        ("Surface Gravity", "surface_gravity", F_DERIVED,
         "Planet Surface Gravity relative to Earth's - mass in Earth units over radius "
         "in Earth units squared. 0.0052 to 1254.7 on the 509 planets that have "
         "BOTH a mass and a radius, averaging 22.23. Earth is 1 by "
         "construction."),
        ("Mass Radius Ratio", "mass_radius_ratio", F_DERIVED,
         "Mass in Earth units divided by radius in Earth units - the mass-radius relationship. 0.0323 to 2742 on the same 509 planets, averaging 81.3."),
        ("Escape Velocity", "escape_velocity_kms", F_DERIVED,
         "Planet Escape Velocity - the speed needed to escape the planet, in KILOMETRES PER SECOND: the square root of twice G times the mass over the radius, with the Jupiter-unit mass and radius converted to kilograms and metres, divided by 1000. From 2.009 km/s on the 509 planets with both a mass and a radius, averaging 66.96. The twin Escape Velocity (Metres Per Second) is the "
         "same figure times 1000. " + CONSTANTS),
        ("Escape Velocity (Metres Per Second)", "escape_velocity_ms",
         F_DERIVED,
         "The same escape velocity in metres per second, as the SI formula "
         "yields it before dividing by 1000. 2009 to 585,451 m/s on 509 "
         "planets, averaging 66,962."),
        ("Orbital Velocity", "orbital_velocity_kms", F_DERIVED,
         "Mean orbital speed assuming a circular orbit, in KILOMETRES PER "
         "SECOND - orbital velocity, speed. The square root of G times the "
         "stellar mass over the semi-major axis, with the solar-unit mass and "
         "the AU converted to kilograms and metres, divided by 1000. 0.235 to "
         "531.29 km/s on the 1593 planets with both a stellar mass and a "
         "semi-major axis, averaging 82.09. The twin Orbital Velocity (Metres "
         "Per Second) is the same figure times 1000. A listing that asks for "
         "the planets' speed lists only the planets that have one - filter "
         "this column IS NOT NULL - because a planet with no recorded "
         "semi-major axis has no velocity and does not belong in a speed "
         "report; filtering on the classification flags alone leaves such a "
         "planet in as a blank row. " + CONSTANTS),
        ("Orbital Velocity (Metres Per Second)", "orbital_velocity_ms",
         F_DERIVED,
         "The same orbital velocity in metres per second, as the SI formula "
         "yields it. 235 to 531,293 m/s on 1593 planets, averaging 82,094."),
        ("Equilibrium Temperature", "equilibrium_temperature", F_DERIVED,
         "The Planetary Equilibrium Temperature in KELVIN - the stellar temperature times the square root of the stellar radius over twice the semi-major axis, with the radius in solar radii and the axis in AU both converted to metres so the ratio under the root is dimensionless. From 2.94 K on the 1533 planets with all three inputs, averaging 886.7 K. A reading that "
         "leaves solar radii over AU unconverted is about 14.7 times larger "
         "and is not published, because a formula over two lengths is a "
         "formula over one unit. " + CONSTANTS),
        ("Transit Depth", "transit_depth", F_DERIVED,
         "Fractional drop in the star's brightness during a transit - the "
         "planet radius over the stellar radius, squared, both radii in EARTH "
         "radii (the planet radius times 11.209, the stellar radius times "
         "109.2). A FRACTION from 0 to 1: 1.3e-05 to 1.135 on the 2684 planets "
         "with both radii, averaging 0.00294. The twin Transit Depth (Percent) "
         "is the same figure times 100; whether a question wants the fraction "
         "or the percent is the caller's to decide, so ask when it is not "
         "said. " + CONSTANTS),
        ("Transit Depth (Percent)", "transit_depth_percent", F_DERIVED,
         "The same transit depth as a PERCENTAGE - the fraction times 100. 0.0013 to 113.47 on 2684 planets, averaging 0.294."),
        ("Planet Star Mass Ratio", "planet_star_mass_ratio", F_DERIVED,
         "Planet mass divided by stellar mass, both in kilograms - the mass "
         "ratio. 1.9e-07 to 0.700 on the 1127 planets with both, averaging "
         "0.00586. The planet mass is Jupiter masses times 1.898E27 and the "
         "stellar mass solar masses times 1.98847E30, because the knowledge "
         "base requires both masses in the same units; the ratio is a pure "
         "number. Kepler-131 c, the super-Earth with the strongest surface "
         "gravity, reads 2.433e-05."),
        ("Kepler Derived Stellar Mass", "kepler_derived_stellar_mass",
         F_DERIVED,
         "Stellar mass in solar masses derived from the planet's orbit - the "
         "semi-major axis in AU cubed over the period in YEARS squared. 0.0233 "
         "to 3.915 on 1831 planets, averaging 1.019. Null on the other 1541 "
         "planets, whose period or semi-major axis is unrecorded. A comparison "
         "of the recorded mass with this derived one runs over the planets that "
         "carry a derived value, so filter this column IS NOT NULL: a planet "
         "picked by its semi-major axis - the outermost of a system, say - can "
         "still lack a period, and without the filter it prints a blank derived "
         "mass as a row of its own. The recorded Host Stellar Mass is "
         "independent of this: 1517 of "
         "the 1541 with no derived mass carry a recorded host mass, and 297 of "
         "the 1831 with a derived mass have no recorded one, so a condition on "
         "the recorded mass is a different screen from a condition on this "
         "one. The period must be converted from days to years for this to "
         "work; using days gives a number about 133,000 times too small."),
        ("Kepler Mass Difference", "kepler_mass_difference", F_DERIVED,
         "The Kepler-derived stellar mass minus the mass the star record "
         "reports, signed. -0.889 to 1.019 on the 1534 planets where both "
         "exist, averaging 0.0139 - so the law checks out on average, with "
         "individual disagreements up to about one solar mass. Kepler Mass "
         "Absolute Difference drops the sign for ranking by how far apart the "
         "two are."),
        ("Kepler Mass Absolute Difference", "kepler_mass_absolute_difference",
         F_DERIVED,
         "How far the Kepler-derived stellar mass is from the recorded one, "
         "regardless of direction - the absolute discrepancy, the size of the "
         "disagreement. 0 to 1.019 solar masses on 1534 planets, averaging "
         "0.0501. The natural sort key when recorded and derived masses are "
         "compared side by side; null where the star has no recorded mass, "
         "and such rows still carry a derived mass."),
        ("Goldilocks Value", "goldilocks_value", F_DERIVED,
         "How centred the planet is in its star's habitable zone - the "
         "semi-major axis minus the inner boundary, over the width of the zone. "
         "-2.27 to 21361 on 1533 planets, averaging 15.58. A value of 0.5 is "
         "perfectly centred, between 0 and 1 is inside the zone, negative is "
         "too close to the star and above 1 too far. The huge maximum reflects "
         "planets thousands of times further out than their zone."),
        ("Planet Distance Light Years (All Recorded)", "stellar_distance_ly", F_DERIVED,
         "Distance to the planet's host star in light-years, converting parsecs "
         "by multiplying by 3.26156. 10.47 to 27723 ly on the 2296 planets whose "
         "star records a distance, averaging 2035. Carries every recorded "
         "distance whatever its quality flags say; Planet Distance Light Years is the same figure nulled wherever a quality "
         "flag is raised."),
        ("Planet Distance Light Years",
         "stellar_distance_ly_clean", F_DERIVED,
         "Distance to the planet's host star in light-years, kept only when "
         "neither of the warehouse's two ever-set quality flags is raised on "
         "the measurement - the distance is not an upper limit (Distance Upper "
         "Limit = 'No') and the magnitude is not blended (Magnitude Blended = "
         "'No') - and null otherwise, including when either flag is missing. "
         "Present on 2283 planets, averaging 2041.2 ly; Planet Distance Light Years (All Recorded) carries every recorded distance, flag-clean or not, 2296 planets averaging 2035."),
        ("Planet Distance Parsecs", "stellar_distance_pc", F_DERIVED,
         "Distance to the planet's host star in parsecs. 3.21 to 8500 pc on "
         "2296 planets, averaging 623.9."),
    ]))

DIMENSIONS.append(prof(
    "Host Star Snapshot", F_HOST, PD, "planet",
    "The host star's properties carried onto the planet row, so a planet-level "
    "question does not need a join. These are the same values the Star Record "
    "dimension publishes; use these when filtering or projecting alongside "
    "planet measures and the Star Record dimension when the question groups "
    "stars.",
    [
        ("Host Stellar Mass", "host_stellar_mass", F_HOST,
         "Host star's mass in solar masses. 0.02 to 3.9 on 3051 of the 3372 "
         "planets, averaging 0.982."),
        ("Host Stellar Radius", "host_stellar_radius", F_HOST,
         "Host star's radius in solar radii. 0.04 to 51.1 on 3015 planets, "
         "averaging 1.482."),
        ("Host Stellar Temperature", "host_stellar_temperature", F_HOST,
         "Host star's effective temperature in Kelvin. 575 to 57000 on 3205 "
         "planets, averaging 5545."),
        ("Host Stellar Luminosity", "host_stellar_luminosity", F_HOST,
         "Host star's luminosity relative to the Sun - the radius squared times "
         "the temperature over 5778 to the fourth power. 7.9e-07 to 631 on 2978 "
         "planets, averaging 4.760."),
        ("Habitable Zone Inner AU", "habitable_zone_inner_au", F_HOST,
         "Habitable Zone Inner Boundary in AU - the square root "
         "of the luminosity over 1.1. 0.00085 to 23.95 on 2978 planets, "
         "averaging 1.212."),
        ("Habitable Zone Outer AU", "habitable_zone_outer_au", F_HOST,
         "Outer edge of the habitable zone in AU - the square root of the "
         "luminosity over 0.53. 0.00122 to 34.50 on 2978 planets, averaging "
         "1.747."),
        ("Planet Companion Count", "companion_count", F_HOST,
         "Number of planetary companions the host star declares. 1 to 7 on all "
         "3372 planets, averaging 1.765. More than 1 puts the planet in a "
         "multi-planetary system, which is true for 1431 of the 3372 planets."),
    ]))

DIMENSIONS.append(prof(
    "Measurement Quality Profile", F_QUAL, PD, "planet",
    "Relative uncertainties, limit flags and blend flags. Read the populations "
    "before using any of these: on this warehouse almost every blend flag and "
    "almost every upper-limit flag is zero, so the concepts they express select "
    "nobody, and the model says so rather than leaving the emptiness to be "
    "discovered.",
    [
        ("Period Relative Uncertainty", "period_relative_uncertainty", F_QUAL,
         "Relative uncertainty in the orbital period, as a percentage - half the "
         "spread between the positive and negative errors, over the value, "
         "times 100. 0 to 475.5 percent on 3180 planets, averaging 0.755. Below "
         "5 percent is the high-precision condition, met by 3125 planets."),
        ("Mass Relative Uncertainty", "mass_relative_uncertainty", F_QUAL,
         "Relative uncertainty in the planet mass, as a percentage. 0.198 to "
         "7990 percent on 987 planets, averaging 30.3. Only 198 planets are "
         "under 5 percent, which makes mass the binding constraint on the "
         "well-characterized test."),
        ("Radius Relative Uncertainty", "radius_relative_uncertainty", F_QUAL,
         "Relative uncertainty in the planet radius, as a percentage. 0 to 3899 "
         "percent on 2656 planets, averaging 17.9. 395 planets are under 5 "
         "percent."),
        ("Semi Major Relative Uncertainty",
         "semi_major_relative_uncertainty", F_QUAL,
         "Relative uncertainty in the semi-major axis, as a percentage. 0 to 100 "
         "percent on 1019 planets, averaging 4.93."),
        ("Eccentricity Relative Uncertainty",
         "eccentricity_relative_uncertainty", F_QUAL,
         "Relative uncertainty in the eccentricity, as a percentage. 0.059 to "
         "12550 percent on 690 planets, averaging 74.2 - by far the least "
         "precisely known parameter, because the values themselves are small."),
        ("Inclination Relative Uncertainty",
         "inclination_relative_uncertainty", F_QUAL,
         "Relative uncertainty in the inclination, as a percentage. 0.0022 to "
         "125 percent on 472 planets, averaging 1.50."),
        ("Density Relative Uncertainty", "density_relative_uncertainty",
         F_QUAL,
         "Relative uncertainty in the density, as a percentage. 1.59 to 2084 "
         "percent on 378 planets, averaging 44.3."),
        ("Mass Source", "mass_source", F_QUAL,
         "How the mass was determined - mass provenance. 'Mass' on 611 planets, "
         "'Msini' on 554 and 'Msin(i)/sin(i)' on 9, with null on 2198. 'Msini' "
         "means the value is a MINIMUM mass because the inclination is unknown, "
         "which is what a radial-velocity measurement gives."),
        ("Minimum Mass Status", "minimum_mass_status", F_QUAL,
         "Whether the mass is a minimum rather than a true mass - the "
         "minimum-mass status. 'Yes' on 554 planets, 'No' on 620 and null on the "
         "2198 with no mass at all. So a mass estimate exists for 1174 planets "
         "and nearly half of those are lower bounds."),
        ("Period Limit Flag", "period_limit_flag", F_QUAL,
         "Limit flag on the orbital period as stored - 0 for a measured value, "
         "1 for an upper limit, -1 for a lower limit. Present on 3304 planets: "
         "0 on 3300, 1 on one, -1 on three. Period Upper Limit is the same "
         "flag read as Yes/No."),
        ("Period Upper Limit", "period_upper_limit", F_QUAL,
         "Whether the orbital period is an Upper Limit Value rather than a "
         "measurement. 'Yes' on a few planets, 'No' on the rest that carry a flag, null on 68. " + FLAG),
        ("Mass Limit Flag", "mass_limit_flag", F_QUAL,
         "Limit flag on the planet mass as stored. Present on 1174 planets: 0 on "
         "1105, 1 on 64, -1 on five. Mass Upper Limit is the same flag read as "
         "Yes/No."),
        ("Mass Upper Limit", "mass_upper_limit", F_QUAL,
         "Whether the planet mass is an Upper Limit Value rather than a "
         "measurement. 'Yes' on some planets, 'No' on most of the rest, null on the 2198 with no mass. " + FLAG),
        ("Radius Limit Flag", "radius_limit_flag", F_QUAL,
         "Limit flag on the planet radius as stored. Present on 2694 planets."),
        ("Radius Upper Limit", "radius_upper_limit", F_QUAL,
         "Whether the radius is an Upper Limit Value rather than a measurement. "
         "'Yes' on a few planets, 'No' on the rest that carry a flag and null on the 678 with no radius. "
         "The concept is published so it is not silently missing, but it "
         "selects one row. " + FLAG),
        ("Eccentricity Limit Flag", "eccentricity_limit_flag", F_QUAL,
         "Limit flag on the eccentricity as stored. Present on 971 planets: 0 "
         "on 891, 1 on 71, -1 on nine."),
        ("Eccentricity Upper Limit", "eccentricity_upper_limit", F_QUAL,
         "Whether the eccentricity is an Upper Limit Value. 'Yes' on some planets, 'No' on most of the rest, null on 2401. " + FLAG),
        ("Inclination Limit Flag", "inclination_limit_flag", F_QUAL,
         "Limit flag on the inclination as stored. Present on 504 planets: 0 on "
         "500 and -1 on four, never 1."),
        ("Inclination Upper Limit", "inclination_upper_limit", F_QUAL,
         "Whether the inclination is an Upper Limit Value.  " + FLAG),
        ("Density Limit Flag", "density_limit_flag", F_QUAL,
         "Limit flag on the density as stored. Present on 387 planets: 0 on "
         "377, 1 on nine, -1 on one."),
        ("Density Upper Limit", "density_upper_limit", F_QUAL,
         "Whether the density is an Upper Limit Value. 'Yes' on a few planets, 'No' on most of the rest that carry a flag, null on 2985. " + FLAG),
        ("Semi Major Limit Flag", "semi_major_limit_flag", F_QUAL,
         "Limit flag on the semi-major axis. Present on 1892 planets."),
        ("Distance Limit Flag", "distance_limit_flag", F_QUAL,
         "Limit flag on the stellar distance as stored. Present on 2293 "
         "planets: 0 on 2285 and -1 (a lower limit) on eight, never 1. Null on "
         "1079 planets whose limit status is unrecorded, which is a different "
         "thing from a measured distance. A filter written as = 0 drops the "
         "eight lower-limit rows, which are measured distances, while "
         "Distance Upper Limit = 'No' keeps every recorded flag that is not an "
         "upper limit (2293 planets) - the two select different rows."),
        ("Distance Upper Limit", "distance_upper_limit", F_QUAL,
         "Whether the host star's distance is an Upper Limit Value.  This is the only quality flag on the distance itself; a screen over stellar measurement quality that uses this flag alone and one that uses both it and Magnitude Blended select different rows. "
         + FLAG),
        ("Stellar Temperature Limit Flag", "temperature_limit_flag", F_QUAL,
         "Limit flag on the stellar temperature as stored. Present on 3204 "
         "planets and 1 on exactly one."),
        ("Stellar Temperature Upper Limit", "stellar_temperature_upper_limit",
         F_QUAL,
         "Whether the host star's temperature is an Upper Limit Value. 'Yes' on a few planets, 'No' on the rest that carry a flag, null on 168. " + FLAG),
        ("Magnitude Limit Flag", "magnitude_limit_flag", F_QUAL,
         "Limit flag on the stellar magnitude. Present on 3251 planets."),
        ("Stellar Radius Limit Flag", "stellar_radius_limit_flag", F_QUAL,
         "Limit flag on the stellar radius. Present on 3014 planets."),
        ("Stellar Mass Limit Flag", "stellar_mass_limit_flag", F_QUAL,
         "Limit flag on the stellar mass as stored. Present on 3047 planets: 0 "
         "on 3041 and -1 on six, never 1."),
        ("Stellar Mass Upper Limit", "stellar_mass_upper_limit", F_QUAL,
         "Whether the host star's mass is an Upper Limit Value.  " + FLAG),
        ("Temperature Blend Flag", "temperature_blend_flag", F_QUAL,
         "Blend flag on the stellar temperature - 1 means the measurement is "
         "contaminated by light from unresolved companions. Present on 3219 planets."),
        ("Temperature Blended", "temperature_blended", F_QUAL,
         "Whether the host star's temperature is a Blended Measurement.  " + FLAG),
        ("Stellar Mass Blend Flag", "stellar_mass_blend_flag", F_QUAL,
         "Blend flag on the stellar mass. Present on 2977 planets."),
        ("Stellar Radius Blend Flag", "stellar_radius_blend_flag", F_QUAL,
         "Blend flag on the stellar radius. Present on 3185 planets."),
        ("Magnitude Blend Flag", "magnitude_blend_flag", F_QUAL,
         "Blend flag on the stellar magnitude as stored. Present on 3251 planets and equal to 1 on a handful of them - the ONLY blended measurements anywhere in this warehouse. Magnitude Blended is the same flag read "
         "as Yes/No."),
        ("Magnitude Blended", "magnitude_blended", F_QUAL,
         "Whether the host star's magnitude is a Blended Measurement - "
         "contaminated by companion light. 'Yes' on a handful of planets, 'No' on the rest that carry a flag, null on 121. The only blend flag in the warehouse that is ever set, "
         "so it is the one a data-quality screen on stellar photometry turns "
         "on. " + FLAG),
        ("Any Stellar Blend", "any_stellar_blend", F_QUAL,
         "Whether any of the four stellar blend flags is set - contaminated "
         "star data. 'Yes' on 9 planets and 'No' on 3363. All nine are flagged "
         "on the magnitude; the temperature, mass and radius flags are zero "
         "throughout."),
    ]))

DIMENSIONS.append(prof(
    "Planet Classification Profile", F_PCLASS, PD, "planet",
    "Knowledge-base planet classifications, each with the population it selects "
    "and the number of planets it cannot judge. Read those numbers first: a "
    "density exists for only 388 planets and a mass for 1174, so several of "
    "these classifications are undecidable for most of the catalogue. Every "
    "flag follows SQL's own three-valued logic: 'Yes' when the definition "
    "holds, 'No' when it is definitely false - for a compound definition, as "
    "soon as one condition is recorded false - and null only when nothing "
    "recorded settles it. So filtering on 'No' selects exactly the planets a "
    "NOT of the definition keeps.",
    [
        ("Gas Giant Planet", "gas_giant_planet", F_PCLASS,
         "Whether the mass exceeds 0.1 Jupiter masses - gas giant, big gassy "
         "planet. 'Yes' on 929 planets, 'No' on 245, and null on the 2198 with "
         "no mass. So three quarters of the catalogue cannot be judged at all."),
        ("Rocky Planet", "rocky_planet", F_PCLASS,
         "Whether the bulk density exceeds 3 grams per cubic centimetre - rocky "
         "planet. 'Yes' on 74 planets, 'No' on 314, and null on the 2984 with no "
         "density."),
        ("Short Period Planet", "short_period_planet", F_PCLASS,
         "Whether the orbital period is under 10 days - short-period, fast "
         "orbit. 'Yes' on 1445 planets, 'No' on 1860, null on 67."),
        ("Hot Jupiter", "hot_jupiter", F_PCLASS,
         "Whether the planet is both a gas giant and short-period - hot "
         "Jupiter. 'Yes' where both hold, 'No' for every planet whose recorded mass rules out a gas giant OR whose recorded period rules out a short-period orbit, even when the other input is missing, and null where neither recorded value settles it. Retrograde Orbit reads a strictly retrograde orbit (inclination above 90 degrees) and Retrograde Orbit (90 Degrees Or More) admits an inclination of exactly 90 degrees; the two readings select different planets."),
        ("Super Earth", "super_earth", F_PCLASS,
         "Whether the planet is rocky AND has a mass between 1 and 10 Earth "
         "masses - super-Earth. 'Yes' on 31 planets, 'No' on 1075 (a recorded "
         "density that is not rocky, or a recorded mass outside that range), "
         "null on 2266. 29 of the 31 were discovered by transit, and "
         "their mean surface gravity is 2.538 Earth gravities; the strongest "
         "is Kepler-131 c at 11.69."),
        ("Planet In Habitable Zone", "planet_in_habitable_zone", F_PCLASS,
         "Whether the semi-major axis lies between the habitable-zone "
         "boundaries. 'Yes' on 28 planets, 'No' on 1505, null on 1839."),
        ("Potentially Habitable", "potentially_habitable", F_PCLASS,
         "Whether the planet is rocky AND in the habitable zone - potentially "
         "habitable exoplanet. ZERO planets qualify: 1538 are 'No' (a recorded "
         "density at or below 3, or an orbit recorded outside the zone) and "
         "1834 cannot be judged. The two conditions never co-occur in this "
         "warehouse, because only 388 planets have a density at all and none "
         "of those 388 that is rocky also sits inside its zone. So a question "
         "about potentially habitable planets has an empty answer, and the "
         "honest reply names the two component populations - 74 rocky planets "
         "and 28 planets in a habitable zone - rather than returning nothing."),
        ("High Eccentricity Planet", "high_eccentricity_planet", F_PCLASS,
         "Whether the eccentricity exceeds 0.25 - high eccentricity, weird "
         "orbit. 'Yes' on 249 planets, 'No' on 725, null on 2398."),
        ("Retrograde Orbit", "retrograde_orbit", F_PCLASS,
         "Whether the inclination exceeds 90 degrees - retrograde, orbiting "
         "backwards, the knowledge base's strict 'greater than 90' reading. "
         "'Yes' on only 8 planets, 'No' on 494, null on 2870. The highest "
         "inclination in the warehouse is 90.76 degrees, so the eight that "
         "qualify clear the threshold by less than a degree - and 21 planets "
         "sit at EXACTLY 90.0 degrees, on the boundary. Retrograde Orbit (90 "
         "Degrees Or More) admits them, selecting 29; which reading a question "
         "means is the caller's to settle, so ask when the boundary matters."),
        ("Retrograde Orbit (90 Degrees Or More)", "retrograde_orbit_inclusive",
         F_PCLASS,
         "The inclusive reading of the retrograde threshold - an inclination "
         "of 90 degrees or more. 'Yes' on 29 planets (the 8 strictly above 90 "
         "plus 21 at exactly 90.0), 'No' on 473, null on 2870. KB 31 defines a retrograde orbit as an inclination strictly greater than 90 degrees, which is the plain Retrograde Orbit; this inclusive twin is for a question that itself says 'at least 90' or '90 or more'. The threshold is the KB's own - do not ask which of the two readings is meant. "),
        ("Inflated Gas Giant", "inflated_gas_giant", F_PCLASS,
         "Whether the planet is a gas giant with a low bulk density - inflated gas giant, big puffy planet. 'Yes' where a giant mass and a low recorded density are both present, 'No' where a recorded mass at or below 0.1 rules out a gas giant or a recorded density rules out inflation, null where neither recorded value settles it. Distance Upper Limit and Magnitude Blended are "
         "two separate measurement-quality flags on the star record and they "
         "select different rows, so a screen over stellar measurement quality "
         "has to say which of them it means; ask rather than choose."),
        ("In Multi Planetary System", "in_multi_planetary_system", F_PCLASS,
         "Whether the host star declares more than one planetary companion. "
         "'Yes' on 1431 planets and 'No' on 1941."),
        ("Period High Precision", "period_high_precision", F_PCLASS,
         "Whether the period's relative uncertainty is under 5 percent - a "
         "high-precision period. 'Yes' on 3125 planets, 'No' on 55, null on "
         "192."),
        ("Mass High Precision", "mass_high_precision", F_PCLASS,
         "Whether the mass's relative uncertainty is under 5 percent. 'Yes' on "
         "198 planets, 'No' on 789, null on 2385 - the scarcest of the three "
         "precision tests."),
        ("Radius High Precision", "radius_high_precision", F_PCLASS,
         "Whether the radius's relative uncertainty is under 5 percent. 'Yes' "
         "on 396 planets, 'No' on 2260, null on 716."),
        ("Well Characterized Planet", "well_characterized_planet", F_PCLASS,
         "Whether mass, radius AND period are all high-precision. 'Yes' on 48 "
         "planets, 'No' on 2881 (any one of the three recorded at 5 percent or "
         "worse), null on 443. The mass test is what narrows it: 3125 planets "
         "have a precise period and 396 a precise radius, but only 198 a "
         "precise mass."),
    ]))

DIMENSIONS.append(prof(
    "Survey Observation Profile", F_OBS, PD, "planet",
    "Which of the three surveys observed the planet, as per-planet flags so a "
    "question can filter without joining the observation bridge. 2460 of the "
    "3372 planets were observed by at least one survey and none by more than "
    "two.",
    [
        ("Kepler Observation", "kepler_observation_indicator", F_OBS,
         "Whether the planet has an observation record linked to the 'kep' "
         "facility - a Kepler mission discovery. 1 on 2329 planets and 0 on "
         "1043."),
        ("K2 Observation", "k2_observation_indicator", F_OBS,
         "Whether the planet has an observation record linked to the 'k2' facility - a K2 mission discovery. 1 on 129 planets."),
        ("TTV Observation", "ttv_observation_indicator", F_OBS,
         "Whether the planet has an observation record linked to the 'ttv' "
         "facility - a transit-timing-variation detection. 1 on 225 planets. "
         "This is the knowledge base's Transit Timing Variation (TTV) Method - planets found or discovered via timing variations or the TTV method. Discovery Method's 'TTV' category is a different reading, the standardised stored label, on 15 planets."),
        ("Planet Observation Count", "observation_count", F_OBS,
         "How many of the three surveys observed the planet. 0, 1 or 2 on all "
         "3372 planets, averaging 0.796 - no planet was observed by all three."),
        ("Observed By A Survey", "observed_by_a_survey", F_OBS,
         "Whether any of the three surveys observed the planet. 'Yes' on 2460 "
         "and 'No' on 912."),
    ]))

# --------------------------------------------------------------------------- #
# star profiles
# --------------------------------------------------------------------------- #
DIMENSIONS.append(prof(
    "Star System Profile", F_SYSTEM, SD, "star",
    "What the star's planets look like in aggregate, and the adjacent-period "
    "ratios a compactness question needs. 569 stars declare more than one "
    "companion and 568 of them have at least one adjacent pair with both "
    "periods recorded.",
    [
        ("Star Planet Count", "star_planet_count", F_SYSTEM,
         "How many planet rows the star actually carries. 1 to 7 on all 2509 "
         "stars, averaging 1.344. It agrees with the star's own declared "
         "companion count on all but ONE star, so the two readings of "
         "multi-planetary differ by a single row - 570 stars have more than one "
         "planet row and 569 declare more than one companion."),
        ("Shortest Orbital Period", "shortest_orbital_period", F_SYSTEM,
         "Period of the innermost planet by period, in days - the fastest "
         "planet in the system. 0.0907 to 7,300,000 on 2444 stars, averaging 3477."),
        ("Longest Orbital Period", "longest_orbital_period", F_SYSTEM,
         "Period of the outermost planet by period, in days. 0.0907 to "
         "7,300,000 on 2444 stars, averaging 3619."),
        ("Innermost Semi Major Axis", "innermost_semi_major_axis", F_SYSTEM,
         "Smallest semi-major axis in the system, in AU. 0.0044 to 2500 on 1244 "
         "stars, averaging 11.32."),
        ("Outermost Semi Major Axis", "outermost_semi_major_axis", F_SYSTEM,
         "Largest semi-major axis in the system, in AU. 0.0044 to 2500 on 1244 "
         "stars, averaging 11.57. The planet that holds it does not always "
         "record a period, so a Kepler's-law check on the outermost planet "
         "filters Kepler Derived Stellar Mass IS NOT NULL."),
        ("Heaviest Planet Mass", "heaviest_planet_mass_jupiter", F_SYSTEM,
         "Mass of the system's heaviest planet, in Jupiter masses. 0.00063 to "
         "28.5 on 920 stars, averaging 3.097."),
        ("Largest Planet Radius", "largest_planet_radius_jupiter", F_SYSTEM,
         "Radius of the system's largest planet, in Jupiter radii. 0.046 to 6.9 "
         "on 1991 stars, averaging 0.399."),
        ("Densest Planet Density", "densest_planet_density", F_SYSTEM,
         "Density of the system's densest planet. 0.046 to 77.7 on only 333 "
         "stars, averaging 2.654."),
        ("Star Gas Giant Count", "star_gas_giant_count", F_SYSTEM,
         "How many of the star's planets are gas giants. 0 to 4 on all 2509 "
         "stars, averaging 0.370."),
        ("Star Rocky Planet Count", "star_rocky_planet_count", F_SYSTEM,
         "How many of the star's planets are rocky. 0 to 4 on all 2509 stars, "
         "averaging 0.0295."),
        ("Star Planets With Density", "star_planets_with_density", F_SYSTEM,
         "How many of the star's planets have a density at all. 0 to 6 on all "
         "2509 stars, averaging 0.155 - the honest denominator for any "
         "rocky-fraction question."),
        ("Star Planets With Composition", "star_planets_with_composition",
         F_SYSTEM,
         "How many of the star's planets carry a density OR a mass - the "
         "planets whose composition class (rocky by density, gas giant by "
         "mass) can be judged at all. 1176 planets over 921 stars; 0 on the "
         "other 1588 stars, whose System Composition is therefore null."),
        ("Star Short Period Count", "star_short_period_count", F_SYSTEM,
         "How many of the star's planets orbit in under 10 days. 0 to 5 on all "
         "2509 stars, averaging 0.576."),
        ("Star Transit Discovery Count", "star_transit_discovery_count",
         F_SYSTEM,
         "How many of the star's planets were found by transit. 0 to 7 on all "
         "2509 stars, averaging 1.062."),
        ("Star Radial Velocity Count", "star_radial_velocity_count", F_SYSTEM,
         "How many of the star's planets were found by radial velocity. 0 to 6 "
         "on all 2509 stars, averaging 0.236."),
        ("Adjacent Pair Count", "adjacent_pair_count", F_SYSTEM,
         "How many adjacent planet pairs the system has with both periods "
         "recorded. 0 to 6 on 2508 stars, averaging 0.343. 568 stars have at "
         "least one pair and 193 have more than one."),
        ("Max Adjacent Period Ratio", "max_adjacent_period_ratio", F_SYSTEM,
         "Largest ratio between the periods of two adjacent planets in the "
         "system. 1.173 to 4482 on 568 stars, averaging 29.78. KB 33 defines a Compact System from this figure - a multi-planet system whose adjacent period ratios all stay under one cutoff - and the cutoff comes from the user."),
        ("Min Adjacent Period Ratio", "min_adjacent_period_ratio", F_SYSTEM,
         "Smallest ratio between the periods of two adjacent planets. 1.006 to "
         "4482 on 568 stars, averaging 28.26."),
        ("Mean Adjacent Period Ratio", "mean_adjacent_period_ratio", F_SYSTEM,
         "ARITHMETIC mean of the system's adjacent Orbital Period Ratios. 1.173 "
         "to 4482 on 568 stars, averaging 28.94. Geometric Mean Adjacent Period "
         "Ratio is the other average of the same ratios; the two agree on "
         "every two-planet system and differ on 177 of the 193 systems with "
         "more than one pair, so which average a question means is the "
         "caller's to settle - ask when it says 'average ratio'."),
        ("Geometric Mean Adjacent Period Ratio",
         "geometric_mean_adjacent_period_ratio", F_SYSTEM,
         "GEOMETRIC mean of the system's adjacent Orbital Period Ratios - the "
         "exponential of the mean logarithm, the conventional average of a "
         "set of ratios. 1.173 to 4482 on 568 stars, averaging 28.60; on the "
         "210 systems whose ratios are all under 3 and whose innermost planet "
         "orbits in under 10 days it averages 1.990. Identical to Mean "
         "Adjacent Period Ratio on two-planet systems and smaller on every "
         "system with more than one pair."),
        ("Multi Planetary System", "multi_planetary_system", F_SYSTEM,
         "Whether the star declares more than one planetary companion - "
         "multi-planetary. 'Yes' on 569 stars and 'No' on 1940."),
        ("Multiple Planet Rows", "multiple_planet_rows", F_SYSTEM,
         "Whether the star actually carries more than one planet row. 'Yes' on "
         "570 stars and 'No' on 1939 - one more than the declared-companion "
         "reading, because a single star's two figures disagree."),
        ("System Composition", "system_composition", F_SYSTEM,
         "What kinds of planet the star hosts, judged from the two "
         "knowledge-base composition classes over every planet with a density "
         "or a mass: 'Rocky Only' (one or more Rocky Planets and no Gas Giant "
         "Planet) on 27 stars, 'Gas Giants Only' (one or more gas giants and "
         "no rocky planet) on 782, 'Mixed' (both) on 35, 'Neither' (planets "
         "judgeable but none in either class) on 77, and null on the 1588 "
         "stars none of whose planets records a density or a mass. Has Rocky Planet "
         "and Has Gas Giant are the two halves as separate Yes/No attributes. "
         "A star can be judged rocky-only here while All Density Measured "
         "Planets Rocky says the same thing of a wider set (49 stars), because "
         "that reading ignores planets whose mass, but not density, is "
         "recorded - the two differ on 22 stars whose gas giants have no "
         "density."),
        ("Has Rocky Planet", "has_rocky_planet", F_SYSTEM,
         "Whether at least one of the star's planets is a Rocky Planet - a "
         "recorded density above 3. 'Yes' on 62 stars, 'No' on 859 whose "
         "judgeable planets are all non-rocky, null on the 1588 with no "
         "judgeable planet."),
        ("Has Gas Giant", "has_gas_giant", F_SYSTEM,
         "Whether at least one of the star's planets is a Gas Giant Planet - a "
         "recorded mass above 0.1 Jupiter masses. 'Yes' on 817 stars, 'No' on "
         "104, null on 1588."),
        ("All Density Measured Planets Rocky", "all_density_measured_rocky",
         F_SYSTEM,
         "Whether every planet of the star that HAS a density is rocky - the "
         "narrower reading that looks only at density-measured planets and "
         "ignores a gas giant known by its mass alone. 'Yes' on 49 stars, 'No' "
         "on 284, and null on the 2176 with no density anywhere in the system. "
         "System Composition = 'Rocky Only' is the reading that also rules out "
         "gas giants by mass, and selects 27 of these 49."),
        ("Star Kepler Observation", "kepler_observation_indicator", F_SYSTEM,
         "Whether any planet of the star was observed by the Kepler mission. 1 "
         "on 1644 stars."),
        ("Star K2 Observation", "k2_observation_indicator", F_SYSTEM,
         "Whether any planet of the star was observed by K2. 1 on 94 stars."),
        ("Star TTV Observation", "ttv_observation_indicator", F_SYSTEM,
         "Whether any planet of the star was detected through transit timing variations."),
    ]))

DIMENSIONS.append(prof(
    "Stellar Formula Profile", F_SFORM, SD, "star",
    "Knowledge-base stellar formulas, as queryable per-star attributes. Each "
    "needs a temperature, a radius or a mass, so each covers a different subset "
    "of the 2509 stars.",
    [
        ("Stellar Luminosity (Intrinsic Brightness, Solar Units)",
         "stellar_luminosity", F_SFORM,
         "Intrinsic brightness of the star relative to the Sun - luminosity in "
         "solar units: the radius in solar radii squared, "
         "times the temperature over 5778 K to the fourth power. 7.9e-07 to 631 "
         "on the 2207 stars with both a radius and a temperature, averaging "
         "5.640. It is the input to both habitable-zone boundaries, and paired "
         "with the effective temperature it is the Hertzsprung-Russell (HR) "
         "Diagram Position the knowledge base defines - a coordinate pair of "
         "temperature and luminosity."),
        ("Star Habitable Zone Inner", "habitable_zone_inner_au", F_SFORM,
         "Habitable Zone Inner Boundary in AU - the square root of the "
         "luminosity over 1.1. 0.00085 to 23.95 on 2207 stars, averaging "
         "1.296."),
        ("Star Habitable Zone Outer", "habitable_zone_outer_au", F_SFORM,
         "Habitable Zone Outer Boundary in AU - the square root of the "
         "luminosity over 0.53. 0.00122 to 34.50 on 2207 stars, averaging "
         "1.866."),
        ("Stellar Density", "stellar_density_kg_m3", F_SFORM,
         "Stellar Density - the star's mass over the volume of a sphere of its radius, in KILOGRAMS PER CUBIC METRE: the solar-unit mass times 1.98847E30 over four-thirds pi times the cube of the solar-unit radius times 6.957E8. 0.0138 to 30,839,868 on the 2117 stars with both a mass and a radius, averaging 16,571; a pulsar in the catalogue sits far above any ordinary star on this figure. The twin "
         "Stellar Density (Solar Units) leaves both inputs in solar units. "
         + CONSTANTS),
        ("Stellar Density (Solar Units)", "stellar_density_solar", F_SFORM,
         "The same formula evaluated with the mass in solar masses and the "
         "radius in solar radii, so the unit is solar masses per cubic solar "
         "radius. 2.3e-06 to 5222 on 2117 stars, averaging 2.806. Divide-free "
         "and ranking-identical to Stellar Density."),
        ("Gravitational Parameter", "gravitational_parameter", F_SFORM,
         "Standard gravitational parameter of the star, in cubic metres per second squared - the gravitational constant times the stellar mass in kilograms, 6.67430E-11 times the solar-unit mass times 1.98847E30. 2.65e+18 to 5.18e+20 on the 2357 stars with a mass, averaging 1.33e+20. " + CONSTANTS),
    ]))

DIMENSIONS.append(prof(
    "Sky Coordinate Profile", F_COORD, SD, "star",
    "Where the star sits on the sky. Both coordinates are stored twice, as "
    "decimal degrees and as a sexagesimal string, and both forms are published "
    "on all 2509 stars.",
    [
        ("Right Ascension Degrees", "right_ascension_degrees", F_COORD,
         "Right ascension in decimal degrees. 0.362 to 359.97 on all 2509 "
         "stars, averaging 255.2."),
        ("Declination Degrees", "declination_degrees", F_COORD,
         "Declination in decimal degrees. -84.23 to 85.74 on all 2509 stars, "
         "averaging 27.90."),
        ("Right Ascension Text", "right_ascension_text", F_COORD,
         "Right ascension in hours, minutes and seconds, e.g. 12h20m43.03s. "
         "2506 distinct strings on all 2509 stars."),
        ("Declination Text", "declination_text", F_COORD,
         "Declination in degrees, arcminutes and arcseconds with a sign prefix, "
         "e.g. +17d47m34.3s. 2508 distinct strings on all 2509 stars."),
        ("Star Temperature Blend Flag", "temperature_blend_flag", F_COORD,
         "Blend flag on the star's temperature. Present on 2369 stars."),
        ("Star Mass Blend Flag", "mass_blend_flag", F_COORD,
         "Blend flag on the star's mass. Present on 2282 stars."),
        ("Star Radius Blend Flag", "radius_blend_flag", F_COORD,
         "Blend flag on the star's radius. Present on 2346 stars."),
        ("Star Magnitude Blend Flag", "magnitude_blend_flag", F_COORD,
         "Blend flag on the star's magnitude as stored. Present on 2400 stars and equal to 1 on a handful of them - the only blended measurements at star grain."),
        ("Star Magnitude Blended", "star_magnitude_blended", F_COORD,
         "Whether the star's magnitude is a Blended Measurement, read as "
         "Yes/No. 'Yes' on a handful of stars, 'No' on the rest that carry a flag, null on the 109 with no flag. " + FLAG),
        ("Any Blended Measurement", "any_blended_measurement", F_COORD,
         "Whether any of the star's four blend flags is set - contaminated star "
         "data. 'Yes' on 7 stars and 'No' on 2502. All seven are flagged on the "
         "magnitude alone."),
    ]))

# --------------------------------------------------------------------------- #
# Names the agent asks for
#
# Every entry below is a name an agent actually typed in the 2026-08-20 atscale
# run and got "Unknown column name(s)" for. The build rule is NAME DECIDES, NOT
# DESCRIPTION: listing "patient ID, person, case" as synonyms inside a
# description does not make `"Patient ID"` resolve, and the agent pays a coin to
# find that out. Each of these is an ALIAS onto the column the level already
# uses - no new data, no new grain, just the name the question is phrased in.
#
# Appended structurally rather than edited into the level definitions above so
# the provenance of each one stays visible.
# --------------------------------------------------------------------------- #
_AGENT_ALIASES = [
    ('Planet Record', 'Planet', 'Planet Name', 'host_star_name',
     "The plain reading of a planet's name is its host star's name ('WASP-1', 2509 distinct over 3372 planets), the same values as Planet Host Star Name: the warehouse stores a host star name and a companion letter and no separate planet-name column. The combined 'star + letter' string ('WASP-1 b', 3372 distinct) is the Planet level itself, and Companion Letter ('b' on 2504 of 3372) is the letter alone. When the caller requests a planet's name AND its star as separate output columns, use Companion Letter for the planet beside Planet Host Star Name for the star, since this name would repeat the star."),
    ('Star Record', 'Star', 'Star Name', 'star_name', ""),
]


def _attach_agent_aliases():
    for dim_name, lvl_name, alias, column, extra in _AGENT_ALIASES:
        for d in DIMENSIONS:
            if d["unique_name"] != dim_name:
                continue
            for lv in d["levels"]:
                if lv["unique_name"] != lvl_name:
                    continue
                secs = lv.setdefault("secondaries", [])
                if any(s[0] == alias for s in secs):
                    break
                folder = secs[0][2] if secs else d.get("folder", dim_name)
                own = lv.get("name_column") or lv.get("column")
                prefix = (
                    f"Alias for the {lvl_name} level's own {column} column, published "
                    f"under the name a question is likely to use. Identical values to "
                    f"{lvl_name}; grouping on either gives the same result."
                    if own == column else
                    f"Published under the name a question is likely to use; reads the "
                    f"{column} column.")
                secs.append((
                    alias, column, folder,
                    prefix + (" " + extra if extra else "")))
                break
            break


_attach_agent_aliases()


# --------------------------------------------------------------------------- #
# Grain-twin cross-linking (the mental_health_19 steering defect, found
# 2026-08-26 and audited across every model).
#
# The same source column published at more than one grain reports different
# headline figures, and a twin pair whose descriptions do not name each other
# actively steers the agent: it follows whichever description happens to
# mention the question's wording, and a by-group question graded against the
# other basis scores 0 with every value "right". Measured: mental_health_19
# submitted the per-patient figures character-for-character where gold wanted
# the pooled ones, because the per-patient twin was the only description that
# mentioned diagnosis.
#
# The pass is evidence-gated rather than folder-gated so it ports across
# models: a secondary is annotated only when its own description quotes a
# headline figure (averaging/mean/average N), a same-column sibling on another
# dataset quotes one too, and the two figures genuinely differ (>0.2%
# relative). Categorical and navigational duplicates never carry disagreeing
# headline figures, so they are untouched, as is any twin that already names
# its sibling (the containment check) - hand-written cross-links win.

import re as _re

_TWIN_FIG = _re.compile(
    r"(?:averaging|mean(?: is)?|average(?: of)?)\s+(-?\d+(?:\.\d+)?)", _re.I)


def _cross_link_grain_twins():
    entries = []
    for _d in DIMENSIONS:
        _ds = _d.get("dataset")
        for _lvl in _d.get("levels", []):
            _secs = _lvl.get("secondaries") or []
            for _i, _s in enumerate(_secs):
                if not isinstance(_s, tuple) or len(_s) < 4:
                    continue
                if _s[3].startswith("Alias for"):
                    continue
                _m = _TWIN_FIG.search(_s[3])
                if not _m:
                    continue
                entries.append((_ds, _secs, _i, _s[0], float(_m.group(1))))
    bycol = {}
    for _e in entries:
        bycol.setdefault(_e[1][_e[2]][1], []).append(_e)
    linked = 0
    for _col, _grp in sorted(bycol.items()):
        if len({_e[0] for _e in _grp}) < 2:
            continue
        for _ds, _secs, _i, _name, _fig in _grp:
            _sibs = []
            for _d2, _, _, _n2, _f2 in _grp:
                if _n2 == _name or _d2 == _ds:
                    continue
                if max(abs(_fig), abs(_f2)) == 0:
                    continue
                if abs(_fig - _f2) / max(abs(_fig), abs(_f2)) < 0.002:
                    continue
                if _n2.lower() in _secs[_i][3].lower():
                    continue
                _sibs.append((_n2, _d2, _f2))
            if not _sibs:
                continue
            _txt = "; ".join(
                f"'{_n2}' is the same quantity at the {_d2} grain, where it "
                f"averages {_f2:g}"
                for _n2, _d2, _f2 in sorted(set(_sibs)))
            _extra = (f" This figure is computed at the {_ds} grain; {_txt}. "
                      "The readings disagree because the grains differ, so say "
                      "which basis you mean, and ask if the question does not.")
            _secs[_i] = (_secs[_i][0], _secs[_i][1], _secs[_i][2],
                         _secs[_i][3] + _extra)
            linked += 1
    return linked


_CROSS_LINKED_TWINS = _cross_link_grain_twins()
