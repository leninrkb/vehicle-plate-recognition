def large(aspect_ratio):
    if 2.2 <= aspect_ratio <= 2.8:
        return True
    return False


def threshold(aspect_ratio):
    return large(aspect_ratio)


    