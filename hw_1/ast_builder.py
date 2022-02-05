import ast
import matplotlib
import matplotlib.cm
import pydot

from zlib import crc32


class AstVisitor(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.graph = pydot.Dot(graph_type='graph', strict=True)
        self.id = 0
        self.cmap = matplotlib.cm.get_cmap('Spectral')

    def generic_visit(self, node):
        if not self.filter(node):
            return

        node_id = self.id
        self.id += 1
        parent_id = self.stack[-1] if self.stack else None
        if parent_id:
            self.graph.add_edge(pydot.Edge(parent_id, node_id))

        self.graph.add_node(pydot.Node(node_id, label=self.get_label(node), style="filled",
                                       fillcolor=self.get_color(node)))

        self.stack.append(node_id)
        super(self.__class__, self).generic_visit(node)
        self.stack.pop()

    def filter(self, node):
        return type(node) not in [ast.Load, ast.Store]

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def get_color(self, node):
        text = node.__class__.__name__
        return self.rgb_to_hex(self.cmap(float(crc32(text.encode()) & 0xffffffff) / 2**32, bytes=True)[:-1])

    def get_label(self, node):
        if isinstance(node, (ast.Sub, ast.USub)):
            return "-"
        elif isinstance(node, ast.Add):
            return "+"
        elif isinstance(node, ast.FunctionDef):
            return f"def: {node.name}"
        elif isinstance(node, ast.Assign):
            return "="
        elif isinstance(node, ast.Name):
            return f"{node.id}"
        elif isinstance(node, ast.arg):
            return f"{node.arg}"
        elif isinstance(node, ast.Constant):
            return f"{node.value}"
        else:
            return node.__class__.__name__


def build_ast(filename, output):
    with open(filename, 'r') as f:
        src = f.read()
    root = ast.parse(src)
    visitor = AstVisitor()
    visitor.visit(root)
    visitor.graph.write_png(output)


if __name__ == '__main__':
    build_ast('fibo.py', "artifacts/ast.png")
