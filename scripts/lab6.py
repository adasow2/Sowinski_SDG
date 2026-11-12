# %%
from pandas._libs import arrays
import rasterio as rio
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# %%
current_folder = Path.cwd()
raster_folder = current_folder / "data/rastry/lab6"
sentinel_folder = raster_folder / "sentinel-2-l2a_2026-06-26_S2C_MSIL2A_20260626T101021_R022_T33UXA_20260626T152309"

rgb_file = str(raster_folder / "tucholski_fragment.tif")
sentinel = {
    file.stem[-3:]: str(file)
    for file in sentinel_folder.iterdir()
    if file.is_file()
}
# %%


"""
Wyświetl raster w kolorach możliwie odzwierciedlających rzeczywistość
Przedstaw i krótko opisz histogram wartości dla każdego kanału
Podziel wartości rastra na 9 równych części (3 x 3), a następnie podaj współrzędne w układzie odniesienia rastra środka każdej z tych części
Zapisz raster do 1 pliku RGB złożonego z zaciągniętych 3 kanałów
"""
sentinel_olsztyn = str(raster_folder / "olsztyn_rgb.tif")

with rio.open(sentinel_olsztyn) as src:
    red = src.read(1)
    green = src.read(2)
    blue = src.read(3)
    meta = src.meta.copy()
    profile = src.profile


# %% zadanie 1
rgb = np.stack([red, green, blue])

raster_rgb = np.moveaxis(rgb, 0, -1)
raster_rgb2 = raster_rgb.astype(float).copy()
for i in range(3):
    low = np.percentile(raster_rgb2[:, :, i], 2)
    high = np.percentile(raster_rgb2[:, :, i], 98)

    raster_rgb2[:, :, i] = np.clip(
        (raster_rgb2[:, :, i] - low) / (high - low),
        0,
        1
    )

plt.imshow(raster_rgb2)
plt.axis("off")
plt.show()
# %% zadanie 2
# Przedstaw i krótko opisz histogram wartości dla każdego kanału

colors = ["red", "green", "blue"]
band_names = ["Czerwony (R)", "Zielony (G)", "Niebieski (B)"]

fig, axes = plt.subplots(3, 2, figsize=(12, 10))

for band, color, name in zip([0, 1, 2], colors, band_names):
    axes[band, 0].hist(raster_rgb[:, :, band].flatten(), bins=50, color=color, alpha=0.7)
    axes[band, 0].set_title(f'Raster oryginalny {name}')
    axes[band, 0].grid(True)

    # Prawy wykres (Raster 2)
    axes[band, 1].hist(raster_rgb2[:, :, band].flatten(), bins=50, color=color, alpha=0.7)
    axes[band, 1].set_title(f'Raster 2 bez wartości odstających {name}')
    axes[band, 1].grid(True)

plt.tight_layout()
plt.show()
"""
Każdy z przedstawionych histogramów ma rozkład asymetryczny prawostronny
"""

# %% zadanie 3
# Podziel wartości rastra na 9 równych części (3 x 3), a następnie podaj współrzędne
# w układzie odniesienia rastra środka każdej z tych części
transform = profile.get('transform')
x0 = transform[2]
y0 = transform[5]

height = raster_rgb2.shape[0]
width = raster_rgb2.shape[1]

# Podział na 3 części w poziomie i 3 w pionie (łącznie 9 kafelków)
h_arrays = np.array_split(raster_rgb2, 3, axis=1)
splited_arrays = []
for a in h_arrays:
    w_arrays = np.array_split(a, 3, axis=0)
    for i in w_arrays:
        splited_arrays.append(i)
