import os
import ffmpeg
from utils import logging


class Transcoder:

    params = {
        'threads': 4,
        'c:v': 'libx264',
        'c:a': 'copy',
        'f': 'mp4',
        'b:v': '1M'
    }

    def __init__(self, file_path):
        self.inputPath = file_path
        self.outputPath = f"../completed/{os.path.basename(file_path)}"

    def transcode(self):

        ffInput = ffmpeg.input(self.inputPath)
        ffOutput = ffInput.output(
            self.outputPath,
            **Transcoder.params
        )
        ffOutput = ffOutput.global_args('-loglevel', 'error')

        try:
            logging.info(f"Transcoding video... (May take a few seconds)")
            ffOutput.run(overwrite_output=True)
            logging.info(
                f"Transcoding complete. Transcoded video is located at {self.outputPath}.")
        except Exception as e:
            logging.error(e.stderr)
