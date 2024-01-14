def large(aspect_ratio):
    if 2.2 <= aspect_ratio <= 2.8:
        return True
    return False

def small(aspect_ratio):
    if 1.2 <= aspect_ratio <= 1.8:
        return True
    return False

def threshold(aspect_ratio):
    return large(aspect_ratio)


    