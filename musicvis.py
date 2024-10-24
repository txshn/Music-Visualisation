import numpy as np
import pygame
import librosa
import time

# Initialize pygame
pygame.init()

# Load the music
audio_file = 'minecraft noise.mp3'
y, sr = librosa.load(audio_file, sr=None)
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

# Set up display
screen = pygame.display.set_mode((1200, 600))  # Updated screen size
background = pygame.image.load('cyber.jpg')  # Load your background image

# Color definitions
wave_color = (0, 255, 255)  # Wave color
start_color = (255, 255, 255)  # Initial white color
end_color = (255, 100, 100)  # Gradually transition to soft red

# Function to interpolate between two colors
def interpolate_color(color1, color2, factor):
    return tuple([int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3)])

# Run the visualizer
running = True
start_time = time.time()
wave_radius = 100  # Starting radius for the wave
color_transition_speed = 0.01  # Controls how fast the color changes
color_factor = 0  # Start with the initial color

while running:
    screen.blit(background, (0, 0))  # Display background

    # Get current position in the song
    song_pos = time.time() - start_time
    current_frame = int(song_pos * sr)

    # Visualizer settings
    amplitude = np.mean(np.abs(y[current_frame:current_frame + 1024]))  # Get amplitude
    circle_radius = 200 + int(50 * amplitude)  # Change solid circle size with amplitude

    # Update wave radius to create moving effect
    wave_radius += 5
    if wave_radius > 600:  # Reset when wave goes off screen
        wave_radius = circle_radius + 50

    # Draw the wave behind the circle
    pygame.draw.circle(screen, wave_color, (600, 300), wave_radius, 5)  # A "wave" with width 5

    # Gradually transition the color inside the circle
    color_factor = (color_factor + color_transition_speed) % 1  # Keeps the factor between 0 and 1
    current_color = interpolate_color(start_color, end_color, color_factor)

    # Draw dynamic color effect inside the circle with smooth transition
    for r in range(circle_radius, 0, -10):  # Draw concentric circles with decreasing radius
        pygame.draw.circle(screen, current_color, (600, 300), r)

    # Remove the black outline (no extra drawing here)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    pygame.time.wait(20)  # Delay for smoother animation

pygame.quit()
