import os.path


def base_path(path: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", path)
    return os.path.abspath(project_root)
