# mesh.py
# by yohannes dawit
#    tools for handling meshes from OFF files.
#    The main "export" is Mesh

from ren3d.math3d import Point, Vector
from ren3d.bbox import BoundingBox
from ren3d.materials import make_material
from ren3d.models import Group, Record


class Triangle:
    """Model for a triangle """

    def __init__(self, points, color=(0, 1, 0), normals=[]):
        
        self.points = list(points)
        self.color = color
        if normals:
            self.normals = normals
        else:
            self.normals= [self._make_normals(self.points)]*3

        self.bbox = BoundingBox()
        self.bbox.include_points(self.points)

    def __repr__(self):
        return f"Triangle({self.points})"
        

    def iter_polygons(self):
        yield Record(points = self.points,
                     color = self.color,
                     normals = self.normals)

    def intersect(self, ray, interval, info):
        if not self.bbox.hit(ray,interval):
            return False


    def _make_normals(self,points):
        U = points[1] - points[0]
        V = points[2] - points[0]
        
        return U.cross(V).normalized()  

    def _setinfo(self,ray,t,info,normal):
        info.t = t
        info.point = ray.point_at(t)
        info.normal = normal
        info.color = self.color
        info.uvn = None
        info.texture = None


class Mesh:
    """model to implement polygonal mesh from OFF file

    Mesh is modeled as a group of triangles with a bounding box.
    """

    def __init__(self, fname, color, recenter=False, smooth=False):
        meshdata = OFFData(fname)
        if recenter:
            meshdata.recenter()

        group = Group()
        for trl in _make_mesh_triangles(meshdata, color, smooth):
            group.add(trl)
        self.group
        self.group = group
        self.bbox = meshdata.bbox

    def iter_polygons(self):
        return self.group.iter_polygons()

    def intersect(self, ray, interval, info):
        if not self.bbox.hit(ray, interval):
            return false
        return self.group.intersect(ray, interval, info)
   
def _make_mesh_triangles(facepoints, facenormals, color):
    """helper function to turn a face into tiangles

    facepoints is list of points and facenormals is a corresponding
    list of normals. color is a material

    """
    color = make_material(color)
    for face in data.face_indexes:
        points = data.get_points(face)
        if smooth:
            normals = data.get_verteces_normals(face)
        else:
            normals = [data.get_face.normal(face)]*len(points)
        for l in range(len(points)-1):
            tri = Triangle([points[0], points[i], points[i+1]],
                           color,
                           (normal[0], normals[i], normals[i+1]))
            yield tri
    

class OFFData:
    """Class for reading OFF files and supplying face information"""

    def __init__(self, fname):
        points, faces = self._readOFF("meshes/"+fname)
        self.points = points
        self.faces = faces
        self.face_indexes = range(len(faces))
        self.bbox = self._make_bbox()
        self._f_norms = [self._compute_face_normal(f) for f in faces]
        self._v_norms = [self._compute_vertex_normal(i)
                         for i in range(len(self.points))]

    def _readOFF(self, fname):
        # Read data from OFF file, return vertices and facelists
        with open(fname) as infile:
            heading = infile.readline()
            if heading[:3] != "OFF":
                raise ValueError("File does not appear to be an OFF")
            nVerts, nFaces, nEdges = [int(v) for v in infile.readline().split()]

            verts = []
            for i in range(nVerts):
                line = infile.readline()
                verts.append(Point(float(s) for s in line.split()[:3]))  # ignore rgb
                faces = []
            for i in range(nFaces):
                indexStrings = infile.readline().split()[1:]
                faces.append(tuple(int(s) for s in indexStrings))
        return verts, faces

    def _make_bbox(self):
        box = BoundingBox()
        box.include_points(self.points)
        return box

    def _compute_face_normal(self, f):
        a, b, c = [self.points[i] for i in f[:3]]
        norm = (b-a).cross(c-a)
        norm.normalize()
        return norm

    def _compute_vertex_normal(self, vert_i):
        n = Vector([0, 0, 0])
        for face_i, face in enumerate(self.faces):
            if vert_i in face:
                n += self._f_norms[face_i]
        try:
            n.normalize()
        except ZeroDivisionError:
            pass
        return n

    def get_points(self, face):
        """returns a list of points for face; face is an index"""
        return [self.points[i] for i in self.faces[face]]

    def get_face_normal(self, face):
        """return normal for face; face is an index."""
        return self._f_norms[face]

    def get_vertex_normals(self, face):
        """return list of normals for a face; face is an index"""
        return [self._v_norms[i] for i in self.faces[face]]
       
    def recenter(self):
        """move points to put midpoint at (0, 0, 0)"""
        
        dist = Vector(self.bbox.midpoint)
        self.points = [vert-dist for vert in self.points]
        # rebuild the bounding box
        self.bbox = self._make_bbox()

