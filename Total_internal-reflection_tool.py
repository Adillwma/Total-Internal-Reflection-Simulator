
#%% - Dependencies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.widgets import Slider, Button, TextBox


import math

def calculate_reflection_refraction(θ1, n1, n2):
    if θ1 == 0:
        return 180, 0, 1

    else:
        # Calculate the angle of refraction (θ2) using Snell's Law
        sin_θ2 = (n1 / n2) * math.sin(math.radians(θ1))
        if -1 <= sin_θ2 <= 1:
            θ2 = math.degrees(math.asin(sin_θ2)) + 180
            if θ1 + θ2 != 0:
                reflection = (math.sin(math.radians(θ1 - θ2)) / math.sin(math.radians(θ1 + θ2)))**2
            else:
                reflection = 1
        else:
            # Handle the case when sin_θ2 is outside the valid range, e.g., set θ2 to a default value or raise an exception.
            # You may need to adjust this based on your specific requirements.
            θ2 = 0  # Just a placeholder value, the alpha value will be set to 0 so the line will not be visible 
            reflection = 1  # 100% reflection



        refraction = 1 - reflection  # Amount of light refracted

        return θ2, reflection, refraction



def init():
    global incident_beam, reflected_beam, refracted_beam, incident_glow, reflected_glow, refracted_glow # Declare incident_beam and laser_state_on as global variables
    incident_beam.set_data([], [])
    incident_glow.set_data([], [])
    reflected_beam.set_data([], [])
    refracted_beam.set_data([], [])
    reflected_glow.set_data([], [])
    refracted_glow.set_data([], [])


    return incident_beam, reflected_beam, refracted_beam, incident_glow, reflected_glow, refracted_glow,

def animate(i):
    global incident_beam, laser_state_on, reflected_beam, incident_glow, reflected_glow, refracted_glow, data_box_1, data_box_2  # Declare incident_beam and laser_state_on as global variables
    if laser_state_on:
        # add the data to the incident_beam object 
        incident_beam.set_data([0, np.deg2rad(incoming_angle)], [0, 1])
        incident_glow.set_data([0, np.deg2rad(incoming_angle)], [0, 1])
                
        refraction_angle, reflection_component, refraction_component = calculate_reflection_refraction(incoming_angle, refractive_index, n1)  # Careful to note that beam is coming from the material to the air so the ordering of the refractive indices is reversed
        reflected_beam.set_data([0, -np.deg2rad(incoming_angle)], [0, 1])
        reflected_glow.set_data([0, -np.deg2rad(incoming_angle)], [0, 1])
        reflected_glow.set_alpha(0.3 * reflection_component)
        reflected_beam.set_alpha(reflection_component)
        reflected_glow.set_linewidth(6 - (refraction_component * 2))
        refracted_beam.set_data([0, np.deg2rad(refraction_angle)], [0, 1])
        refracted_glow.set_data([0, np.deg2rad(refraction_angle)], [0, 1])
        refracted_beam.set_alpha(refraction_component)
        refracted_glow.set_alpha(0.3 * refraction_component)
        refracted_glow.set_linewidth(6 - (reflection_component * 2))

        data_box_1.set_text('Current Values\n\nAngle of Incidence: {:.2f}°\nRefractive Index: {:.2f}'.format(incoming_angle, refractive_index))

        if reflection_component > 0:    
            # round to 2dp
            reflection_angle = np.round(-incoming_angle, 2)
        else:
            reflection_angle = 'N/A'

        if refraction_component > 0:
            refraction_angle = np.round(refraction_angle, 2)
        else:
            refraction_angle = 'N/A'

        data_box_2.set_text(f'Current Values\n\nAngle of Refraction: {refraction_angle}°\nAngle of Reflection: {reflection_angle}°')



    else:
        incident_beam.set_data([], [])
        reflected_beam.set_data([], [])
        refracted_beam.set_data([], [])
        incident_glow.set_data([], [])
        reflected_glow.set_data([], [])
        refracted_glow.set_data([], [])
        data_box_1.set_text(f'Current Values\n\nAngle of Incidence: N/A°\nRefractive Index: {refractive_index}')
        data_box_2.set_text('Current Values\n\nAngle of Refraction: N/A°\nAngle of Reflection: N/A')

    return incident_beam, reflected_beam, refracted_beam, incident_glow, reflected_glow, refracted_glow,

def laser_on_off_switch(event):
    global laser_state_on  # Declare line and laser_state_on as global variables
    if button_on_off.label.get_text() == 'TURN LASER\nOFF':
        button_on_off.label.set_text('TURN LASER\nON')
        button_on_off.color = 'lightblue'
        laser_state_on = False
        print('Laser Turned OFF')
    else:
        button_on_off.label.set_text('TURN LASER\nOFF')
        laser_state_on = True
        button_on_off.color = 'red'
        print('Laser Turned ON')

def update_refractive_index(val):
    global refractive_index
    refractive_index = refractive_index_slider.val
    print('Refractive Index: ', refractive_index)

def update_incoming_angle(val):
    global incoming_angle
    incoming_angle = incoming_angle_slider.val
    print('Incoming Angle: ', incoming_angle)

            
initial_refractive_index = 1.5 # n
initial_incoming_angle = 0     # Degrees   #### ANGLE OF INCIDENCE!!!!
material_radius = 0.4  # Radius of the material
fps = 30  # Frames per second for the animation 

# Initial states
refractive_index = initial_refractive_index
incoming_angle = initial_incoming_angle
laser_state_on = False

n1 = 1.0  # Refractive index of the external medium (e.g., air)


### Compute ###
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 10))
# Rotate the 0 angle (e.g., 45 degrees counterclockwise)
ax.set_theta_offset(np.pi*1.5)  # Set the theta_offset property








# Set custom theta tick labels from 0 to -180 and 180 to 0
theta_labels = [0, 45, 90, 135, 180, -135, -90, -45]  # Custom labels
ax.set_xticklabels([str(label) + '°' for label in theta_labels])  # Add degree symbol

plt.subplots_adjust(bottom=0.3)  # Adjust the bottom margin to make space for sliders














# Create frequency slider
ax_refractive_index = plt.axes([0.2, 0.02, 0.65, 0.01])
refractive_index_slider = Slider(ax=ax_refractive_index, label='Material Refractive Index', valmin=1.0, valmax=4.0, valinit=initial_refractive_index, color='blue')
refractive_index_slider.on_changed(update_refractive_index)

# Create amplitude slider
ax_incoming_angle = plt.axes([0.2, 0.06, 0.65, 0.01])
incoming_angle_slider = Slider(ax=ax_incoming_angle, label='Incoming Angle (Deg)', valmin=-90.0, valmax=89.9999, valinit=initial_incoming_angle, color='blue')
incoming_angle_slider.on_changed(update_incoming_angle)

# Create buttons
ax_button_on_off = plt.axes([0.46, 0.17, 0.1, 0.05])
button_on_off = Button(ax_button_on_off, 'TURN LASER\nON', color='lightblue', hovercolor='0.975')
button_on_off.on_clicked(laser_on_off_switch)




### DRAW THE SIMICIRCLE OF TH EBOTTOM OF THE MATERIAL 
# Create angular values for half a circle (0 to 180 degrees)
theta = np.linspace(-np.pi/2, np.pi/2, 100)

# Corresponding radial values to form the circle
r = np.ones(100) * material_radius  # Set the radial value to 1 for the entire half-circle

ax.plot(theta, r, 'k', label='Material', alpha=0.5)  # Plot the half-circle

### DRAW THE FLAT LINE AT THE TOP OF THE MATERIAL 
# Define the starting and ending points of the line in polar coordinates
start_theta = np.deg2rad(90)  # Starting angle in radians
start_r = material_radius  # Starting radial value
end_theta = np.deg2rad(-90)  # Ending angle in radians
end_r = material_radius  # Ending radial value

# Plot the straight line
ax.plot([start_theta, end_theta], [start_r, end_r], 'k', alpha=0.5)  # Plot the half-circle





# Initialize lines
# Define the radial distance (r) and angle (theta) for the line
r_line = 0.7  # Radial distance
theta_line = np.deg2rad(0)  # Angle in radians

# Plot the line from the origin
incident_beam, = ax.plot([0, theta_line], [0, r_line], 'lime', label='Laser', lw=2) 
incident_glow, = ax.plot([0, theta_line], [0, r_line], 'limegreen', lw=6, alpha=0.3, label='Glow')

reflected_beam, = ax.plot([0, -theta_line], [0, r_line], 'lime', label='Reflected Beam', lw=2)  
reflected_glow, = ax.plot([0, -theta_line], [0, r_line], 'limegreen', lw=6, alpha=0.3, label='Glow')

refracted_beam, = ax.plot([0, 180-theta_line], [0, r_line], 'lime', label='Refracted Beam', lw=2)  
refracted_glow, = ax.plot([0, 180-theta_line], [0, r_line], 'limegreen', lw=6, alpha=0.3, label='Glow')




# Create a small outlined box on the figure to show the current values for angles and refractive index

# Create a rectangle in axes coords
left, width = -0.15, 0.3
bottom, height = -0.27, 0.15
right = left + width
top = bottom + height
data_box_1 = ax.text(right, top, 'Current Values\n\nAngle of Incidence: {:.2f}°\nRefractive Index: {:.2f}'.format(incoming_angle, refractive_index), horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))




# Create a rectangle in axes coords
left, width = 0.53, 0.3
right = left + width
top = bottom + height
data_box_2 = ax.text(right, top, 'Current Values\n\nAngle of Refraction: N/A°\nAngle of Reflection: N/A°', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))









# Setup plot
ax.set_rlim(0, 1)  # Set the radial limits
ax.set_yticklabels([])  # This removes the labels on the radial axis without removing the ticks themselves
title_y_position = 1.05  # Adjust this value to move the title up or down
ax.set_title('Total Internal Reflection (TIR) Visualizer', y=title_y_position)
#ax.legend(loc='upper right')
ax.grid(alpha=0.3)

# Add the title above the bottom two sliders
plt.figtext(0.5, 0.10, 'Settings', ha='center', fontsize=10, color='black')

# Run Animation and show or save it
anim = FuncAnimation(fig, animate, init_func=init, frames=None, interval=1/fps*1000, blit=True)   #interval *1000 to convert seconds to ms
plt.show()
