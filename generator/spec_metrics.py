"""Metrics and calculated metrics for the planets_data model."""

F_COUNT = "Record And Entity Counts"
F_SUPPORT = "Support Sets And Coverage"
F_ORBITM = "Orbital Measures"
F_PHYSM = "Physical Measures"
F_DERIVM = "Derived Quantity Measures"
F_STARM = "Stellar Measures"
F_SYSM = "Star System Measures"
F_FLAGM = "Classification Counts"
F_QUALM = "Measurement Quality Measures"
F_CALC_RATE = "Calculations - Shares And Rates"
F_CALC_GROUP = "Calculations - Group Formulas"

P = "Planet Detail"
S = "Star Detail"
O = "Planet Observation"
F = "Survey Facility Detail"


def m(name, dataset, column, method, folder, desc, **kw):
    d = {"unique_name": name, "label": name, "dataset": dataset,
         "column": column, "calculation_method": method, "folder": folder,
         "description": desc}
    d.update(kw)
    return d


METRICS = [
    # ------------------------------------------------------------- counts --
    m("Planet Count", P, "planet_row_count", "sum", F_COUNT,
      "How many planets, number of exoplanets. All 3372 regardless of which "
      "measurements they carry, so a question about a physical property must "
      "filter first - a mass exists for 1174 and a density for 388."),
    m("Star Count", S, "star_row_count", "sum", F_COUNT,
      "How many host stars, number of stars, number of systems. All 2509, each "
      "hosting at least one planet."),
    m("Distinct Star Count On Planets", P, "star", "count distinct", F_COUNT,
      "How many distinct host stars the selected planets belong to. 2509 across "
      "all 3372 planets. Use this rather than Planet Count whenever the question "
      "counts stars or systems but filters planets."),
    m("Observation Count", O, "observation_row_count", "sum", F_COUNT,
      "How many planet-to-survey observation records. All 2683, over 2460 "
      "planets and 3 facilities."),
    m("Distinct Observed Planet Count", O, "planet", "count distinct",
      F_COUNT,
      "How many distinct planets the selected observations cover. 2460 across "
      "all 2683 observations, so 912 planets were never observed by any of the "
      "three surveys."),
    m("Distinct Observed Star Count", O, "star", "count distinct", F_COUNT,
      "How many distinct host stars the selected observations reach. 1740 across "
      "all 2683 observations."),
    m("Survey Facility Count", F, "facility_row_count", "sum", F_COUNT,
      "How many observing facilities. Exactly 3: 'kep', 'k2' and 'ttv'."),

    # ------------------------------------------------------- support sets --
    m("Planets With A Period", P, "orbital_period_days", "count non-null",
      F_SUPPORT,
      "How many of the selected planets record an orbital period. 3305 of 3372 "
      "warehouse-wide."),
    m("Planets With A Semi Major Axis", P, "semi_major_axis_au",
      "count non-null", F_SUPPORT,
      "How many of the selected planets record a semi-major axis. 1897 of 3372 "
      "warehouse-wide - the binding constraint on the equilibrium temperature, "
      "the orbital velocity, the habitable-zone test and the Kepler's-law "
      "check."),
    m("Planets With A Mass", P, "planet_mass_jupiter", "count non-null",
      F_SUPPORT,
      "How many of the selected planets record a mass. 1174 of 3372 "
      "warehouse-wide, and 554 of those are minimum masses rather than true "
      "ones."),
    m("Planets With A Radius", P, "planet_radius_jupiter", "count non-null",
      F_SUPPORT,
      "How many of the selected planets record a radius. 2694 of 3372 "
      "warehouse-wide."),
    m("Planets With A Density", P, "planet_density", "count non-null",
      F_SUPPORT,
      "How many of the selected planets record a bulk density. 388 of 3372 "
      "warehouse-wide - the scarcest physical measurement, and the ceiling on "
      "every rocky, super-Earth, inflated-giant and potentially-habitable "
      "answer."),
    m("Planets With An Eccentricity", P, "eccentricity", "count non-null",
      F_SUPPORT,
      "How many of the selected planets record an eccentricity. 974 of 3372 "
      "warehouse-wide."),
    m("Planets With An Inclination", P, "inclination_degrees",
      "count non-null", F_SUPPORT,
      "How many of the selected planets record an inclination. 502 of 3372 "
      "warehouse-wide - so a retrograde-orbit question can only be answered for "
      "one planet in seven."),
    m("Planets With A Surface Gravity", P, "surface_gravity",
      "count non-null", F_SUPPORT,
      "How many of the selected planets have a computable surface gravity, "
      "which needs both a mass and a radius. 509 of 3372 warehouse-wide. The "
      "same 509 have an escape velocity and a mass-radius ratio."),
    m("Planets With An Equilibrium Temperature", P,
      "equilibrium_temperature", "count non-null", F_SUPPORT,
      "How many of the selected planets have a computable equilibrium "
      "temperature, which needs a stellar temperature, a stellar radius and a "
      "semi-major axis. 1533 of 3372 warehouse-wide. The same 1533 have a "
      "Goldilocks value."),
    m("Planets With A Transit Depth", P, "transit_depth", "count non-null",
      F_SUPPORT,
      "How many of the selected planets have a computable transit depth, which "
      "needs a planet radius and a stellar radius. 2684 of 3372 "
      "warehouse-wide."),
    m("Planets With An Orbital Velocity", P, "orbital_velocity_ms",
      "count non-null", F_SUPPORT,
      "How many of the selected planets have a computable orbital velocity. "
      "1593 of 3372 warehouse-wide."),
    m("Planets With A Mass Ratio", P, "planet_star_mass_ratio",
      "count non-null", F_SUPPORT,
      "How many of the selected planets have a computable planet-star mass "
      "ratio. 1127 of 3372 warehouse-wide."),
    m("Planets With A Kepler Mass", P, "kepler_derived_stellar_mass",
      "count non-null", F_SUPPORT,
      "How many of the selected planets yield a Kepler's-law stellar mass. 1831 "
      "of 3372 warehouse-wide; 1534 of those also have a reported stellar mass "
      "to compare against."),
    m("Planets With A Host Distance", P, "stellar_distance_pc",
      "count non-null", F_SUPPORT,
      "How many of the selected planets have a host-star distance. 2296 of 3372 "
      "warehouse-wide."),
    m("Planets With A Next Period Ratio", P, "next_planet_period_ratio",
      "count non-null", F_SUPPORT,
      "How many of the selected planets have a longer-period sibling, and so an "
      "adjacent period ratio. 861 of 3372 warehouse-wide."),
    m("Stars With A Distance", S, "stellar_distance_pc", "count non-null",
      F_SUPPORT,
      "How many of the selected stars record a distance. 1996 of 2509 "
      "warehouse-wide."),
    m("Stars With A Mass", S, "stellar_mass", "count non-null", F_SUPPORT,
      "How many of the selected stars record a mass. 2357 of 2509 "
      "warehouse-wide - the support set for the gravitational parameter."),
    m("Stars With A Radius", S, "stellar_radius", "count non-null", F_SUPPORT,
      "How many of the selected stars record a radius. 2228 of 2509 "
      "warehouse-wide."),
    m("Stars With A Temperature", S, "stellar_temperature", "count non-null",
      F_SUPPORT,
      "How many of the selected stars record an effective temperature. 2379 of "
      "2509 warehouse-wide."),
    m("Stars With A Luminosity", S, "stellar_luminosity", "count non-null",
      F_SUPPORT,
      "How many of the selected stars have a computable luminosity, which needs "
      "both a radius and a temperature. 2207 of 2509 warehouse-wide. The same "
      "2207 have habitable-zone boundaries."),
    m("Stars With A Density", S, "stellar_density_solar", "count non-null",
      F_SUPPORT,
      "How many of the selected stars have a computable mean density. 2117 of "
      "2509 warehouse-wide."),
    m("Stars With A Magnitude", S, "optical_magnitude", "count non-null",
      F_SUPPORT,
      "How many of the selected stars record an apparent magnitude. 2400 of "
      "2509 warehouse-wide; the same 2400 record a photometric band."),
    m("Stars With An Adjacent Pair", S, "max_adjacent_period_ratio",
      "count non-null", F_SUPPORT,
      "How many of the selected stars have at least one adjacent planet pair "
      "with both periods recorded. 568 of 2509 warehouse-wide, out of 569 that "
      "declare more than one companion."),

    # ------------------------------------------------------------- orbital --
    m("Mean Orbital Period Days", P, "orbital_period_days", "average",
      F_ORBITM,
      "Mean orbital period in days. 2725.8 across the 3305 planets that record "
      "one. The distribution spans eight orders of magnitude, so this mean is "
      "dominated by a few very wide orbits and the median would be far lower."),
    m("Minimum Orbital Period Days", P, "orbital_period_days", "minimum",
      F_ORBITM,
      "Shortest orbital period among the selected planets. 0.0907 days "
      "warehouse-wide - about two hours."),
    m("Maximum Orbital Period Days", P, "orbital_period_days", "maximum",
      F_ORBITM,
      "Longest orbital period among the selected planets. 7,300,000 days "
      "warehouse-wide, or about 20,000 years."),
    m("Mean Semi Major Axis", P, "semi_major_axis_au", "average", F_ORBITM,
      "Mean semi-major axis in AU. 7.7042 across 1897 planets."),
    m("Mean Eccentricity", P, "eccentricity", "average", F_ORBITM,
      "Mean orbital eccentricity. 0.17079 across 974 planets."),
    m("Maximum Eccentricity", P, "eccentricity", "maximum", F_ORBITM,
      "Highest eccentricity among the selected planets. 0.956 warehouse-wide - "
      "a nearly parabolic orbit."),
    m("Mean Inclination", P, "inclination_degrees", "average", F_ORBITM,
      "Mean orbital inclination in degrees. 85.935 across 502 planets."),
    m("Maximum Inclination", P, "inclination_degrees", "maximum", F_ORBITM,
      "Highest inclination among the selected planets. 90.76 degrees "
      "warehouse-wide, which is only 0.76 above the retrograde threshold."),
    m("Mean Next Period Ratio", P, "next_planet_period_ratio", "average",
      F_ORBITM,
      "Mean ratio between adjacent planets' periods, over planets. 20.361 "
      "across 861 planets. For the per-system figure use the star-level "
      "measures, which average the ratios inside each system first."),

    # ------------------------------------------------------------ physical --
    m("Mean Planet Mass Jupiter", P, "planet_mass_jupiter", "average",
      F_PHYSM,
      "Mean planet mass in Jupiter masses. 2.6284 across the 1174 planets that "
      "record one."),
    m("Mean Planet Mass Earth", P, "planet_mass_earth", "average", F_PHYSM,
      "Mean planet mass in Earth masses. 835.37 across 1174 planets - the same "
      "figure multiplied by 317.83."),
    m("Maximum Planet Mass Jupiter", P, "planet_mass_jupiter", "maximum",
      F_PHYSM,
      "Heaviest planet among the selection, in Jupiter masses. 28.5 "
      "warehouse-wide."),
    m("Mean Planet Radius Jupiter", P, "planet_radius_jupiter", "average",
      F_PHYSM,
      "Mean planet radius in Jupiter radii. 0.34199 across 2694 planets."),
    m("Mean Planet Radius Earth", P, "planet_radius_earth", "average",
      F_PHYSM,
      "Mean planet radius in Earth radii. 3.8333 across 2694 planets."),
    m("Maximum Planet Radius Jupiter", P, "planet_radius_jupiter", "maximum",
      F_PHYSM,
      "Largest planet among the selection, in Jupiter radii. 6.9 "
      "warehouse-wide."),
    m("Mean Planet Density", P, "planet_density", "average", F_PHYSM,
      "Mean bulk density in grams per cubic centimetre. 2.5591 across only 388 "
      "planets."),
    m("Maximum Planet Density", P, "planet_density", "maximum", F_PHYSM,
      "Highest bulk density among the selection. 77.7 grams per cubic "
      "centimetre warehouse-wide - far denser than any rock, which is a "
      "measurement artefact rather than a physical planet."),
    m("Total Note Count", P, "note_count", "sum", F_PHYSM,
      "Notes added across the selected planets. 2376 warehouse-wide over 3372 "
      "planets."),

    # ------------------------------------------------------------- derived --
    m("Mean Surface Gravity", P, "surface_gravity", "average", F_DERIVM,
      "Mean surface gravity relative to Earth's. 22.225 across the 509 planets with both a mass and a radius."),
    m("Maximum Surface Gravity", P, "surface_gravity", "maximum", F_DERIVM,
      "Strongest surface gravity among the selection. 1254.7 Earth gravities "
      "warehouse-wide; among super-Earths the strongest is 11.693, on "
      "Kepler-131 c."),
    m("Mean Mass Radius Ratio", P, "mass_radius_ratio", "average", F_DERIVM,
      "Mean mass-radius ratio in Earth units. 81.316 across 509 planets."),
    m("Maximum Mass Radius Ratio", P, "mass_radius_ratio", "maximum",
      F_DERIVM,
      "Largest mass-radius ratio among the selection."),
    m("Mean Escape Velocity", P, "escape_velocity_kms", "average", F_DERIVM,
      "Mean escape velocity in kilometres per second. 66.962 across 509 "
      "planets."),
    m("Maximum Escape Velocity", P, "escape_velocity_kms", "maximum",
      F_DERIVM,
      "Highest escape velocity among the selection, in kilometres per second."),
    m("Mean Orbital Velocity", P, "orbital_velocity_kms", "average", F_DERIVM,
      "Mean orbital velocity in kilometres per second. 82.094 across 1593 "
      "planets."),
    m("Maximum Orbital Velocity", P, "orbital_velocity_kms", "maximum",
      F_DERIVM,
      "Highest orbital velocity among the selection, in kilometres per second. "
      "531.29 warehouse-wide."),
    m("Mean Equilibrium Temperature", P, "equilibrium_temperature",
      "average", F_DERIVM,
      "Mean equilibrium temperature in Kelvin, both lengths in the formula converted to metres. 886.69 K across 1533 planets."),
    m("Maximum Equilibrium Temperature", P, "equilibrium_temperature",
      "maximum", F_DERIVM,
      "Highest equilibrium temperature among the selection, in Kelvin."),
    m("Mean Transit Depth", P, "transit_depth", "average", F_DERIVM,
      "Mean transit depth as a fraction, both radii in Earth radii. 0.0029442 "
      "across 2684 planets; times 100 for the percent reading."),
    m("Maximum Transit Depth", P, "transit_depth", "maximum", F_DERIVM,
      "Deepest transit among the selection, as a fraction. 1.1347 warehouse-wide."),
    m("Mean Planet Star Mass Ratio", P, "planet_star_mass_ratio", "average",
      F_DERIVM,
      "Mean planet-to-star mass ratio, both masses in kilograms. 0.0058646 "
      "across 1127 planets."),
    m("Maximum Planet Star Mass Ratio", P, "planet_star_mass_ratio",
      "maximum", F_DERIVM,
      "Largest planet-to-star mass ratio among the selection. 0.69997 "
      "warehouse-wide - a companion nearly as heavy as its host."),
    m("Mean Kepler Derived Stellar Mass", P, "kepler_derived_stellar_mass",
      "average", F_DERIVM,
      "Mean stellar mass derived from Kepler's third law. 1.0188 solar masses "
      "across 1831 planets - almost exactly one, which is the law checking "
      "out."),
    m("Mean Kepler Mass Difference", P, "kepler_mass_difference", "average",
      F_DERIVM,
      "Mean signed difference between the Kepler-derived stellar mass and the "
      "reported one. 0.013911 solar masses across 1534 planets, so the two "
      "agree on average to about one percent of a solar mass."),
    m("Mean Kepler Mass Absolute Difference", P,
      "kepler_mass_absolute_difference", "average", F_DERIVM,
      "Mean size of the disagreement between the Kepler-derived and recorded "
      "stellar masses, sign dropped. 0.05014 solar masses across 1534 "
      "planets."),
    m("Mean Goldilocks Value", P, "goldilocks_value", "average", F_DERIVM,
      "Mean Goldilocks value. 15.579 across 1533 planets - far above the 0.5 "
      "that marks a perfectly centred orbit, because most planets in this "
      "catalogue orbit well outside their star's habitable zone."),
    m("Mean Planet Distance Light Years (All Recorded)", P, "stellar_distance_ly",
      "average", F_DERIVM,
      "Mean distance to the selected planets' host stars, in light-years. "
      "2035.0 across the 2296 planets whose star records a distance, whatever "
      "its quality flags say. Mean Planet Distance Light Years is the same mean over only the flag-clean measurements; a "
      "question that wants solid, reliable distances may mean either screen - "
      "ask which."),
    m("Mean Planet Distance Light Years", P,
      "stellar_distance_ly_clean", "average", F_DERIVM,
      "Mean distance in light-years counting only measurements with no set "
      "quality flag: the distance is not an upper limit AND the magnitude is "
      "not blended - the only two quality flags ever set in this warehouse. "
      "2041.2 ly across the 2283 flag-clean planets; Mean Planet Distance Light Years (All Recorded) is the same mean over every recorded distance, 2035.0 across 2296."),

    # ------------------------------------------------------------- stellar --
    m("Mean Stellar Distance Parsecs", S, "stellar_distance_pc", "average",
      F_STARM,
      "Mean distance to the selected stars, in parsecs. 660.37 across the 1996 "
      "stars that record one."),
    m("Mean Stellar Distance Light Years", S, "stellar_distance_ly",
      "average", F_STARM,
      "Mean distance to the selected stars, in light-years. 2153.8 across 1996 "
      "stars - the parsec figure times 3.26156."),
    m("Mean Stellar Mass", S, "stellar_mass", "average", F_STARM,
      "Mean stellar mass in solar masses. 0.99986 across 2357 stars, so the "
      "typical host is almost exactly Sun-like."),
    m("Mean Stellar Radius", S, "stellar_radius", "average", F_STARM,
      "Mean stellar radius in solar radii. 1.6097 across 2228 stars."),
    m("Mean Stellar Temperature", S, "stellar_temperature", "average",
      F_STARM,
      "Mean effective temperature in Kelvin. 5545.5 across 2379 stars."),
    m("Maximum Stellar Temperature", S, "stellar_temperature", "maximum",
      F_STARM,
      "Hottest star among the selection. 57,000 K warehouse-wide."),
    m("Mean Optical Magnitude", S, "optical_magnitude", "average", F_STARM,
      "Mean apparent magnitude. 12.893 across 2400 stars. Remember the scale is "
      "inverted, so a higher mean means a fainter sample. Among the 49 stars "
      "whose every measured planet is rocky it is 11.870."),
    m("Minimum Optical Magnitude", S, "optical_magnitude", "minimum",
      F_STARM,
      "Brightest star among the selection - the MINIMUM magnitude, because the scale is inverted. 0.85 warehouse-wide."),
    m("Mean Stellar Luminosity", S, "stellar_luminosity", "average", F_STARM,
      "Mean luminosity relative to the Sun - the stars' average intrinsic "
      "brightness in solar units, the mean of Stellar Luminosity (Intrinsic "
      "Brightness, Solar Units); group it by System Composition or the rocky "
      "and gas-giant flags for a per-class mean."),
    m("Maximum Stellar Luminosity", S, "stellar_luminosity", "maximum",
      F_STARM,
      "Most luminous star among the selection. 630.99 solar luminosities "
      "warehouse-wide."),
    m("Mean Stellar Density", S, "stellar_density_kg_m3", "average", F_STARM,
      "Mean stellar density in kilograms per cubic metre. 16,571 across 2117 "
      "stars, pulled far above the Sun's 1410 by a few very compact objects."),
    m("Maximum Stellar Density", S, "stellar_density_kg_m3", "maximum",
      F_STARM,
      "Densest star among the selection, in kilograms per cubic metre. 30,839,868 warehouse-wide."),
    m("Minimum Stellar Density", S, "stellar_density_kg_m3", "minimum",
      F_STARM,
      "Least dense star among the selection, in kilograms per cubic metre. 0.013781 warehouse-wide."),
    m("Mean Stellar Density (Solar Units)", S, "stellar_density_solar",
      "average", F_STARM,
      "Mean stellar density with both inputs left in solar units. 2.806 across "
      "2117 stars."),
    m("Mean Gravitational Parameter", S, "gravitational_parameter",
      "average", F_STARM,
      "Mean standard gravitational parameter, in cubic metres per second "
      "squared. 1.3270e+20 across 2357 stars - essentially the Sun's value, "
      "because the mean stellar mass is one solar mass."),
    m("Mean Habitable Zone Inner", S, "habitable_zone_inner_au", "average",
      F_STARM,
      "Mean inner edge of the habitable zone, in AU. 1.2955 across 2207 "
      "stars."),
    m("Mean Habitable Zone Outer", S, "habitable_zone_outer_au", "average",
      F_STARM,
      "Mean outer edge of the habitable zone, in AU. 1.8664 across 2207 "
      "stars."),

    # -------------------------------------------------------- star systems --
    m("Mean Star Planet Count", S, "star_planet_count", "average", F_SYSM,
      "Mean number of planets per star. 1.344 across all 2509 stars."),
    m("Maximum Star Planet Count", S, "star_planet_count", "maximum", F_SYSM,
      "Largest number of planets in one system. 7 warehouse-wide."),
    m("Total System Planets", S, "star_planet_count", "sum", F_SYSM,
      "Planets added across the selected stars. 3372 warehouse-wide, which is "
      "the whole catalogue."),
    m("Mean Companion Count", S, "companion_count", "average", F_SYSM,
      "Mean declared companion count per star. 1.3436 across all 2509 stars - "
      "essentially identical to the planet-row count, which they disagree with "
      "on exactly one star."),
    m("Mean Shortest Orbital Period", S, "shortest_orbital_period",
      "average", F_SYSM,
      "Mean of each system's shortest orbital period, in days. 3476.5 across "
      "2444 stars."),
    m("Mean Max Adjacent Period Ratio", S, "max_adjacent_period_ratio",
      "average", F_SYSM,
      "Mean of each system's largest adjacent period ratio. 29.783 across the "
      "568 stars that have an adjacent pair."),
    m("Mean Adjacent Period Ratio Per System", S,
      "mean_adjacent_period_ratio", "average", F_SYSM,
      "Mean of each system's ARITHMETIC-mean adjacent period ratio. 28.940 "
      "across 568 stars. The geometric-mean twin is Mean Geometric Adjacent "
      "Period Ratio Per System."),
    m("Mean Geometric Adjacent Period Ratio Per System", S,
      "geometric_mean_adjacent_period_ratio", "average", F_SYSM,
      "Mean of each system's GEOMETRIC-mean adjacent period ratio. 28.598 "
      "across 568 stars; 1.9896 across the 210 systems whose ratios are all "
      "under 3 with an innermost planet under 10 days."),
    m("Rocky Only Star Count", S, "rocky_only_indicator", "sum", F_SYSM,
      "How many of the selected stars have one or more rocky planets and no "
      "gas giant - System Composition 'Rocky Only'. 27 of 2509 "
      "warehouse-wide."),
    m("Gas Giants Only Star Count", S, "gas_giants_only_indicator", "sum",
      F_SYSM,
      "How many of the selected stars have one or more gas giants and no rocky "
      "planet - System Composition 'Gas Giants Only'. 782 of 2509 "
      "warehouse-wide."),
    m("Total Adjacent Pairs", S, "adjacent_pair_count", "sum", F_SYSM,
      "Adjacent planet pairs added across the selected stars. 861 "
      "warehouse-wide."),
    m("Total Star Gas Giants", S, "star_gas_giant_count", "sum", F_SYSM,
      "Gas giants added across the selected stars. 929 warehouse-wide."),
    m("Total Star Rocky Planets", S, "star_rocky_planet_count", "sum",
      F_SYSM,
      "Rocky planets added across the selected stars. 74 warehouse-wide."),
    m("Total Star Planets With Density", S, "star_planets_with_density",
      "sum", F_SYSM,
      "Planets with a recorded density, added across the selected stars. 388 "
      "warehouse-wide."),
    m("Total Star Short Period Planets", S, "star_short_period_count", "sum",
      F_SYSM,
      "Short-period planets added across the selected stars. 1445 "
      "warehouse-wide."),
    m("Total Star Transit Discoveries", S, "star_transit_discovery_count",
      "sum", F_SYSM,
      "Transit discoveries added across the selected stars. 2664 "
      "warehouse-wide."),
    m("Total Star Radial Velocity Discoveries", S,
      "star_radial_velocity_count", "sum", F_SYSM,
      "Radial-velocity discoveries added across the selected stars. 591 "
      "warehouse-wide."),
    m("Multi Planetary Star Count", S, "multi_planetary_indicator", "sum",
      F_SYSM,
      "How many of the selected stars declare more than one companion. 569 of "
      "2509 warehouse-wide. The reading that counts actual planet rows gives "
      "570."),
    m("Kepler Star Count", S, "kepler_observation_indicator", "sum", F_SYSM,
      "How many of the selected stars have a planet observed by the Kepler "
      "mission. 1644 of 2509 warehouse-wide."),
    m("K2 Star Count", S, "k2_observation_indicator", "sum", F_SYSM,
      "How many of the selected stars have a planet observed by K2. 94 of 2509 "
      "warehouse-wide."),
    m("TTV Star Count", S, "ttv_observation_indicator", "sum", F_SYSM,
      "How many of the selected stars carry a planet with a TTV "
      "observation record, over the 2509 host stars."),

    # ------------------------------------------------- classification counts --
    m("Gas Giant Count", P, "gas_giant_indicator", "sum", F_FLAGM,
      "How many of the selected planets are gas giants - a mass above 0.1 "
      "Jupiter masses. 929 of the 1174 planets with a mass warehouse-wide."),
    m("Rocky Planet Count", P, "rocky_indicator", "sum", F_FLAGM,
      "How many of the selected planets are rocky - a density above 3. 74 of "
      "the 388 with a density warehouse-wide."),
    m("Short Period Planet Count", P, "short_period_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets orbit in under 10 days. 1445 of the "
      "3305 with a period warehouse-wide."),
    m("Hot Jupiter Count", P, "hot_jupiter_indicator", "sum", F_FLAGM,
      "How many of the selected planets are hot Jupiters - both a gas giant and short-period. None of them is also retrograde."),
    m("Super Earth Count", P, "super_earth_indicator", "sum", F_FLAGM,
      "How many of the selected planets are super-Earths - rocky with a mass "
      "between 1 and 10 Earth masses. 31 warehouse-wide, of which 29 were found "
      "by transit."),
    m("Habitable Zone Planet Count", P, "habitable_zone_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets orbit inside their star's habitable "
      "zone. 28 warehouse-wide."),
    m("Potentially Habitable Count", P, "potentially_habitable_indicator",
      "sum", F_FLAGM,
      "How many of the selected planets are both rocky AND in the habitable "
      "zone. ZERO warehouse-wide - the two conditions never co-occur, even "
      "though 74 planets are rocky and 28 sit in a habitable zone. Published so "
      "the emptiness is visible rather than mistaken for a filter error."),
    m("High Eccentricity Count", P, "high_eccentricity_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets have an eccentricity above 0.25. 249 of "
      "the 974 with an eccentricity warehouse-wide."),
    m("Retrograde Orbit Count", P, "retrograde_indicator", "sum", F_FLAGM,
      "How many of the selected planets orbit retrograde - an inclination above "
      "90 degrees. 8 of the 502 with an inclination warehouse-wide."),
    m("Inflated Gas Giant Count", P, "inflated_gas_giant_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets are inflated gas giants - a giant mass with a low density."),
    m("Well Characterized Count", P, "well_characterized_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets have high-precision mass, radius AND "
      "period. 48 warehouse-wide."),
    m("Transit Discovery Count", P, "transit_discovery_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets were discovered by transit. 2664 of "
      "3372 warehouse-wide."),
    m("Radial Velocity Discovery Count", P, "radial_velocity_indicator",
      "sum", F_FLAGM,
      "How many of the selected planets were discovered by radial velocity. 591 "
      "of 3372 warehouse-wide."),
    m("Kepler Observed Planet Count", P, "kepler_observation_indicator",
      "sum", F_FLAGM,
      "How many of the selected planets were observed by the Kepler mission. "
      "2329 of 3372 warehouse-wide."),
    m("K2 Observed Planet Count", P, "k2_observation_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets were observed by K2. 129 of 3372 "
      "warehouse-wide."),
    m("TTV Observed Planet Count", P, "ttv_observation_indicator", "sum",
      F_FLAGM,
      "How many of the selected planets carry a TTV observation record. "
      "225 of 3372 warehouse-wide."),

    # ---------------------------------------------------- measurement quality --
    m("Mean Period Relative Uncertainty", P, "period_relative_uncertainty",
      "average", F_QUALM,
      "Mean relative uncertainty in the orbital period, as a percentage. 0.755 "
      "across 3180 planets - the best-known parameter in the catalogue."),
    m("Mean Mass Relative Uncertainty", P, "mass_relative_uncertainty",
      "average", F_QUALM,
      "Mean relative uncertainty in the planet mass, as a percentage. 30.343 "
      "across 987 planets."),
    m("Mean Radius Relative Uncertainty", P, "radius_relative_uncertainty",
      "average", F_QUALM,
      "Mean relative uncertainty in the planet radius, as a percentage. 17.864 "
      "across 2656 planets."),
    m("Mean Density Relative Uncertainty", P, "density_relative_uncertainty",
      "average", F_QUALM,
      "Mean relative uncertainty in the density, as a percentage. 44.315 across "
      "378 planets."),
    m("Mean Eccentricity Relative Uncertainty", P,
      "eccentricity_relative_uncertainty", "average", F_QUALM,
      "Mean relative uncertainty in the eccentricity, as a percentage. 74.166 "
      "across 690 planets - the least precisely known parameter."),
    m("Radius Upper Limit Count", P, "radius_upper_limit_indicator", "sum",
      F_QUALM,
      "How many of the selected planets have a radius that is an upper limit "
      "rather than a measurement. Exactly 1 warehouse-wide, out of the 2694 "
      "with a radius."),
    m("Temperature Blend Count", P, "temperature_blend_indicator", "sum",
      F_QUALM,
      "How many of the selected planets have a host-star temperature flagged as "
      "contaminated by companion light. ZERO warehouse-wide - the flag is 0 on "
      "all 3219 planets that carry it. So no planet has a bad temperature "
      "reading in this warehouse, whichever survey found it."),
    m("Distance Upper Limit Count", P, "distance_upper_limit_indicator",
      "sum", F_QUALM,
      "How many of the selected planets have a host-star distance that is an "
      "upper limit. ZERO warehouse-wide."),
    m("Mass Upper Limit Count", P, "mass_upper_limit_indicator", "sum",
      F_QUALM,
      "How many of the selected planets have a mass that is an upper limit "
      "rather than a measurement. 64 of the 1174 with a mass warehouse-wide."),
    m("Magnitude Blend Count", P, "magnitude_blend_indicator", "sum",
      F_QUALM,
      "How many of the selected planets orbit a star whose magnitude is a blended measurement - the only blended measurements in the warehouse."),
    m("Minimum Mass Count", P, "planet_mass_jupiter", "count non-null",
      F_QUALM,
      "How many of the selected planets record a mass at all. 1174 "
      "warehouse-wide; the Mass Source attribute says which of them are minimum "
      "masses - 554 read 'Msini' and 9 read 'Msin(i)/sin(i)'.",
      is_hidden=True),
]

# --------------------------------------------------------------------------- #
# calculated metrics
# --------------------------------------------------------------------------- #

def c(name, folder, desc, expr):
    return {"unique_name": name, "label": name, "folder": folder,
            "description": desc, "expression": expr}


def _ratio(num, den):
    return (f"CASE WHEN ISEMPTY([Measures].[{den}]) OR [Measures].[{den}] = 0 "
            f"THEN NULL ELSE [Measures].[{num}] / [Measures].[{den}] END")


def _share_of_all(num, den):
    return (f"CASE WHEN ISEMPTY(AllMember([Measures].[{den}])) OR "
            f"AllMember([Measures].[{den}]) = 0 THEN NULL ELSE "
            f"[Measures].[{num}] / AllMember([Measures].[{den}]) END")


CALCULATIONS = [
    c("Planet Share Of All Planets", F_CALC_RATE,
      "Share of all 3372 planets falling in the current selection - what "
      "percentage of the catalogue. Returned as a FRACTION from 0 to 1, not a "
      "percentage. The denominator strips every filter and grouping, so this "
      "works beside any grouping including a category the user defined in "
      "conversation.",
      _share_of_all("Planet Count", "Planet Count")),
    c("Star Share Of All Stars", F_CALC_RATE,
      "Share of all 2509 host stars falling in the current selection. A "
      "FRACTION from 0 to 1.",
      _share_of_all("Star Count", "Star Count")),
    c("Gas Giant Rate", F_CALC_RATE,
      "Among planets carrying a mass, the share that are gas giants. A "
      "FRACTION from 0 to 1; warehouse-wide 929/1174, or 0.7913. The "
      "denominator is the mass coverage rather than all 3372 planets, because a "
      "planet with no mass is unknown rather than small.",
      _ratio("Gas Giant Count", "Planets With A Mass")),
    c("Rocky Planet Rate", F_CALC_RATE,
      "Among planets carrying a density, the share that are rocky. A "
      "FRACTION from 0 to 1; warehouse-wide 74/388, or 0.19072.",
      _ratio("Rocky Planet Count", "Planets With A Density")),
    c("Short Period Rate", F_CALC_RATE,
      "Among planets carrying a period, the share orbiting in under 10 "
      "days. A FRACTION from 0 to 1; warehouse-wide 1445/3305, or 0.43722.",
      _ratio("Short Period Planet Count", "Planets With A Period")),
    c("High Eccentricity Rate", F_CALC_RATE,
      "Among planets carrying an eccentricity, the share above "
      "0.25. A FRACTION from 0 to 1; warehouse-wide 249/974, or 0.25565.",
      _ratio("High Eccentricity Count", "Planets With An Eccentricity")),
    c("Retrograde Rate", F_CALC_RATE,
      "Among planets carrying an inclination, the share orbiting "
      "retrograde. A FRACTION from 0 to 1; warehouse-wide 8/502, or 0.015936.",
      _ratio("Retrograde Orbit Count", "Planets With An Inclination")),
    c("Inflated Gas Giant Rate", F_CALC_RATE,
      "Among planets carrying a density, the share that are inflated gas "
      "giants. A FRACTION from 0 to 1.",
      _ratio("Inflated Gas Giant Count", "Planets With A Density")),
    c("Super Earth Rate", F_CALC_RATE,
      "Among planets carrying a density, the share that are "
      "super-Earths. A FRACTION from 0 to 1; warehouse-wide 31/388, or "
      "0.079897.",
      _ratio("Super Earth Count", "Planets With A Density")),
    c("Habitable Zone Rate", F_CALC_RATE,
      "The proportion of the planets whose habitable zone can be evaluated that "
      "sit inside it. A FRACTION from 0 to 1; warehouse-wide 28/1533, or "
      "0.018265.",
      _ratio("Habitable Zone Planet Count",
             "Planets With An Equilibrium Temperature")),
    c("Well Characterized Rate", F_CALC_RATE,
      "The proportion of the selected planets with high-precision mass, radius "
      "and period. A FRACTION from 0 to 1; warehouse-wide 48/3372, or 0.014235.",
      _ratio("Well Characterized Count", "Planet Count")),
    c("Transit Discovery Rate", F_CALC_RATE,
      "The proportion of the selected planets discovered by transit. A FRACTION "
      "from 0 to 1; warehouse-wide 2664/3372, or 0.79004.",
      _ratio("Transit Discovery Count", "Planet Count")),
    c("Radial Velocity Discovery Rate", F_CALC_RATE,
      "The proportion of the selected planets discovered by radial velocity. A "
      "FRACTION from 0 to 1; warehouse-wide 591/3372, or 0.17527.",
      _ratio("Radial Velocity Discovery Count", "Planet Count")),
    c("Kepler Observation Rate", F_CALC_RATE,
      "The proportion of the selected planets observed by the Kepler mission. A "
      "FRACTION from 0 to 1; warehouse-wide 2329/3372, or 0.69069.",
      _ratio("Kepler Observed Planet Count", "Planet Count")),
    c("Mass Coverage Rate", F_CALC_RATE,
      "The proportion of the selected planets that record a mass. A FRACTION "
      "from 0 to 1; warehouse-wide 1174/3372, or 0.34816. Report it beside any "
      "mass-based average, because that average describes a third of the "
      "catalogue.",
      _ratio("Planets With A Mass", "Planet Count")),
    c("Density Coverage Rate", F_CALC_RATE,
      "The proportion of the selected planets that record a density. A FRACTION "
      "from 0 to 1; warehouse-wide 388/3372, or 0.11507 - the tightest coverage "
      "in the model, and the ceiling on every composition question.",
      _ratio("Planets With A Density", "Planet Count")),
    c("Multi Planetary Star Rate", F_CALC_RATE,
      "The proportion of the selected stars that declare more than one "
      "companion. A FRACTION from 0 to 1; warehouse-wide 569/2509, or 0.22678.",
      _ratio("Multi Planetary Star Count", "Star Count")),
    c("Observed Planet Rate", F_CALC_RATE,
      "The proportion of the selected planets observed by at least one of the "
      "three surveys. A FRACTION from 0 to 1; warehouse-wide 2460/3372, or "
      "0.72953. It uses the distinct planet count on the observation bridge, so "
      "a planet observed twice still counts once.",
      _ratio("Distinct Observed Planet Count", "Planet Count")),

    # ------------------------------------------------- group formulas --
    c("Group Planets Per Star", F_CALC_GROUP,
      "Planets divided by host stars, for the current selection - planets per "
      "system. Warehouse-wide 3372/2509, or 1.344.",
      _ratio("Planet Count", "Distinct Star Count On Planets")),
    c("Group Mass Ratio (Pooled)", F_CALC_GROUP,
      "The planet-to-star mass ratio recomputed for the WHOLE selected group "
      "from aggregated masses rather than averaged per planet: the mean planet "
      "mass in kilograms (Jupiter masses times 1.898E27) over the mean stellar "
      "mass in kilograms (solar masses times 1.98847E30). Warehouse-wide "
      "2.6284 x 1.898E27 / (0.99986 x 1.98847E30), or 0.0025091, against a "
      "per-planet mean of 0.0058646 - the gap is large because the per-planet "
      "mean is pulled up by low-mass hosts. Quote the pooled figure for a "
      "population and the mean for a typical planet.",
      "CASE WHEN ISEMPTY([Measures].[Mean Stellar Mass]) OR "
      "[Measures].[Mean Stellar Mass] = 0 THEN NULL ELSE "
      "[Measures].[Mean Planet Mass Jupiter] * 1898.0 / 1988470.0 / "
      "[Measures].[Mean Stellar Mass] END"),
    c("Group Surface Gravity (Pooled)", F_CALC_GROUP,
      "Surface gravity recomputed for the whole selected group from the mean "
      "mass and mean radius in Earth units, rather than averaged per planet. The two differ because the ratio of means is not the "
      "mean of ratios.",
      "CASE WHEN ISEMPTY([Measures].[Mean Planet Radius Earth]) OR "
      "[Measures].[Mean Planet Radius Earth] = 0 THEN NULL ELSE "
      "[Measures].[Mean Planet Mass Earth] / "
      "([Measures].[Mean Planet Radius Earth] * "
      "[Measures].[Mean Planet Radius Earth]) END"),
    c("Group Mass Radius Ratio (Pooled)", F_CALC_GROUP,
      "The mass-radius relationship recomputed for the whole selected group: "
      "the mean mass in Earth units over the mean radius in Earth units. "
      "Warehouse-wide 835.37 / 3.8333, or 217.93, against a per-planet mean of "
      "81.316.",
      _ratio("Mean Planet Mass Earth", "Mean Planet Radius Earth")),
    c("Group Stellar Luminosity (Pooled)", F_CALC_GROUP,
      "Stellar luminosity recomputed for the whole selected group from the mean "
      "radius and mean temperature, rather than averaged per star: the mean "
      "radius squared times the mean temperature over 5778 to the fourth power. "
      "Warehouse-wide 1.6097 squared times (5545.5/5778) to the fourth, or "
      "2.2477, against a per-star mean of 5.6405 - so averaging the stars "
      "first more than doubles the answer, because luminosity is a steep "
      "function of both inputs.",
      # Written as repeated multiplication, not POWER(x, 4). The engine rejected
      # the POWER form at publish time - "not valid as either MDX or DAX" - and
      # took the whole catalog down with it, which sml-cli validate does not
      # catch. Plain arithmetic parses on both sides of that fence. The NULL
      # guard matches the sibling group formulas above: an empty temperature
      # would otherwise make the fourth power read as zero.
      "CASE WHEN ISEMPTY([Measures].[Mean Stellar Radius]) OR "
      "ISEMPTY([Measures].[Mean Stellar Temperature]) THEN NULL ELSE "
      "[Measures].[Mean Stellar Radius] * [Measures].[Mean Stellar Radius] * "
      "([Measures].[Mean Stellar Temperature] / 5778) * "
      "([Measures].[Mean Stellar Temperature] / 5778) * "
      "([Measures].[Mean Stellar Temperature] / 5778) * "
      "([Measures].[Mean Stellar Temperature] / 5778) END"),
    c("Group Rocky Fraction Per System", F_CALC_GROUP,
      "Rocky planets divided by planets with a density, for the selected stars - "
      "the rocky fraction of a system's measured planets. Warehouse-wide 74/388, "
      "or 0.19072. At a single star it is that star's own fraction, which is 1 "
      "for the 49 stars whose every measured planet is rocky.",
      _ratio("Total Star Rocky Planets", "Total Star Planets With Density")),
    c("Group Observations Per Planet", F_CALC_GROUP,
      "Observation records divided by distinct planets observed. Warehouse-wide "
      "2683/2460, or 1.0906 - so most observed planets appear once and a few "
      "appear twice. No planet appears three times.",
      _ratio("Observation Count", "Distinct Observed Planet Count")),
]
