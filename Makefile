# meshanvil -- validation targets.
#
# There is no test suite here and adding one would be dishonest: every check that
# matters needs a real 3D source, and sources are never in the repository. What CI
# can verify is that the scripts parse and that nothing private came back in.

BLENDER ?= /Applications/Blender.app/Contents/MacOS/Blender
PYTHON  ?= python3

.PHONY: check compile hygiene logics

check: compile hygiene

compile:
	$(PYTHON) -m compileall -q pipeline tools
	@find pipeline tools -name '__pycache__' -type d -exec rm -rf {} +

hygiene:
	@bash scripts/check_hygiene.sh

# logics-manager is a devDependency: npm ci, then this runs the pinned version.
logics:
	npx --no-install logics-manager lint --require-status
	npx --no-install logics-manager audit --group-by-doc
