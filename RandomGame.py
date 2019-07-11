import os
import sys
import time
import hashlib
import numpy as np
import scipy.ndimage
import tkinter as tk
from PIL import Image, ImageTk

def toImg(arr):
    arr = arr - arr.min()
    arr = arr / arr.max()
    arr = arr * 255
    arr = np.round(arr).astype("uint8")
    return ImageTk.PhotoImage(Image.fromarray(arr))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seed_str = sys.argv[1]
        print("Seed string:", seed_str)
        seed = np.array(int(hashlib.md5(seed_str.encode()).hexdigest()[16:], 16)).astype(np.uint32).item()
        print("Hashed seed:", seed)
        np.random.seed(seed)
    else:
        print("Using random seed")
    root = tk.Tk()
    root.title("RandomGame")
    canvas = tk.Canvas(root, width=512, height=512)
    canvas.pack()
    T = np.random.uniform(-1, 1, (4, 3, 3, 3))
    A = np.random.uniform(-1, 1, (4, 3, 3, 3))
    S = np.random.uniform(-1, 1, (256, 256, 3))
    actions = []
    def add_action(i):
        def f(e):
            if i not in actions:
                actions.append(i)
        return f
    def remove_action(i):
        def f(e):
            if i in actions:
                actions.remove(i)
        return f
    root.bind("<Up>", add_action(0))
    root.bind("<Down>", add_action(1))
    root.bind("<Left>", add_action(2))
    root.bind("<Right>", add_action(3))
    root.bind("<KeyRelease-Up>", remove_action(0))
    root.bind("<KeyRelease-Down>", remove_action(1))
    root.bind("<KeyRelease-Left>", remove_action(2))
    root.bind("<KeyRelease-Right>", remove_action(3))
    def update():
        global T
        global S
        global canvas
        global root
        while True:
            time.sleep(1/60)
            img = toImg(S)
            canvas.delete("all")
            canvas.create_image(256, 256, anchor="center", image=img)
            for i, t in enumerate(T):
                S = scipy.ndimage.filters.convolve(S, t, mode="constant")
                if i < len(T) - 1 or len(actions) > 0:
                    np.maximum(S, 0, S)
            for i, a in enumerate(actions):
                S = scipy.ndimage.filters.convolve(S, A[a], mode="constant")
                if i < len(actions) - 1:
                    np.maximum(S, 0, S)
            S = np.tanh(S)
            root.update()
    root.after(0, update)
    os.system('xset r off')
    root.mainloop()
    os.system('xset r on')

