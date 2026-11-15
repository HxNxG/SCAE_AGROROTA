"""Keep the original CLI available for existing training commands."""

if __package__:
    from .ml.train_nn import entrenar_ensamble_neuronal
else:
    from ml.train_nn import entrenar_ensamble_neuronal


if __name__ == "__main__":
    entrenar_ensamble_neuronal()
