from .state import active_layers

def remove_selected_layers(tree):
    selected_items = tree.selection()
    if not selected_items:
        return

    for item_id in selected_items:
        if item_id in active_layers:
            del active_layers[item_id]
        tree.delete(item_id)