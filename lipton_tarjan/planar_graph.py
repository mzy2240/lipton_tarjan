import numpy as np
from numba import jitclass
from numba.types import void, int32, float32
from .planar_graph_edges import PlanarGraphEdges, planar_graph_edges_nb_type


@jitclass([('_vertex_costs', float32[:]),
        ('_incident_edge_example_indices', int32[:]),
        ('_edges', planar_graph_edges_nb_type),
        ('_size', int32)])
class PlanarGraph:

    def __init__(self, vertex_costs, incident_edge_example_indices, edges):

        self._vertex_costs = vertex_costs
        self._incident_edge_example_indices = incident_edge_example_indices
        self._edges = edges
        self._size = len(self._vertex_costs)

    @property
    def vertex_costs(self):

        return self._vertex_costs

    @property
    def incident_edge_example_indices(self):

        return self._incident_edge_example_indices

    @property
    def edges(self):

        return self._edges

    @property
    def size(self):

        return self._size

    @property
    def edges_count(self):

        return self._edges.size

    def get_incident_edge_indices(self, vertex):

        if self._incident_edge_example_indices[vertex] == -1:
            return

        start_edge_index = self._incident_edge_example_indices[vertex]

        yield start_edge_index

        edge_index = self._edges.get_next_edge_index(start_edge_index, vertex)

        while edge_index != start_edge_index:

            yield edge_index

            edge_index = self._edges.get_next_edge_index(edge_index, vertex)

    def get_adjacent_vertices(self, vertex):

        for edge_index in self.get_incident_edge_indices(vertex):
            yield self._edges.get_opposite_vertex(edge_index, vertex)


planar_graph_nb_type = PlanarGraph.class_type.instance_type