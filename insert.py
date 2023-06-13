import re
import os
import shutil

def insert(s):
    diff = 0
    for m in re.finditer(r"\@\@\@INSERT_FILE_([A-Za-z0-9._]*)\@\@\@", s):
        with open(os.path.join("insert", m.group(1)), "r") as f:
            replace = f.read()
            s = s[:m.start(0)-diff] + replace + s[m.end(0)-diff:]
            diff += (m.end(0) - m.start(0)) - len(replace)
    return s

def formatfile(path):
    ret = os.system(f"tidy -quiet -indent --tidy-mark no -m {path}")
    if ret == 2 or ret < 0:
        raise Exception(f"bad return value from tidy ({ret})")

def gen_dir(i_dir, i_basedir, i_outdir):
    outdir = os.path.join(i_outdir, i_dir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fulldir = os.path.join(i_basedir, i_dir)

    for file in os.listdir(fulldir):
        infile = os.path.join(fulldir, file)
        outfile = os.path.join(outdir, file)
        if os.path.isdir(infile):
            gen_dir(os.path.join(i_dir, file), i_basedir, i_outdir)
        else:
            with open(infile, "r") as f:
                with open(outfile, "w") as fo:
                    fo.write(insert(f.read()))
                formatfile(outfile)

if os.path.exists("output"):
    shutil.rmtree("output")

shutil.copytree("files", "output")

gen_dir("", "gen", "output")
