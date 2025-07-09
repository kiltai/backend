import numpy as np
import soundfile as sf
import io

def tts_audio_bytes(text):
    from TTS.api import TTS
    import numpy as np
    import soundfile as sf
    import io

    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    wav = tts.tts(text)
    buf = io.BytesIO()
    sf.write(buf, wav, 22050, format='WAV')
    return buf.getvalue() 