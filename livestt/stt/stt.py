from faster_whisper import WhisperModel
from typing import NamedTuple


class transcribe_return_type(NamedTuple):
    text: str
    language_probability: float
    language: str
    segment_end: float
    segment_start: float


def transcribe(
    input_file: str,
    language="en",
    model_name="tiny.en",
):
    """
    Transcribes the given file. Outputs the text with other information.

    :param str input_file: Filename of the audio input. Example: output.wav
    :param str language: Language of model
    :param str model_name: Model name. Can be tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large, distil-large-v2, distil-medium.en, distil-small.en
    """
    model = WhisperModel(model_name, device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        input_file, beam_size=5, language=language)

    for segment in segments:
        yield segment
        # return transcribe_return_type(segment.text, info.language_probability, info.language,
        # segment.end, segment.start)
    yield transcribe_return_type("", 0.0, "", 0.0, 0.0)


if __name__ == "__main__":
    text = transcribe("test.wav")
    for t in text:
        print(t)
