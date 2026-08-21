"""Create a tiny public STEP source for the FreeCAD import smoke test."""
from pathlib import Path

import FreeCAD as App
import Import, Part

root = Path.cwd()
target = root / "work" / "in" / "fixture_box.step"
target.parent.mkdir(parents=True, exist_ok=True)
document = App.newDocument("meshanvil_step_fixture")
box = document.addObject("Part::Feature", "FixtureBox")
box.Shape = Part.makeBox(40, 30, 20)
Import.export([box], str(target))
print(target)
