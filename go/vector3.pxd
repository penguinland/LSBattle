cdef class Vector3:
    cdef double _x, _y, _z
    cpdef copy(self)

cdef Vector3 vec3_from_floats(double x, double y, double z)
