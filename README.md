# planets_data

AtScale SML semantic model over the BIRD-Interact `planets_data` database.
Built by `generator/build.sh`: edit the spec and re-run, never hand-edit the
emitted YAML.

## Shape

A clean star schema.

| dataset | grain | rows |
|---|---|---|
| `Planet Detail` | planet | 3372 |
| `Star Detail` | host star | 2509 |
| `Planet Observation` | planet × survey | 2683 |
| `Survey Facility Detail` | survey | 3 |

`orbital_characteristics` (3371), `physical_properties` (3359) and
`data_quality_tracking` (3372) are each 1:1 with a planet and all fold onto one
wide fact. `planet_instrument_observations` is a genuine bridge — 2460 planets
over 3 facilities, so 912 planets were observed by none and none by more than
two.

## Coverage decides everything

| measurement | planets |
|---|---|
| orbital period | 3305 |
| planet radius | 2694 |
| semi-major axis | 1897 |
| planet mass | 1174 |
| eccentricity | 974 |
| inclination | 502 |
| **bulk density** | **388** |

Every derived quantity inherits the scarcest input it needs: transit depth 2684,
Kepler's-law mass 1831, orbital velocity 1593, equilibrium temperature and
Goldilocks value 1533, mass ratio 1127, and surface gravity / escape velocity /
mass-radius ratio **509 each**. Every rocky, super-Earth, inflated-giant and
potentially-habitable answer is bounded by that 388.

## Constants are composed, formulas run at warehouse types (2026-08-27)

Every KB formula that needs a constant the KB does not state uses the standard
published value written out in the SQL and composed in the formula's own shape:
G = 6.67430E-11, M☉ = 1.98847E30 kg, R☉ = 6.957E8 m, 1 AU = 1.496E11 m,
M♃ = 1.898E27 kg, R♃ = 7.1492E7 m, R☉ = 109.2 R⊕. The first build substituted
pre-collapsed textbook shortcuts (Earth's 11186 m/s escape speed, the Sun's
1.408 g/cm³, GM☉ = 1.32712440018e20, 0.00095458 M☉/M♃) — right to three or four
digits, wrong after that, and the grader compares two decimals of values like
585 km/s or 1.5e20.

The stellar mass, radius and temperature live as JSON numbers whose column
meaning says REAL, so formulas read them through `::real` before widening —
what a plain SQL reader of the warehouse gets. The densest/least-dense ratio is
2,237,875,936 read that way and 2,237,875,810 read as exact decimals.

| quantity | bare reading | twin |
|---|---|---|
| Escape / Orbital Velocity | km/s (the follow-ups ask "in km/s") | `(Metres Per Second)` |
| Stellar Density | kg/m³ (the follow-ups ask "in kg/m^3") | `(Solar Units)` |
| Equilibrium Temperature | Kelvin, both lengths in metres | — |
| Transit Depth | fraction, both radii in Earth radii | `(Percent)` |
| Orbital Period | days, as recorded | `(Years)` |

The "as written" mixed-unit readings the first build shipped beside the
temperature and the transit depth are gone: a formula over two lengths is a
formula over one unit, and the literal reading is a unit error, not a
competing interpretation. Display copies of `real` columns go through
`::text::numeric` (the decimal Postgres prints, not the IEEE widening).

## Flags follow SQL's three-valued logic

Every Yes/No classification is 'Yes' when the definition holds, 'No' when it is
*definitely* false — for a compound, as soon as one input is recorded false —
and null only when nothing recorded settles it, so `= 'No'` selects exactly
what `NOT (<definition>)` keeps. Every quality flag that ever varies has a
Yes/No twin on the value 1 (`Mass Upper Limit`, `Distance Upper Limit`,
`Magnitude Blended`, …) whose 'No' means *recorded and not 1*.

`Retrograde Orbit (90 Degrees Or More)` ships beside the strict reading: 21
planets sit at exactly 90.0°, and the inclusive reading admits 5 hot Jupiters
where the strict one admits none.

`System Composition` (Rocky Only 27 / Gas Giants Only 782 / Mixed 35 / Neither
77) judges a star over every planet with a density *or* a mass, using both KB
classes; `All Density Measured Planets Rocky` (49) is the narrower reading that
ignores a gas giant known by mass alone. `Geometric Mean Adjacent Period Ratio`
is the other average of a set of ratios (differs from the arithmetic mean on
177 systems). `Kepler Mass Absolute Difference` is the sort key for a
recorded-vs-derived comparison.

## Concepts that are empty, not rare

* **No planet is both rocky and in its habitable zone** — the
  potentially-habitable count is 0 out of 328 judgeable, while 74 planets are
  rocky and 28 sit in a zone.
* **No hot Jupiter orbits retrograde** — a question asking for both returns
  nothing. (Max inclination in the catalogue is 90.76°, so only 8 planets clear
  the 90° threshold at all.)
* **The stellar temperature, mass and radius blend flags are 0 on every row.** The
  only blended measurements anywhere are 9 magnitudes. So no planet has a
  contaminated temperature reading, whichever survey found it.
* **Exactly one planet's radius is an upper limit.** The semi-major axis,
  magnitude and stellar-radius limit flags are zero throughout.

## Two dirty text columns

**Discovery method** — 38 spellings of six categories. Grouping by the raw text
splits Transit across five buckets (`Photometric` 578, `TR` 536, `Transit Method`
523, `Photometry` 516, `Transit` 511) that are one category of 2664. Membership is
matched **exactly** against KB 51's label lists; a substring reading would pull
other timing labels into TTV. One label starts with a Greek mu and is matched via
`chr(956)` so the emitted SQL stays ASCII.

**Photometric band** — 10 spellings of three bands, five for Kepler alone. The
canonical form folds `V-band` into Johnson V (779 stars); the stricter reading
that keeps it separate ships beside it (624 + 155).

## The magnitude scale is inverted

A *smaller* number is a *brighter* star. "The brightest star" is the **minimum**
of the magnitude column — `alf Tau` at 0.85. Star names are catalogue form, so
`alf Tau` rather than Aldebaran, and survey codes are lower case `kep` / `k2` /
`ttv`.

## Withheld threshold

**Compact System** depends on a cutoff on the adjacent period ratio that the
knowledge base masks on a running task, so **no compactness flag ships**. The
components do: max, min, arithmetic and geometric mean adjacent period ratio per system, plus the
adjacent pair count and the innermost period. (333 stars have every adjacent
ratio below 3; 210 of those also have an innermost planet under 10 days.)

## Unit conversions used, each named in the spec

`3.26156` ly/pc · `317.83` M⊕/M♃ · `11.209` R⊕/R♃ · `5778 K` solar T ·
`6.67430E-11` G · `1.98847E30 kg` M☉ · `6.957E8 m` R☉ · `1.496E11 m` AU ·
`1.898E27 kg` M♃ · `7.1492E7 m` R♃ · `109.2` R⊕/R☉ · `365.25` days/year.

The orbital period is stored in **days** while Kepler's third law needs years;
using days directly gives a stellar mass ~133,000× too small.

## Build

```
generator/build.sh
```

1. answer-key firewall — permitted question fields only
2. warehouse dry-run — 4 datasets, grain uniqueness, **275 pinned constants**
3. generate + 19 build gates
4. question-leakage gate (6-word runs)
5. masked-threshold gate against the KB
6. `sml-cli validate`
