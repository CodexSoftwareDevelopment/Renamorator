import os
from typing import Callable, Dict, Tuple
from .file_collector import _extend_windows_path

def run_rename_pipeline(
    mapping: Dict[str, str],
    log_function: Callable[[str], None] = print
) -> Tuple[Dict[str,str], Dict[str,str]]:
    """
    Given old_path→new_name, attempt os.rename on each. Returns two dicts:
      - successes: {old_path: new_path}
      - failures:  {old_path: error_message}
    """
    successes: Dict[str,str] = {}
    failures: Dict[str,str] = {}
    for old_path, new_name in mapping.items():
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        new_path = _extend_windows_path(new_path)
        try:
            os.rename(old_path, new_path)
            successes[old_path] = new_path
            log_function(f"✅ Renamed {old_path} → {new_name}")
        except Exception as e:
            failures[old_path] = str(e)
            log_function(f"❌ Rename failed {old_path}: {e}")
    return successes, failures
