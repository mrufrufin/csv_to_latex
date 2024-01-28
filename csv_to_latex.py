import csv
import argparse
import os
import re
from distutils.util import strtobool

FDIR = os.path.split(__file__)[0]
DEFOUTF = os.path.join(FDIR, "out.txt")
DEFINF = os.path.join(FDIR, "in.csv")
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--i", type=str, default=DEFINF, help="input file")
parser.add_argument("--vert", type=strtobool, default=True, help="vertical")
parser.add_argument("--entrypos", type=str, default="l", help="entry position (l,c,r)")
parser.add_argument("--center", type=strtobool, default=True, help="center table")
parser.add_argument("--capheader", type=strtobool, default=True, help="capitalize header")

args = parser.parse_args()

infile = args.i
fname = os.path.splitext(infile)[0]
outfile = fname + ".txt"
fname_p = re.sub(r'_', ' ', fname).title()
rstr = ""

header = []
res = {}
with open(infile, 'r', newline='') as csvr:
    rdr = csv.DictReader(csvr)
    for i,row in enumerate(rdr):
        if i == 0:
            header = list(row.keys())
            res = {k:[] for k in header}
        for k,v in row.items():
            res[k].append(v)

num_col = len(header)
num_rows = len(res[header[0]])
rstr += "\\begin{table}[ht]\n"
rstr += f"\\caption{{{fname_p}}}\n"
rstr += f"\\label{{{fname}}}\n"
if args.center == True:
    rstr += "\\centering\n"
rstr += "\\begin{tabular}{"
if args.vert == True:
    for _ in range(num_col):
        rstr += args.entrypos
else:
    rstr += args.entrypos
    rstr += args.entrypos
rstr += "}\n"
rstr += "\\toprule\n"
if args.vert == True:
    for i,h in enumerate(header):
        h_p = re.sub(r'_', ' ', h)
        if args.capheader == True:
            rstr += h_p.title()
        else:
            rstr += h_p
        if i != (num_col - 1):
            rstr += " & "
else:
    rstr += "Field & Value"
rstr += " \\\\\n"
rstr += "\\midrule\n"
if args.vert == True:
    for i in range(num_rows):
        for j in range(num_col):
            cur_col = header[j]
            cur_entry = re.sub(r'_', "\_", res[cur_col][i])
            rstr += f"{cur_entry} "
            if j == (num_col - 1):
                rstr += "\\\\ \n"
            else:
                rstr += " & "
        if i != (num_rows - 1):
            rstr += "\\midrule\n"
        else:
            rstr += "\\bottomrule\n"
else:
    for i in range(num_col):
        cur_col = header[i]
        cur_col_p = re.sub(r'_', '\_', cur_col)
        rstr += f"{cur_col_p} "
        for j in range(num_rows):
            cur_entry = re.sub(r'_', '\_', res[cur_col][j])
            rstr += f"& {cur_entry}"
        rstr += " \\\\ \n"
        if i == (num_col - 1):
            rstr += "\\bottomrule\n"
        else:
            rstr += "\\midrule\n"

rstr+= "\\end{tabular}\n"
rstr += "\\end{table}\n"

print(rstr)

with open(outfile, "w") as f:
    f.write(rstr)