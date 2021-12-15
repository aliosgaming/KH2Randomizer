
from Class.newLocationClass import KH2Location
from List.configDict import locationCategory, locationDepth
from List.NewLocationList import Locations

class ItemDepths():
    def __init__(self, location_depth: locationDepth, locations:Locations):
        location_graph = locations.location_graph
        self.depth_classification = {}
        self.very_restricted_locations = location_depth in [locationDepth.FirstBoss,locationDepth.SecondBoss,locationDepth.DataFight]

        # first boss - default to no, enable the first bosses
        # first visit - default to no, enable before and including first boss
        # second boss - default to no, enable second boss check
        # second visit - default to yes, disable datas
        # datas - default to no, set datas to yes
        # anywhere, set all to yes
        if location_depth in [locationDepth.FirstBoss,locationDepth.FirstVisit,locationDepth.SecondBoss,locationDepth.DataFight]:
            for l in locations.getAllSoraLocations():
                self.depth_classification[l] = False
        else:
            for l in locations.getAllSoraLocations():
                self.depth_classification[l] = True

        first_boss_nodes = locations.first_boss_nodes
        second_boss_nodes = locations.second_boss_nodes
        data_nodes = locations.data_nodes

        if location_depth is locationDepth.FirstBoss:
            for node in first_boss_nodes:
                node_locations = location_graph.node_data(node).locations
                # try to find a popup location
                found_location = False
                for loc in node_locations:
                    if loc.LocationCategory is locationCategory.POPUP:
                        self.depth_classification[loc] = True
                        found_location = True
                        break
                # if no popup at first boss location, just prefer the first location in that node
                if not found_location:
                    self.depth_classification[node_locations[0]] = True
        elif location_depth is locationDepth.FirstVisit:
            for node in first_boss_nodes:
                current_node = node
                # backtrack on the graph until we can't anymore
                while location_graph.inc_edges(current_node):
                    node_locations = location_graph.node_data(current_node).locations
                    for loc in node_locations:
                        self.depth_classification[loc] = True
                    parent_edge = location_graph.inc_edges(current_node)[0]
                    parent,_ = location_graph.edge_by_id(parent_edge)
                    current_node = parent
        elif location_depth is locationDepth.SecondBoss:
            for node in second_boss_nodes:
                node_locations = location_graph.node_data(node).locations
                # try to find a popup location
                found_location = False
                for loc in node_locations:
                    if loc.LocationCategory is locationCategory.POPUP:
                        self.depth_classification[loc] = True
                        found_location = True
                        break
                # if no popup at first boss location, just prefer the first location in that node
                if not found_location:
                    self.depth_classification[node_locations[0]] = True
        elif location_depth is locationDepth.SecondVisit:
            for node in data_nodes:
                node_locations = location_graph.node_data(node).locations
                self.depth_classification[node_locations[0]] = False
        elif location_depth is locationDepth.DataFight:
            for node in data_nodes:
                node_locations = location_graph.node_data(node).locations
                self.depth_classification[node_locations[0]] = True

    def isValid(self, loc: KH2Location):
        return self.depth_classification[loc]