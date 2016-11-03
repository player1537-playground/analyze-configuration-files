#!/usr/bin/env python

import ast

class NodeVisitorWithReturn(ast.NodeVisitor):
    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        val = None
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        val = self.visit(item)
            elif isinstance(value, ast.AST):
                val = self.visit(value)
        return val

class FindName(NodeVisitorWithReturn):
    def visit_Name(self, node):
        return node

class Printer(NodeVisitorWithReturn):
    def visit_Assign(self, assign):
        name_nodes = []
        for target in assign.targets:
            name_node = FindName().visit(target)
            name_nodes.append(name_node)

        value = None
        if isinstance(assign.value, ast.Str):
            value = assign.value

        if not name_nodes or value is None:
            return

        print('{} = {}'.format(
            ' = '.join('{.id}'.format(node) for node in name_nodes),
            '{.s}'.format(value),
        ))

def main(filename):
    with open(filename, 'rt') as f:
        source = f.read()

    tree = ast.parse(source, filename=filename)
    Printer().visit(tree)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
