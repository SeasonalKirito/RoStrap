from utils.enums import ENUMS

class URI:
    def parse_roblox_uri(uri):
        if uri.startswith("roblox-player:"):
            param_stream = uri[len("roblox-player:"):]

        elif uri.startswith("roblox://"):
            param_stream = uri[len("roblox://"):]
        else:
            raise ValueError("Invalid Roblox URI")

        params = {}
        for item in param_stream.split("+"):
            if ":" in item:
                key, value = item.split(":", 1)
                params[key] = value
            else:
                params[item] = True
        return params

    def construct_launch_command(uri=None):
        if uri:
            cmd = [ENUMS.PATHS["ROBLOX_PLAYER_PATH"], uri]
        else:
            cmd = [ENUMS.PATHS["ROBLOX_PLAYER_PATH"], "--app"]
        return cmd
    