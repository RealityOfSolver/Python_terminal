import numpy as np
import asyncio
import math

# Configuration
screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.02
illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

A = 1.0
B = 1.0
R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))

def render_frame(A: float, B: float) -> np.ndarray:
    cos_A = np.cos(A)
    sin_A = np.sin(A)
    cos_B = np.cos(B)
    sin_B = np.sin(B)

    output = np.full((screen_size, screen_size), " ")
    zbuffer = np.zeros((screen_size, screen_size))

    phi = np.arange(0, 2 * np.pi, phi_spacing)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)
    
    theta = np.arange(0, 2 * np.pi, theta_spacing)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    circle_x = R2 + R1 * cos_theta
    circle_y = R1 * sin_theta

    x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T
    y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T
    z = ((K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T
    
    ooz = np.reciprocal(z)
    xp = (screen_size / 2 + K1 * ooz * x).astype(int)
    yp = (screen_size / 2 - K1 * ooz * y).astype(int)
    
    L1 = (((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta)) - sin_A * sin_theta)
    L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))
    L = np.around(((L1 + L2) * 8)).astype(int).T
    
    mask_L = L >= 0
    chars = illumination[np.clip(L, 0, 11)] # Prevents index errors

    for i in range(len(theta)):
        # Ensure we stay within screen bounds
        mask = (mask_L[i]) & (xp[i] >= 0) & (xp[i] < screen_size) & (yp[i] >= 0) & (yp[i] < screen_size)
        
        for j in range(len(phi)):
            if mask[j] and ooz[i, j] > zbuffer[xp[i, j], yp[i, j]]:
                zbuffer[xp[i, j], yp[i, j]] = ooz[i, j]
                output[xp[i, j], yp[i, j]] = chars[i, j]

    return output

async def animation_loop():
    global A, B
    while True:
        A += 0.1  # Rotation speed A
        B += 0.05 # Rotation speed B
        
        frame_array = render_frame(A, B)
        
        # Convert the numpy array into a single string for the terminal
        output_string = ""
        for row in frame_array:
            output_string += "".join(row) + "\n"
        
        # Clear the terminal effectively by overwriting
        print(output_string)
        
        # This is CRITICAL for iPad. It yields control back to the browser
        # so it can actually draw the text.
        await asyncio.sleep(0.01)

# Start the async process
asyncio.ensure_future(animation_loop())
