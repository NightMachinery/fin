import numpy as np
from numpy import mean, sqrt, square, arange
from IPython import embed
import time

def monitor_audio(v1=None, v2=None, verbose=False):
    import traceback
    try:
        # print("WTF!")
        # import sounddevice
        # v1.value = 110
        print("WTF2")
        import sounddevice as sd # should not be imported before multiprocessing begins.
        # if q:
            # q.put(f"STARTING verbose={verbose}")
        print("WTF3")
        s_in = sd.InputStream()
        print("WTF4")
        # raise Exception("test exc")
        # print("WTF5")
        with s_in:
            print("in with")
            while True:
                # print("in while")
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
        print("loop ended")
        raise Exception("monitor_audio's loop has ended!")
    except:
        print("Exception from monitor_audio:")
        print(traceback.format_exc())

if __name__ == "__main__":
    from multiprocessing import Process, Queue, Value
    # q = Queue()
    vol_norm = Value('d', 980.0)
    vol_rms = Value('d', 980.0)
    p_audio_monitor = Process(target=monitor_audio, args=(vol_norm, vol_rms, True))
    p_audio_monitor.daemon = True
    p_audio_monitor.start()
    time.sleep(1)
    print(f"Current audio level: {vol_norm.value}   {vol_rms.value}")
    p_audio_monitor.join()
    print(f"Current audio level: {vol_norm.value}   {vol_rms.value}")
    exit()
    monitor_audio(verbose=True)
