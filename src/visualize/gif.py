#region imports
import glob
from PIL import Image
#endregion

def save_gif(folder, name, dur=400, lp = 0):
    frames = [Image.open(image) for image in glob.glob(f"{folder}/*.png")]
    frame_one = frames[0]
    frame_one.save(f"{folder}{name}.gif", format="GIF", append_images=frames, save_all=True, duration=dur, loop=lp)