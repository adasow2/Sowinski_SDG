# %%
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
olsztyn = Path(r"C:\Users\sowin\Desktop\semestr_4\kow\ćwiczenia\dane\dane wejściowe\olsztyn\dane_clip")




with rio.open(str(olsztyn / "B04.tif")) as r_src, rio.open(str(olsztyn / "B03.tif")) as g_src, rio.open(str(olsztyn / "B02.tif")) as b_src:
    red = r_src.read(1)
    green = g_src.read(1)
    blue = b_src.read(1)

    meta = r_src.meta.copy()


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
# Podziel wartości rastra na 9 równych części (3 x 3), a następnie podaj współrzędne w układzie odniesienia rastra środka każdej z tych części

height, width, _ = raster_rgb.shape

# Rozmiar pojedynczego wycinka (części)
h_part = height // 3
w_part = width // 3

centers_pixel = []
centers_geo = []

fig, axes = plt.subplots(3, 3, figsize=(10, 10))
axes = axes.flatten()

part_idx = 0
for i in range(3):
    for j in range(3):
        # Definicja granic wycinka w pikselach
        row_start = i * h_part
        row_end = (i + 1) * h_part if i < 2 else height
        col_start = j * w_part
        col_end = (j + 1) * w_part if j < 2 else width

        # Wycinek rastra
        part = raster_rgb2[row_start:row_end, col_start:col_end]

        # Środek wycinka w układzie współrzędnych pikselowych (wiersz, kolumna) względem całego rastra
        center_row = (row_start + row_end - 1) / 2.0
        center_col = (col_start + col_end - 1) / 2.0
        centers_pixel.append((center_row, center_col))

        # Współrzędne w układzie odniesienia rastra (georeferencja / transformacja afiniczna)
        # src.transform * (kolumna, wiersz) -> uwaga: w rasterio transform przyjmuje (x, y) czyli (col, row)
        geo_x, geo_y = rio.transform.xy(profile['transform'], center_row, center_col)
        centers_geo.append((geo_x, geo_y))

        print(f"Część {part_idx + 1} (3x3 - rząd {i+1}, kolumna {j+1}):")
        print(f"  Środek w pikselach (wiersz, kolumna): ({center_row:.1f}, {center_col:.1f})")
        print(f"  Środek w układzie geograficznym/projektowanym (X, Y): ({geo_x:.2f}, {geo_y:.2f})")

        # Wizualizacja części
        axes[part_idx].imshow(part)
        axes[part_idx].set_title(f"Część {part_idx + 1}\nX:{geo_x:.1f}, Y:{geo_y:.1f}", fontsize=8)
        axes[part_idx].axis("off")

        part_idx += 1

plt.tight_layout()
plt.show()

# %% zadanie 4
# Zapisz raster do 1 pliku RGB złożonego z zaciągniętych 3 kanałów (lub zapisz wynikowy raster)

# %%
meta.update({
    "count": 3
})

# %%
output_path = raster_folder / "olsztyn_rgb_output.tif"
with rio.open(output_path, 'w', **meta) as dst:
    dst.write(rgb)

print(f"Zapisano raster do pliku: {output_path}")
