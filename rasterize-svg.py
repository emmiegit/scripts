#!/usr/bin/env python

import argparse
import subprocess

# ImageMagick deals with bitmaps first and foremost, so in order to convert a vector image
# to a bitmap, you need to first specify the canvas size before it does the initial SVG
# draw. Otherwise it will first write out the default canvas size and then blow it up
# like it was a JPEG.


def rasterize(input_file, output_file, size, other_arguments):
    arguments = [
        "magick",
        "-size",
        size,
        input_file,
        output_file,
    ]
    arguments.extend(other_arguments)
    subprocess.check_call(arguments)


def main():
    argparser = argparse.ArgumentParser(
        "rasterize-svg",
        "Helper utility to convert SVGs to raster formats",
    )
    argparser.add_argument(
        "size",
        help="The image dimensions of the output file to write",
    )
    argparser.add_argument(
        "input_file",
        help="The input SVG file to read",
    )
    argparser.add_argument(
        "output_file",
        help="Where to write the output file (specify extension)",
    )
    args, extra_args = argparser.parse_known_args()
    rasterize(args.input_file, args.output_file, args.size, extra_args)


if __name__ == "__main__":
    main()
