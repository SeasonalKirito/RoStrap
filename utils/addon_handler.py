from utils.enums import ENUMS
import os

class AddonHandler:
    def _get_addons():
        addons = ENUMS.PATHS["ADDONS_PATH"]

        if not os.path.exists(addons):
            return False

        addon_files = [f for f in os.listdir(addons) if os.path.isfile(os.path.join(addons, f))]
        
        if not addon_files:
            return False

        return addon_files