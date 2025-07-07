import xarray as xr

# Open the NetCDF file
ds = xr.open_dataset('elec_s_1024.nc')

# Print dataset summary
print(ds)

# List all variables and coordinates
print(ds.variables)
# List all variables
for var in ds.data_vars:
    print(f"{var}: dims={ds[var].dims}, shape={ds[var].shape}")
# Check for time-varying line capacity (dynamic line rating data)
if 'lines_s_max_pu' in ds.data_vars:
    print("lines_s_max_pu dims:", ds['lines_s_max_pu'].dims)
import matplotlib.pyplot as plt

lines_nom = ds['lines_s_nom'].values
plt.hist(lines_nom, bins=50)
plt.xlabel('Nominal Line Rating [MW]')
plt.ylabel('Number of Lines')
plt.title('Distribution of Transmission Line Ratings')
plt.show()
plt.scatter(ds['buses_x'], ds['buses_y'], s=5)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Bus Map')
plt.show()
for var in ds.data_vars:
    if 'lines_i' in ds[var].dims and 'snapshots' in ds[var].dims:
        print(f"{var}: dims={ds[var].dims}, shape={ds[var].shape}")
weather_vars = ['temperature', 'temp', 'wind', 'wind_speed', 'solar', 'irradiance', 'radiation']
for var in ds.data_vars:
    for w in weather_vars:
        if w in var.lower():
            print(var, ds[var].dims)

