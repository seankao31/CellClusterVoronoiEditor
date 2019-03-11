import itertools
import numpy as np

from scipy.spatial import ConvexHull


class VoronoiAnalysis:
    def __init__(self, vor):
        if vor.points.shape[1] != 2:
            raise ValueError("Voronoi diagram is not 2-D.")
        self.voronoi = vor

    def segments(self, radius=None):
        vor = self.voronoi
        self.bounded_ridge_vertices = []
        self.augmented_vertices = vor.vertices.tolist()
        center = vor.points.mean(axis=0)
        if radius is None:
            ptp_bound = vor.points.ptp(axis=0)
            radius = ptp_bound.max()

        finite_segments = []
        infinite_segments = []
        for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.all(simplex >= 0):
                finite_segments.append(vor.vertices[simplex])
                self.bounded_ridge_vertices.append(simplex.tolist())
            else:
                i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

                t = vor.points[pointidx[1]] - vor.points[pointidx[0]]
                t /= np.linalg.norm(t)  # tangent
                n = np.array([-t[1], t[0]])  # normal

                midpoint = vor.points[pointidx].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[i] + direction * np.linalg.norm(
                    np.absolute(vor.vertices[i])+np.array([radius, radius]))

                infinite_segments.append([vor.vertices[i], far_point])
                self.bounded_ridge_vertices.append(
                        [i, len(self.augmented_vertices)])
                self.augmented_vertices.append(far_point.tolist())

        return finite_segments, infinite_segments

    def finitePolygons(self, bbox):
        bbox = np.asarray(bbox)
        radius = max(bbox[1]-bbox[0])
        finite_segments, infinite_segments = self.segments(radius=radius)
        vor = self.voronoi
        self.bounded_regions = []

        # Map a given point to infinte_segments assiociating with it
        segs_of_point = [[] for _ in range(len(vor.points))]
        for ridge, (p1, p2) in enumerate(vor.ridge_points):
            segs_of_point[p1].append(ridge)
            segs_of_point[p2].append(ridge)

        n = len(self.augmented_vertices)
        bbox_vertices = list(range(n, n+4))
        self.augmented_vertices += [
                list(t) for t in itertools.product(
                        *list(map(list, zip(*bbox))))]

        self.bounded_areas = []

        for p, region in enumerate(vor.point_region):
            vertices = vor.regions[region]

            if all(v >= 0 for v in vertices):
                # finite region
                self.bounded_regions.append(vertices)

                # calculate polygon area
                vs = vor.vertices[vertices]
                hull = ConvexHull(vs)
                vs = vs[hull.vertices]  # sort
                self.bounded_areas.append(self.polyArea(vs))
                continue

            self.bounded_areas.append(-1)

            # reconstruct bounded region
            new_region = [v for v in vertices if v >= 0]
            rs = segs_of_point[p]
            inf_rs = [r for r in rs if any(
                    v < 0 for v in vor.ridge_vertices[r])]
            rs = [self.bounded_ridge_vertices[r] for r in rs]
            # add far points
            new_region.append(self.bounded_ridge_vertices[inf_rs[0]][1])
            new_region.append(self.bounded_ridge_vertices[inf_rs[1]][1])

            # optionally add vertices of bounding box
            new_region += list(filter(
                    lambda v: self.decideAddPoint(v, p, rs),
                    bbox_vertices))

            # convex hull
            vertices = np.array(self.augmented_vertices)[new_region]
            hull = ConvexHull(vertices)
            new_region = np.array(new_region)[hull.vertices]

            # finish
            self.bounded_regions.append(new_region.tolist())

        return (self.bounded_regions, np.asarray(self.augmented_vertices),
                self.bounded_areas, finite_segments, infinite_segments)

    def decideAddPoint(self, v, p, rs):
        v = np.array(self.augmented_vertices[v])
        p = self.voronoi.points[p]
        rs = [np.array([self.augmented_vertices[r[0]],
                        self.augmented_vertices[r[1]]]) for r in rs]
        result = []
        for r in rs:
            result.append(np.sign(np.cross(r[1]-r[0], v-r[0])) ==
                          np.sign(np.cross(r[1]-r[0], p-r[0])))

        return all(result)

    def polyArea(self, points):
        points = np.array(points)
        x = points.transpose()[0]
        y = points.transpose()[1]
        return 0.5*np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
