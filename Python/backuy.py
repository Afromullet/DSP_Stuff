import numpy as np
import matplotlib.pyplot as plt

# Parameters
scan_rate = 1.0  # Rotations per second for the scan
beamwidth_degrees = 20.0  # Beamwidth in degrees
pri = 1.0  # Pulse Repetition Interval in seconds
duration = 5.0  # Duration of the signal in seconds

# Calculate scan angles over time
t = np.linspace(0, duration, 1000, endpoint=False)
scan_angles_degrees = 180 * scan_rate * t

# Calculate sinusoidal motion based on scan angles
sinusoidal_motion = np.sin(np.radians(scan_angles_degrees))

# Calculate the number of pulses per scan based on beamwidth and PRI
pulses_per_scan = int(360 / beamwidth_degrees)

# Create the pulse train
pulse_train = np.zeros_like(t)
pulse_train[:pulses_per_scan] = 1

# Superimpose sinusoidal motion on the pulse train
combined_signal = pulse_train * sinusoidal_motion

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, pulse_train, label='Pulse Train')
plt.title('Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, combined_signal, label='Combined Signal')
plt.title('Combined Signal with Sinusoidal Motion')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()




import numpy as np
import matplotlib.pyplot as plt

# Parameters for existing pulse train
pri = 1.0  # Pulse Repetition Interval in seconds
duration = 5.0  # Duration of the signal in seconds

# Generate the existing pulse train (square wave for demonstration)
t_existing = np.linspace(0, duration, 1000, endpoint=False)
existing_pulse_train = np.zeros_like(t_existing)
existing_pulse_train[::int(1/pri)] = 1  # Generate a simple square wave pulse train

# Parameters for scan
scan_rate = 1.0  # Rotations per second for the scan
beamwidth_degrees = 20.0  # Beamwidth in degrees

# Calculate scan angles over time
t_scan = np.linspace(0, duration, 1000, endpoint=False)
scan_angles_degrees = 180 * scan_rate * t_scan

# Calculate sinusoidal motion based on scan angles
sinusoidal_motion = np.sin(np.radians(scan_angles_degrees))

# Apply scanning effect to the existing pulse train by modulating amplitude
scanned_pulse_train = existing_pulse_train * sinusoidal_motion

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t_existing, existing_pulse_train, label='Existing Pulse Train')
plt.title('Existing Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_scan, scanned_pulse_train, label='Scanned Pulse Train')
plt.title('Scanned Pulse Train with Sinusoidal Motion')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Parameters for existing pulse train
pri = 1.0  # Pulse Repetition Interval in seconds
duration = 5.0  # Duration of the signal in seconds

# Generate the existing pulse train using signal.square
t_existing = np.linspace(0, duration, 1000, endpoint=False)
existing_pulse_train = square(2 * np.pi * (1 / pri) * t_existing)

# Parameters for scan
scan_rate = 1.0  # Rotations per second for the scan
beamwidth_degrees = 20.0  # Beamwidth in degrees

# Calculate scan angles over time
t_scan = np.linspace(0, duration, 1000, endpoint=False)
scan_angles_degrees = 180 * scan_rate * t_scan

# Calculate sinusoidal motion based on scan angles
sinusoidal_motion = np.sin(np.radians(scan_angles_degrees))

# Apply scanning effect to the existing pulse train by modulating amplitude
scanned_pulse_train = existing_pulse_train * sinusoidal_motion

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t_existing, existing_pulse_train, label='Existing Pulse Train')
plt.title('Existing Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_scan, scanned_pulse_train, label='Scanned Pulse Train')
plt.title('Scanned Pulse Train with Sinusoidal Motion')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()
