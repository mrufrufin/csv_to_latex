#!/usr/bin/env python
import csv
import argparse
import os
import re
from distutils.util import strtobool

num_matcher = re.compile(r"\-?((\d+)(\.\d*)?(e?\d+)?)")

def is_float(ipt):
    ret = False
    res = num_matcher.search(ipt)
    if res != None:
        startpos, endpos = res.span()
        if (endpos - startpos) == len(ipt):
            ret = True
    return ret



def format_poss_float(ipt, prec = -1):
    to_ff = False
    if prec >= 0:
        to_ff =True
    ret = ""
    cur_is_float = is_float(ipt)
    if cur_is_float == True and to_ff == True:
        ret = str(round(float(ipt), prec))
    else:
        ret = ipt
    return ret


FDIR = os.path.split(__file__)[0]
DEFOUTF = os.path.join(FDIR, "out.txt")
DEFINF = os.path.join(FDIR, "in.csv")
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--input", type=str, default=DEFINF, help="input file")
parser.add_argument("-v", "--vert", type=strtobool, default=True, help="vertical")
parser.add_argument("-s", "--save", type=strtobool, default=False, help="to save")
parser.add_argument("-st", "--subtable", type=strtobool, default=False, help="make as subtable")
parser.add_argument("-ep", "--entrypos", type=str, default="l", help="entry position (l,c,r)")
parser.add_argument("-c", "--center", type=strtobool, default=True, help="center table")
parser.add_argument("-ch", "--capheader", type=strtobool, default=True, help="capitalize header")
parser.add_argument("-f", "--precision", type=int, default=-1, help="float precision")

args = parser.parse_args()
tabwidth = 0.5
infile = args.input
fname = os.path.splitext(infile)[0]
outfile = fname + ".txt"
fname_p = re.sub(r'_', ' ', fname).title()
rstr = ""
prec = args.precision
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
if args.subtable == False:
    rstr += "\\begin{table}[ht]\n"
else:
    rstr += "\\begin{table*}[ht]\n"
    if args.center == True:
        rstr += "\\centering\n"
if args.subtable == True:
    rstr+= "\\captionsetup[subtable]{justification=centering,position = top}\n"
    rstr += "\\captionsetup[table]{position = top}\n"
rstr += f"\\caption{{{fname_p}}}\n"
rstr += f"\\label{{{fname}}}\n"
if args.subtable == True:
        rstr += f"\\begin{{subtable}}[t]{{ {tabwidth}\\textwidth }}\n"
        rstr += f"\\caption{{{fname_p}}}\n"
        rstr += f"\label{{{fname}}}\n"

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
            rstr += f"\\textbf{{{h_p.title()}}}"
        else:
            rstr += f"\\textbf{{{h_p}}}"
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
            #cur_entry2 = re.sub(r'%', "\%", cur_entry)
            cur_entry2 = format_poss_float(re.sub(r'%', '\%', cur_entry), prec=prec)
            rstr += f"{cur_entry2} "
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
            cur_entry2 = format_poss_float(re.sub(r'%', '\%', cur_entry), prec=prec)

            rstr += f"& {cur_entry2}"
        rstr += " \\\\ \n"
        if i == (num_col - 1):
            rstr += "\\bottomrule\n"
        else:
            rstr += "\\midrule\n"

rstr+= "\\end{tabular}\n"
if args.subtable == False:
    rstr += "\\end{table}\n"
else:
    rstr += "\\end{subtable}\n"
    rstr += "\\end{table*}\n"

print(f"\n{rstr}")

if args.save == True:
    with open(outfile, "w") as f:
        f.write(rstr)
