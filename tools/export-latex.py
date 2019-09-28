"""
Prepare notebooks for PDF export via LaTeX
"""
import distutils.dir_util
import glob
import os
import shutil
import subprocess

from latex import execute_and_clear, key, strip_latex

base_dir = os.path.abspath("..")
latex_dir = os.path.join("..", "tex")
source_dir = "../solutions/"
nb_files = glob.glob(os.path.join(source_dir, "*.ipynb"))
nb_files = sorted(nb_files, key=lambda v: key(v))

for nb_file in nb_files:
    print(f"Processing {nb_file}")
    nb = execute_and_clear(nb_file, source_dir)

    _, base = os.path.split(nb_file)
    out = os.path.abspath(os.path.join("..", base))
    base, _ = os.path.splitext(base)
    to_export = strip_latex(nb)
    if base == "installation":
        to_export = to_export.replace("\section{", "\section*{")
    with open(os.path.join(latex_dir, base + ".tex"), "w") as output:
        output.write(to_export)

distutils.dir_util.copy_tree(
    os.path.join(source_dir, "images"), os.path.join(latex_dir, "images")
)
cwd = os.path.abspath(latex_dir)
os.chdir(cwd)
tex_file = os.path.join(cwd, "python-introduction.tex")
subprocess.run(["pdflatex", tex_file], cwd=cwd)
subprocess.run(["pdflatex", tex_file], cwd=cwd)

print("Copying file to final location.")
pdf_file = tex_file.replace(".tex", ".pdf")
pdf_file_name = os.path.split(pdf_file)[1]
target = os.path.abspath(os.path.join("..", pdf_file_name))
print(pdf_file)
print(target)
shutil.copyfile(pdf_file, target)
