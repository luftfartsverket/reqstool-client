# Copyright © LFV

from dataclasses import dataclass
import os

from reqstool.locations.location import LocationInterface


@dataclass
class LocalLocation(LocationInterface):
    def _make_available_on_localdisk(self, dst_path: str):
        # dst_directory already exists but should a symlimk, remove
        os.rmdir(dst_path)

        src_path = os.path.abspath(self.path)

        dst_path_parent_directory, dst_path_last_segment = os.path.split(dst_path)

        dst_dir_fd = os.open(dst_path_parent_directory, os.O_RDONLY)

        symlink_name = str(dst_path_last_segment)  # Name of the symlink to be created
        os.symlink(src_path, symlink_name, dir_fd=dst_dir_fd, target_is_directory=True)

        os.close(dst_dir_fd)
