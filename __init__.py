
import os
import re
import torch
import folder_paths


class MiniMaxH3ConditioningSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "filename": (
                    "STRING",
                    {"default": "minimax_conditioning.pt"},
                ),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    CATEGORY = "model/conditioning/minimax"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, conditioning, filename):
        # Force saving again when the node is executed.
        return float("nan")

    def save(self, conditioning, filename):
        output_dir = os.path.join(
            folder_paths.get_output_directory(),
            "minimax_h3_conditioning",
        )
        os.makedirs(output_dir, exist_ok=True)

        filename = os.path.basename(filename.strip())
        filename = re.sub(
            r'[<>:"/\\|?*\x00-\x1f]', "_", filename
        )

        if not filename:
            filename = "minimax_conditioning.pt"

        if not filename.lower().endswith(".pt"):
            filename += ".pt"

        filepath = os.path.join(output_dir, filename)

        torch.save(conditioning, filepath)
        print(f"[MiniMax H3 Conditioning Saver] Saved: {filepath}")

        return {"ui": {"text": [f"Saved: {filepath}"]}}


class MiniMaxH3ConditioningLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "filename": (
                    "STRING",
                    {"default": "minimax_conditioning.pt"},
                ),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "load"
    CATEGORY = "model/conditioning/minimax"

    @classmethod
    def IS_CHANGED(cls, filename):
        # Reload the file on each execution.
        return float("nan")

    def load(self, filename):
        output_dir = os.path.join(
            folder_paths.get_output_directory(),
            "minimax_h3_conditioning",
        )

        filename = os.path.basename(filename.strip())
        filename = re.sub(
            r'[<>:"/\\|?*\x00-\x1f]', "_", filename
        )

        if not filename.lower().endswith(".pt"):
            filename += ".pt"

        filepath = os.path.join(output_dir, filename)

        if not os.path.isfile(filepath):
            raise FileNotFoundError(
                f"Conditioning file not found: {filepath}"
            )

        # Only load files created by you or another trusted source.
        conditioning = torch.load(
            filepath,
            map_location="cpu",
            weights_only=False,
        )

        if not isinstance(conditioning, list):
            raise ValueError(
                "Invalid conditioning file: expected a CONDITIONING list."
            )

        print(
            f"[MiniMax H3 Conditioning Loader] Loaded: {filepath}"
        )

        return (conditioning,)


NODE_CLASS_MAPPINGS = {
    "MiniMaxH3ConditioningSaver": MiniMaxH3ConditioningSaver,
    "MiniMaxH3ConditioningLoader": MiniMaxH3ConditioningLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MiniMaxH3ConditioningSaver": "MiniMax H3 Conditioning Saver",
    "MiniMaxH3ConditioningLoader": "MiniMax H3 Conditioning Loader",
}
