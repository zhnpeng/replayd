# -*- encoding=utf-8 -*-
import sys
import argparse
from .manager import Manager
from .sink import Sinker
from .source import SchemaSourcer, SampleSourcer


parser = argparse.ArgumentParser(description="replayd cli parameters")
parser.add_argument(
    '--mode',
    "-m",
    dest="mode",
    required=True,
    choices=["sample", "schema"],
    help="mode [sample|schema]"
)
parser.add_argument(
    '--interval',
    "-t",
    dest="interval",
    type=float,
    default=0,
    help="optional play interval in s, default is 0 which means not interval"
)
parser.add_argument(
    '--loop',
    "-l",
    dest="loop",
    type=int,
    default=1,
    help="optional loop default is 1"
)
parser.add_argument(
    '--aware-datetime',
    "-a",
    dest="aware_datetime",
    default="",
    type=str,
    help="optional, if this argument is set, processing time will set to sample data using built-in formats"
)
parser.add_argument(
    '--datetime-format',
    "-d",
    dest="datetime_format",
    type=str,
    default="",
    help="optional, datetime format"
)
parser.add_argument(
    '--input',
    "-i",
    dest="input",
    help="input should be either a schema or sample filename, accroding to mode field"
)
parser.add_argument(
    '--output',
    "-o",
    dest="output",
    help="config filename in json format, which represent to output config"
)
parser.add_argument(
    '--encoding',
    "-e",
    dest="encoding",
    default="utf-8",
    help="output encoding"
)

def main():
    args = parser.parse_args(args=sys.argv[1:] or ["--help"])
    output_config = args.output
    sinker = Sinker()
    if output_config:
        sinker = Sinker(filename=output_config)
    if args.mode == "sample":
        if args.input is None:
            parser.print_help()
            return -1
        sourcer = SampleSourcer(args.input, interval=args.interval, aware_datetime=args.aware_datetime, datetime_format=args.datetime_format, encoding=args.encoding)
    elif args.mode == "schema":
        if args.input is None:
            parser.print_help()
            return -1
        sourcer = SchemaSourcer(args.input, interval=args.interval, encoding=args.encoding)
    else:
        parser.print_help()
        return -1
    manager = Manager(sourcer, sinker, loop=args.loop, interval=args.interval)
    manager.run()
