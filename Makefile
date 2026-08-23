# meshanvil -- validation targets.
#
# The checks that matter on geometry need a real 3D source, and sources are never in the
# repository. What CI can verify is that everything parses, that the host logic holds
# (scripts/selfcheck.py, no Blender needed), and that nothing private came back in.

BLENDER ?= /Applications/Blender.app/Contents/MacOS/Blender
PYTHON  ?= python3

.PHONY: check compile types viewer-bundle test selfcheck i18n hygiene fixture viewer-smoke logics package package-check install-check release-dry-run

check: compile types viewer-bundle test i18n hygiene

compile:
	$(PYTHON) -m compileall -q meshanvil meshanvil_engine pipeline tools scripts tests
	@find meshanvil meshanvil_engine pipeline tools scripts tests -name '__pycache__' -type d -exec rm -rf {} +

# JSDoc types over the viewer: checked, never emitted, so the page keeps loading as plain JS.
types:
	@npx --no-install tsc --noEmit && echo "types: ok"

viewer-bundle:
	@npm run check:viewer --silent

test:
	@$(PYTHON) -m pytest -q

selfcheck:
	@$(PYTHON) scripts/selfcheck.py

i18n:
	@$(PYTHON) scripts/i18n_check.py

hygiene:
	@bash scripts/check_hygiene.sh

# Needs Blender, so it stays out of check and out of CI: it asserts that the generated
# fixture's own defects are still found unaided, which is the ground truth the tools rely on.
fixture:
	@$(PYTHON) scripts/fixture_check.py

viewer-smoke:
	@$(PYTHON) scripts/viewer_smoke.py

# logics-manager is a devDependency: npm ci, then this runs the pinned version.
logics:
	npx --no-install logics-manager lint --require-status
	npx --no-install logics-manager audit --group-by-doc

package:
	@rm -rf dist *.egg-info      # a stale SOURCES.txt re-adds files package-data never listed
	@$(PYTHON) -m pip wheel . --no-deps -w dist
	@$(PYTHON) scripts/check_package.py dist/meshanvil-*.whl

package-check:
	@$(PYTHON) scripts/check_package.py dist/meshanvil-*.whl

install-check: package
	@$(PYTHON) scripts/install_check.py dist/meshanvil-*.whl

release-dry-run: check package install-check logics
	@$(PYTHON) scripts/release.py --dry-run
