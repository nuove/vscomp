import vapoursynth as vs
from vapoursynth import core
from awsmfunc import FrameInfo
from vspreview import set_output
import random

clip1 = core.lsmas.LWLibavSource(r"<path>")
clip2 = core.lsmas.LWLibavSource(r"<path>")
grp1 = "Placeholder1"
grp2 = "Placeholder2"

clip2 = core.std.AssumeFPS(clip2, fpsnum=24000, fpsden=1001) # change the fps of clip2 to a constant frame rate
matched_clip = core.vivtc.VFM(clip2, 1)
decimated_clip = core.vivtc.VDecimate(matched_clip)

clip1 = core.std.Trim(clip1, first=random.randint(0, clip1.num_frames - 11), last=random.randint(11, clip1.num_frames - 1)) # trim the clip randomly
decimated_clip = core.std.Trim(decimated_clip, first=random.randint(0, decimated_clip.num_frames - 11), last=random.randint(11, decimated_clip.num_frames - 1)) # trim the clip randomly

# making sure sure the clips have the same number of frames and fps
if clip1.num_frames > decimated_clip.num_frames:
    clip1 = core.std.Trim(clip1, last=decimated_clip.num_frames - 1)
elif clip1.num_frames < decimated_clip.num_frames:
    decimated_clip = core.std.Trim(decimated_clip, last=clip1.num_frames - 1)

clip2 = core.std.AssumeFPS(clip2, fpsnum=clip1.fps_num, fpsden=clip1.fps_den) # change the fps of clip2 to match clip1

#Displays the frame number, type and fps
clip1 = FrameInfo(clip1, grp1)
decimated_clip = FrameInfo(decimated_clip, grp2)

#Slow.pics labelling
clip1 = core.std.SetFrameProp(clip1, prop='Name', data=grp1)
decimated_clip = core.std.SetFrameProp(decimated_clip, prop='Name', data=grp2)

set_output(clip1, name=grp1)
set_output(decimated_clip, name=grp2)