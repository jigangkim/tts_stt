#!/usr/bin/env python
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All Rights Reserved.

"""Adapted from Google Cloud Text-To-Speech API sample application."""

import argparse
import glob
import os


VOICENAME = ["en-US-Neural2-J", "en-US-Studio-M"][0]
ENCODING_SEL = 2 # 2: MP3, 3: OGG_OPUS
RATE = 1.0
PITCH = 0.0
GAIN = 0.0


def synthesize_text_file(text_file):
    """Synthesizes speech from the input file of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    with open(text_file, "r") as f:
        text = f.read()
        input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=VOICENAME,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding(ENCODING_SEL),
        speaking_rate=RATE,
        pitch=PITCH,
        volume_gain_db=GAIN,
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    name = os.path.basename(text_file).split('.')[0]
    ext = ['mp3', 'ogg'][ENCODING_SEL-2]
    # The response's audio_content is binary.
    with open(f"{name}.{ext}", "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{name}.{ext}"')


def synthesize_ssml_file(ssml_file):
    """Synthesizes speech from the input file of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    with open(ssml_file, "r") as f:
        ssml = f.read()
        input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=VOICENAME,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding(ENCODING_SEL),
        speaking_rate=RATE,
        pitch=PITCH,
        volume_gain_db=GAIN,
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    name = os.path.basename(ssml_file).split('.')[0]
    ext = ['mp3', 'ogg'][ENCODING_SEL-2]
    # The response's audio_content is binary.
    with open(f"{name}.{ext}", "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{name}.{ext}"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./')
    parser.add_argument('--file_ext', type=str, default='.txt')
    args = parser.parse_args()

    list_of_scripts = [os.path.abspath(match) for match in sorted(glob.glob(args.file_path + '/*%s'%(args.file_ext)))]
    if len(list_of_scripts) == 0:
        print('No files found in %s'%(args.file_path))
        exit(1)
    else:
        if args.file_ext == '.txt':
            for script in list_of_scripts:
                synthesize_text_file(script)
        elif args.file_ext == '.ssml':
            for script in list_of_scripts:
                synthesize_ssml_file(script)
        else:
            raise ValueError('File extension %s not supported'%(args.file_ext))
    