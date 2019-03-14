#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de>
#
# Distributed under terms of the MIT license.

"""
A dependency tree representation.
"""

import enum
import pygraphviz as pgv

class BuildState(enum.Enum):
    PENDING = enum.auto()
    BUILDING = enum.auto()
    FAILED = enum.auto()
    SUCCEEDED = enum.auto()
    ABORTED = enum.auto()

class Tree:
    def __init__(self, pkgs):
        self.nodes = {}
        for pkg in pkgs:
            self.add_pkg(pkg)
        assert len(self.nodes) == len(pkgs), \
                'Unexpected number of nodes: {}, ' \
                'expected: {}'.format(len(self.nodes), len(pkgs))
        for node in self.nodes.values():
            assert node.is_initialized(), \
                    'Node {} was not properly initialized.'.format(node.name)
    def add_pkg_stub(self, pkg_name):
        """ Add a node that only contains the name to the tree.

        Returns:
            The newly created node if not yet in the tree or the tree node if
            already exists.
        """
        if pkg_name in self.nodes:
            return self.nodes[pkg_name]
        else:
            node = Node(pkg_name)
            self.nodes[pkg_name] = node
            return node

    def add_pkg(self, pkg):
        if not pkg.name in self.nodes:
            node = Node(pkg.name)
            node.pkg = pkg
            self.nodes[pkg.name] = node
        else:
            node = self.nodes[pkg.name]
        if not node.is_initialized():
            deps = []
            for dep in pkg.get_build_dependencies()['ros'] | \
                       pkg.get_run_dependencies()['ros']:
                deps.append(self.add_pkg_stub(dep))
            node.init_deps(deps)
            node.pkg = pkg

    def get_build_leaves(self):
        """Return all nodes that have no unbuilt dependencies."""
        leaves = []
        for node in self.nodes.values():
            if not node.state == BuildState.PENDING:
                continue
            is_leave = True
            for dep in node.dependencies:
                if not dep.state == BuildState.SUCCEEDED:
                    is_leave = False
            if is_leave:
                leaves.append(node)
        return leaves

    def is_built(self):
        """ Check if all packages have been built successfully. """
        for node in self.nodes.values():
            if node.state != BuildState.SUCCEEDED:
                return False
        return True
    def is_failed(self):
        """ Check if any build and therefore the build tree failed. """
        for node in self.nodes.values():
            if node.state == BuildState.FAILED:
                return True
        return False

    def to_dot(self):
        """ Generate a DOT representation of the tree.

        Returns:
            A pgv graph object.
        """
        graph = pgv.AGraph(directed=True)
        graph.node_attr['shape'] = 'rectangle'
        for node in self.nodes:
            graph.add_node(node)
        for node in self.nodes.values():
            for dep in node.dependencies:
                graph.add_edge(node.name, dep.name)
        return graph

    def draw_tree(self, output_file):
        graph = self.to_dot()
        graph.draw(output_file,prog='dot')

class Node:
    def __init__(self, name, pkg = None):
        """Fully initialize the note.

        Args:
            name: The package name, e.g., ros-kinetic-catkin
            pkg: The name of this package.
        """
        self.name = name
        self.state = BuildState.PENDING
        self.build_id = None
        self.initialized = False
        self.pkg = pkg
        self.dependencies = None
    def init_deps(self, deps):
        """ Initialize the dependencies of the node.

        This must happen in a separate step because the dependencies may not yet
        be in the tree during the creation of this object.

        Args:
            deps: A list of strings of package name this package depends on.
        """
        self.dependencies = deps
    def is_initialized(self):
        return self.pkg != None and self.dependencies != None
    def is_built(self):
        return self.built
