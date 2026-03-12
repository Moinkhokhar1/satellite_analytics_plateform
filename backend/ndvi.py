import matplotlib
matplotlib.use('Agg')

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
from rasterio.plot import reshape_as_image

RESULT_FOLDER = "results"
os.makedirs(RESULT_FOLDER, exist_ok=True)

def calculate_indices(image_path):

    with rasterio.open(image_path) as src:

        red = src.read(1).astype(float)
        nir = src.read(2).astype(float)
        green = src.read(3).astype(float)

        # ---------- ORIGINAL RGB IMAGE ----------
        rgb = src.read([1,2,3])
        rgb = reshape_as_image(rgb)

        plt.figure(figsize=(6,6))
        plt.imshow(rgb)
        plt.axis("off")
        plt.savefig(os.path.join(RESULT_FOLDER,"original.png"))
        plt.close()

        # ---------- NDVI ----------
        ndvi = (nir - red) / (nir + red + 0.0001)

        plt.figure(figsize=(6,6))
        plt.imshow(ndvi, cmap="RdYlGn")
        plt.colorbar(label="NDVI")
        plt.savefig(os.path.join(RESULT_FOLDER,"ndvi.png"))
        plt.close()
    
        
        print("NDVI Statistics")
        print("Min:", np.min(ndvi))
        print("Max:", np.max(ndvi))
        print("Mean:", np.mean(ndvi))
        print("----------------------")


        # ---------- NDWI ----------
        ndwi = (green - nir) / (green + nir + 0.0001)

        plt.figure(figsize=(6,6))
        plt.imshow(ndwi, cmap="Blues")
        plt.colorbar(label="NDWI")
        plt.savefig(os.path.join(RESULT_FOLDER,"ndwi.png"))
        plt.close()
        
        print("NDWI Statistics")
        print("Min:", np.min(ndwi))
        print("Max:", np.max(ndwi))
        print("Mean:", np.mean(ndwi))
        print("----------------------")

        # ---------- LAND CLASSIFICATION ----------
        classification = np.zeros_like(ndvi)

        # Water
        classification[ndwi > 0.3] = 1

        # Vegetation
        classification[ndvi > 0.3] = 2

        # Urban / barren
        classification[(ndvi < 0.2) & (ndwi < 0)] = 3

        plt.figure(figsize=(6,6))
        plt.imshow(classification, cmap="viridis")
        plt.colorbar()
        plt.savefig(os.path.join(RESULT_FOLDER,"classification.png"))
        plt.close()

        return (
            "original.png",
            "ndvi.png",
            "ndwi.png",
            "classification.png"
        )