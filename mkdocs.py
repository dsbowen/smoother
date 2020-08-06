from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

src_href = Github('https://github.com/dsbowen/smoother/blob/master')

path = 'smoother/__init__.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.rm_properties()
compile_md(soup, compiler='sklearn', outfile='docs_md/smoother.md')

path = 'smoother/utils.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.import_path = 'smoother'
compile_md(soup, compiler='sklearn', outfile='docs_md/utils.md')