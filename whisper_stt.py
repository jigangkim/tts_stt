import argparse
import os
import torch
import whisper


OUTPUT_FORMAT = ["txt", "vtt", "srt", "tsv", "json", "all"][5]


def main(audio_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("small.en", device=device)
    writer = whisper.utils.get_writer(OUTPUT_FORMAT, ".")
    result = model.transcribe(audio_path)
    writer(result, audio_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='./audio.mp3')
    args = parser.parse_args()

    os.path.isfile(args.file)
    main(args.file)