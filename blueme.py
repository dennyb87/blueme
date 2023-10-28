import os
import sys
from dataclasses import dataclass
from io import BufferedRandom
from typing import List

from pydub import AudioSegment


class CleanedTrack(BufferedRandom):
    @property
    def filename(self) -> str:
        return os.path.basename(self.name)


@dataclass
class BlueAndMe:
    dir_path: str
    format: str = "mp3"
    bitrate: str = "128k"

    @property
    def filenames(self) -> str:
        return os.listdir(self.dir_path)

    def cleaned_name(self, filnename: str) -> str:
        extenstion = ".mp3"
        title = filnename.strip(extenstion)
        alphanumeric_sliced = "".join(filter(str.isalnum, title))[:30]
        new_name = f"{alphanumeric_sliced}{extenstion}"
        return os.path.abspath(os.path.join(self.dir_path, new_name))

    def convert_dir(self) -> List[str]:
        out_names = []
        for filename in self.filenames:
            print(f"\nProcessing {filename}")
            cleaned_track = self.clean_track(filename)
            out_names.append(cleaned_track.filename)
            print(f"\nConverted to {cleaned_track.filename}")
        return out_names

    def clean_track(self, filename: str) -> CleanedTrack:
        path = os.path.abspath(os.path.join(self.dir_path, filename))
        track = AudioSegment.from_file(path, format=self.format)
        cleaned_track = track.export(
            self.cleaned_name(filename),
            format=self.format,
            bitrate=self.bitrate,
            tags={},
        )
        return CleanedTrack(cleaned_track)


if __name__ == "__main__":
    BlueAndMe(dir_path=sys.argv[1]).convert_dir()
