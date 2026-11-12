"""Spec for the planets_data AtScale SML model."""

from spec_dims import DIMENSIONS                       # noqa: F401
from spec_metrics import METRICS, CALCULATIONS         # noqa: F401
from sql_defs import ALL_SQL as DATASETS               # noqa: F401

DATABASE = "planets_data"
CONNECTION = "bird_planets_data"
MODEL_NAME = "Exoplanet Catalogue"
MODEL_LABEL = "Exoplanet Catalogue"

MODEL_DESCRIPTION = (
    "A confirmed-exoplanet catalogue: 3372 planets, 2509 host stars and three "
    "observing surveys. Orientation: this is a clean star schema. The planet is "
    "the fact grain, the orbital record, the physical record and the "
    "data-quality record are each exactly 1:1 with a planet and all three fold "
    "onto it, and every planet names a host star that resolves. The "
    "planet-to-survey table is a genuine bridge - 2683 rows over 2460 planets "
    "and 3 facilities - and survey membership is also published as three "
    "per-planet flags so a question can filter without joining it. Every "
    "knowledge-base formula ships both as a queryable per-row attribute and as "
    "an aggregate measure. "
    "FIVE THINGS DECIDE MOST ANSWERS HERE. "
    "First, COVERAGE. The orbital measurements are far better populated than "
    "the physical ones, and every derived quantity inherits the scarcest input "
    "it needs. A period exists for 3305 planets, a radius for 2694, a "
    "semi-major axis for 1897, a mass for 1174, an eccentricity for 974, an "
    "inclination for 502 and a DENSITY FOR ONLY 388. So the transit depth "
    "covers 2684 planets, the Kepler's-law mass check 1831, the orbital "
    "velocity 1593, the equilibrium temperature and the Goldilocks value 1533, "
    "the mass ratio 1127, and the surface gravity, escape velocity and "
    "mass-radius ratio 509 each. Every rocky, super-Earth, inflated-giant and "
    "potentially-habitable answer is bounded by that 388. Each object publishes "
    "its own support set and the Support Sets And Coverage folder collects "
    "them. "
    "Second, UNITS AND CONSTANTS. Every derived quantity is evaluated in "
    "consistent SI units from the standard physical constants written out in "
    "full - G = 6.67430E-11, the solar mass 1.98847E30 kg, the solar radius "
    "6.957E8 m, the astronomical unit 1.496E11 m, Jupiter's mass 1.898E27 kg "
    "and radius 7.1492E7 m, 109.2 Earth radii per solar radius - and at the "
    "warehouse's own column types, so a figure here is the figure a plain SQL "
    "reader of the same tables computes. Velocities carry kilometres per "
    "second under their bare names with metres-per-second twins; the stellar "
    "density is kilograms per cubic metre with a solar-units twin; the transit "
    "depth is a fraction with a percent twin; the equilibrium temperature is "
    "Kelvin with both lengths in metres. The orbital period is DAYS as "
    "recorded, with a years twin for Kepler's third law. "
    "Third, SEVERAL CONCEPTS ARE EMPTY RATHER THAN RARE, and a question about "
    "them has no answer rather than a small one. NO planet is both rocky and in "
    "its star's habitable zone, so the potentially-habitable count is zero even "
    "though 74 planets are rocky and 28 sit in a zone. NO hot Jupiter also "
    "orbits retrograde, so a question asking for both returns nothing. The blend flags are published beside their values. The limit flags are published beside their values. "
    "Fourth, TWO TEXT COLUMNS ARE DIRTY. The discovery method is stored in 38 "
    "spellings of six standard categories, so grouping by the raw text splits "
    "Transit across five buckets - 'Photometric' 578, 'TR' 536, 'Transit "
    "Method' 523, 'Photometry' 516 and 'Transit' 511, which are one category of "
    "2664. Membership is matched EXACTLY against the label lists the knowledge "
    "base gives, because a substring reading would also pull 'Timing "
    "Variations' and 'Eclipse Timing' into TTV. The photometric band "
    "is stored in 10 spellings of three bands, five of them for Kepler alone; "
    "the canonical form folds 'V-band' into Johnson V and a stricter reading "
    "that keeps it separate ships beside it, moving 155 stars. "
    "Fifth, THE MAGNITUDE SCALE IS INVERTED. A smaller number is a brighter "
    "star, so 'the brightest star' is the MINIMUM of the magnitude column, and a maximum returns the faintest. Star names are stored in "
    "catalogue form, so 'alf Tau' rather than 'Aldebaran'. "
    "Two more things worth knowing. The three survey codes are stored lower "
    "case as 'kep', 'k2' and 'ttv', so a filter written as 'Kepler' matches "
    "nothing. And a star's declared companion count and the number of planet "
    "rows it actually carries agree on all but ONE of the 2509 stars, so the "
    "two readings of 'multi-planetary system' give 569 and 570. "
    "Finally, what the warehouse does not hold. There is no spectral type, no "
    "metallicity and no age, so a stellar classification can only be built from "
    "mass, radius and temperature. The compactness of a system - KB 33's Compact System - depends on a threshold on the adjacent period ratio that the user supplies, so this model publishes the ratios - the maximum, minimum, arithmetic mean and geometric mean per system - and no compactness flag. A star's planetary make-up is System Composition - "
    "rocky only, gas giants only, mixed or neither - judged over the planets "
    "whose density or mass is recorded. And the "
    "orbital period is stored in DAYS while Kepler's third law needs years, so "
    "the derived stellar mass divides by 365.25 squared; using days directly "
    "gives a number about 133,000 times too small."
    " In a FROM clause this model is named \"<schema>\".\"Exoplanet Catalogue\" with the "
    "schema exactly as list_models prints it, or in full "
    "\"atscale_catalogs\".\"<schema>\".\"Exoplanet Catalogue\"; a bare table name is refused "
    "before dispatch. Engine notes, the same for every model here. COUNT(*) is refused - "
    "a semantic model has no row count of its own - so a count names a published count "
    "metric or COUNT(DISTINCT <key column>). A SELECT with no measure, a flat listing as "
    "much as a subquery, returns DISTINCT attribute tuples: a listing of entities that "
    "leaves out their ID column merges rows with equal values (1000 shows listed by title "
    "and a flag came back as 109 rows), so a per-entity listing projects the entity's ID. "
    "SUM or AVG over a dimension ATTRIBUTE is refused before the query is dispatched, "
    "with a message naming the workaround, while COUNT over an attribute aggregates "
    "correctly and agrees with COUNT(DISTINCT <key column>), so an aggregate of a per-row "
    "score names the published metric rather than wrapping the attribute - and where the "
    "aggregate has no metric, select the attribute at row grain in a FROM-subquery that "
    "also selects the row's ID column, and aggregate outside it - a select with no "
    "measure returns DISTINCT attribute tuples, so without the ID duplicate values "
    "collapse and an outer AVG averages the distinct values only. ORDER BY <col> DESC "
    "places NULLs FIRST and ASC places them LAST, which is what Postgres does, and an "
    "explicit NULLS FIRST or NULLS LAST is honoured, so a top-N over a nullable column "
    "writes DESC NULLS LAST or filters that column IS NOT NULL. ORDER BY a column the "
    "outer SELECT does not project is an internal render fault, so put the ORDER BY and "
    "its LIMIT inside the subquery that projects the sort column, and sorting by an "
    "ATTRIBUTE the query neither projects nor groups by is refused outright with a "
    "message saying to add it to the select list, while a published MEASURE can be sorted "
    "on without being projected - projecting only a CAST or ROUND of a column does not "
    "count, so give the rounded expression an alias and ORDER BY the alias; ORDER BY an "
    "aggregate the SELECT does not project, such as ORDER BY COUNT(DISTINCT <key>) DESC "
    "LIMIT 1 for the most frequent group, is refused the same way, so compute the "
    "aggregate under an alias in a FROM-subquery that holds the ORDER BY and LIMIT and "
    "project only the group outside. A window column is filtered by selecting it in a "
    "FROM-subquery and filtering its alias in the outer WHERE; filtering it in HAVING "
    "after a GROUP BY is refused as an incorrectly constructed constraint. ROUND to a "
    "fixed number of decimals goes through a numeric cast that must carry precision and "
    "scale - a bare CAST(x AS numeric) is refused with 'Numeric values are only accepted "
    "with specified precision and scale', so write CAST(x AS numeric(18,4)), and note "
    "that the result comes back as a string rather than a number. A top-level UNION ALL "
    "over the model works and a listing UNION ALL a one-row summary is a working shape, "
    "but a UNION inside a subquery, CTE or WHERE is refused, a NULL literal in a branch "
    "may be written as CAST(NULL AS VARCHAR) though a bare NULL is also accepted, and the "
    "branch order is preserved, so a listing followed by a one-row summary comes back in "
    "that order. Not accepted in submitted SQL in any spelling: PERCENTILE_CONT, MEDIAN, "
    "PERCENT_RANK, CORR, REGR_SLOPE, JSON aggregation, GREATEST/LEAST, IN (subquery), "
    "EXISTS and CTEs - whatever this model precomputes for those is named above. "
    "STRING_AGG over a FROM-subquery that projects the rows is accepted, but an ORDER BY inside the STRING_AGG call is refused before the query is dispatched, and element order then follows the warehouse. NULLIF is refused before the query is dispatched, so a divide-by-zero guard is written CASE WHEN <b> = 0 THEN NULL ELSE <a> / <b> END. A published median "
    "metric is called by its name with the suffix _instance_0.5; the plain name is not "
    "found. Two FROM-subqueries joined with a comma are refused; one subquery with "
    "conditional aggregates in the outer SELECT, such as MAX(CASE WHEN ... THEN x END), "
    "gives two figures in one row. A WHERE on one dataset's column while projecting "
    "another dataset's column, where the two datasets are not joined, is silently "
    "dropped: the filter becomes true and every row returns with no error. Missing-input "
    "policy: a figure whose input has no recorded row is null, never zero, unless its own "
    "label or description says it treats the absent input as zero; where both readings "
    "are published each one names the other. Stored text is matched as stored; no "
    "attribute in this model holds one value under spellings that differ only in case or "
    "spacing."
)

RELATIONSHIPS = [
    {"unique_name": "planet_detail_to_planet",
     "from": {"dataset": "Planet Detail", "join_columns": ["planet"]},
     "to": {"dimension": "Planet Record", "level": "Planet"}},
    {"unique_name": "observation_to_planet",
     "from": {"dataset": "Planet Observation", "join_columns": ["planet"]},
     "to": {"dimension": "Planet Record", "level": "Planet"}},
    {"unique_name": "planet_to_star",
     "from": {"dataset": "Planet Detail", "join_columns": ["star"]},
     "to": {"dimension": "Star Record", "level": "Star"}},
    {"unique_name": "star_detail_to_star",
     "from": {"dataset": "Star Detail", "join_columns": ["star"]},
     "to": {"dimension": "Star Record", "level": "Star"}},
    {"unique_name": "observation_to_star",
     "from": {"dataset": "Planet Observation", "join_columns": ["star"]},
     "to": {"dimension": "Star Record", "level": "Star"}},
    {"unique_name": "observation_to_facility",
     "from": {"dataset": "Planet Observation", "join_columns": ["facility"]},
     "to": {"dimension": "Survey Facility", "level": "Facility Name"}},
    {"unique_name": "facility_detail_to_facility",
     "from": {"dataset": "Survey Facility Detail", "join_columns": ["facility"]},
     "to": {"dimension": "Survey Facility", "level": "Facility Name"}},
]

RESERVED_ENTITY_WORDS = [
    "Planet", "Star", "System", "Survey", "Observation", "Facility",
    "Exoplanet", "Host", "Companion",
]

DISCOVERY_PHRASES = [
    # knowledge-base formula names
    "Distance in Light-Years", "Planet Mass in Earth Units",
    "Planet Radius in Earth Units", "Stellar Luminosity",
    "Planet Surface Gravity", "Planetary Equilibrium Temperature",
    "Habitable Zone Inner Boundary", "Habitable Zone Outer Boundary",
    "Relative Uncertainty", "Transit Depth", "Planet Escape Velocity",
    "Orbital Velocity", "Stellar Density", "Goldilocks Value",
    "Kepler", "Mass-Radius Relationship", "Orbital Period Ratio",
    "Planet-Star Mass Ratio", "Gravitational Parameter",
    "HR) Diagram Position", "Hertzsprung-Russell",
    # knowledge-base classification names
    "Gas Giant", "Rocky Planet", "Short-Period", "Hot Jupiter",
    "Super-Earth", "Planet in Habitable Zone", "Potentially Habitable",
    "High Eccentricity", "Multi-planetary", "High-Precision",
    "Well-Characterized", "Retrograde", "Inflated Gas Giant",
    "Minimum Mass", "Upper Limit", "Blended", "Discovery Method",
    # stored values and column meanings
    "kep", "k2", "ttv", "Kepler mission", "K2 mission",
    "TTV Method", "Photometric", "Photometry", "RadVel",
    "Doppler", "Microlensing", "Direct Imaging", "Radial Velocity",
    "Johnson V", "K-band", "V-band", "parsec", "light-year", "solar radii",
    "solar masses", "Jupiter masses", "Jupiter radii", "Earth masses",
    "Earth radii", "right ascension", "declination", "apparent magnitude",
    "effective temperature", "semi-major axis", "eccentricity",
    "inclination", "bulk density", "companion letter", "note",
    "alf Tau", "55 Cnc", "PSR J1719-1438", "Kepler-57 b", "HD 209458 b",
    "KOI-55 b", "Kepler-131 c",
    # ordinary analyst vocabulary
    "what percentage", "support set", "coverage", "per star", "per planet",
    "pooled", "inverted", "brightest", "densest", "kilometres per second",
    "kilograms per cubic metre", "geometric mean", "composition", "percent",
    "upper limit", "blended measurement", "absolute discrepancy",
]

QUESTION_COLLOQUIALISMS = [
    "average surface pull", "watching stars dim", "scorching hot",
    "spinning backwards", "how long their year is", "fact-check",
    "weird orbits", "big gassy planets", "star wobble method",
    "biggest dimming effect", "dip in brightness", "strongest gravity pull",
    "big, puffy gas planets", "solid distance number", "bad measurement",
    "really tightly packed", "super fast",
    "biggest mass-to-size ratio", "light filter", "group the filters together",
    "average brightness", "temperature reading is bad", "hottest planet",
    "just an estimate", "looks brightest from Earth", "the data is messy",
    "clean category", "easier to compare", "very good measurements",
    "how big they are", "pre-compiled list", "dodgy star measurements",
    "potentially contaminated star data", "pre-calculated summary",
    "how we're finding planets", "discovery technique",
]

DANGLING_ALLOW = {
    "Pooled", "Yes", "No", "None", "Other", "Transit", "Imaging", "TTV",
    "Microlensing", "Radial Velocity", "Johnson", "Kepler", "Mass", "Msini",
    "Johnson V", "K-band", "V-band", "Photometry", "Photometric",
    "Timing Variations", "Eclipse Timing Variations", "Transit Method",
    "HR", "Hertzsprung-Russell (HR)",
    "TR", "Extensive", "Kepler-57 b", "Kepler-131 c", "HD 209458 b",
    "KOI-55 b", "PSR J1719-1438", "Rocky Only", "Gas Giants Only", "Mixed",
    "Neither", "Solar Units", "Metres Per Second", "Percent", "Years",
    "90 Degrees Or More",
}

GRAIN = {
    "Planet Detail": (3372, ["planet"]),
    "Star Detail": (2509, ["star"]),
    "Planet Observation": (2683, ["observation"]),
    "Survey Facility Detail": (3, ["facility"]),
}

PD = "Planet Detail"
SD = "Star Detail"
OD = "Planet Observation"
FD = "Survey Facility Detail"

PINNED = [
    # -------------------------------------------------- shape and coverage --
    ("distinct stars on planets", PD, "SELECT count(DISTINCT star) FROM d",
     2509, 0),
    ("distinct planet names", PD, "SELECT count(DISTINCT planet_name) FROM d",
     3372, 0),
    ("distinct host names", PD, "SELECT count(DISTINCT host_star_name) FROM d",
     2509, 0),
    ("distinct raw methods", PD,
     "SELECT count(DISTINCT discovery_method_stored) FROM d", 38, 0),
    ("distinct standard methods", PD,
     "SELECT count(DISTINCT discovery_method) FROM d", 6, 0),
    ("distinct update dates", PD,
     "SELECT count(DISTINCT record_update_date) FROM d", 82, 0),
    ("earliest update", PD, "SELECT min(record_update_year) FROM d", 2014, 0),
    ("latest update", PD, "SELECT max(record_update_year) FROM d", 2016, 0),
    ("planets with a period", PD,
     "SELECT count(orbital_period_days) FROM d", 3305, 0),
    ("planets with a semi-major axis", PD,
     "SELECT count(semi_major_axis_au) FROM d", 1897, 0),
    ("planets with a mass", PD, "SELECT count(planet_mass_jupiter) FROM d",
     1174, 0),
    ("planets with a radius", PD,
     "SELECT count(planet_radius_jupiter) FROM d", 2694, 0),
    ("planets with a density", PD, "SELECT count(planet_density) FROM d",
     388, 0),
    ("planets with an eccentricity", PD, "SELECT count(eccentricity) FROM d",
     974, 0),
    ("planets with an inclination", PD,
     "SELECT count(inclination_degrees) FROM d", 502, 0),
    ("planets with a surface gravity", PD,
     "SELECT count(surface_gravity) FROM d", 509, 0),
    ("planets with a mass ratio", PD,
     "SELECT count(planet_star_mass_ratio) FROM d", 1127, 0),
    ("planets with a kepler mass", PD,
     "SELECT count(kepler_derived_stellar_mass) FROM d", 1831, 0),
    # Kepler Derived Stellar Mass null basis (planets_data_4): the derived mass
    # and the recorded host mass are null on different planets.
    ("planets with no derived mass", PD,
     "SELECT count(*) FROM d WHERE kepler_derived_stellar_mass IS NULL", 1541, 0),
    ("no derived mass but a recorded host mass", PD,
     "SELECT count(*) FROM d WHERE kepler_derived_stellar_mass IS NULL "
     "AND host_stellar_mass IS NOT NULL", 1517, 0),
    ("derived mass but no recorded host mass", PD,
     "SELECT count(*) FROM d WHERE kepler_derived_stellar_mass IS NOT NULL "
     "AND host_stellar_mass IS NULL", 297, 0),
    ("planets with a kepler difference", PD,
     "SELECT count(kepler_mass_difference) FROM d", 1534, 0),
    ("planets with a goldilocks value", PD,
     "SELECT count(goldilocks_value) FROM d", 1533, 0),
    ("planets with a host distance", PD,
     "SELECT count(stellar_distance_pc) FROM d", 2296, 0),
    ("planets with a next period ratio", PD,
     "SELECT count(next_planet_period_ratio) FROM d", 861, 0),
    ("planets with a host mass", PD, "SELECT count(host_stellar_mass) FROM d",
     3051, 0),
    ("planets with a host radius", PD,
     "SELECT count(host_stellar_radius) FROM d", 3015, 0),
    ("planets with a host temperature", PD,
     "SELECT count(host_stellar_temperature) FROM d", 3205, 0),
    ("planets with a host luminosity", PD,
     "SELECT count(host_stellar_luminosity) FROM d", 2978, 0),
    ("stars with a distance", SD, "SELECT count(stellar_distance_pc) FROM d",
     1996, 0),
    ("stars with a mass", SD, "SELECT count(stellar_mass) FROM d", 2357, 0),
    ("stars with a radius", SD, "SELECT count(stellar_radius) FROM d", 2228, 0),
    ("stars with a temperature", SD,
     "SELECT count(stellar_temperature) FROM d", 2379, 0),
    ("stars with a magnitude", SD, "SELECT count(optical_magnitude) FROM d",
     2400, 0),
    ("stars with a luminosity", SD, "SELECT count(stellar_luminosity) FROM d",
     2207, 0),
    ("stars with a grav parameter", SD,
     "SELECT count(gravitational_parameter) FROM d", 2357, 0),
    ("stars with an adjacent pair", SD,
     "SELECT count(max_adjacent_period_ratio) FROM d", 568, 0),
    ("stars with a pair count", SD, "SELECT count(adjacent_pair_count) FROM d",
     2508, 0),
    ("stars with a shortest period", SD,
     "SELECT count(shortest_orbital_period) FROM d", 2444, 0),
    ("stars with a heaviest planet", SD,
     "SELECT count(heaviest_planet_mass_jupiter) FROM d", 920, 0),
    ("stars with a densest planet", SD,
     "SELECT count(densest_planet_density) FROM d", 333, 0),
    ("stars with an innermost axis", SD,
     "SELECT count(innermost_semi_major_axis) FROM d", 1244, 0),
    ("distinct RA text", SD,
     "SELECT count(DISTINCT right_ascension_text) FROM d", 2506, 0),
    ("distinct Dec text", SD,
     "SELECT count(DISTINCT declination_text) FROM d", 2508, 0),
    ("distinct raw bands", SD,
     "SELECT count(DISTINCT photometric_band_stored) FROM d", 10, 0),
    ("observations", OD, "SELECT count(*) FROM d", 2683, 0),
    ("distinct observed planets", OD,
     "SELECT count(DISTINCT planet) FROM d", 2460, 0),
    ("distinct observed stars", OD, "SELECT count(DISTINCT star) FROM d",
     1740, 0),
    ("kep observations", OD,
     "SELECT count(*) FROM d WHERE facility = 'kep'", 2329, 0),
    ("ttv observations", OD,
     "SELECT count(*) FROM d WHERE facility = 'ttv'", 225, 0),
    ("k2 observations", OD,
     "SELECT count(*) FROM d WHERE facility = 'k2'", 129, 0),
    ("kep distinct stars", OD,
     "SELECT count(DISTINCT star) FROM d WHERE facility = 'kep'", 1644, 0),
    ("ttv distinct stars", OD,
     "SELECT count(DISTINCT star) FROM d WHERE facility = 'ttv'", 114, 0),
    ("k2 distinct stars", OD,
     "SELECT count(DISTINCT star) FROM d WHERE facility = 'k2'", 94, 0),
    ("max observations per planet", OD,
     "SELECT max(n) FROM (SELECT count(*) n FROM d GROUP BY planet) x", 2, 0),
    ("facilities", FD, "SELECT count(*) FROM d", 3, 0),
    # ------------------------------------------------------ discovery groups --
    ("transit planets", PD,
     "SELECT count(*) FROM d WHERE discovery_method = 'Transit'", 2664, 0),
    ("radial velocity planets", PD,
     "SELECT count(*) FROM d WHERE discovery_method = 'Radial Velocity'",
     591, 0),
    ("imaging planets", PD,
     "SELECT count(*) FROM d WHERE discovery_method = 'Imaging'", 42, 0),
    ("microlensing planets", PD,
     "SELECT count(*) FROM d WHERE discovery_method = 'Microlensing'", 39, 0),
    ("other-method planets", PD,
     "SELECT count(*) FROM d WHERE discovery_method = 'Other'", 21, 0),
    ("ttv-method planets", PD,
     "SELECT count(*) FROM d WHERE discovery_method = 'TTV'", 15, 0),
    ("raw Photometric", PD,
     "SELECT count(*) FROM d WHERE discovery_method_stored = 'Photometric'",
     578, 0),
    ("raw TR", PD,
     "SELECT count(*) FROM d WHERE discovery_method_stored = 'TR'", 536, 0),
    ("raw Transit Method", PD,
     "SELECT count(*) FROM d WHERE discovery_method_stored = 'Transit Method'",
     523, 0),
    ("raw Photometry", PD,
     "SELECT count(*) FROM d WHERE discovery_method_stored = 'Photometry'",
     516, 0),
    ("raw Transit", PD,
     "SELECT count(*) FROM d WHERE discovery_method_stored = 'Transit'", 511, 0),
    ("transit indicator total", PD,
     "SELECT sum(transit_discovery_indicator) FROM d", 2664, 0),
    ("radvel indicator total", PD,
     "SELECT sum(radial_velocity_indicator) FROM d", 591, 0),
    # ----------------------------------------------------- photometric bands --
    ("band Kepler", SD,
     "SELECT count(*) FROM d WHERE photometric_band = 'Kepler'", 1306, 0),
    ("band Johnson V", SD,
     "SELECT count(*) FROM d WHERE photometric_band = 'Johnson V'", 779, 0),
    ("band K-band", SD,
     "SELECT count(*) FROM d WHERE photometric_band = 'K-band'", 315, 0),
    ("band null", SD,
     "SELECT count(*) FROM d WHERE photometric_band IS NULL", 109, 0),
    ("strict Johnson V", SD,
     "SELECT count(*) FROM d WHERE photometric_band_strict = 'Johnson V'",
     624, 0),
    ("strict V-band", SD,
     "SELECT count(*) FROM d WHERE photometric_band_strict = 'V-band'", 155, 0),
    ("group V-Band", SD,
     "SELECT count(*) FROM d WHERE photometric_band_group = 'V-Band'", 779, 0),
    ("group Kepler-Band", SD,
     "SELECT count(*) FROM d WHERE photometric_band_group = 'Kepler-Band'",
     1306, 0),
    ("group null", SD,
     "SELECT count(*) FROM d WHERE photometric_band_group IS NULL", 424, 0),
    ("raw Kepler spelling", SD,
     "SELECT count(*) FROM d WHERE photometric_band_stored = 'Kepler'", 341, 0),
    ("raw Kep-b", SD,
     "SELECT count(*) FROM d WHERE photometric_band_stored = 'Kep-b'", 335, 0),
    ("raw Kepler-band", SD,
     "SELECT count(*) FROM d WHERE photometric_band_stored = 'Kepler-band'",
     323, 0),
    ("raw Kep", SD,
     "SELECT count(*) FROM d WHERE photometric_band_stored = 'Kep'", 307, 0),
    ("raw V", SD,
     "SELECT count(*) FROM d WHERE photometric_band_stored = 'V'", 165, 0),
    # ---------------------------------------------------------- populations --
    ("companion letter b", PD,
     "SELECT count(*) FROM d WHERE companion_letter = 'b'", 2504, 0),
    ("companion letter c", PD,
     "SELECT count(*) FROM d WHERE companion_letter = 'c'", 572, 0),
    ("companion letter h", PD,
     "SELECT count(*) FROM d WHERE companion_letter = 'h'", 3, 0),
    ("gas giants", PD, "SELECT sum(gas_giant_indicator) FROM d", 929, 0),
    ("gas giant no", PD,
     "SELECT count(*) FROM d WHERE gas_giant_planet = 'No'", 245, 0),
    ("rocky planets", PD, "SELECT sum(rocky_indicator) FROM d", 74, 0),
    ("rocky no", PD, "SELECT count(*) FROM d WHERE rocky_planet = 'No'", 314, 0),
    ("short period planets", PD, "SELECT sum(short_period_indicator) FROM d",
     1445, 0),
    ("short period no", PD,
     "SELECT count(*) FROM d WHERE short_period_planet = 'No'", 1860, 0),
    ("hot jupiters", PD, "SELECT sum(hot_jupiter_indicator) FROM d", 327, 0),
    ("hot jupiter retrograde", PD,
     "SELECT count(*) FROM d WHERE hot_jupiter = 'Yes' "
     "AND retrograde_orbit = 'Yes'", 0, 0),
    ("super earths", PD, "SELECT sum(super_earth_indicator) FROM d", 31, 0),
    ("super earths by transit", PD,
     "SELECT count(*) FROM d WHERE super_earth = 'Yes' "
     "AND discovery_method = 'Transit'", 29, 0),
    ("habitable zone planets", PD,
     "SELECT sum(habitable_zone_indicator) FROM d", 28, 0),
    ("potentially habitable", PD,
     "SELECT sum(potentially_habitable_indicator) FROM d", 0, 0),
    ("high eccentricity", PD, "SELECT sum(high_eccentricity_indicator) FROM d",
     249, 0),
    ("retrograde planets", PD, "SELECT sum(retrograde_indicator) FROM d", 8, 0),
    ("inflated gas giants", PD,
     "SELECT sum(inflated_gas_giant_indicator) FROM d", 103, 0),
    ("inflated giants with a distance", PD,
     "SELECT count(*) FROM d WHERE inflated_gas_giant = 'Yes' "
     "AND stellar_distance_ly IS NOT NULL", 84, 0),
    ("multi planetary planets", PD,
     "SELECT count(*) FROM d WHERE in_multi_planetary_system = 'Yes'", 1431, 0),
    ("period high precision", PD,
     "SELECT count(*) FROM d WHERE period_high_precision = 'Yes'", 3125, 0),
    ("mass high precision", PD,
     "SELECT count(*) FROM d WHERE mass_high_precision = 'Yes'", 198, 0),
    ("well characterized", PD,
     "SELECT sum(well_characterized_indicator) FROM d", 48, 0),
    ("minimum mass planets", PD,
     "SELECT count(*) FROM d WHERE minimum_mass_status = 'Yes'", 554, 0),
    ("true mass planets", PD,
     "SELECT count(*) FROM d WHERE mass_source = 'Mass'", 611, 0),
    ("corrected mass planets", PD,
     "SELECT count(*) FROM d WHERE mass_source = 'Msin(i)/sin(i)'", 9, 0),
    ("radius upper limits", PD,
     "SELECT sum(radius_upper_limit_indicator) FROM d", 1, 0),
    ("distance upper limits", PD,
     "SELECT sum(distance_upper_limit_indicator) FROM d", 0, 0),
    ("temperature blends", PD,
     "SELECT sum(temperature_blend_indicator) FROM d", 0, 0),
    ("any stellar blend", PD,
     "SELECT count(*) FROM d WHERE any_stellar_blend = 'Yes'", 9, 0),
    ("kepler observed planets", PD,
     "SELECT sum(kepler_observation_indicator) FROM d", 2329, 0),
    ("k2 observed planets", PD, "SELECT sum(k2_observation_indicator) FROM d",
     129, 0),
    ("ttv observed planets", PD,
     "SELECT sum(ttv_observation_indicator) FROM d", 225, 0),
    ("planets observed", PD,
     "SELECT count(*) FROM d WHERE observed_by_a_survey = 'Yes'", 2460, 0),
    ("planets unobserved", PD,
     "SELECT count(*) FROM d WHERE observed_by_a_survey = 'No'", 912, 0),
    ("k2 gas giants", PD,
     "SELECT count(*) FROM d WHERE k2_observation_indicator = 1 "
     "AND gas_giant_planet = 'Yes'", 14, 0),
    ("kepler planets with a bad temperature", PD,
     "SELECT count(*) FROM d WHERE kepler_observation_indicator = 1 "
     "AND temperature_blend_flag = 1", 0, 0),
    ("multi planetary stars", SD,
     "SELECT sum(multi_planetary_indicator) FROM d", 569, 0),
    ("stars with multiple planet rows", SD,
     "SELECT count(*) FROM d WHERE multiple_planet_rows = 'Yes'", 570, 0),
    ("companion and row count disagree", SD,
     "SELECT count(*) FROM d WHERE (companion_count > 1) "
     "<> (star_planet_count > 1)", 1, 0),
    ("kepler stars", SD, "SELECT sum(kepler_observation_indicator) FROM d",
     1644, 0),
    ("k2 stars", SD, "SELECT sum(k2_observation_indicator) FROM d", 94, 0),
    ("ttv stars", SD, "SELECT sum(ttv_observation_indicator) FROM d", 114, 0),
    ("stars with more than one pair", SD,
     "SELECT count(*) FROM d WHERE adjacent_pair_count > 1", 193, 0),
    ("stars all ratios under 3", SD,
     "SELECT count(*) FROM d WHERE max_adjacent_period_ratio < 3", 333, 0),
    ("stars all ratios under 3 and fast", SD,
     "SELECT count(*) FROM d WHERE max_adjacent_period_ratio < 3 "
     "AND shortest_orbital_period < 10", 210, 0),
    ("star blends", SD,
     "SELECT count(*) FROM d WHERE any_blended_measurement = 'Yes'", 7, 0),
    # ------------------------------------------------------ means and ranges --
    ("mean period", PD, "SELECT avg(orbital_period_days) FROM d", 2725.8, 5e-1),
    ("min period", PD, "SELECT min(orbital_period_days) FROM d", 0.0907063,
     5e-7),
    ("max period", PD, "SELECT max(orbital_period_days) FROM d", 7300000, 5e-1),
    ("mean semi-major axis", PD, "SELECT avg(semi_major_axis_au) FROM d",
     7.7042, 5e-4),
    ("max semi-major axis", PD, "SELECT max(semi_major_axis_au) FROM d",
     2500, 5e-9),
    ("mean eccentricity", PD, "SELECT avg(eccentricity) FROM d", 0.17079, 5e-6),
    ("max eccentricity", PD, "SELECT max(eccentricity) FROM d", 0.956, 5e-6),
    ("mean inclination", PD, "SELECT avg(inclination_degrees) FROM d",
     85.935, 5e-3),
    ("max inclination", PD, "SELECT max(inclination_degrees) FROM d",
     90.76, 5e-3),
    ("min inclination", PD, "SELECT min(inclination_degrees) FROM d",
     17.6, 5e-3),
    ("mean mass jupiter", PD, "SELECT avg(planet_mass_jupiter) FROM d",
     2.6284, 5e-4),
    ("max mass jupiter", PD, "SELECT max(planet_mass_jupiter) FROM d",
     28.5, 5e-4),
    ("mean mass earth", PD, "SELECT avg(planet_mass_earth) FROM d",
     835.37, 5e-2),
    ("max mass earth", PD, "SELECT max(planet_mass_earth) FROM d", 9058.2, 5e-1),
    ("mean radius jupiter", PD, "SELECT avg(planet_radius_jupiter) FROM d",
     0.34199, 5e-5),
    ("max radius jupiter", PD, "SELECT max(planet_radius_jupiter) FROM d",
     6.9, 5e-4),
    ("mean radius earth", PD, "SELECT avg(planet_radius_earth) FROM d",
     3.8333, 5e-4),
    ("max radius earth", PD, "SELECT max(planet_radius_earth) FROM d",
     77.342, 5e-3),
    ("mean density", PD, "SELECT avg(planet_density) FROM d", 2.5591, 5e-4),
    ("max density", PD, "SELECT max(planet_density) FROM d", 77.7, 5e-4),
    ("min density", PD, "SELECT min(planet_density) FROM d", 0.03, 5e-6),
    ("mean surface gravity", PD, "SELECT avg(surface_gravity) FROM d",
     22.225, 5e-3),
    ("max surface gravity", PD, "SELECT max(surface_gravity) FROM d",
     1254.7, 5e-1),
    ("mean surface gravity super earth transit", PD,
     "SELECT avg(surface_gravity) FROM d WHERE super_earth = 'Yes' "
     "AND discovery_method = 'Transit'", 2.5379, 5e-4),
    ("max surface gravity super earth", PD,
     "SELECT max(surface_gravity) FROM d WHERE super_earth = 'Yes'",
     11.6926, 5e-4),
    ("mean mass radius ratio", PD, "SELECT avg(mass_radius_ratio) FROM d",
     81.316, 5e-3),
    ("max mass radius ratio", PD, "SELECT max(mass_radius_ratio) FROM d",
     2742.43, 5e-2),
    ("mean kepler mass", PD,
     "SELECT avg(kepler_derived_stellar_mass) FROM d", 1.0188, 5e-4),
    ("max kepler mass", PD,
     "SELECT max(kepler_derived_stellar_mass) FROM d", 3.9148, 5e-4),
    ("mean kepler difference", PD, "SELECT avg(kepler_mass_difference) FROM d",
     0.013911, 5e-7),
    ("mean goldilocks", PD, "SELECT avg(goldilocks_value) FROM d",
     15.579, 5e-3),
    ("mean planet distance ly", PD, "SELECT avg(stellar_distance_ly) FROM d",
     2035.0, 5e-1),
    ("mean distance ly inflated giants", PD,
     "SELECT avg(stellar_distance_ly) FROM d "
     "WHERE inflated_gas_giant = 'Yes' AND stellar_distance_ly IS NOT NULL",
     1497.29, 5e-2),
    ("mean note count", PD, "SELECT avg(note_count) FROM d", 0.70463, 5e-5),
    ("total note count", PD, "SELECT sum(note_count) FROM d", 2376, 0),
    ("mean next period ratio", PD,
     "SELECT avg(next_planet_period_ratio) FROM d", 20.361, 5e-3),
    ("mean period uncertainty", PD,
     "SELECT avg(period_relative_uncertainty) FROM d", 0.75482, 5e-5),
    ("mean mass uncertainty", PD,
     "SELECT avg(mass_relative_uncertainty) FROM d", 30.343, 5e-3),
    ("mean radius uncertainty", PD,
     "SELECT avg(radius_relative_uncertainty) FROM d", 17.864, 5e-3),
    ("mean density uncertainty", PD,
     "SELECT avg(density_relative_uncertainty) FROM d", 44.315, 5e-3),
    ("mean eccentricity uncertainty", PD,
     "SELECT avg(eccentricity_relative_uncertainty) FROM d", 74.166, 5e-3),
    ("mean stellar distance pc", SD,
     "SELECT avg(stellar_distance_pc) FROM d", 660.37, 5e-2),
    ("mean stellar distance ly", SD,
     "SELECT avg(stellar_distance_ly) FROM d", 2153.8, 5e-1),
    ("max stellar distance pc", SD,
     "SELECT max(stellar_distance_pc) FROM d", 8500, 5e-2),
    ("min stellar distance pc", SD,
     "SELECT min(stellar_distance_pc) FROM d", 3.21, 5e-3),
    ("mean stellar mass", SD, "SELECT avg(stellar_mass) FROM d", 0.99986, 5e-5),
    ("max stellar mass", SD, "SELECT max(stellar_mass) FROM d", 3.9, 5e-4),
    ("min stellar mass", SD, "SELECT min(stellar_mass) FROM d", 0.02, 5e-4),
    ("mean stellar radius", SD, "SELECT avg(stellar_radius) FROM d",
     1.6097, 5e-4),
    ("max stellar radius", SD, "SELECT max(stellar_radius) FROM d",
     51.1, 5e-3),
    ("mean stellar temperature", SD,
     "SELECT avg(stellar_temperature) FROM d", 5545.5, 5e-2),
    ("max stellar temperature", SD,
     "SELECT max(stellar_temperature) FROM d", 57000, 0),
    ("min stellar temperature", SD,
     "SELECT min(stellar_temperature) FROM d", 575, 0),
    ("mean optical magnitude", SD, "SELECT avg(optical_magnitude) FROM d",
     12.893, 5e-3),
    ("min optical magnitude", SD, "SELECT min(optical_magnitude) FROM d",
     0.85, 5e-4),
    ("max optical magnitude", SD, "SELECT max(optical_magnitude) FROM d",
     20.15, 5e-3),
    ("mean stellar luminosity", SD, "SELECT avg(stellar_luminosity) FROM d",
     5.6405, 5e-4),
    ("max stellar luminosity", SD, "SELECT max(stellar_luminosity) FROM d",
     630.99, 5e-2),
    ("mean grav parameter", SD,
     "SELECT avg(gravitational_parameter) FROM d", 1.32697e20, 5e15),
    ("min grav parameter", SD,
     "SELECT min(gravitational_parameter) FROM d", 2.6542e18, 5e14),
    ("max grav parameter", SD,
     "SELECT max(gravitational_parameter) FROM d", 5.1758e20, 5e16),
    ("mean hz inner", SD, "SELECT avg(habitable_zone_inner_au) FROM d",
     1.2955, 5e-4),
    ("mean hz outer", SD, "SELECT avg(habitable_zone_outer_au) FROM d",
     1.8664, 5e-4),
    ("mean planet count", SD, "SELECT avg(star_planet_count) FROM d",
     1.344, 5e-4),
    ("max planet count", SD, "SELECT max(star_planet_count) FROM d", 7, 0),
    ("total system planets", SD, "SELECT sum(star_planet_count) FROM d",
     3372, 0),
    ("mean companion count", SD, "SELECT avg(companion_count) FROM d",
     1.3436, 5e-4),
    ("mean shortest period", SD,
     "SELECT avg(shortest_orbital_period) FROM d", 3476.5, 5e-1),
    ("mean max adjacent ratio", SD,
     "SELECT avg(max_adjacent_period_ratio) FROM d", 29.783, 5e-3),
    ("mean mean adjacent ratio", SD,
     "SELECT avg(mean_adjacent_period_ratio) FROM d", 28.940, 5e-3),
    ("min min adjacent ratio", SD,
     "SELECT min(min_adjacent_period_ratio) FROM d", 1.0061, 5e-4),
    ("max max adjacent ratio", SD,
     "SELECT max(max_adjacent_period_ratio) FROM d", 4482.2, 5e-1),
    ("total adjacent pairs", SD, "SELECT sum(adjacent_pair_count) FROM d",
     861, 0),
    ("total star gas giants", SD, "SELECT sum(star_gas_giant_count) FROM d",
     929, 0),
    ("total star rocky", SD, "SELECT sum(star_rocky_planet_count) FROM d",
     74, 0),
    ("total star with density", SD,
     "SELECT sum(star_planets_with_density) FROM d", 388, 0),
    ("total star short period", SD,
     "SELECT sum(star_short_period_count) FROM d", 1445, 0),
    ("total star transit", SD,
     "SELECT sum(star_transit_discovery_count) FROM d", 2664, 0),
    ("total star radvel", SD,
     "SELECT sum(star_radial_velocity_count) FROM d", 591, 0),
    ("mean heaviest planet", SD,
     "SELECT avg(heaviest_planet_mass_jupiter) FROM d", 3.0974, 5e-4),
    ("mean largest radius", SD,
     "SELECT avg(largest_planet_radius_jupiter) FROM d", 0.39878, 5e-5),
    ("mean densest planet", SD, "SELECT avg(densest_planet_density) FROM d",
     2.6541, 5e-4),
    ("mean RA", SD, "SELECT avg(right_ascension_degrees) FROM d", 255.23, 5e-2),
    ("mean Dec", SD, "SELECT avg(declination_degrees) FROM d", 27.901, 5e-3),
    ("min Dec", SD, "SELECT min(declination_degrees) FROM d", -84.232, 5e-3),
    ("max Dec", SD, "SELECT max(declination_degrees) FROM d", 85.736, 5e-3),
    # ------------------------------------------ 2026-08-27 constants and units --
    ("planets with an eq temperature", PD,
     "SELECT count(equilibrium_temperature) FROM d", 1533, 0),
    ("planets with an escape velocity", PD,
     "SELECT count(escape_velocity_kms) FROM d", 509, 0),
    ("planets with an orbital velocity", PD,
     "SELECT count(orbital_velocity_kms) FROM d", 1593, 0),
    ("planets with a transit depth", PD, "SELECT count(transit_depth) FROM d",
     2684, 0),
    ("stars with a density", SD, "SELECT count(stellar_density_kg_m3) FROM d",
     2117, 0),
    ("mean eq temperature", PD, "SELECT avg(equilibrium_temperature) FROM d",
     886.69, 5e-2),
    ("max eq temperature", PD, "SELECT max(equilibrium_temperature) FROM d",
     7720.038224, 5e-6),
    ("hottest non hot jupiter", PD,
     "SELECT planet_name FROM d WHERE hot_jupiter = 'No' "
     "AND equilibrium_temperature IS NOT NULL "
     "ORDER BY equilibrium_temperature DESC LIMIT 1", "KOI-55 b", 0),
    ("mean eq temperature K2 giants", PD,
     "SELECT avg(equilibrium_temperature) FROM d "
     "WHERE k2_observation_indicator = 1 AND gas_giant_planet = 'Yes'",
     1395.505740, 5e-6),
    ("mean transit depth", PD, "SELECT avg(transit_depth) FROM d",
     0.0029442, 5e-8),
    ("max transit depth", PD, "SELECT max(transit_depth) FROM d", 1.1347, 5e-4),
    ("max transit depth percent radvel", PD,
     "SELECT max(transit_depth_percent) FROM d "
     "WHERE discovery_method = 'Radial Velocity'", 1.463525553, 5e-9),
    ("mean mass ratio", PD, "SELECT avg(planet_star_mass_ratio) FROM d",
     0.0058646, 5e-8),
    ("max mass ratio", PD, "SELECT max(planet_star_mass_ratio) FROM d",
     0.69997, 5e-5),
    ("mean escape velocity", PD, "SELECT avg(escape_velocity_kms) FROM d",
     66.962, 5e-3),
    ("max escape velocity", PD, "SELECT max(escape_velocity_kms) FROM d",
     585.451326, 5e-6),
    ("max escape velocity ms", PD, "SELECT max(escape_velocity_ms) FROM d",
     585451.326, 5e-3),
    ("mean orbital velocity", PD, "SELECT avg(orbital_velocity_kms) FROM d",
     82.094, 5e-3),
    ("max orbital velocity", PD, "SELECT max(orbital_velocity_kms) FROM d",
     531.293, 5e-3),
    ("mean kepler abs difference", PD,
     "SELECT avg(kepler_mass_absolute_difference) FROM d", 0.050136, 5e-6),
    ("mean stellar density", SD, "SELECT avg(stellar_density_kg_m3) FROM d",
     16570.6, 5e-1),
    ("max stellar density", SD, "SELECT max(stellar_density_kg_m3) FROM d",
     30839867.77, 5e-2),
    ("densest star", SD,
     "SELECT star_name FROM d ORDER BY stellar_density_kg_m3 DESC NULLS LAST "
     "LIMIT 1", "PSR J1719-1438", 0),
    ("density max over min", SD,
     "SELECT max(stellar_density_kg_m3) / min(stellar_density_kg_m3) FROM d",
     2237875935.98, 5e-2),
    ("55 Cnc density", SD,
     "SELECT stellar_density_kg_m3 FROM d WHERE star_name = '55 Cnc'",
     1544.622195, 5e-6),
    ("mean stellar density solar", SD,
     "SELECT avg(stellar_density_solar) FROM d", 2.806, 5e-3),
    ("alf Tau grav parameter", SD,
     "SELECT gravitational_parameter FROM d WHERE star_name = 'alf Tau'",
     1.499695915e20, 5e11),
    ("hot jupiter no", PD,
     "SELECT count(*) FROM d WHERE hot_jupiter = 'No'", 1967, 0),
    ("hot jupiter null", PD,
     "SELECT count(*) FROM d WHERE hot_jupiter IS NULL", 1078, 0),
    ("super earth no", PD,
     "SELECT count(*) FROM d WHERE super_earth = 'No'", 1075, 0),
    ("inflated no", PD,
     "SELECT count(*) FROM d WHERE inflated_gas_giant = 'No'", 422, 0),
    ("potentially habitable judgeable", PD,
     "SELECT count(*) FROM d WHERE potentially_habitable IS NOT NULL", 1538, 0),
    ("well characterized judgeable", PD,
     "SELECT count(*) FROM d WHERE well_characterized_planet IS NOT NULL",
     2929, 0),
    ("radius high precision", PD,
     "SELECT count(*) FROM d WHERE radius_high_precision = 'Yes'", 396, 0),
    ("retrograde inclusive", PD,
     "SELECT sum(retrograde_inclusive_indicator) FROM d", 29, 0),
    ("hot jupiter at 90 or more", PD,
     "SELECT count(*) FROM d WHERE hot_jupiter = 'Yes' "
     "AND retrograde_orbit_inclusive = 'Yes'", 5, 0),
    ("inclination exactly 90", PD,
     "SELECT count(*) FROM d WHERE inclination_degrees = 90", 21, 0),
    ("mass upper limits", PD, "SELECT sum(mass_upper_limit_indicator) FROM d",
     64, 0),
    ("eccentricity upper limits", PD,
     "SELECT count(*) FROM d WHERE eccentricity_upper_limit = 'Yes'", 71, 0),
    ("density upper limits", PD,
     "SELECT count(*) FROM d WHERE density_upper_limit = 'Yes'", 9, 0),
    ("distance upper limit no", PD,
     "SELECT count(*) FROM d WHERE distance_upper_limit = 'No'", 2293, 0),
    ("magnitude blended yes", PD,
     "SELECT count(*) FROM d WHERE magnitude_blended = 'Yes'", 9, 0),
    ("inflated giants clean distance", PD,
     "SELECT count(*) FROM d WHERE inflated_gas_giant = 'Yes' "
     "AND distance_upper_limit = 'No' AND magnitude_blended = 'No'", 78, 0),
    ("mean distance ly inflated giants clean", PD,
     "SELECT avg(stellar_distance_ly) FROM d WHERE inflated_gas_giant = 'Yes' "
     "AND distance_upper_limit = 'No' AND magnitude_blended = 'No'",
     1446.1213, 5e-4),
    ("clean distance column non-null count", PD,
     "SELECT count(stellar_distance_ly_clean) FROM d", 2188, 0),
    ("clean distance column mean", PD,
     "SELECT avg(stellar_distance_ly_clean) FROM d", 1869.1787, 5e-4),
    ("clean distance column matches two-filter screen on inflated giants", PD,
     "SELECT avg(stellar_distance_ly_clean) FROM d "
     "WHERE inflated_gas_giant = 'Yes'", 1446.1213, 5e-4),
    ("rocky only stars", SD,
     "SELECT count(*) FROM d WHERE system_composition = 'Rocky Only'", 27, 0),
    ("gas giants only stars", SD,
     "SELECT count(*) FROM d WHERE system_composition = 'Gas Giants Only'",
     782, 0),
    ("mixed stars", SD,
     "SELECT count(*) FROM d WHERE system_composition = 'Mixed'", 35, 0),
    ("neither stars", SD,
     "SELECT count(*) FROM d WHERE system_composition = 'Neither'", 77, 0),
    ("composition null", SD,
     "SELECT count(*) FROM d WHERE system_composition IS NULL", 1588, 0),
    ("has rocky yes", SD,
     "SELECT count(*) FROM d WHERE has_rocky_planet = 'Yes'", 62, 0),
    ("has gas giant yes", SD,
     "SELECT count(*) FROM d WHERE has_gas_giant = 'Yes'", 817, 0),
    ("rocky only indicator", SD, "SELECT sum(rocky_only_indicator) FROM d",
     27, 0),
    ("all density measured rocky", SD,
     "SELECT count(*) FROM d WHERE all_density_measured_rocky = 'Yes'", 49, 0),
    ("all density measured rocky no", SD,
     "SELECT count(*) FROM d WHERE all_density_measured_rocky = 'No'", 284, 0),
    ("mean luminosity rocky-only stars", SD,
     "SELECT avg(stellar_luminosity) FROM d "
     "WHERE system_composition = 'Rocky Only'", 0.96207389, 5e-8),
    ("mean mass gas-giants-only stars", SD,
     "SELECT avg(stellar_mass) FROM d "
     "WHERE system_composition = 'Gas Giants Only'", 1.12379, 5e-5),
    ("mean luminosity all-density-rocky stars", SD,
     "SELECT avg(stellar_luminosity) FROM d "
     "WHERE all_density_measured_rocky = 'Yes'", 1.6729, 5e-4),
    ("mean magnitude all-density-rocky stars", SD,
     "SELECT avg(optical_magnitude) FROM d "
     "WHERE all_density_measured_rocky = 'Yes'", 11.870, 5e-3),
    ("stars with a geometric mean", SD,
     "SELECT count(geometric_mean_adjacent_period_ratio) FROM d", 568, 0),
    ("mean geometric ratio", SD,
     "SELECT avg(geometric_mean_adjacent_period_ratio) FROM d", 28.598, 5e-3),
    ("mean geometric ratio compact", SD,
     "SELECT avg(geometric_mean_adjacent_period_ratio) FROM d "
     "WHERE max_adjacent_period_ratio < 3 AND shortest_orbital_period < 10",
     1.98959, 5e-5),
    ("geometric vs arithmetic differ", SD,
     "SELECT count(*) FROM d WHERE round(geometric_mean_adjacent_period_ratio"
     "::numeric, 3) <> round(mean_adjacent_period_ratio::numeric, 3)", 177, 0),
    ("compact systems complete pairs", SD,
     "SELECT count(*) FROM d WHERE max_adjacent_period_ratio < 3 "
     "AND shortest_orbital_period < 10 "
     "AND adjacent_pair_count = companion_count - 1", 210, 0),
    ("planets with composition", SD,
     "SELECT sum(star_planets_with_composition) FROM d", 1176, 0),
    ("real display rows differing from float print", PD,
     "SELECT count(*) FROM d WHERE orbital_period_days::text "
     "<> orbital_period_days::double precision::real::text", 1, 0),
]
