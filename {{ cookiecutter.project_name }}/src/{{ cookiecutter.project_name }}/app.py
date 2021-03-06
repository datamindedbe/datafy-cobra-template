import argparse
import logging
import sys

from {{ cookiecutter.project_name }}.jobs import entrypoint
# this import is required to discover the jobs
# noinspection PyUnresolvedReferences
from {{ cookiecutter.project_name }}.jobs import sample, preprocessing, pig_tables, model_training, model_run


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(description="{{ cookiecutter.project_name }}")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=True
    )
    parser.add_argument(
        "-j",
        "--jobs",
        nargs="+",
        dest="jobs",
        help="jobs that need to be executed",
        required=True,
    )
    args = parser.parse_args()
    logging.info(f"Using args: {args}")

    for job_name in args.jobs:
        logging.info(f"Executing job {job_name}")
        job = entrypoint.all[job_name]
        job(args.env, args.date)


if __name__ == "__main__":
    main()

