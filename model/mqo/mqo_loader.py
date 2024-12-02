import operator
import re


class Face(object):
    # __slots__ contains a list of all fields within the class
    __slots__ = ("n", "indices", "material", "uv", "h")

    def __init__(self, n=0, indices=None, material=None, uv=None, color=None):
        """
        Inputs:
        - n, the number of vertices in this face. Must be 3 or 4.
        - indices, the list of indices into some external list of vertices to
          describe the face. Must have length n.
        - material is an index into some external list of materials
        - uv is a string depicting a space-separated list of floats, which has
          something to do with the texture of the material (if the material has
          a texture and isn't just a flat color)
        - color is entirely unused!? but we keep it because it's part of the MQO
          standard and we're parsing raw MQO data into here.
        """
        self.n = int(n)
        # According to the MQO 1.0 spec, a face must consist of either 3 or 4
        # vertices.
        if self.n not in (3, 4):
            self.n = 0
            return

        self.indices = [int(i) for i in indices.split()]
        if len(self.indices) != self.n:
            raise IOError("Face format is clashed")

        if material is None:
            self.material = -1
        else:
            self.material = int(material)

        if uv is None or self.material == -1:
            self.uv = None
        else:
            self.uv = [float(i) for i in uv.split()]
            if len(self.uv) != self.n * 2:
                raise IOError("Face format is clashed")
            # TODO: what's the point of this!? Does it have to do with mirroring
            # the texture?
            for i in range(1, self.n * 2, 2):
                self.uv[i] = 1.0 - self.uv[i]

        self.make_hash()

    def make_hash(self):
        self.h = hash(tuple(self.indices))

    def __eq__(self, other):
        return self.h == other.h and self.indices == other.indices

    def create_mirror(self, vertices, xi):
        """
        vertices is a list of vertices, which correspond to self.indices.
        xi is a list of 3 numbers, each of which is either 1 or -1, indicating
        whether to mirror along the x, y, and/or z axes.

        We return a new face formed by mirroring self along the axes indicated
        by xi, after appending any new vertices needed.
        """
        face = Face()
        face.n = self.n
        face.material = self.material
        if self.uv:
            face.uv = self.uv[:]
            face.uv[2], face.uv[-2] = face.uv[-2], face.uv[2]
            face.uv[3], face.uv[-1] = face.uv[-1], face.uv[3]
        else:
            face.uv = None

        # For each vertex in the face, in reverse order, reflect it via xi and
        # store that new vertex in the new face.
        it = list(range(self.n))
        # Regardless of whether the face has 3 or 4 vertices, if you swap the
        # second one with the last one, we reverse the order of the vertices.
        # ABC -> ACB, and
        # ABCD -> ADCB (equivalent to DCBA)
        it[1], it[-1] = it[-1], it[1]
        face.indices = []
        c = 0
        for i in it:
            v = list(map(operator.mul, xi, vertices[self.indices[i]]))
            try:
                index = vertices.index(v)
            except ValueError:
                index = len(vertices)
                vertices.append(v)
                c += 1
            face.indices.append(index)
        face.make_hash()
        return face


class Material(object):
    """
    This is a glorified mutable tuple of (color, texture_name)
    """
    __slots__ = ("color", "tex_name")

    def __init__(self):
        self.color = None
        self.tex_name = ""

    def __eq__(self, other):
        return self.color == other.color and self.tex_name == other.tex_name


class Obj(object):
    def __init__(self):
        self.vertices = []
        self.faces  = []
        self.mirror = None
        self.mirror_axis = None

    def __iadd__(self, other):
        """
        Override the `+=` operator

        WARNING: this mutates the other object by changing the indices in the
        faces! It's possible that the other Obj we're appending will contain
        invalid state after this function returns.
        """
        # vmap is a map from indices in other.vertices to indices in
        # self.vertices.
        # We create it when appending vertices from other to self, and then use
        # it when appending faces from other to self.
        vmap = [0] * len(other.vertices)
        n = len(self.vertices)  # Index of the next vertex to add
        for i, v in enumerate(other.vertices):
            try:
                vmap[i] = self.vertices.index(v)
            except ValueError:
                vmap[i] = n
                n += 1
                self.vertices.append(v)

        for face in other.faces:
            face.indices = [vmap[i] for i in face.indices]
            face.make_hash()
            if face not in self.faces:
                self.faces.append(face)
        return self

    def expand_mirror(self):
        """
        For each face in the object, also include the face reflected across the
        mirror, then remove the ability to mirror any more.

        TODO: self.mirror appears to be unused. Can we use only mirror_axis
        instead?
        """
        if self.mirror in [None, 0] or self.mirror_axis is None:
            return

        x = y = z = 1.0
        if self.mirror_axis & 1: x = -1.0
        if self.mirror_axis & 2: y = -1.0
        if self.mirror_axis & 4: z = -1.0
        xi = [x, y, z]
        mirrored_faces = [f.create_mirror(self.vertices, xi)
                          for f in self.faces]
        self.faces.extend(mirrored_faces)
        self.mirror = None

    def check_material_uv(self, materials, mmap):
        """
        For each face in the object, ensure that it has a compatible material:
        - if the face's material has no texture, erase the face's uv values
        - if the face has no uv values, ensure its material has no texture
        - if the face has no material at all, give it our default color

        materials is a list of materials, which might be mutated if we need to
        add new materials to it.

        mmap (which needs to be renamed!) is a mapping from the indices used in
        our faces to the indices of the materials list.
        TODO: explain why this exists
        """
        def get_color_index(color):
            # If the color is not in the materials list yet, insert it and then
            # return that new index.
            m = Material()
            m.color = color
            try:
                return materials.index(m)
            except ValueError:
                materials.append(m)
                return len(materials) - 1

        for face in self.faces:
            if face.material >= 0:
                mi = mmap[face.material]
                face.material = mi
                if not materials[mi].tex_name:
                    # No texture is set in the material, so erase the UV
                    # coordinates of the face.
                    face.uv = None
                elif face.uv is None:
                    # The material has a texture but the faces have no UV
                    # coordinates, so assign a new material with only color and
                    # not texture.
                    face.material = get_color_index(materials[mi].color)
            else:
                # This face has no material yet. Create a new one with the right
                # color.
                face.uv = None
                face.material = get_color_index(self.color)

    def normalize(self, length=1.0, dy=-0.5):
        """
        Scale all the vertices so that the range of y values is length, and also
        translate all vertices in the y direction so the smallest value is dy.
        Using the default argument values, you'll move the vertices so that the
        range of y values is -0.5 to +0.5, and x and z are scaled
        proportionately.
        """
        ys = [y for _, y, _ in self.vertices]
        max_y = max(ys)
        min_y = min(ys)
        ly = max_y - min_y
        factor = length / ly
        self.vertices = [[x * factor, (y - min_y) * factor + dy, z * factor]
                         for x, y, z in self.vertices]


class MqoObject(object):
    """
    This class is a way to take an open file handle pointing at a Metasequoia
    document, and constructing an Obj and a Material list from it, both of which
    should be considered public fields.
    """
    _re_chunk  = re.compile(r"^(\w+)\s*(\d+)?\s*{")      # e.g., 'Material 3 {'
    _re_object = re.compile(r'^Object\s*"([^"]+)"\s+{')  # e.g., 'Object "a" {'
    # The use of re.VERBOSE means "ignore whitespace, newlines, and anything
    # after a comment delimiter in the regex."
    _re_face   = re.compile(r"""
                            ^(\w+)\s*              #1 number of vertices
                            V\(([^)]*)\)\s*        #2 vertex index
                            (?:M\(([^)]*)\))?\s*   #3 material index
                            (?:UV\(([^)]*)\))?\s*  #4 UV value
                            (?:COL\(([^)]*)\))?\s* #5 vertex color
                            """, re.VERBOSE)

    def __init__(self, imqo):
        """
        imqo is an open file handle that contains an MQO (Metasequoia) document
        """
        self._check_header(imqo)
        self.obj = Obj()
        materials = []
        try:
            while True:
                chunk = self._search_chunk(imqo).lower()
                if chunk == "object": # There might be many objects...
                    obj = self._object_chunk(imqo)
                    obj.expand_mirror()
                    self.obj += obj
                elif chunk == "material": # ...but only 1 material chunk.
                    materials = self._material_chunk(imqo)
                else:
                    self._skip_chunk(imqo)
        except StopIteration:  # imqo hit the end of the file
            pass
        if not materials:
            raise IOError("Material-Chunk is essential")

        # We will now remove duplicate materials, so that self.materials is a
        # list of unique materials, and mmap is a list containing the indices in
        # self.materials for each original material.
        self.materials = []
        mmap = [0]*len(materials)
        for i, m in enumerate(materials):
            try:
                index = self.materials.index(m)
            except ValueError:
                index = len(self.materials)
                self.materials.append(m)
            mmap[i] = index
        self.obj.check_material_uv(self.materials, mmap)
        self.obj.normalize()

        # Sort the faces within the Obj so that the ones with the earliest
        # materials come first, and the ones with complex textures come last.
        def key(face):
            return face.material + (1000000 if face.uv is None else 0)
        self.obj.faces.sort(key=key)

    ###### read tool ######

    def _check_header(self, imqo):
        """
        We expect imqo to be an open file handle containing a Metasequoia
        document. We consume the first two lines of the file, and throw
        exceptions if they look unexpected.
        """
        firstline = next(imqo)
        if "Metasequoia Document" not in firstline:
            raise IOError("This file is not Metasequoia Document")

        line = next(imqo)
        m = re.match(r"^Format (\w+) Ver (\d+)\.(\d+)", line)
        if m:
            if m.group(1) != "Text":
                raise IOError("This file format is not supported")
            if m.group(2) != "1":
                raise IOError("This file version is not supported")
        else:
            raise IOError("This file does not look like a Metasequoia document")

    def _search_chunk(self, imqo):
        """
        We expect imqo to be an open file handle to the middle of a Metasequoia
        document. We consume lines until the next time we find what looks like
        the beginning of either a chunk or an object, and then return the name
        of the thing we found.
        """
        while True:
            line = next(imqo).strip()
            m = self._re_chunk.match(line)
            if m:
                return m.group(1)
            m = self._re_object.match(line)
            if m:
                return "object"

    def _material_chunk(self, imqo):
        """
        imqo should be an open file handle into the middle of a Metasequoia
        document, pointing to the line just after the Material block was opened.
        We consume lines until we hit the end of the block, and return a list of
        all materials found.

        A material line consists of the name in quote marks, and then a bunch of
        fields (consisting of the name of the field and then its value in
        parentheses), all on a single line. We ignore the name and all fields
        except the "col" (color) and "tex" (texture) ones.
        """
        # TODO: write some tests, then simplify this
        re_comp = re.compile(r"""
                             \s+           # Whitespace
                             (?=           # Zero-width lookahead
                                 \w+       # Parameter
                                 \(        # Literal open-parenthesis
                                     [^)]* # Value
                                 \)        # Literal close-parenthesis
                             )
                             """, re.VERBOSE)
        re_field = re.compile(r"^(\w+)\(([^)]*)\)")
        materials = []
        while True:
            line = next(imqo).strip()
            if line == "}":
                break
            material = Material()
            fields = re_comp.split(line)
            for field in fields:
                m = re_field.match(field)
                if m:
                    if m.group(1) == "col":
                        material.color = [float(i)for i in m.group(2).split()]
                    elif m.group(1) == "tex":
                        material.tex_name = m.group(2)[1:-1]
            materials.append(material)
        return materials

    def _object_chunk(self, imqo):
        obj = Obj()
        vertices = []
        while True:
            line = next(imqo).strip()
            if line == "}":
                break
            m = self._re_chunk.match(line)
            if m:
                chunk = m.group(1).lower()
                if chunk == "vertex":
                    vertices = self._vertex_chunk(imqo)
                elif chunk == "face":
                    obj.faces = self._face_chunk(imqo)
                else:
                    self._skip_chunk(imqo)
            else:
                fields = line.split()
                name = fields[0]
                if name == "mirror":
                    obj.mirror = int(fields[1])
                elif name == "mirror_axis":
                    obj.mirror_axis = int(fields[1])
                elif name == "color":
                    obj.color = [float(i) for i in fields[1:]]
                elif name == "scale":
                    obj.scale = [float(i) for i in fields[1:]]
                    if obj.scale != [1.0,1.0,1.0]:
                        print("s",obj.scale)
                elif name == "rotation":
                    obj.rotation = [float(i) for i in fields[1:]]
                    if obj.rotation != [.0,.0,.0]:
                        print("r",obj.rotation)
                elif name == "translation":
                    obj.translation = [float(i) for i in fields[1:]]
                    if obj.translation != [.0,.0,.0]:
                        print("t",obj.translation)

        vmap = [0]*len(vertices)
        for i, v in enumerate(vertices):
            try:
                vmap[i] = obj.vertices.index(v)
            except ValueError:
                vmap[i] = len(obj.vertices)
                obj.vertices.append(v)
        for face in obj.faces:
            face.indices = [vmap[i] for i in face.indices]

        return obj

    def _vertex_chunk(self, imqo):
        """
        The vertices are space-separated (x, y, z) tuples, one per line. We
        parse all of them until we hit the end of the block (with a "}"), and
        then return a list of them all.
        """
        vertices = []
        while True:
            line = next(imqo).strip()
            if line == "}":
                break
            v = list(map(float, line.split()))
            vertices.append(v)
        return vertices

    def _face_chunk(self, imqo):
        faces = []
        while True:
            line = next(imqo).strip()
            if line == "}":
                break
            m = self._re_face.match(line)
            face = Face(*m.groups())
            if face.n != 0 and face not in faces:
                faces.append(face)
        return faces

    def _skip_chunk(self, imqo):
        """
        We advance the open file descriptor until the end of the current chunk
        (delimited with a "}"). If this section opens its own sub-chunk, we skip
        all of that as well.
        """
        while True:
            line = next(imqo).strip()
            if line == "}":
                break
            if self._re_chunk.match(line):
                self._skip_chunk(imqo)


if __name__ == "__main__":
    import time, sys
    class F(object):
        def __init__(self, io):
            self.lis = io.readlines()
            self.n = len(self.lis)
            self.i = 0
            self.ii = 0
            print("-"*100)
        def __next__(self):
            if self.i < self.n:
                self.i += 1
                if self.i*100/self.n > self.ii:
                    sys.stdout.write("#")
                    sys.stdout.flush()
                    self.ii += 1
                return self.lis[self.i-1]
            else:
                print()
                raise StopIteration

    t1 = time.time()
    name = "../resources/img/allosaurus/allosaurus.mqo"
    m = MqoObject(F(open(name)))
    t2 = time.time()
    print(t2 - t1)
