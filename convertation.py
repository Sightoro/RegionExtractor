import argparse
import os

parser = argparse.ArgumentParser(description='dbf file for DB')
parser.add_argument('indir', type=str, help='Input dir for videos')
args = parser.parse_args()
os.system("dbf-to-sqlite {} addresses_database.db".format(args.indir))
os.system("echo DB is created")
