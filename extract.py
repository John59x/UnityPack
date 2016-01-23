#!/usr/bin/env python
import os
import sys
import unitypack
from PIL import ImageOps


SUPPORTED_FORMATS = (
	"AudioClip",
	"Shader",
	"TextAsset",
	"Texture2D",
)


def write_to_file(filename, contents, mode="w"):
	basedir = "out"

	if not os.path.exists(basedir):
		os.makedirs(basedir)

	path = os.path.join(basedir, filename)
	with open(path, mode) as f:
		written = f.write(contents)

	print("Written %i bytes to %r" % (written, path))


def handle_asset(asset):
	print(asset)
	for id, obj in asset.objects.items():
		if obj.type not in SUPPORTED_FORMATS:
			print("Skipping %r" % (obj))
			continue

		d = obj.read()

		if obj.type == "AudioClip":
			write_to_file(d.name + ".fsb", d.data, mode="wb")

		elif obj.type == "Shader":
			write_to_file(d.name + ".cg", d.script)

		elif obj.type == "TextAsset":
			write_to_file(d.name + ".txt", d.script)

		elif obj.type == "Texture2D":
			print("Decoding %r" % (d))
			img = ImageOps.flip(d.image)
			img.save("out/%s.png" % (d.name))


def main():
	files = sys.argv[1:]
	for file in files:
		if file.endswith(".assets"):
			with open(file, "rb") as f:
				asset = unitypack.Asset.from_file(f)
			handle_asset(asset)
			continue

		with open(file, "rb") as f:
			bundle = unitypack.load(f)

		for asset in bundle.assets:
			handle_asset(asset)


if __name__ == "__main__":
	main()
