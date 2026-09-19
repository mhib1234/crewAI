"""Tests for crewai_files.core.sources."""
from __future__ import annotations

import tempfile

from crewai_files import FileStream


class TestFileStreamFilenameInference:
    def test_infers_filename_from_named_file(self, tmp_path):
        path = tmp_path / "report.txt"
        path.write_bytes(b"hello")
        with path.open("rb") as stream:
            assert FileStream(stream=stream).filename == "report.txt"

    def test_accepts_stream_whose_name_is_not_a_path(self):
        """open(fd) exposes an int .name; it must not be fed to Path()."""
        with tempfile.TemporaryFile() as original:
            original.write(b"A file supplied to an agent.")
            original.seek(0)
            with open(original.fileno(), "rb", closefd=False) as stream:
                source = FileStream(stream=stream)
                assert source.filename is None
                assert source.read() == b"A file supplied to an agent."

    def test_explicit_filename_wins_over_stream_name(self, tmp_path):
        path = tmp_path / "report.txt"
        path.write_bytes(b"hello")
        with path.open("rb") as stream:
            source = FileStream(stream=stream, filename="given.txt")
            assert source.filename == "given.txt"
