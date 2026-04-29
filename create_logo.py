import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 20

x = np.linspace(0, 1, n)

# gradient
prob = 0.75 - 0.4 * x

# biased noise
noise = 0.05 * np.random.randn(n) + 0.08
prob = prob + noise

prob = np.clip(prob, 0.4, 0.95)

grid = np.random.rand(n, n) < prob

# -----------------------
# create RGBA image
# -----------------------
blue = np.array([57/255, 103/255, 229/255, 1.0])  # #3967E5
transparent = np.array([0, 0, 0, 0])

rgba = np.zeros((n, n, 4))

for i in range(n):
    for j in range(n):
        rgba[i, j] = blue if grid[i, j] else transparent

# -----------------------
# plot
# -----------------------
fig, ax = plt.subplots(figsize=(4, 4))
ax.imshow(rgba)
ax.axis("off")

# -----------------------
# save
# -----------------------
plt.savefig("assets/images/mathcodelab_logo.png", dpi=300, bbox_inches="tight", pad_inches=0, transparent=True)
plt.savefig("assets/images/mathcodelab_logo.svg", bbox_inches="tight", pad_inches=0, transparent=True)

# plt.show()