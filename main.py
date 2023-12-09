import logging
import coloredlogs
from cmd import parse_and_run

coloredlogs.install(level='INFO', fmt='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Welcome to mario fuzz!")
    parse_and_run()


if __name__ == '__main__':
    main()
