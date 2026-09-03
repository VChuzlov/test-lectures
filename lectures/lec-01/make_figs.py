"""
make_figs.py — все графики этой лекции в одном месте.

Запуск из папки лекции:
    python make_figs.py

Правило: НИ ОДНОГО графика руками в графическом редакторе. Всё, что на слайде,
должно пересобираться этой командой — тогда правка данных не превращается
в перерисовку десяти картинок.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from tools.figtheme import use_adaptive, save_adaptive  # noqa: E402


use_adaptive()


def fig_tiobe():
    data = {
        'Python': 18.53,
        'C': 11.10,
        'C++': 8.62,
        'Java': 8.25,
        'C#': 4.09,
        'JavaScript': 2.63,
        'Visual Basic': 2.18,
        'SQL': 1.88,
        'R': 1.56,
        'Rust': 1.45,
    }
    
    fig, ax = plt.subplots(figsize=(5.6, 5.5))
    sns.barplot(
        data=data,
        orient='h',
        ax=ax
    )
    ax.bar_label(ax.containers[0], fontsize=10)
    ax.set_xlabel("Рейтинг, %")
    plt.tight_layout()
    save_adaptive(fig, "pics/tiobe")
    plt.close(fig)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("fig_") and callable(fn):
            print(f"  {name}")
            fn()
    print("Готово. Компоненты обновлены в components/")
