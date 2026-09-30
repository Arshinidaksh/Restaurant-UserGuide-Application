"""
Master Multi-Agent Pipeline Orchestrator
Coordinates specification ingestion, headless browser capturing, and slide rendering.
"""
import os
import sys
import argparse
import json

WORKSPACE_DIR = r"c:\Users\ISARVA\Documents\Restaurant-UserGuide-Application"
sys.path.insert(0, WORKSPACE_DIR)

from scripts.pipeline.compose_slides import build_part_slides

def run_pipeline(spec_path: str, capture: bool = True, render: bool = True):
    print("=" * 60)
    print("POS PRESENTATION SLIDE GENERATION PIPELINE")
    print("=" * 60)

    if not os.path.exists(spec_path):
        print(f"Error: Specification file not found at {spec_path}")
        return False

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    part_id = spec.get("part_id", "custom").lower()
    screens_dir = os.path.join(WORKSPACE_DIR, "project", f"screens_part_{part_id}")
    os.makedirs(screens_dir, exist_ok=True)

    # Stage 1: Browser Navigation & Screen Capture
    if capture:
        from scripts.pipeline.capture_screens import run_screen_capture
        print(f"\n[STAGE 1/2] Initiating Browser Agent Screen Capture...")
        run_screen_capture(spec_path, screens_dir)
    else:
        print("\n[STAGE 1/2] Skipping Screen Capture (using existing screens)...")

    # Stage 2: Slide Composer & Layout Engine
    if render:
        print(f"\n[STAGE 2/2] Initiating Slide Composer Agent...")
        build_part_slides(spec_path, screens_dir)
    else:
        print("\n[STAGE 2/2] Skipping Slide Composition...")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Slide Generation Pipeline")
    parser.add_argument("--spec", required=True, help="Path to Part specification JSON")
    parser.add_argument("--no-capture", action="store_true", help="Skip browser capture stage")
    parser.add_argument("--no-render", action="store_true", help="Skip rendering stage")

    args = parser.parse_args()
    run_pipeline(
        spec_path=args.spec,
        capture=not args.no_capture,
        render=not args.no_render
    )
