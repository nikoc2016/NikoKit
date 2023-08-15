def get_texture_from_text(file_path):
    _buffer = []
    tex_path_list = []
    with open(file_path, "r") as f:
        while True:
            content = f.readline()
            if not content:
                break
            if ".ftn" in content:
                _buffer.append(content.strip())
    if _buffer:
        tex_path_list = [_clip.split().pop().replace(";", "").replace("\"", "").replace("//", "/") for _clip in
                         _buffer]

    return list(set(tex_path_list))