"""Evidence join used by the inactive composed pipeline."""
import argparse
import os


def require_evidence(include_image, node_result, image_result):
    if include_image not in ("true", "false"):
        raise ValueError("include_image must be true or false")
    if node_result != "success":
        raise ValueError(f"required node result is {node_result or 'missing'}")
    expected = "success" if include_image == "true" else "skipped"
    if image_result != expected:
        raise ValueError(f"image result is {image_result or 'missing'}; expected {expected}")
    return "READY: selected evidence complete; no release or deployment authorized"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default=os.environ.get("INCLUDE_IMAGE", "false"))
    parser.add_argument("--node-result", default=os.environ.get("NODE_RESULT", ""))
    parser.add_argument("--image-result", default=os.environ.get("IMAGE_RESULT", ""))
    args = parser.parse_args()
    try:
        print(require_evidence(args.image, args.node_result, args.image_result))
    except ValueError as error:
        print(f"BLOCKED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
