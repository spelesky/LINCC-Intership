# LINCC-Intership
# qp_to_hats

**`qp_to_hats`** is a utility for converting probabilistic ensembles generated using [`qp`](https://github.com/LSSTDESC/qp) into formats compatible with [HATS](https://github.com/LSSTDESC/hats) via [LSDB](https://github.com/LSSTDESC/lsdb). This tool facilitates transforming ensemble data into nested-pandas `NestedFrame`s, managing multiple distribution formats (e.g., `norm`, `hist`, `interp`, `mixmod`, `quant`), and saving them for spatial querying in LSDB catalogs.

---

## Features

- Convert `qp.Ensemble` objects into nested-pandas `NestedFrame`s
- Handle various probability distribution types:  
  `norm`, `interp`, `mixmod`, `hist`, and `quant` (99, 20, 5 percentiles)
- Generate multiple ensemble representations from a single input (e.g., histograms, quantiles, interpolations)
- Export processed data into HATS-compatible LSDB catalogs
- Read HATS catalogs and reconstruct `qp.Ensemble`s

---

## Requirements

- Python 3.8+
- [`qp`](https://github.com/LSSTDESC/qp)
- [`nested-pandas`](https://github.com/LSSTDESC/nested-pandas)
- [`lsdb`](https://github.com/LSSTDESC/lsdb)
- [`hats`](https://github.com/LSSTDESC/hats)
- `numpy`
- `pandas`

---

## Function Overview

| Function | Description |
|----------|-------------|
| `ens_to_df` | Aggregates all converted ensemble representations into a single `pandas.DataFrame` |
| `df_to_hats` | Converts the DataFrame to an LSDB catalog and saves it to disk in HATS format |
| `hats_to_qp` | Loads a HATS LSDB catalog and reconstructs `qp.Ensemble` objects |

---

## Helper Function Overview

| Function | Description |
|----------|-------------|
| `convert_ens` | Converts a `qp.Ensemble` into multiple probabilistic formats (e.g., histogram, quantiles, interpolation, normal) and returns a dictionary of `NestedFrame` objects, using a naming convention based on the input algorithm and format. |
| `convert_ens_to_nested_frame` | Flattens a single `qp.Ensemble` into a nested-pandas `NestedFrame`, aligning any required metadata (e.g., `xvals`, `bins`, `quants`) and grouping by object ID for downstream analysis. |

---

## Example Usage

```python
ens = qp.Ensemble(...)  # your qp.Ensemble object
algo = "photoz_algo1"

# Convert ensemble to DataFrame with nested data
df = ens_to_df(ens, algo)

# Save the DataFrame to a HATS-compatible catalog
catalog = df_to_hats(df, name="photoz_catalog")

# Later, load and recover qp.Ensemble objects from catalog
recovered_ensembles = hats_to_qp("photoz_catalog")
