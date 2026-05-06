import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Power Semiconductor Thermal Simulator", layout="wide")

st.title("⚡ Power Semiconductor Thermal Network Simulator")
st.markdown("""
This dashboard simulates the **1D Transient Thermal Resistance Network (Cauer Model)** of a power semiconductor (like a SiC MOSFET). 
It models heat transfer using the **Electrical-Thermal Analogy**, where Power = Current, Temperature = Voltage, and Thermal Resistance = Electrical Resistance.
""")

# Sidebar for inputs
st.sidebar.header("Simulation Parameters")

# Operating Conditions
st.sidebar.subheader("Operating Conditions")
P_loss = st.sidebar.slider("Power Loss (Watts)", min_value=1.0, max_value=200.0, value=50.0, step=1.0)
T_ambient = st.sidebar.slider("Ambient Temperature (°C)", min_value=-20.0, max_value=85.0, value=25.0, step=1.0)

# Thermal Resistances
st.sidebar.subheader("Thermal Resistances (Rth) - °C/W")
st.sidebar.caption("Higher value = Harder for heat to escape")
Rth_jc = st.sidebar.slider("Junction-to-Case", 0.1, 2.0, 0.5, 0.1)
Rth_ch = st.sidebar.slider("Case-to-Heatsink (TIM)", 0.05, 1.0, 0.2, 0.05)
Rth_ha = st.sidebar.slider("Heatsink-to-Ambient", 0.5, 10.0, 2.0, 0.1)

# Thermal Capacitances
st.sidebar.subheader("Thermal Capacitances (Cth) - J/K")
st.sidebar.caption("Higher value = Takes longer to heat up")
Cth_j = st.sidebar.number_input("Junction Capacitance", value=0.01, format="%.3f")
Cth_c = st.sidebar.number_input("Case Capacitance", value=1.0, format="%.2f")
Cth_h = st.sidebar.number_input("Heatsink Capacitance", value=15.0, format="%.1f")

# Simulation Settings
st.sidebar.subheader("Time Settings")
t_end = st.sidebar.slider("Simulation Time (seconds)", 1, 100, 20)

# --- RUN SIMULATION ---
@st.cache_data
def run_simulation(P_loss, T_ambient, Rth_jc, Rth_ch, Rth_ha, Cth_j, Cth_c, Cth_h, t_end):
    dt = 0.001 # 1 millisecond time step
    time = np.arange(0, t_end, dt)
    
    # Initialize temperatures at ambient
    T_j, T_c, T_h = T_ambient, T_ambient, T_ambient
    
    # Arrays to store history
    T_j_hist = np.zeros(len(time))
    T_c_hist = np.zeros(len(time))
    T_h_hist = np.zeros(len(time))
    
    for i in range(len(time)):
        # Heat Flow (Current)
        Q_jc = (T_j - T_c) / Rth_jc
        Q_ch = (T_c - T_h) / Rth_ch
        Q_ha = (T_h - T_ambient) / Rth_ha
        
        # Temp Change (Voltage Change)
        dT_j = (P_loss - Q_jc) * dt / Cth_j
        dT_c = (Q_jc - Q_ch) * dt / Cth_c
        dT_h = (Q_ch - Q_ha) * dt / Cth_h
        
        # Update current temps
        T_j += dT_j
        T_c += dT_c
        T_h += dT_h
        
        # Save to history
        T_j_hist[i] = T_j
        T_c_hist[i] = T_c
        T_h_hist[i] = T_h
        
    return time, T_j_hist, T_c_hist, T_h_hist

# Execute simulation
time, T_j_hist, T_c_hist, T_h_hist = run_simulation(
    P_loss, T_ambient, Rth_jc, Rth_ch, Rth_ha, Cth_j, Cth_c, Cth_h, t_end
)

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time, T_j_hist, label='Junction (Silicon Chip)', color='#d62728', linewidth=2)
ax.plot(time, T_c_hist, label='Case (Package Base)', color='#ff7f0e', linewidth=2)
ax.plot(time, T_h_hist, label='Heatsink', color='#1f77b4', linewidth=2)
ax.axhline(y=T_ambient, color='gray', linestyle='--', label='Ambient Air')

# Add warning line if Junction Temp exceeds typical limits (e.g., 175 C for SiC)
ax.axhline(y=175.0, color='red', linestyle=':', label='Max Tj (175°C) Limit')

ax.set_title('Transient Thermal Simulation', fontsize=16)
ax.set_xlabel('Time (seconds)', fontsize=12)
ax.set_ylabel('Temperature (°C)', fontsize=12)

# Place legend outside plot
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax.grid(True, alpha=0.3)

# --- DISPLAY ON DASHBOARD ---
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("Final State")
    
    # Calculate margin to 175C limit
    margin = 175.0 - T_j_hist[-1]
    delta_str = f"{margin:.1f} °C margin" if margin >= 0 else f"{abs(margin):.1f} °C over limit!"
    
    st.metric("Junction Temp", f"{T_j_hist[-1]:.1f} °C", delta=delta_str, delta_color="normal" if margin >= 0 else "inverse")
    st.metric("Case Temp", f"{T_c_hist[-1]:.1f} °C")
    st.metric("Heatsink Temp", f"{T_h_hist[-1]:.1f} °C")

st.markdown("---")
st.markdown("""
### 🎓 Why this matters for Power Electronics:
During active power cycling (a common test at IALB), researchers turn a chip on and off repeatedly to see when it breaks. 
The stress is caused by the **Junction (Chip)** heating up much faster than the **Case (Package)** or **Heatsink** due to its tiny thermal capacitance. 
This temperature difference causes mechanical stress (warping) which eventually destroys the chip. This simulator lets you visualize exactly how those temperatures diverge under different power loads!
""")
