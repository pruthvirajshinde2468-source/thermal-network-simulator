# Power Semiconductor Thermal Network Simulator

A Python-based 1D Transient Thermal Resistance Network (Cauer Model) simulator wrapped in an interactive Streamlit web dashboard. 

This tool is designed to simulate the thermal dynamics of power semiconductors (such as SiC MOSFETs) during active power cycling, which is critical for understanding thermo-mechanical stress and reliability in power electronics packaging.

## 🚀 Features
* **Electrical-Thermal Analogy Simulation:** Accurately models heat transfer using numerical Euler integration.
* **Transient Analysis:** Simulates the wildly different thermal capacitances of the silicon junction, the package case, and the heatsink.
* **Interactive Dashboard:** Tweak power loss, ambient temperature, and thermal resistances in real-time to see how the temperature curves react.

## 🛠️ Installation & Usage

1. Clone the repository:
```bash
git clone <your-repository-url>
cd thermal-simulator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit Dashboard:
```bash
streamlit run app.py
```

## 📚 The Physics Behind It
In power electronics reliability testing, researchers turn a chip on and off repeatedly. Because the silicon chip (Junction) has very low thermal capacitance compared to its copper Case and aluminum Heatsink, it heats up almost instantly. This temperature difference ($\Delta T$) causes the materials to expand at different rates, leading to thermo-mechanical stress, bond-wire fatigue, and solder degradation.

This simulator allows you to input power loss and thermal impedances to predict the exact temperature delta between layers over time.
