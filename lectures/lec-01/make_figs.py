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

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figtheme import use_adaptive, save_adaptive  # noqa: E402

use_adaptive()


def fig_cp():
    """Изобарная теплоёмкость олефинов: C_p = A + Bt + Ct² + Dt³ + Et⁴."""
    T = np.linspace(250, 350, 120)

    def cp(A, B, C, D, E):
        return A + B * T + C * T**2 + D * T**3 + E * T**4

    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.plot(T, cp(22.22, 0.1385, 7e-4, -7.7979e-07, 2.362e-10), label="1-гексен")
    ax.plot(T, cp(18.00, 0.1200, 6e-4, -6.5000e-07, 2.000e-10), ls="--", label="1-пентен")
    ax.plot(T, cp(14.00, 0.1000, 5e-4, -5.5000e-07, 1.700e-10), ls=":", label="1-бутен")
    ax.set_xlabel("Температура, K")
    ax.set_ylabel("C$_p$, Дж/(моль·К)")
    ax.legend()
    save_adaptive(fig, "pics/cp")
    plt.close(fig)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("fig_") and callable(fn):
            print(f"  {name}")
            fn()
    print("Готово. Компоненты обновлены в components/")
