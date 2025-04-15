pip install streamlit

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Настройки страницы
st.set_page_config(page_title="Генерация водорода из пористого кремния", layout="centered")

# Заголовок
st.title("💧 Симуляция генерации водорода из пористого кремния")

st.markdown("""
Этот интерфейс моделирует кинетику реакции окисления пористого кремния (PSi) с водой и щелочью, 
в результате которой выделяется водород. 
Вы можете варьировать температуру, концентрацию NaOH и площадь поверхности нанопорошка.
""")

# Константы Аррениуса
A = 1e5  # 1/ч
Ea = 55000  # Дж/моль
R = 8.314  # Дж/(моль·К)
H2_max = 6.25  # % массы — теоретический максимум

# Модель реакции
def reaction_model(H2, t, T, NaOH_conc, surface_area):
    k = A * np.exp(-Ea / (R * T))
    rate = k * NaOH_conc * surface_area
    dH2dt = rate * (1 - H2 / H2_max)
    return dH2dt

# Симуляция
def simulate_hydrogen(T_C, NaOH_M, surface_cm2, duration_h=10):
    T_K = T_C + 273.15
    surface_area = surface_cm2 / 100.0
    t = np.linspace(0, duration_h, 300)
    H2 = odeint(reaction_model, 0, t, args=(T_K, NaOH_M, surface_area))
    return t, H2.flatten()

# --- Интерфейс пользователя ---
col1, col2 = st.columns(2)
with col1:
    T_C = st.slider("Температура (°C)", min_value=-20, max_value=100, value=25, step=1)
    NaOH_M = st.slider("Концентрация NaOH (моль/л)", min_value=0.01, max_value=2.0, value=0.5, step=0.01)
with col2:
    surface_cm2 = st.slider("Площадь поверхности (см²)", min_value=10, max_value=1000, value=200, step=10)
    duration = st.slider("Длительность симуляции (ч)", 1, 50, 10)

# --- Расчёт и график ---
t, H2 = simulate_hydrogen(T_C, NaOH_M, surface_cm2, duration)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, H2, label="Генерация H₂")
ax.set_xlabel("Время (ч)")
ax.set_ylabel("H₂ (% массы)")
ax.set_title("Кинетика выделения водорода")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# --- Итог ---
st.markdown(f"""
📈 **Максимум H₂:** {H2[-1]:.2f} % массы  
🌡️ **Температура:** {T_C} °C  
🧪 **NaOH:** {NaOH_M} M  
📐 **Площадь поверхности:** {surface_cm2} см²
""")
