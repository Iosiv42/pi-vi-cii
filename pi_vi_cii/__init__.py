__all__ = [
    "main_cli",
]

import argparse


def main_cli() -> None:
    """ Main function for CLI pi-vi-cii tool. """

    from pi_vi_cii.play_ascii import play_ascii

    parser = argparse.ArgumentParser(
        prog='pi-vi-cii',
        description='Play video in terminal',
        epilog='Hope it help helps you'
    )

    parser.add_argument("path_to_video")
    args = parser.parse_args()
    play_ascii(args.path_to_video)
