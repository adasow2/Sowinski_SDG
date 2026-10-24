from .state import active_layers
import matplotlib.pyplot as plt

def plot_selected_layers(tree):
    """Wyświetla zaznaczone warstwy GeoPandas bezpośrednio z obiektów VectorLayer."""
    selected_items = tree.selection()
    if not selected_items:
        return

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Wybrane warstwy")

    plotted_count = 0
    for layer_id in selected_items:
        if layer_id in active_layers:
            layer_obj = active_layers[layer_id]
            # Pobieramy GeoDataFrame bezpośrednio z obiektu VectorLayer
            if layer_obj.df is not None:
                layer_obj.df.plot(
                    ax=ax,
                    alpha=0.6,
                    edgecolor='k',
                    label=layer_obj.name
                )
                plotted_count += 1

    if plotted_count > 0:
        ax.legend()
        plt.tight_layout()
        plt.show()
    else:
        plt.close(fig)