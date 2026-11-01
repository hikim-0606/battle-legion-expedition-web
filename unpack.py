"""Verify compiled game parts, then extract only approved static files."""
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
ALLOWED_FILES = {'index.service.worker.js', 'index.html', 'index.js', 'index.png', 'index.pck', 'index.icon.png', 'index.180x180.png', 'index.wasm', 'index.audio.position.worklet.js', 'index.apple-touch-icon.png', 'index.manifest.json', 'index.offline.html', 'index.audio.worklet.js', 'index.512x512.png', 'index.144x144.png'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    manifest = json.loads((ROOT / "artifact-manifest.json").read_text(encoding="utf-8"))
    if set(manifest["allowed_files"]) != ALLOWED_FILES:
        raise ValueError("Unexpected manifest file allowlist")
    assembled = bytearray()
    part_names = set()
    for number, part in enumerate(manifest["parts"], 1):
        expected = f"battle-legion-web-v0.6.8.zip.{number:03d}.part"
        if part["name"] != expected or expected in part_names:
            raise ValueError("Unsafe or unordered part name")
        part_names.add(expected)
        data = (ROOT / expected).read_bytes()
        if len(data) != part["bytes"] or len(data) > 20 * 1024 * 1024 or sha(data) != part["sha256"]:
            raise ValueError("Part integrity check failed: " + expected)
        assembled.extend(data)
    if len(assembled) != manifest["archive_bytes"] or sha(assembled) != manifest["archive_sha256"]:
        raise ValueError("Archive integrity check failed")
    with zipfile.ZipFile(io.BytesIO(assembled)) as archive:
        infos = archive.infolist()
        names = [entry.filename for entry in infos]
        if len(names) != len(set(names)) or set(names) != ALLOWED_FILES:
            raise ValueError("ZIP entry allowlist mismatch")
        # Verify every payload before creating public/. Flat names prevent traversal.
        payloads = {}
        for entry in infos:
            name = entry.filename
            if entry.is_dir() or "/" in name or "\\" in name or name in {".", ".."} or entry.flag_bits & 1:
                raise ValueError("Unsafe ZIP entry")
            expected = manifest["files"][name]
            if entry.file_size != expected["bytes"] or entry.file_size > 128 * 1024 * 1024:
                raise ValueError("Unexpected expanded file size")
            data = archive.read(entry)
            if sha(data) != expected["sha256"]:
                raise ValueError("Output integrity check failed: " + name)
            payloads[name] = data
    output = ROOT / "public"
    if output.exists() and (output.is_symlink() or not output.is_dir() or any(output.iterdir())):
        raise ValueError("public/ must be absent or empty; existing content is preserved")
    output.mkdir(exist_ok=True)
    for name, data in payloads.items():
        (output / name).write_bytes(data)
    print(json.dumps({"verified": True, "files": len(payloads), "archive_sha256": manifest["archive_sha256"]}))

if __name__ == "__main__":
    main()
