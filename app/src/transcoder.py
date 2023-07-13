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
        inputPath = file_path
        outputPath = f"../completed/{os.path.basename(file_path)}"

        ffInput = ffmpeg.input(inputPath)
        ffOutput = ffInput.output(
            outputPath,
            **Transcoder.params
        )
        ffOutput = ffOutput.global_args('-loglevel', 'error')

        try:
            logging.info(f"Transcoding video...")
            ffOutput.run(overwrite_output=True)
            logging.info(
                f"Transcoding complete. Transcoded video is located at {outputPath}.")
            # return valuable info that can be used in post_process_video
        except Exception as e:
            logging.error(e.stderr)
