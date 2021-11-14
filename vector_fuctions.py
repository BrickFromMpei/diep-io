def vector_delta(vector1, vector2):
    check_vector(vector1, vector2)
    position_delta = []
    for j in range(len(vector1)):
        position_delta.append(vector2[j] - vector1[j])
    return position_delta


def cos_angle(vector1, vector2):
    check_vector(vector1, vector2)
    scalar_value = scalar(vector1, vector2)
    return scalar_value / (vector_len(vector1) * vector_len(vector2))


def scalar(vector1, vector2):
    check_vector(vector1, vector2)
    return sum(vector1[i] * vector2[i] for i in range(len(vector1)))


def vector_len(vector):
    return sum(x**2 for x in vector)**.5


def reflect(vector, normal_vector):
    check_vector(vector, normal_vector)
    reflect_vector = []
    scalar_value = scalar(vector, normal_vector)
    for i in range(len(vector)):
        reflect_vector.append(
            vector[i] - 2 * normal_vector[i] * scalar_value
        )
    return reflect_vector

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