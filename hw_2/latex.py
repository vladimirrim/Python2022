from astgen.ast_builder import draw_ast


def indent_text(text, indent):
    return '\t' * indent + text


def draw_column_str(n_cols):
    return " ".join('l' * n_cols)


def draw_tabular_str(col_str):
    return "\\begin{tabular}{" + col_str + "}\n"


def draw_table_str():
    return "\\begin{table}\n" + indent_text("\\begin{center}\n", 1)


def draw_doc_start():
    return "\\documentclass[pmlr]{jmlr}\n\\begin{document}\n"


def draw_doc_end():
    return "\\end{document}"


def draw_latex_start(content):
    return draw_doc_start() + draw_table_str() + indent_text(draw_tabular_str(draw_column_str(len(content))), 2)


def draw_latex_content(content):
    return "".join(map(lambda row: indent_text(" & ".join(row) + " \\\\\n", 3), content))


def draw_table_end():
    return indent_text("\\end{tabular}\n", 2) + indent_text("\\end{center}\n", 1) + "\\end{table}\n"


def draw_image(path):
    return "\\begin{figure}[h]\n" + "\\includegraphics[width=0.6\\linewidth]{" + path + "}\n\\end{figure}\n"


if __name__ == "__main__":
    input_matrix = [['1', '2', '3'],
                    ['4', '5', '6'],
                    ['7', '8', '9']]

    draw_ast()

    with open('artifacts/file.tex', 'w') as f:
        f.write(draw_latex_start(input_matrix) +
                draw_latex_content(input_matrix) +
                draw_table_end() +
                draw_image('artifacts/ast.png') +
                draw_doc_end())
