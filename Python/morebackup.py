__________________________

Circular

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Parameters for existing pulse train
prf = 1000.0  # Pulse Repetition Frequency in Hz
duration = 5.0  # Duration of the signal in seconds

# Generate the existing pulse train using signal.square
t_existing = np.linspace(0, duration, int(duration * prf), endpoint=False)
existing_pulse_train = square(2 * np.pi * prf * t_existing)

# Parameters for circular scan
rotation_rate = 1.0  # Rotations per second for the scan
beamwidth_degrees = 20.0  # Beamwidth in degrees

# Calculate hits per scan based on beamwidth
pri = 1 / prf  # Calculate PRI from PRF
hits_per_scan = int(360 / beamwidth_degrees)  # Calculate hits per scan based on beamwidth

# Apply modulation using Amplitude Modulation with Sinusoidal Function
t = np.linspace(0, duration, len(existing_pulse_train), endpoint=False)
sinusoidal_motion = np.sin(2 * np.pi * rotation_rate * t)
modulated_pulse_train = existing_pulse_train * sinusoidal_motion

# Plotting
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t_existing, existing_pulse_train, label='Existing Pulse Train')
plt.title('Existing Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, sinusoidal_motion[:len(existing_pulse_train)], label='Circular Scan Motion')
plt.title('Circular Scan Motion')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, modulated_pulse_train, label='Modulated Pulse Train')
plt.title('Modulated Pulse Train with Circular Scan')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()

______________

Raster

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Parameters for existing pulse train
prf = 1000.0  # Pulse Repetition Frequency in Hz
duration = 5.0  # Duration of the signal in seconds

# Generate the existing pulse train using signal.square
t_existing = np.linspace(0, duration, int(duration * prf), endpoint=False)
existing_pulse_train = square(2 * np.pi * prf * t_existing)

# Parameters for raster scan
scan_rate = 1.0  # Sweeps per second for the scan (linear motion)
scan_extent = 10.0  # Extent of the scan in degrees

# Calculate the time it takes for one complete back-and-forth sweep (raster scan)
sweep_time = 1 / scan_rate

# Calculate the position of the sensor or beam at each time step
scan_positions = np.abs(t_existing % (2 * sweep_time) - sweep_time)

# Apply modulation using the scan positions
modulated_pulse_train = existing_pulse_train * scan_positions

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t_existing, existing_pulse_train, label='Existing Pulse Train')
plt.title('Existing Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_existing, modulated_pulse_train, label='Modulated Pulse Train with Raster Scan')
plt.title('Modulated Pulse Train with Raster Scan')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()

____________________ 

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Parameters for existing pulse train
prf = 1000.0  # Pulse Repetition Frequency in Hz
duration = 10.0  # Duration of the signal in seconds

# Generate the existing pulse train using signal.square
t_existing = np.linspace(0, duration, int(duration * prf), endpoint=False)
existing_pulse_train = square(2 * np.pi * prf * t_existing)

# Parameters for raster scan with dwell-and-switch
scan_rate = 1.0  # Sweeps per second for the scan (linear motion)
scan_extent = 10.0  # Extent of the scan in degrees
dwell_time = 0.5  # Duration of the dwell in seconds

# Calculate the time it takes for one complete back-and-forth sweep (raster scan)
sweep_time = 1 / scan_rate

# Calculate the position of the sensor or beam at each time step
scan_positions = np.abs(t_existing % (2 * sweep_time) - sweep_time)

# Add dwell time at the end of each sweep
dwell_mask = (t_existing % (2 * sweep_time) > sweep_time) & (t_existing % (2 * sweep_time) <= (sweep_time + dwell_time))
scan_positions[dwell_mask] = 0  # Dwell at the end of each sweep

# Apply modulation using the scan positions
modulated_pulse_train = existing_pulse_train * scan_positions

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t_existing, existing_pulse_train, label='Existing Pulse Train')
plt.title('Existing Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_existing, modulated_pulse_train, label='Modulated Pulse Train with Dwell-and-Switch')
plt.title('Modulated Pulse Train with Dwell-and-Switch')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()

__________________________

Conical 


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Parameters for existing pulse train
prf = 1000.0  # Pulse Repetition Frequency in Hz
duration = 10.0  # Duration of the signal in seconds

# Generate the existing pulse train using signal.square
t_existing = np.linspace(0, duration, int(duration * prf), endpoint=False)
existing_pulse_train = square(2 * np.pi * prf * t_existing)

# Parameters for conical scan
rotation_rate = 1.0  # Rotations per second for the conical scan
tilt_angle_degrees = 30.0  # Tilt angle of the cone in degrees

# Calculate the scan angles over time for the conical scan
scan_angles_degrees = 180 * rotation_rate * t_existing

# Calculate the sinusoidal motion to simulate the conical scan
sinusoidal_motion = np.sin(np.radians(scan_angles_degrees + tilt_angle_degrees))

# Apply modulation using the sinusoidal motion
modulated_pulse_train = existing_pulse_train * sinusoidal_motion

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t_existing, existing_pulse_train, label='Existing Pulse Train')
plt.title('Existing Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_existing, modulated_pulse_train, label='Modulated Pulse Train with Conical Scan')
plt.title('Modulated Pulse Train with Conical Scan')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()

______________

Ciruclar with hits per scan

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Parameters for existing pulse train
prf = 1000.0  # Pulse Repetition Frequency in Hz
duration = 5.0  # Duration of the signal in seconds

# Generate the existing pulse train using signal.square
t_existing = np.linspace(0, duration, int(duration * prf), endpoint=False)
existing_pulse_train = square(2 * np.pi * prf * t_existing)

# Parameters for circular scan
rotation_rate = 1.0  # Rotations per second for the scan
beamwidth_degrees = 20.0  # Beamwidth in degrees

# Calculate hits per scan based on beamwidth
pri = 1 / prf  # Calculate PRI from PRF
hits_per_scan = int(360 / beamwidth_degrees)  # Calculate hits per scan based on beamwidth

# Apply modulation using Amplitude Modulation with Sinusoidal Function
t = np.linspace(0, duration, len(existing_pulse_train), endpoint=False)
sinusoidal_motion = np.sin(2 * np.pi * rotation_rate * t)

# Adjust the modulation to control hits per scan
hits_indices = np.arange(0, len(existing_pulse_train), int(len(existing_pulse_train) / hits_per_scan))
modulation_indices = np.tile(hits_indices, hits_per_scan)[:len(existing_pulse_train)]
modulated_pulse_train = existing_pulse_train * sinusoidal_motion * (modulation_indices == np.arange(len(existing_pulse_train)))

# Plotting
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t_existing, existing_pulse_train, label='Existing Pulse Train')
plt.title('Existing Pulse Train')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, sinusoidal_motion[:len(existing_pulse_train)], label='Circular Scan Motion')
plt.title('Circular Scan Motion')
plt.xlabel('Time (seconds)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, modulated_pulse_train, label='Modulated Pulse Train')
plt.title('Modulated Pulse Train with Circular Scan and Hits Per Scan')
plt.xlabel('Time (seconds)')
plt.legend()

plt.tight_layout()
plt.show()