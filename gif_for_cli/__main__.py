"""
Copyright 2018 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import hashlib
import json
import os
from os.path import expanduser
import sys

from . import __version__
from .constants import STORED_CELL_CHAR
from .display import display
from .generate import generate
from .generate.utils import process_input_source
from .utils import get_parser, get_output_dirnames


def execute(environ, argv, stdout):
    parser = get_parser(environ)

    args = parser.parse_args(argv)


    input_source = args.input_source

    input_source_file = process_input_source(input_source)


    home_dir = expanduser('~')

    m = hashlib.md5()
    m.update(input_source_file.encode('utf8'))
    input_source_hash = m.hexdigest()

    output_dirnames = get_output_dirnames(
        home_dir,
        __version__,
        input_source_hash,
        args.cols,
        args.cell_width,
        args.cell_height
    )

    if not os.path.exists(output_dirnames['.']):
        for output_dirname in output_dirnames.values():
            if not os.path.exists(output_dirname):
                os.makedirs(output_dirname)

        generate(
            stdout=stdout,
            input_source=input_source,
            input_source_file=input_source_file,
            cols=args.cols,
            cell_width=args.cell_width,
            cell_height=args.cell_height,
            output_dirnames=output_dirnames,
            cpu_pool_size=args.cpu_pool_size,
        )


    with open('{}/config.json'.format(output_dirnames['.']), 'r') as f:
        config = json.load(f)


    display(
        display_dirname=output_dirnames[args.display_mode],
        stdout=stdout,
        num_loops=args.num_loops,
        cell_char=args.cell_char,
        seconds_per_frame=config['seconds'] / config['num_frames']
    )


def main(): # pragma: no cover
    execute(os.environ, sys.argv[1:], sys.stdout)


if __name__ == '__main__': # pragma: no cover
    main()
