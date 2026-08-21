# meshanvil -- validation targets.
#
# The checks that matter on geometry need a real 3D source, and sources are never in the
# repository. What CI can verify is that everything parses, that the host logic holds
# (scripts/selfcheck.py, no Blender needed), and that nothing private came back in.

BLENDER ?= /Applications/Blender.app/Contents/MacOS/Blender
PYTHON  ?= python3

.PHONY: check compile types selfcheck hygiene fixture logics

check: compile types selfcheck hygiene

compile:
	$(PYTHON) -m compileall -q meshanvil meshanvil_engine pipeline tools scripts
	@find meshanvil meshanvil_engine pipeline tools scripts -name '__pycache__' -type d -exec rm -rf {} +

# JSDoc types over the viewer: checked, never emitted, so the page keeps loading as plain JS.
types:
	@npx --no-install tsc --noEmit && echo "types: ok"

selfcheck:
	@$(PYTHON) scripts/selfcheck.py

hygiene:
	@bash scripts/check_hygiene.sh

# Needs Blender, so it stays out of check and out of CI: it asserts that the generated
# fixture's own defects are still found unaided, which is the ground truth the tools rely on.
fixture:
	@$(PYTHON) scripts/fixture_check.py

# logics-manager is a devDependency: npm ci, then this runs the pinned version.
logics:
	npx --no-install logics-manager lint --require-status
	npx --no-install logics-manager audit --group-by-doc
