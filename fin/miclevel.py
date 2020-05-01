import numpy as np
from numpy import mean, sqrt, square, arange
from IPython import embed

def monitor_audio(v1=None, v2=None, verbose=False):
    import sounddevice as sd # should not be imported before multiprocessing begins.
    # if q:
        # q.put(f"STARTING verbose={verbose}")
    s_in = sd.InputStream()
    with s_in:
        while True:
            inframes = s_in.read(100)
            indata = inframes[0][:,0] # the last zero means channel 0. We could simply use all the channels and rms would work over the flattened array.
            vol_norm = np.linalg.norm(indata)
            # embed()
            # exit()
            rms = sqrt(mean(square(indata)))
            # print(vol_norm)
            if verbose:
                print ("|" * int(vol_norm * 10))
                print ("*" * int(rms * 100))
            # if q:
                # q.put((vol_norm, rms))
            if v1:
                v1.value = vol_norm
            if v2:
                v2.value = rms

if __name__ == "__main__":
    monitor_audio(verbose=True)
