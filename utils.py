def get_file_contents(filepath):
    file_descriptor = open(filepath, "r")
    return file_descriptor.read()
