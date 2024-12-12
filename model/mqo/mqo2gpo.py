import os

from . import mqo_loader


class Point:
    """
    This is basically a pair of (vertex, uv), where the vertex is an (x, y, z)
    tuple of a location in space, and the uv is a pair of coordinates on a
    texture image. Unlike the points in an MQO face, *which* texture the uv
    coordinates go to is not specified in here! Consequently, the same location
    in space, if it's where multiple faces with multiple textures meet, must be
    represented by multiple instances of this class.
    """
    def __init__(self, vertex, texcoord=None):
        self.vertex = vertex
        self.texcoord = texcoord

    def __eq__(self, othr):
        if not isinstance(othr, Point):
            return False
        return (self.vertex == othr.vertex and self.texcoord == othr.texcoord)

    def __str__(self):
        """
        This is how the Point will be written out to a .gpo file:
        p x y z u v
        where the p is a literal 'p', and the u and v are both 0 if none is
        supplied (if this Point does not have a texture).
        """
        s = "p %f %f %f "%tuple(self.vertex)
        if self.texcoord is not None:
            s += "%f %f"%tuple(self.texcoord)
        else:
            s += "0 0"
        return s


def output(name: str, points, objects):
    """
    Writes a .gpo file with the given name, containing the given points and
    objects.
    """
    with open(name+".gpo", "w") as of:
        of.write("Game Polygon Object\n")
        for point in points:
            of.write(str(point) + "\n")
        for material, indices in objects:
            of.write(str(material) + "\n")
            of.write("i " + " ".join([str(i)for i in indices]) + "\n")


def mqo2gpo(name: str):
    """
    Given a filename describing a Metasequoia document, convert the data to a
    .gpo file.
    """
    mqo = mqo_loader.MqoObject(open(name))

    pre_len = len(mqo.obj.vertices)
    points = [None]*pre_len

    def _uv(obj, face, i):
        """
        Given a face with a texture and an index of a vertex on that face,
        construct a Point that has the same texture. Insert it into `p` in the
        same location as the original vertex was in obj.vertices, unless
        "another" Point (with the same coordinates but a different texture
        because it was part of a different face) is already there, in which case
        add it to the end of `points` (skipping this step if it's already added
        to the end of `points` somewhere). Then, return the index in `p` at
        which this point exists.
        """
        index = face.indices[i]
        p = Point(obj.vertices[index], face.uv[i*2:i*2+2])
        if points[index] is None or points[index].texcoord is None:
            points[index] = p
        elif p.texcoord != points[index].texcoord:
            for k in range(pre_len, len(points)):
                if p == points[k]:
                    index = k
                    break
            else:
                index = len(points)
                points.append(p)
        return index

    def _col(obj, face, i):
        """
        Given a face that has no texture and an index of a vertex on that face,
        construct a Point in `points` at the same index as it is in `obj`, and
        return that index.
        """
        index = face.indices[i]
        p = Point(obj.vertices[index])
        if points[index] is None:
            points[index] = p
        return index

    objects = []
    for num, face in enumerate(mqo.obj.faces):
        # Faces within mqo.obj are sorted by material. If this face's material
        # is different from the previous one...
        if num == 0 or face.material != mqo.obj.faces[num-1].material:
            # ...create a new object for this material.
            objects.append([mqo.materials[face.material], []])
            indices = objects[-1][1]
        if face.uv is None:
            if face.n == 3:
                l = [_col(mqo.obj, face, i) for i in (0,1,2)]
            else:
                l = [_col(mqo.obj, face, i) for i in (0,1,2,3)]
                l = [l[i] for i in (0,1,2,0,2,3)]
        else:
            if face.n == 3:
                l = [_uv(mqo.obj, face, i) for i in (0,1,2)]
            else:
                l = [_uv(mqo.obj, face, i) for i in (0,1,2,3)]
                l = [l[i] for i in (0,1,2,0,2,3)]
        # Add triples of point indices to the end of the current object for each
        # triangle involved.
        indices.extend(l)

    # QUESTIONABLE JUDGEMENT ALERT! It's possible (though exceedingly unlikely)
    # that some vertices in the original model are unused. Any such unused
    # points will still have None as their value in the `points` list. We filter
    # them out by constructing a map from the vertex index in the original list
    # to its index in a list with all unused points removed, and then update all
    # indices used in all objects to the new set of indices.
    pmap = [0]*len(points)
    index = 0
    for i, p in enumerate(points):
        if p is None:
            continue
        pmap[i] = index
        index += 1
    for obj in objects:
        obj[1] = [pmap[i]for i in obj[1]]
    points = [p for p in points if p is not None]

    # Now, write out the .gpo file.
    name, ext = os.path.splitext(name)
    output(name, points, objects)
