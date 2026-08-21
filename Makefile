# meshanvil -- validation targets.
#
# The checks that matter on geometry need a real 3D source, and sources are never in the
# repository. What CI can verify is that everything parses, that the host logic holds
# (scripts/selfcheck.py, no Blender needed), and that nothing private came back in.

BLENDER ?= /Applications/Blender.app/Contents/MacOS/Blender
PYTHON  ?= python3

.PHONY: check compile selfcheck hygiene logics

check: compile selfcheck hygiene

compile:
	$(PYTHON) -m compileall -q meshanvil meshanvil_engine pipeline tools scripts
	@find meshanvil meshanvil_engine pipeline tools scripts -name '__pycache__' -type d -exec rm -rf {} +

selfcheck:
	@$(PYTHON) scripts/selfcheck.py

hygiene:
	@bash scripts/check_hygiene.sh

# logics-manager is a devDependency: npm ci, then this runs the pinned version.
logics:
	npx --no-install logics-manager lint --require-status
	npx --no-install logics-manager audit --group-by-doc
