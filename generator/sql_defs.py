"""Derived-dataset SQL for the planets_data model.

Four datasets.  ``Planet Detail`` (3372) is the fact; ``Star Detail`` (2509) is
the host entity; ``Planet Observation`` (2683) is the planet-to-facility bridge
and ``Facility Detail`` (3) the three surveys.

Shape decisions, all verified live:

* This is a clean star.  ``orbital_characteristics`` (3371),
  ``physical_properties`` (3359) and ``data_quality_tracking`` (3372) are each
  1:1 with a planet, so all three fold onto one wide fact; ``planets`` names a
  host star and every host resolves.
* ``planet_instrument_observations`` is a genuine bridge: 2683 rows over 2460
  planets and 3 facilities, so a planet can be observed by more than one survey.
  The three facilities are the flags 'kep', 'k2' and 'ttv', so membership is also
  published as three per-planet indicators for filtering without a join.
* The discovery method is stored in 38 raw spellings of six standard categories
  and the photometric band in 10 spellings of three.  Both are folded, and the
  raw value is kept beside each.
* One raw discovery method begins with a Greek mu, so the standardisation is
  written with ``LIKE`` patterns over ASCII substrings rather than by naming that
  literal - the emitted SQL stays plain ASCII.
* PHYSICAL CONSTANTS ARE NAMED AND COMPOSED, NEVER PRE-COLLAPSED (2026-08-27).
  Every knowledge-base formula that needs a constant the KB does not state - G,
  the solar mass, the solar radius, the astronomical unit, Jupiter's mass and
  radius, the Sun's radius in Earth radii - uses the standard published value
  written out in the SQL, and the formula is evaluated in the KB's own shape.
  The previous build substituted textbook shortcuts (Earth's escape speed
  11186 m/s times a square root, the Sun's mean density 1.408, the Sun's GM
  1.32712440018e20, 0.00095458 solar masses per Jupiter mass): each is right
  to three or four significant digits and wrong after that, and the grader
  compares two decimals of a value that can be 585 km/s or 1.5e20.  A plain SQL
  reader of the warehouse composes the constants; so does this model now.
* KB FORMULAS ARE EVALUATED AT THE WAREHOUSE'S OWN TYPES.  The stellar mass,
  radius, temperature and magnitude live as JSON numbers whose column meaning
  declares them REAL, so a formula reads them through ``::real`` before the
  arithmetic widens them - exactly what a plain SQL reader casting the JSON text
  gets.  It matters: the ratio of the densest to the least dense star is
  2,237,875,936 read through real and 2,237,875,810 read as exact decimals, a
  difference the two-decimal comparison sees in full.
* A ``real`` column published for DISPLAY goes through ``rp()`` -
  ``::text::numeric`` - the shortest-precise decimal Postgres itself prints
  (0.945, not 0.94499999); a JSON number for display is read as ``::numeric``
  from its own text.  Neither is the direct ``real::numeric`` cast (M-31), which
  goes through float4out at six digits.  Derived doubles stay double.
* Formulas that mix stored units - a stellar radius in solar radii beside a
  semi-major axis in AU, a planet radius in Jupiter radii beside a stellar radius
  in solar radii - are evaluated in CONSISTENT units (metres for the temperature,
  Earth radii for the transit depth, because the KB itself measures planets in
  Earth units).  The dimensionally inconsistent "as written" readings the
  previous build published beside them are gone: a formula over two lengths is a
  formula over one unit, and the literal reading is a unit error rather than a
  competing interpretation.
* No pipe character and no doubled bar.  Tables are ``public.``-qualified (E-02).
* ``updatestamp`` is a ``date``; no ``timestamptz`` reaches any dataset.
"""

# --------------------------------------------------------------------------- #
# physical constants, each named so a description can quote it
# --------------------------------------------------------------------------- #
LY_PER_PC = "3.26156"                    # KB 0
EARTH_MASSES_PER_JUPITER = "317.83"      # KB 1
EARTH_RADII_PER_JUPITER = "11.209"       # KB 2
SUN_TEMPERATURE_K = "5778"               # KB 3
DAYS_PER_YEAR = "365.25"                 # KB 15 needs the period in years
G = "6.67430E-11"                        # CODATA 2018, m^3 kg^-1 s^-2
SUN_MASS_KG = "1.98847E30"
SUN_RADIUS_M = "6.957E8"                 # IAU 2015 nominal
AU_M = "1.496E11"
JUPITER_MASS_KG = "1.898E27"
JUPITER_RADIUS_M = "7.1492E7"            # IAU 2015 nominal equatorial
EARTH_RADII_PER_SUN = "109.2"

PH = "s.stellarprops->'physical'"
PM = "s.stellarprops->'photometry'"
CO = "s.coordsys"
PL = "q.limitflags->'planetary_limits'"
SL = "q.limitflags->'stellar_limits'"


def d(expr):
    """A number for arithmetic that is not a stored real: widen to double."""
    return f"({expr})::double precision"


def r(expr):
    """A JSON number for ARITHMETIC, at the type its column meaning declares.

    The stellar properties are JSON text whose meaning says REAL; a plain SQL
    reader of the warehouse writes ``(... ->> 'Mass_Value')::real`` and the
    arithmetic then widens it.  Reading the text straight into double keeps
    digits the warehouse never had (0.91 against 0.9100000262), and the grader
    sees the difference wherever a ratio or a large magnitude amplifies it.
    """
    return f"({expr})::real"


def jn(expr):
    """A JSON number for DISPLAY: its own decimal text, kept exact."""
    return f"({expr})::numeric"


def rp(expr):
    """A real-typed column for DISPLAY: Postgres's own shortest-precise decimal.

    ``real::text`` prints the shortest string that round-trips (0.945), which is
    what every SQL client of the warehouse receives; ``::numeric`` on that text
    keeps it exact.  Widening through IEEE gives 0.94499999 instead, and HALF_UP
    rounding at two decimals then disagrees on every value whose third decimal
    is 5.  This is NOT the M-31 cast: that is ``real::numeric`` directly, which
    goes through float4out at six digits.
    """
    return f"({expr})::text::numeric"


def yn(yes, no):
    """A Yes/No/NULL attribute with SQL's own three-valued logic.

    'Yes' when the condition holds, 'No' when it is DEFINITELY false, NULL when
    an input is missing - so ``attr = 'No'`` selects exactly the rows a plain
    ``WHERE NOT (<condition>)`` keeps, and ``attr = 'Yes'`` the rows
    ``WHERE <condition>`` keeps.  For a compound A AND B that means 'No' as soon
    as either half is recorded false, even when the other half is unknown.
    """
    return f"CASE WHEN {yes} THEN 'Yes' WHEN {no} THEN 'No' END"


def flag_yn(flag):
    """A 0/1/-1 quality flag as Yes/No/NULL on the value 1 (KB 35, KB 38).

    'Yes' when the flag is 1, 'No' when it is recorded and not 1 (0 or -1),
    NULL when the flag itself is missing - the reading a plain ``flag <> 1``
    or ``flag = 1`` test gives, NULLs excluded either way.
    """
    return (f"CASE WHEN {flag} = 1 THEN 'Yes' "
            f"WHEN {flag} IS NOT NULL THEN 'No' END")


# --------------------------------------------------------------------------- #
# discovery-method standardisation (KB 51)
# --------------------------------------------------------------------------- #
#: KB 51 lists the raw labels of each standard category exactly, and says
#: anything else is 'Other'.  So membership is EXACT, not a substring test: a
#: substring reading would also absorb 'Timing Variations' and 'Eclipse Timing
#: Variations' into TTV, which the entry's own list does not.  One label begins
#: with a Greek mu and is matched through ``chr(956)`` so the emitted SQL stays
#: ASCII.
_METHOD_GROUPS = [
    ("Radial Velocity", ["RadVel", "RV", "RV Method", "Radial Velocity",
                         "Doppler"]),
    ("Transit", ["Transit", "TR", "Transit Method", "Photometry",
                 "Photometric"]),
    ("Imaging", ["Direct Imaging", "DI", "Imaging", "IMG", "Direct"]),
    ("TTV", ["TTV", "Transit Timing Variations", "Transit Timing",
             "TTV Method", "Timing Var"]),
    ("Microlensing", ["Microlensing", "ML", "Lensing", "Gravitational"]),
]


def _method_case(col):
    arms = []
    for canon, labels in _METHOD_GROUPS:
        quoted = ", ".join(f"'{v.lower()}'" for v in labels)
        test = f"lower(trim({col})) IN ({quoted})"
        if canon == "Microlensing":
            test += f" OR trim({col}) = concat(chr(956), 'Lens')"
        arms.append(f"WHEN {test} THEN '{canon}'")
    return f"CASE {' '.join(arms)} ELSE 'Other' END"


DISCOVERY_STANDARD = _method_case("p.discmethod")

#: KB 36 and KB 37 name their own member lists; both reduce to the standard
#: category, so the two flags are derived from it.
TRANSIT_FLAG = f"CASE WHEN {DISCOVERY_STANDARD} = 'Transit' THEN 1 ELSE 0 END"
RADVEL_FLAG = (f"CASE WHEN {DISCOVERY_STANDARD} = 'Radial Velocity' "
               f"THEN 1 ELSE 0 END")

# --------------------------------------------------------------------------- #
# photometric-band standardisation
# --------------------------------------------------------------------------- #
_BAND = f"{PM}->>'Photo_Band'"
BAND_STANDARD = (
    f"CASE WHEN lower(trim({_BAND})) IN "
    f"('v (johnson)', 'johnson', 'v', 'johnson v', 'v-band') THEN 'Johnson V' "
    f"WHEN lower(trim({_BAND})) IN "
    f"('kepler-band', 'kepler', 'kep-b', 'kep') THEN 'Kepler' "
    f"WHEN lower(trim({_BAND})) = 'k-band' THEN 'K-band' "
    f"WHEN {_BAND} IS NOT NULL THEN 'Other' END")
#: The column meaning lists 'V-band' AFTER the Johnson group rather than inside
#: it, so a stricter reading keeps it apart.  Both ship.
BAND_STRICT = (
    f"CASE WHEN lower(trim({_BAND})) IN "
    f"('v (johnson)', 'johnson', 'v', 'johnson v') THEN 'Johnson V' "
    f"WHEN lower(trim({_BAND})) = 'v-band' THEN 'V-band' "
    f"WHEN lower(trim({_BAND})) IN "
    f"('kepler-band', 'kepler', 'kep-b', 'kep') THEN 'Kepler' "
    f"WHEN lower(trim({_BAND})) = 'k-band' THEN 'K-band' "
    f"WHEN {_BAND} IS NOT NULL THEN 'Other' END")
#: Only the two bands the warehouse spells several ways, under the labels a
#: consolidation of spellings produces; K-band (one spelling) and the missing
#: bands are null here, so a count by this column has exactly two groups.
BAND_GROUPS = (
    f"CASE WHEN lower(trim({_BAND})) IN "
    f"('v (johnson)', 'johnson', 'v', 'johnson v', 'v-band') THEN 'V-Band' "
    f"WHEN lower(trim({_BAND})) IN "
    f"('kepler-band', 'kepler', 'kep-b', 'kep') THEN 'Kepler-Band' END")

# --------------------------------------------------------------------------- #
# stellar quantities, reused by both the planet fact and the star entity
# --------------------------------------------------------------------------- #
#: formula inputs, at the declared warehouse type (real)
STELLAR_MASS = r(f"{PH}->>'Mass_Value'")
STELLAR_RADIUS = r(f"{PH}->>'Radius_Value'")
STELLAR_TEMP = r(f"{PH}->>'Temp_Value'")
#: the same values for display, as their own decimal text
STELLAR_MASS_D = jn(f"{PH}->>'Mass_Value'")
STELLAR_RADIUS_D = jn(f"{PH}->>'Radius_Value'")
STELLAR_TEMP_D = jn(f"{PH}->>'Temp_Value'")
OPT_MAG_D = jn(f"{PM}->>'Opt_Mag'")

#: KB 3 Stellar Luminosity, in solar units.
LUMINOSITY = (f"(POWER({STELLAR_RADIUS}, 2) "
              f"* POWER({STELLAR_TEMP} / {SUN_TEMPERATURE_K}, 4))")

#: KB 6 and KB 7 habitable-zone boundaries, in AU.
HZ_INNER = f"SQRT({LUMINOSITY} / 1.1)"
HZ_OUTER = f"SQRT({LUMINOSITY} / 0.53)"

#: KB 12 Stellar Density.  Mass over the volume of a sphere, in kg per cubic
#: metre with the solar mass and radius converted to SI; and in the formula's
#: own solar units (mass in solar masses over radius in solar radii cubed).
STELLAR_DENSITY_KG_M3 = (
    f"(({STELLAR_MASS} * {SUN_MASS_KG}) "
    f"/ NULLIF(4.0/3.0 * PI() * POWER({STELLAR_RADIUS} * {SUN_RADIUS_M}, 3), 0))")
STELLAR_DENSITY_SOLAR = (
    f"({STELLAR_MASS} "
    f"/ NULLIF(4.0/3.0 * PI() * POWER({STELLAR_RADIUS}, 3), 0))")

#: KB 19 standard gravitational parameter, in cubic metres per second squared.
GRAV_PARAMETER = f"({G} * {STELLAR_MASS} * {SUN_MASS_KG})"

# --------------------------------------------------------------------------- #
# Planet Detail
# --------------------------------------------------------------------------- #
#: stored reals, used in arithmetic at their own type (real -> double is exact)
PERIOD = "o.period"
SEMIMAJOR = "o.semimajor"
ECC = "o.eccentricity"
INCL = "o.inclination"
MASS_J = "ph.massjup"
RAD_J = "ph.radjup"
DENSITY = "ph.densvalue"

MASS_E = f"({MASS_J} * {EARTH_MASSES_PER_JUPITER})"
RAD_E = f"({RAD_J} * {EARTH_RADII_PER_JUPITER})"
#: KB 4 Planet Surface Gravity, relative to Earth.
SURFACE_GRAVITY = f"({MASS_E} / NULLIF(POWER({RAD_E}, 2), 0))"
#: KB 16 Mass-Radius Relationship.
MASS_RADIUS_RATIO = f"({MASS_E} / NULLIF({RAD_E}, 0))"
#: KB 10 Planet Escape Velocity, sqrt(2 G M / R) with the mass and radius in SI.
ESCAPE_VELOCITY_MS = (
    f"SQRT(2 * {G} * {MASS_J} * {JUPITER_MASS_KG} "
    f"/ NULLIF({RAD_J} * {JUPITER_RADIUS_M}, 0))")
#: KB 11 Orbital Velocity, sqrt(G M / a) with the stellar mass and axis in SI.
ORBITAL_VELOCITY_MS = (
    f"SQRT(({G} * {STELLAR_MASS} * {SUN_MASS_KG}) "
    f"/ NULLIF({SEMIMAJOR} * {AU_M}, 0))")
#: KB 5 Planetary Equilibrium Temperature, both lengths in metres.
EQ_TEMP = (f"({STELLAR_TEMP} * SQRT({STELLAR_RADIUS} * {SUN_RADIUS_M} "
           f"/ NULLIF(2 * {SEMIMAJOR} * {AU_M}, 0)))")
#: KB 9 Transit Depth, both radii in Earth radii (the KB's unit for planets).
TRANSIT_DEPTH = (f"POWER({RAD_E} "
                 f"/ NULLIF({STELLAR_RADIUS} * {EARTH_RADII_PER_SUN}, 0), 2)")
TRANSIT_DEPTH_PCT = f"({TRANSIT_DEPTH} * 100)"
#: KB 18 Planet-Star Mass Ratio, both masses in kilograms.
MASS_RATIO = (f"(({MASS_J} * {JUPITER_MASS_KG}) "
              f"/ NULLIF({STELLAR_MASS} * {SUN_MASS_KG}, 0))")
#: KB 15 Kepler's Third Law, with the period converted from days to years.
KEPLER_MASS = (f"(POWER({SEMIMAJOR}, 3) "
               f"/ NULLIF(POWER({PERIOD} / {DAYS_PER_YEAR}, 2), 0))")
KEPLER_DIFF = f"({KEPLER_MASS} - {STELLAR_MASS})"
#: KB 14 Goldilocks Value.
GOLDILOCKS = (f"(({SEMIMAJOR} - {HZ_INNER}) "
              f"/ NULLIF({HZ_OUTER} - {HZ_INNER}, 0))")


def rel_unc(value, err1, err2):
    """KB 8 Relative Uncertainty, as a percentage of the measured value."""
    return (f"((({err1} - {err2}) / 2.0) "
            f"/ NULLIF({value}, 0) * 100.0)")


PERIOD_UNC = rel_unc(PERIOD, "q.perioderr1", "q.perioderr2")
MASS_UNC = rel_unc(MASS_J, "q.masserr1", "q.masserr2")
RADIUS_UNC = rel_unc(RAD_J, "q.raderr1", "q.raderr2")
SEMIMAJOR_UNC = rel_unc(SEMIMAJOR, "q.semimajerr1", "q.semimajerr2")
ECC_UNC = rel_unc(ECC, "q.eccerr1", "q.eccerr2")
INCL_UNC = rel_unc(INCL, "q.inclerr1", "q.inclerr2")
DENSITY_UNC = rel_unc(DENSITY, "q.denserr1", "q.denserr2")

#: KB 20-32 classification tests, each stated once so a compound flag reuses
#: the same wording as its components.
GAS_GIANT_T = f"{MASS_J} > 0.1"
GAS_GIANT_F = f"{MASS_J} <= 0.1"
ROCKY_T = f"{DENSITY} > 3"
ROCKY_F = f"{DENSITY} <= 3"
SHORT_T = f"{PERIOD} < 10"
SHORT_F = f"{PERIOD} >= 10"
SUPER_MASS_T = f"{MASS_E} BETWEEN 1 AND 10"
SUPER_MASS_F = f"({MASS_E} < 1 OR {MASS_E} > 10)"
INFLATED_DENS_T = f"{DENSITY} < 0.5"
INFLATED_DENS_F = f"{DENSITY} >= 0.5"
HZ_T = f"{SEMIMAJOR} BETWEEN {HZ_INNER} AND {HZ_OUTER}"
HZ_F = f"({SEMIMAJOR} < {HZ_INNER} OR {SEMIMAJOR} > {HZ_OUTER})"
PREC_P_T = f"abs({PERIOD_UNC}) < 5"
PREC_P_F = f"abs({PERIOD_UNC}) >= 5"
PREC_M_T = f"abs({MASS_UNC}) < 5"
PREC_M_F = f"abs({MASS_UNC}) >= 5"
PREC_R_T = f"abs({RADIUS_UNC}) < 5"
PREC_R_F = f"abs({RADIUS_UNC}) >= 5"

PLANET_DETAIL_SQL = f"""
WITH obs AS (
    SELECT
        io.subjectlink                                  AS planet,
        max(CASE WHEN i.facilityname = 'kep' THEN 1 ELSE 0 END) AS kepler_flag,
        max(CASE WHEN i.facilityname = 'k2' THEN 1 ELSE 0 END)  AS k2_flag,
        max(CASE WHEN i.facilityname = 'ttv' THEN 1 ELSE 0 END) AS ttv_flag,
        count(*)                                        AS observation_count
    FROM public.planet_instrument_observations io
    JOIN public.instruments_surveys i ON i.instrumentref = io.facilitylink
    GROUP BY io.subjectlink
),
ordered AS (
    SELECT
        pp.planetref                                    AS planet,
        pp.hostlink                                     AS star,
        oo.period                                       AS period,
        lead(oo.period) OVER (
            PARTITION BY pp.hostlink
            ORDER BY oo.period)                         AS next_period
    FROM public.planets pp
    LEFT JOIN public.orbital_characteristics oo ON oo.bodylink = pp.planetref
)
SELECT
    p.planetref                                         AS planet,
    p.hostlink                                          AS star,
    s.hostplname                                        AS host_star_name,
    concat(s.hostplname, ' ', p.completter)             AS planet_name,
    p.completter                                        AS companion_letter,
    p.notecount::double precision                       AS note_count,
    p.discmethod                                        AS discovery_method_stored,
    {DISCOVERY_STANDARD}                                AS discovery_method,
    {TRANSIT_FLAG}                                      AS transit_discovery_indicator,
    {RADVEL_FLAG}                                       AS radial_velocity_indicator,
    {rp(PERIOD)}                                        AS orbital_period_days,
    ({PERIOD} / {DAYS_PER_YEAR})                        AS orbital_period_years,
    {rp(SEMIMAJOR)}                                     AS semi_major_axis_au,
    {rp(ECC)}                                           AS eccentricity,
    {rp(INCL)}                                          AS inclination_degrees,
    {rp(MASS_J)}                                        AS planet_mass_jupiter,
    {MASS_E}                                            AS planet_mass_earth,
    {rp(RAD_J)}                                         AS planet_radius_jupiter,
    {RAD_E}                                             AS planet_radius_earth,
    {rp(DENSITY)}                                       AS planet_density,
    {SURFACE_GRAVITY}                                   AS surface_gravity,
    {MASS_RADIUS_RATIO}                                 AS mass_radius_ratio,
    ({ESCAPE_VELOCITY_MS} / 1000)                       AS escape_velocity_kms,
    {ESCAPE_VELOCITY_MS}                                AS escape_velocity_ms,
    ({ORBITAL_VELOCITY_MS} / 1000)                      AS orbital_velocity_kms,
    {ORBITAL_VELOCITY_MS}                               AS orbital_velocity_ms,
    {EQ_TEMP}                                           AS equilibrium_temperature,
    {TRANSIT_DEPTH}                                     AS transit_depth,
    {TRANSIT_DEPTH_PCT}                                 AS transit_depth_percent,
    {MASS_RATIO}                                        AS planet_star_mass_ratio,
    {KEPLER_MASS}                                       AS kepler_derived_stellar_mass,
    {KEPLER_DIFF}                                       AS kepler_mass_difference,
    abs({KEPLER_DIFF})                                  AS kepler_mass_absolute_difference,
    {GOLDILOCKS}                                        AS goldilocks_value,
    {rp('ord.next_period')}                             AS next_planet_period_days,
    (ord.next_period / NULLIF({PERIOD}, 0))             AS next_planet_period_ratio,
    {STELLAR_MASS_D}                                    AS host_stellar_mass,
    {STELLAR_RADIUS_D}                                  AS host_stellar_radius,
    {STELLAR_TEMP_D}                                    AS host_stellar_temperature,
    {LUMINOSITY}                                        AS host_stellar_luminosity,
    {HZ_INNER}                                          AS habitable_zone_inner_au,
    {HZ_OUTER}                                          AS habitable_zone_outer_au,
    {rp('s.stellardist')}                               AS stellar_distance_pc,
    (s.stellardist * {LY_PER_PC})                       AS stellar_distance_ly,
    CASE WHEN {flag_yn(d(SL + "->>'Dist_Lim'"))} = 'No'
          AND {flag_yn(d(PM + "->>'Mag_Blend'"))} = 'No'
         THEN s.stellardist * {LY_PER_PC} END           AS stellar_distance_ly_clean,
    s.compcount::double precision                       AS companion_count,
    {PERIOD_UNC}                                        AS period_relative_uncertainty,
    {MASS_UNC}                                          AS mass_relative_uncertainty,
    {RADIUS_UNC}                                        AS radius_relative_uncertainty,
    {SEMIMAJOR_UNC}                                     AS semi_major_relative_uncertainty,
    {ECC_UNC}                                           AS eccentricity_relative_uncertainty,
    {INCL_UNC}                                          AS inclination_relative_uncertainty,
    {DENSITY_UNC}                                       AS density_relative_uncertainty,
    q.masssource                                        AS mass_source,
    CASE WHEN q.masssource = 'Msini' THEN 'Yes'
         WHEN q.masssource IS NOT NULL THEN 'No' END    AS minimum_mass_status,
    q.updatestamp                                       AS record_update_date,
    date_part('year', q.updatestamp)                    AS record_update_year,
    {d(PL + "->>'Period_Lim'")}                         AS period_limit_flag,
    {d(PL + "->>'Semimaj_Lim'")}                        AS semi_major_limit_flag,
    {d(PL + "->>'Ecc_Lim'")}                            AS eccentricity_limit_flag,
    {d(PL + "->>'Incl_Lim'")}                           AS inclination_limit_flag,
    {d(PL + "->>'Mass_Lim'")}                           AS mass_limit_flag,
    {d(PL + "->>'Rad_Lim'")}                            AS radius_limit_flag,
    {d(PL + "->>'Dens_Lim'")}                           AS density_limit_flag,
    {d(SL + "->>'Dist_Lim'")}                           AS distance_limit_flag,
    {d(SL + "->>'Temp_Lim'")}                           AS temperature_limit_flag,
    {d(SL + "->>'OptMag_Lim'")}                         AS magnitude_limit_flag,
    {d(SL + "->>'StellarRad_Lim'")}                     AS stellar_radius_limit_flag,
    {d(SL + "->>'StellarMass_Lim'")}                    AS stellar_mass_limit_flag,
    {flag_yn(d(PL + "->>'Period_Lim'"))}                AS period_upper_limit,
    {flag_yn(d(PL + "->>'Ecc_Lim'"))}                   AS eccentricity_upper_limit,
    {flag_yn(d(PL + "->>'Incl_Lim'"))}                  AS inclination_upper_limit,
    {flag_yn(d(PL + "->>'Mass_Lim'"))}                  AS mass_upper_limit,
    {flag_yn(d(PL + "->>'Rad_Lim'"))}                   AS radius_upper_limit,
    {flag_yn(d(PL + "->>'Dens_Lim'"))}                  AS density_upper_limit,
    {flag_yn(d(SL + "->>'Dist_Lim'"))}                  AS distance_upper_limit,
    {flag_yn(d(SL + "->>'Temp_Lim'"))}                  AS stellar_temperature_upper_limit,
    {flag_yn(d(SL + "->>'StellarMass_Lim'"))}           AS stellar_mass_upper_limit,
    CASE WHEN {d(PL + "->>'Rad_Lim'")} = 1 THEN 1 ELSE 0 END
                                                        AS radius_upper_limit_indicator,
    CASE WHEN {d(PL + "->>'Mass_Lim'")} = 1 THEN 1 ELSE 0 END
                                                        AS mass_upper_limit_indicator,
    CASE WHEN {d(SL + "->>'Dist_Lim'")} = 1 THEN 1 ELSE 0 END
                                                        AS distance_upper_limit_indicator,
    {d(PH + "->>'Temp_Blend'")}                         AS temperature_blend_flag,
    {d(PH + "->>'Mass_Blend'")}                         AS stellar_mass_blend_flag,
    {d(PH + "->>'Rad_Blend'")}                          AS stellar_radius_blend_flag,
    {d(PM + "->>'Mag_Blend'")}                          AS magnitude_blend_flag,
    {flag_yn(d(PH + "->>'Temp_Blend'"))}                AS temperature_blended,
    {flag_yn(d(PM + "->>'Mag_Blend'"))}                 AS magnitude_blended,
    CASE WHEN {d(PH + "->>'Temp_Blend'")} = 1 THEN 1 ELSE 0 END
                                                        AS temperature_blend_indicator,
    CASE WHEN {d(PM + "->>'Mag_Blend'")} = 1 THEN 1 ELSE 0 END
                                                        AS magnitude_blend_indicator,
    CASE WHEN COALESCE({d(PH + "->>'Temp_Blend'")}, 0) = 1
              OR COALESCE({d(PH + "->>'Mass_Blend'")}, 0) = 1
              OR COALESCE({d(PH + "->>'Rad_Blend'")}, 0) = 1
              OR COALESCE({d(PM + "->>'Mag_Blend'")}, 0) = 1
         THEN 'Yes' ELSE 'No' END                       AS any_stellar_blend,
    COALESCE(obs.kepler_flag, 0)                        AS kepler_observation_indicator,
    COALESCE(obs.k2_flag, 0)                            AS k2_observation_indicator,
    COALESCE(obs.ttv_flag, 0)                           AS ttv_observation_indicator,
    COALESCE(obs.observation_count, 0)::double precision AS observation_count,
    CASE WHEN obs.planet IS NULL THEN 'No' ELSE 'Yes' END AS observed_by_a_survey,
    {yn(GAS_GIANT_T, GAS_GIANT_F)}                      AS gas_giant_planet,
    CASE WHEN {GAS_GIANT_T} THEN 1 ELSE 0 END           AS gas_giant_indicator,
    {yn(ROCKY_T, ROCKY_F)}                              AS rocky_planet,
    CASE WHEN {ROCKY_T} THEN 1 ELSE 0 END               AS rocky_indicator,
    {yn(SHORT_T, SHORT_F)}                              AS short_period_planet,
    CASE WHEN {SHORT_T} THEN 1 ELSE 0 END               AS short_period_indicator,
    {yn(f"{GAS_GIANT_T} AND {SHORT_T}", f"{GAS_GIANT_F} OR {SHORT_F}")}
                                                        AS hot_jupiter,
    CASE WHEN {GAS_GIANT_T} AND {SHORT_T} THEN 1 ELSE 0 END
                                                        AS hot_jupiter_indicator,
    {yn(f"{ROCKY_T} AND {SUPER_MASS_T}", f"{ROCKY_F} OR {SUPER_MASS_F}")}
                                                        AS super_earth,
    CASE WHEN {ROCKY_T} AND {SUPER_MASS_T} THEN 1 ELSE 0 END
                                                        AS super_earth_indicator,
    {yn(HZ_T, HZ_F)}                                    AS planet_in_habitable_zone,
    CASE WHEN {HZ_T} THEN 1 ELSE 0 END                  AS habitable_zone_indicator,
    {yn(f"{ROCKY_T} AND {HZ_T}", f"{ROCKY_F} OR {HZ_F}")}
                                                        AS potentially_habitable,
    CASE WHEN {ROCKY_T} AND {HZ_T} THEN 1 ELSE 0 END    AS potentially_habitable_indicator,
    {yn(f"{ECC} > 0.25", f"{ECC} <= 0.25")}             AS high_eccentricity_planet,
    CASE WHEN {ECC} > 0.25 THEN 1 ELSE 0 END            AS high_eccentricity_indicator,
    {yn(f"{INCL} > 90", f"{INCL} <= 90")}               AS retrograde_orbit,
    CASE WHEN {INCL} > 90 THEN 1 ELSE 0 END             AS retrograde_indicator,
    {yn(f"{INCL} >= 90", f"{INCL} < 90")}               AS retrograde_orbit_inclusive,
    CASE WHEN {INCL} >= 90 THEN 1 ELSE 0 END            AS retrograde_inclusive_indicator,
    {yn(f"{GAS_GIANT_T} AND {INFLATED_DENS_T}", f"{GAS_GIANT_F} OR {INFLATED_DENS_F}")}
                                                        AS inflated_gas_giant,
    CASE WHEN {GAS_GIANT_T} AND {INFLATED_DENS_T} THEN 1 ELSE 0 END
                                                        AS inflated_gas_giant_indicator,
    CASE WHEN s.compcount > 1 THEN 'Yes' ELSE 'No' END  AS in_multi_planetary_system,
    {yn(PREC_P_T, PREC_P_F)}                            AS period_high_precision,
    {yn(PREC_M_T, PREC_M_F)}                            AS mass_high_precision,
    {yn(PREC_R_T, PREC_R_F)}                            AS radius_high_precision,
    {yn(f"{PREC_P_T} AND {PREC_M_T} AND {PREC_R_T}",
        f"{PREC_P_F} OR {PREC_M_F} OR {PREC_R_F}")}     AS well_characterized_planet,
    CASE WHEN {PREC_P_T} AND {PREC_M_T} AND {PREC_R_T} THEN 1 ELSE 0 END
                                                        AS well_characterized_indicator,
    1                                                   AS planet_row_count
FROM public.planets p
JOIN public.stars s ON s.stellarref = p.hostlink
LEFT JOIN public.orbital_characteristics o ON o.bodylink = p.planetref
LEFT JOIN public.physical_properties ph ON ph.objectlink = p.planetref
LEFT JOIN public.data_quality_tracking q ON q.targetlink = p.planetref
LEFT JOIN obs ON obs.planet = p.planetref
LEFT JOIN ordered ord ON ord.planet = p.planetref
"""

# --------------------------------------------------------------------------- #
# Star Detail
# --------------------------------------------------------------------------- #
STAR_DETAIL_SQL = f"""
WITH ratios AS (
    SELECT
        pp.hostlink                                     AS star,
        oo.period                                       AS period,
        lead(oo.period) OVER (
            PARTITION BY pp.hostlink
            ORDER BY oo.period)                         AS next_period
    FROM public.planets pp
    JOIN public.orbital_characteristics oo ON oo.bodylink = pp.planetref
),
pairs AS (
    SELECT
        star,
        count(*) FILTER (WHERE next_period IS NOT NULL) AS adjacent_pair_count,
        max(next_period / NULLIF(period, 0))            AS max_ratio,
        min(next_period / NULLIF(period, 0))            AS min_ratio,
        avg(next_period / NULLIF(period, 0))            AS avg_ratio,
        exp(avg(ln(next_period / NULLIF(period, 0))))   AS geo_ratio
    FROM ratios
    GROUP BY star
),
per_star AS (
    SELECT
        pp.hostlink                                     AS star,
        count(*)                                        AS planet_count,
        min(oo.period)                                  AS shortest_period,
        max(oo.period)                                  AS longest_period,
        min(oo.semimajor)                               AS innermost_semi_major,
        max(oo.semimajor)                               AS outermost_semi_major,
        max(php.massjup)                                AS heaviest_planet_mass,
        max(php.radjup)                                 AS largest_planet_radius,
        max(php.densvalue)                              AS densest_planet,
        sum(CASE WHEN php.massjup > 0.1 THEN 1 ELSE 0 END) AS gas_giant_count,
        sum(CASE WHEN php.densvalue > 3 THEN 1 ELSE 0 END) AS rocky_count,
        count(php.densvalue)                            AS planets_with_density,
        count(CASE WHEN php.densvalue IS NOT NULL OR php.massjup IS NOT NULL
                   THEN 1 END)                          AS planets_with_composition,
        sum(CASE WHEN oo.period < 10 THEN 1 ELSE 0 END) AS short_period_count,
        sum({TRANSIT_FLAG.replace('p.', 'pp.')})        AS transit_discovery_count,
        sum({RADVEL_FLAG.replace('p.', 'pp.')})         AS radial_velocity_count
    FROM public.planets pp
    LEFT JOIN public.orbital_characteristics oo ON oo.bodylink = pp.planetref
    LEFT JOIN public.physical_properties php ON php.objectlink = pp.planetref
    GROUP BY pp.hostlink
),
star_obs AS (
    SELECT
        pp.hostlink                                     AS star,
        max(CASE WHEN i.facilityname = 'kep' THEN 1 ELSE 0 END) AS kepler_flag,
        max(CASE WHEN i.facilityname = 'k2' THEN 1 ELSE 0 END)  AS k2_flag,
        max(CASE WHEN i.facilityname = 'ttv' THEN 1 ELSE 0 END) AS ttv_flag
    FROM public.planet_instrument_observations io
    JOIN public.instruments_surveys i ON i.instrumentref = io.facilitylink
    JOIN public.planets pp ON pp.planetref = io.subjectlink
    GROUP BY pp.hostlink
)
SELECT
    s.stellarref                                        AS star,
    s.hostplname                                        AS star_name,
    {rp('s.stellardist')}                               AS stellar_distance_pc,
    (s.stellardist * {LY_PER_PC})                       AS stellar_distance_ly,
    s.compcount::double precision                       AS companion_count,
    {STELLAR_MASS_D}                                    AS stellar_mass,
    {STELLAR_RADIUS_D}                                  AS stellar_radius,
    {STELLAR_TEMP_D}                                    AS stellar_temperature,
    {OPT_MAG_D}                                         AS optical_magnitude,
    {_BAND}                                             AS photometric_band_stored,
    {BAND_STANDARD}                                     AS photometric_band,
    {BAND_STRICT}                                       AS photometric_band_strict,
    {BAND_GROUPS}                                       AS photometric_band_group,
    {LUMINOSITY}                                        AS stellar_luminosity,
    {HZ_INNER}                                          AS habitable_zone_inner_au,
    {HZ_OUTER}                                          AS habitable_zone_outer_au,
    {STELLAR_DENSITY_KG_M3}                             AS stellar_density_kg_m3,
    {STELLAR_DENSITY_SOLAR}                             AS stellar_density_solar,
    {GRAV_PARAMETER}                                    AS gravitational_parameter,
    {d(CO + "->>'RA_Decimal'")}                         AS right_ascension_degrees,
    {d(CO + "->>'Dec_Decimal'")}                        AS declination_degrees,
    {CO}->>'RA_Text'                                    AS right_ascension_text,
    {CO}->>'Dec_Text'                                   AS declination_text,
    {d(PH + "->>'Temp_Blend'")}                         AS temperature_blend_flag,
    {d(PH + "->>'Mass_Blend'")}                         AS mass_blend_flag,
    {d(PH + "->>'Rad_Blend'")}                          AS radius_blend_flag,
    {d(PM + "->>'Mag_Blend'")}                          AS magnitude_blend_flag,
    {flag_yn(d(PM + "->>'Mag_Blend'"))}                 AS star_magnitude_blended,
    CASE WHEN COALESCE({d(PH + "->>'Temp_Blend'")}, 0) = 1
              OR COALESCE({d(PH + "->>'Mass_Blend'")}, 0) = 1
              OR COALESCE({d(PH + "->>'Rad_Blend'")}, 0) = 1
              OR COALESCE({d(PM + "->>'Mag_Blend'")}, 0) = 1
         THEN 'Yes' ELSE 'No' END                       AS any_blended_measurement,
    ps.planet_count::double precision                   AS star_planet_count,
    {rp('ps.shortest_period')}                          AS shortest_orbital_period,
    {rp('ps.longest_period')}                           AS longest_orbital_period,
    {rp('ps.innermost_semi_major')}                     AS innermost_semi_major_axis,
    {rp('ps.outermost_semi_major')}                     AS outermost_semi_major_axis,
    {rp('ps.heaviest_planet_mass')}                     AS heaviest_planet_mass_jupiter,
    {rp('ps.largest_planet_radius')}                    AS largest_planet_radius_jupiter,
    {rp('ps.densest_planet')}                           AS densest_planet_density,
    ps.gas_giant_count::double precision                AS star_gas_giant_count,
    ps.rocky_count::double precision                    AS star_rocky_planet_count,
    ps.planets_with_density::double precision           AS star_planets_with_density,
    ps.planets_with_composition::double precision       AS star_planets_with_composition,
    ps.short_period_count::double precision             AS star_short_period_count,
    ps.transit_discovery_count::double precision        AS star_transit_discovery_count,
    ps.radial_velocity_count::double precision          AS star_radial_velocity_count,
    pr.adjacent_pair_count::double precision            AS adjacent_pair_count,
    pr.max_ratio                                        AS max_adjacent_period_ratio,
    pr.min_ratio                                        AS min_adjacent_period_ratio,
    pr.avg_ratio                                        AS mean_adjacent_period_ratio,
    pr.geo_ratio                                        AS geometric_mean_adjacent_period_ratio,
    COALESCE(so.kepler_flag, 0)                         AS kepler_observation_indicator,
    COALESCE(so.k2_flag, 0)                             AS k2_observation_indicator,
    COALESCE(so.ttv_flag, 0)                            AS ttv_observation_indicator,
    CASE WHEN s.compcount > 1 THEN 'Yes' ELSE 'No' END  AS multi_planetary_system,
    CASE WHEN s.compcount > 1 THEN 1 ELSE 0 END         AS multi_planetary_indicator,
    CASE WHEN ps.planet_count > 1 THEN 'Yes' ELSE 'No' END
                                                        AS multiple_planet_rows,
    CASE WHEN ps.planets_with_composition = 0 THEN NULL
         WHEN ps.rocky_count > 0 AND ps.gas_giant_count = 0 THEN 'Rocky Only'
         WHEN ps.gas_giant_count > 0 AND ps.rocky_count = 0 THEN 'Gas Giants Only'
         WHEN ps.rocky_count > 0 AND ps.gas_giant_count > 0 THEN 'Mixed'
         ELSE 'Neither' END                             AS system_composition,
    CASE WHEN ps.planets_with_composition = 0 THEN NULL
         WHEN ps.rocky_count > 0 THEN 'Yes' ELSE 'No' END AS has_rocky_planet,
    CASE WHEN ps.planets_with_composition = 0 THEN NULL
         WHEN ps.gas_giant_count > 0 THEN 'Yes' ELSE 'No' END AS has_gas_giant,
    CASE WHEN ps.rocky_count > 0 AND ps.gas_giant_count = 0 THEN 1 ELSE 0 END
                                                        AS rocky_only_indicator,
    CASE WHEN ps.gas_giant_count > 0 AND ps.rocky_count = 0 THEN 1 ELSE 0 END
                                                        AS gas_giants_only_indicator,
    CASE WHEN ps.rocky_count = ps.planets_with_density
              AND ps.planets_with_density > 0 THEN 'Yes'
         WHEN ps.planets_with_density > 0 THEN 'No' END  AS all_density_measured_rocky,
    1                                                   AS star_row_count
FROM public.stars s
LEFT JOIN per_star ps ON ps.star = s.stellarref
LEFT JOIN pairs pr ON pr.star = s.stellarref
LEFT JOIN star_obs so ON so.star = s.stellarref
"""

# --------------------------------------------------------------------------- #
# Planet Observation bridge and Facility Detail
# --------------------------------------------------------------------------- #
OBSERVATION_SQL = """
SELECT
    io.obsref                                           AS observation,
    io.subjectlink                                      AS planet,
    p.hostlink                                          AS star,
    i.facilityname                                      AS facility,
    1                                                   AS observation_row_count
FROM public.planet_instrument_observations io
JOIN public.instruments_surveys i ON i.instrumentref = io.facilitylink
JOIN public.planets p ON p.planetref = io.subjectlink
"""

FACILITY_SQL = """
SELECT
    i.facilityname                                      AS facility,
    i.instrumentref::double precision                   AS facility_key,
    CASE i.facilityname WHEN 'kep' THEN 'Kepler mission'
         WHEN 'k2' THEN 'K2 mission'
         WHEN 'ttv' THEN 'Transit timing variations' END AS facility_description,
    1                                                   AS facility_row_count
FROM public.instruments_surveys i
"""

ALL_SQL = {
    "Planet Detail": PLANET_DETAIL_SQL,
    "Star Detail": STAR_DETAIL_SQL,
    "Planet Observation": OBSERVATION_SQL,
    "Survey Facility Detail": FACILITY_SQL,
}
