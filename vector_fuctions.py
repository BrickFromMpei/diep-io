def vector_delta(vector1, vector2):
    return [x - y for x, y in zip(vector1, vector2)]


def cos_angle(vector1, vector2):
    scalar_value = scalar(vector1, vector2)
    return scalar_value / (vector_len(vector1) * vector_len(vector2))


def scalar(vector1, vector2):
    return sum(x * y for x, y in zip(vector1, vector2))


def vector_len(vector):
    return sum(x**2 for x in vector)**.5


def vector_sum(vector1, vector2, coef=1):
    return [x + y*coef for x, y in zip(vector1, vector2)]


def vector_multiply(vector, number):
    return [x * number for x in vector]


def reflect(vector, normal_vector):
    scalar_value = scalar(vector, normal_vector)
    return [v - 2*n*scalar_value for v, n in zip(vector, normal_vector)]


def normal(transform1, transform2):
    check_vector(transform1.size, transform2.size)
    check_vector(transform1.position, transform1.size)
    check_vector(transform1.position, transform2.position)
    normal_vector = []
    for i in range(len(transform1.position)):
        size = transform1.size[i]/2 + transform2.size[i]/2
        pos_delta = round(transform1.position[i] - transform2.position[i])
        if abs(pos_delta) != size:
            normal_vector.append(0)
        else:
            if pos_delta > 0:
                normal_vector.append(1)
            else:
                normal_vector.append(-1)
    return normal_vector


def check_vector(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Length on vectors must be equal")