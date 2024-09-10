import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

R_s = 1085.619911     # Electrolyte resistance
R_ct = 2 * 38.84e6    # Charge transfer resistance
C_dl = 1.8422654e-10  # Double-layer capacitance
A_w = 20e6            # Warburg impedance coefficient

frequencies = np.logspace(6, -1, num=70)

# Mathematical Formalism
def impedance(f, R_s, R_ct, C_dl, A_w):
    Z_w = A_w / np.sqrt(1j * 2 * np.pi * f)   # Warburg impedance
    Z_series = R_ct + Z_w                     # Series combination of R_ct and Z_w
    Z_C = 1j * 2 * np.pi * f * C_dl           # Capacitor impedance
    Z_parallel = 1 / ((Z_series ** -1) + Z_C) # Parallel combination with capacitance
    Z_total = R_s + Z_parallel                # Series combination of R_s and parallel part
    return Z_total

real_values = []
imaginary_values = []
impedance_values = []
phase_values = []

for f in frequencies:
    Z = impedance(f, R_s, R_ct, C_dl, A_w)
    real_values.append(np.real(Z))
    imaginary_values.append(np.imag(Z))
    impedance_values.append(np.abs(Z))
    phase_values.append(np.angle(Z, deg=True))

f_1khz = 1000
Z_1khz = impedance(f_1khz, R_s, R_ct, C_dl, A_w)

print(f"Impedance at 1 kHz: {Z_1khz} Ohms, |Z| = {np.abs(Z_1khz)} Ohms, Phase = {np.angle(Z_1khz, deg=True)} degrees")

fig, ax1 = plt.subplots(figsize=(8, 6))
ax1.loglog(frequencies, np.array(impedance_values) * 1e-6, marker='o', color='blue')
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('|Z| (M$\Omega$)', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:.1f}'.format(y)))

ax2 = ax1.twinx()
ax2.semilogx(frequencies, phase_values, marker='+', color='green')
ax2.set_ylabel('Phase (degrees)', color='black')
ax2.tick_params(axis='y', labelcolor='black')

plt.title("Bode Plot")
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(np.array(real_values) * 1e-6, -np.array(imaginary_values) * 1e-6, marker='o')
plt.title("Nyquist Plot")
plt.xlabel("Z$_{Re}$ (M$\Omega$)")
plt.ylabel("-Z$_{Img}$ (M$\Omega$)")
plt.grid(True)
plt.show()
