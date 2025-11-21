# GDP Analysis and Interactive Visualizations

Exploratory analysis and interactive visualizations of GDP per capita (nominal USD) using the included World Bank-style CSV dataset (`gdp_pc_data.csv`). This repository contains Jupyter notebooks for static plotting and interactive Dash apps that let you explore GDP per-capita trends and maps for 2024.

**Notebooks & Key Files**
- `gdp_plots.ipynb`: Static exploratory plots using `pandas`, `seaborn` and `matplotlib` (time series comparisons between countries).
- `gdp_graph_choice.ipynb`: Interactive Dash app to plot GDP-per-capita time series for selected countries and year ranges (uses `plotly.express`, `dash`, and `dash_bootstrap_components`).
- `gdp_maps.ipynb`: Interactive Dash choropleth maps for 2024 GDP-per-capita (uses `plotly.express`, `pycountry`, and Dash components).
- `gdp_pc_data.csv`: Primary dataset used by the notebooks (included in this repository).
- `assets/style.css`: styling used by the notebooks or dashboards (if referenced).

**Quick Overview**
- The notebooks load `gdp_pc_data.csv` with slightly different CSV options (e.g., `header=2` or `skiprows=4`) — open the notebook to see the exact read parameters used for each analysis.
- Interactive apps are implemented inside notebooks. To run them you can either run the notebooks (recommended) or export the notebook to a script and run the script as a Dash app.

**Installation**

The notebooks were developed in a Python data environment. Recommended approach is to use Conda and a virtual environment named `gdp_analysis` (or any name you prefer).

Open PowerShell and run:

```powershell
conda create -n gdp_analysis python=3.10 -y
conda install requirements.txt
conda activate gdp_analysis
```

**Usage**

1. Open the notebooks in Jupyter Lab or Notebook

```powershell
jupyter lab
# or
jupyter notebook
```

Then open and run the notebook cells for:
- `gdp_plots.ipynb` — run the cells to generate static visualizations.
- `gdp_graph_choice.ipynb` — run all cells to start the interactive Dash plotter.
- `gdp_maps.ipynb` — run all cells to start the interactive choropleth maps.

When the Dash apps are started from the notebooks you will typically see a local server URL printed in the notebook output (e.g. `http://127.0.0.1:8050`) — open that URL in your browser to interact with the app.

2. Running the Dash apps as scripts (optional)

If you prefer to run the Dash apps as standalone Python scripts, convert the notebook to a script and then run it. Example (from the project root):

```powershell
jupyter nbconvert --to script gdp_graph_choice.ipynb
python gdp_graph_choice.py
```

**Data notes**
- The dataset `gdp_pc_data.csv` is formatted like World Bank time series CSVs and contains country names and columns for years (1960–2024). Some notebooks read the CSV using `header=2` or `skiprows=4` to align with the dataset header structure used by the author. If you get errors when loading the CSV, open it in a text editor or spreadsheet and inspect where the header row with year labels begins, then adjust the `read_csv` parameters accordingly.
- The notebooks rely on country names being resolvable to ISO3 codes (for maps). Some country name mismatches may cause `pycountry` to fail to find a code; the map notebook filters out entries where an ISO3 code was not found.

**Examples**

- Read the CSV like in `gdp_plots.ipynb` and preview:

```python
import pandas as pd
gdp_data = pd.read_csv('gdp_pc_data.csv', skiprows=4, usecols=['Country Name'] + [str(year) for year in range(1960, 2025)])
gdp_data.head()
```

- Start `gdp_plots.ipynb` to create comparison plots (matplotlib/seaborn).

![Poland vs Greece GDP p/c 2000-2024 Plot](assets/pol_gre.png)

![Japan vs U.S. GDP p/c 1980-2024 Plot](assets/jap_us.png)

- Start `gdp_graph_choice.ipynb` to pick countries and year ranges interactively, and `gdp_maps.ipynb` to view choropleth maps for 2024.

![U.S. vs China vs India GDP p/c 1960-2024 Plot](assets/us_cn_in.png)

![China vs India GDP p/c 2000-2020 Plot](assets/cn_in.png)

![Europe Interactive GDP p/c Map](assets/europe.png)

![Asia Interactive GDP p/c Map](assets/asia.png)

**Troubleshooting**
- If plotting cells raise errors about missing packages, install the missing package into your activated environment with `pip install <package>` or `conda install <package> -c conda-forge`.
- If the Dash app does not appear in the browser after running the notebook, confirm the kernel output shows a server URL and that you do not have a firewall blocking the port (default 8050).
- For country-code mapping issues, verify the `Country Name` strings in `gdp_pc_data.csv` match names understood by `pycountry`. You can add a small mapping table to translate non-standard names to canonical names.

**Contributing**
- Improvements and bug fixes welcome. Open an issue or submit a pull request with a clear description of the change.

**License**
- This repository includes a `LICENSE` file — please review it for terms of reuse.

**Contact / Author**
- Author: repository owner (see repository metadata).
