"""
Program: Lab14_Jigsa-1
Author: Jigsa
Purpose: Plot a spiral using matplotlib to visualize the polar coordinate relationship between radius and angle.
Date: 2025-08-02
"""

import numpy as np               # Numerical computations
import matplotlib.pyplot as plt # Plotting and visualization

# Generate data for the spiral
theta = np.linspace(0, 4 * np.pi, 100)     # Angle values
r = np.linspace(0, 300, 100)               # Radius values
x = r * np.cos(theta)                      # Convert to x-coordinates
y = r * np.sin(theta)                      # Convert to y-coordinates

# Plot the spiral
plt.figure()
plt.plot(x, y, color='blue')               # Spiral line in blue
plt.title('Spiral')                        # Title
plt.grid(True)                             # Add grid
plt.axis('equal')                          # Equal aspect ratio

# Display the plot
plt.show()

