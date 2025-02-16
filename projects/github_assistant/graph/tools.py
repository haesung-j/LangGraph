import os
import nbformat
from langchain_core.tools import tool


def get_directory_tree_str(root_dir):
    directory_structure = "<directory_structure>\n"
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, "").count(os.sep)
        indent = " " * 4 * (level)
        directory_structure += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            directory_structure += f"{sub_indent}{f}\n"
    directory_structure += "</directory_structure>"
    return directory_structure


def get_cells(ipynb_filepath):
    # ipynb 파일 읽기
    with open(ipynb_filepath, "r", encoding="utf-8") as file:
        notebook = nbformat.read(file, as_version=4)

    # 코드셀과 마크다운 셀 구분
    cells = []
    for cell in notebook.cells:
        c = dict()
        c["type"] = cell.cell_type
        c["content"] = cell.source
        cells.append(c)
    return cells


def convert_notebook_to_md(output_cells):
    body = ""
    for cell in output_cells:
        if cell["type"] == "code":
            body += f"\n```python\n{cell['content']}\n```\n"
        elif cell["type"] == "markdown":
            body += f"\n{cell['content']}\n"

    # # 파일로 저장
    # with open(filename, "w", encoding="utf-8") as file:
    #     file.write(body)
    return body


def read_ipynb(notebook_path):
    cells = get_cells(notebook_path)
    # md_path = notebook_path.replace(".ipynb", ".md")
    result = convert_notebook_to_md(cells)
    return result


@tool
def get_directory_structure(root_dir: str) -> str:
    """Get the directory structure of the project. If you need to check the directory structure, use this tool."""
    return get_directory_tree_str(root_dir)


@tool
def get_file_contents(file_path: str) -> str:
    """Get the contents of a file. If you need to check the contents of each file, use this tool"""

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        # 파이썬 파일인 경우에만 코드 블록으로 감싸기
        if file_path.endswith((".py")):
            return f"```python\n{content}\n```"
        elif file_path.endswith((".ipynb")):
            return read_ipynb(file_path)
    return content
