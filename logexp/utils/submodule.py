import importlib
import pkgutil


# This code is from
# https://github.com/allenai/allennlp/blob/v0.9.0/allennlp/common/util.py#L308-L334
def import_submodules(module_name: str) -> None:
    module = importlib.import_module(module_name)
    path = getattr(module, "__path__", [])
    path_string = "" if not path else path[0]

    for module_finder, name, _ in pkgutil.walk_packages(path):
        if path_string and module_finder.path != path_string:
            continue
        import_submodules(f"{module_name}.{name}")
