import xarray as xr
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

folder = r'C:\Users\nihar\Project\Project\networks'  # Folder with all NetCDF files
output_folder = r'C:\Users\nihar\Project\Project\Output'  # Where results and plots will be saved
os.makedirs(output_folder, exist_ok=True)

files = [f for f in os.listdir(folder) if f.endswith('.nc')]
all_stats = []

for filename in files:
    print(f"\nProcessing: {filename}")
    ds = xr.open_dataset(os.path.join(folder, filename))
    summary = {'file': filename}

    # General dimensions and basic info
    summary['num_snapshots'] = len(ds['snapshots']) if 'snapshots' in ds else np.nan
    summary['num_lines'] = len(ds['lines_i']) if 'lines_i' in ds else np.nan
    summary['num_buses'] = len(ds['buses_i']) if 'buses_i' in ds else np.nan
    summary['num_generators'] = len(ds['generators_i']) if 'generators_i' in ds else np.nan
    summary['num_loads'] = len(ds['loads_i']) if 'loads_i' in ds else np.nan

    # --- LINE DATA ---
    if 'lines_s_nom' in ds.data_vars:
        lines_nom = ds['lines_s_nom'].values
        summary['lines_nom_mean'] = np.nanmean(lines_nom)
        summary['lines_nom_max'] = np.nanmax(lines_nom)
        summary['lines_nom_min'] = np.nanmin(lines_nom)
        plt.figure()
        plt.hist(lines_nom, bins=50)
        plt.xlabel('Nominal Line Rating [MW]')
        plt.ylabel('Number of Lines')
        plt.title(f'Line Ratings - {filename}')
        plt.tight_layout()
        plt.savefig(f'{output_folder}{filename}_line_rating.png')
        plt.close()
        # Save to Excel
        df_lines = pd.DataFrame({'lines_i': ds['lines_i'].values, 'lines_s_nom': lines_nom})
        df_lines.to_excel(f'{output_folder}{filename}_lines.xlsx', index=False)

    # --- GENERATOR DATA ---
    if 'generators_p_nom' in ds.data_vars:
        gen_nom = ds['generators_p_nom'].values
        summary['gen_nom_mean'] = np.nanmean(gen_nom)
        summary['gen_nom_max'] = np.nanmax(gen_nom)
        summary['gen_nom_min'] = np.nanmin(gen_nom)
        plt.figure()
        plt.hist(gen_nom, bins=50)
        plt.xlabel('Generator Nominal Power [MW]')
        plt.ylabel('Number of Generators')
        plt.title(f'Generator Power - {filename}')
        plt.tight_layout()
        plt.savefig(f'{output_folder}{filename}_generator_nom.png')
        plt.close()
        df_gens = pd.DataFrame({'generators_i': ds['generators_i'].values, 'generators_p_nom': gen_nom})
        df_gens.to_excel(f'{output_folder}{filename}_generators.xlsx', index=False)

    # --- LOAD DATA ---
    if 'loads_t_p_set' in ds.data_vars:
        # Mean total load per hour
        total_load_per_hour = ds['loads_t_p_set'].sum(dim='loads_t_p_set_i').values
        summary['avg_total_load'] = np.nanmean(total_load_per_hour)
        plt.figure()
        plt.plot(total_load_per_hour)
        plt.xlabel('Hour')
        plt.ylabel('Total Load [MW]')
        plt.title(f'Total Load Time Series - {filename}')
        plt.tight_layout()
        plt.savefig(f'{output_folder}{filename}_total_load.png')
        plt.close()
        df_loads = pd.DataFrame(total_load_per_hour, columns=['Total_Load'])
        df_loads.to_excel(f'{output_folder}{filename}_total_load_timeseries.xlsx', index=False)

    # --- BUS MAP ---
    if 'buses_x' in ds.data_vars and 'buses_y' in ds.data_vars:
        plt.figure()
        plt.scatter(ds['buses_x'].values, ds['buses_y'].values, s=5)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Bus Map - {filename}')
        plt.tight_layout()
        plt.savefig(f'{output_folder}{filename}_bus_map.png')
        plt.close()
        # Save bus coordinates
        df_buses = pd.DataFrame({
            'buses_i': ds['buses_i'].values,
            'x': ds['buses_x'].values,
            'y': ds['buses_y'].values
        })
        df_buses.to_excel(f'{output_folder}{filename}_bus_coordinates.xlsx', index=False)

    # --- EXPORT VARIABLE LIST (for documentation) ---
    with open(f'{output_folder}{filename}_variable_list.txt', 'w') as f:
        for var in ds.data_vars:
            f.write(f"{var}: dims={ds[var].dims}, shape={ds[var].shape}\n")

    all_stats.append(summary)
    ds.close()

# Save all summary statistics
df_stats = pd.DataFrame(all_stats)
df_stats.to_excel(f'{output_folder}summary_statistics_all_files.xlsx', index=False)
print("\nAll processing complete. Results and plots saved in the 'output/' folder.")

