"""
mqo is the Metaseqoia file format, describing a 3D model/graphic.
See http://metaseq.net/en/format.html for the file format.

Our .mqo files are typically within resources/img/

The format for our models is roughly this:
- two lines of boilerplate at the top, saying that this is a Metasequoia
  document of a specific format and version
- a single material chunk, and then an arbitrary number of object chunks.
- (there can be other chunks, too, but we ignore them)

A chunk has a line describing what's going to come, ending with a "{", then a
bunch of lines in the body, followed by a line with a "}".
- The material chunk starts with the word "Material" and the number of lines
  within it.
- An object chunk starts with the word "Object" and the name of the object
  surrounded by double-quotes.
- Within an object, there is a vertices chunk that starts with "vertex" and the
  number of lines within it.
- Within an object, there is also a faces chunk that starts with "face" and
  the number of lines within it.

Each line within the material chunk contains:
- the name of the material (seemingly unused: we use its index instead)
- a bunch of fields of the format `name(value)`. We care about only:
  - the "col" field, describing a color: four space-separated floats between 0
    and 1 indicating red, green, blue, and opacity levels
  - the "tex" field, describing a texture (which I suspect is an image file in
    the same directory)

Each object chunk contains:
- the vertex chunk, each line of which contains a three space-separated floats
  representing (x, y, z) coordinates
- the face chunk, each line of which contains:
  - the number of vertices in the face (3 for a triangle, 4 for a quadrilateral)
  - the "V" field, which contains a space-separated list of the indices into the
    vertex chunk for the vertices of the face (length should match the
    previously-described number)
  - the "M" field, which is an index into the material chunk indicating which
    material to apply to this face
  - the "UV" field, which has something to do with applying texture? It's a
    space-separated list of floats, with length twice the length of the V field
    (something to do with mapping sections of an image from the material's "tex"
    field to the vertices of the face?).
  - the "COL" field, indicating something to do with the color of the face? It's
    a space-separated list of integers of the same length as the "V" field. Many
    of them are a little less than 4.3 billion, suggesting that they're unsigned
    32-bit integers that should be interpreted as signed 32-bit integers.
- various other 1-line fields consisting of the field name, then a space, and
  the field value (which might be a number or a space-separated list of
  numbers). An example of a fields is "scale 1.000000 1.000000 1.000000".
  - The fields we seem to care about within an object are the mirror,
    mirror_axis, color, scale, rotation, and translation.

----------------

In contrast, .gpo files have a slightly different format. Each line in them
describes either a point (denoted by a line starting with 'p'), a material
(denoted by a line starting with 'm'), or a description of an object's shape
(denoted by a line starting with 'i', possibly short for "indices"). All lines
in the file consist of space-separated vaues:
- 'p' lines contain the x, y, and z coordinates of the point, then the UV
  coordinates of its texture (or "0 0" for points that do not have texture).
- 'm' lines contain the RGBA values of its color, optionally followed by the
  name of the image file containing its texture. They are immeditaley followed
  by the single 'i' line that uses this material.
- 'i' lines contain the indices of the points in triangles that use the
  color/texture described on the preceding 'm' line. The number of indices on an
  'i' line is a multiple of 3: each triple of them corresponds to a different
  triangle that uses the same material (color/texture).

Note that, in a .gpo file, a single (x, y, z) point in space may have multiple
'p'-lines associated with it, if multiple faces with different UV-values for
their textures all converge on that vertex!
"""
