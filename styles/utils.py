def select_thumbnail(explicit, images, existing=None):
    if explicit:
        return explicit
    if images:
        return images[0]
    return existing