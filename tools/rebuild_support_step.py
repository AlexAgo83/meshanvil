"""Regenerer le support moteur haut en B-rep et l'exporter en STEP.

Blender n'ecrit pas de STEP, et passer par un maillage donnerait un STEP tesselle : les
bossages Ø52 deviendraient 32 facettes planes, sans diametre cotable ni percage
reconnaissable en CAO. La piece ayant ete construite a partir de nombres et non sculptee,
elle se rejoue ici en primitives exactes -- faces cylindriques reelles, fichier leger.

Les cotes ci-dessous sont celles relevees sur l'assemblage : entre-joues des chapes 62,3 mm,
alesage chape Ø13,98 a X 1876,7 / Z 316,2, face moteur a Z 196 avec 2 trous Ø9,66 entraxe 47.

    <FreeCAD>/Contents/Resources/bin/freecadcmd tools/rebuild_support_step.py [-- <sortie.stp>]

`FreeCAD -c` execute le script puis reste sur son invite : c'est freecadcmd qu'il faut.
"""
import os
import sys
import FreeCAD as App
import Part

# Derive from this file's location: the repository must not carry anyone's home path.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = (sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv
       else os.path.join(ROOT, "work", "out", "support_moteur_haut.stp"))

PLATINE = [(196, 1812, 1858, -52, 27), (208, 1814, 1856, -50, 25)]
BRAS_G = [(205, 1816, 1852, -42, -6), (230, 1820, 1852, -60, -24),
          (256, 1828, 1856, -92, -56), (288, 1848, 1884, -104, -58),
          (316, 1856, 1898, -112, -58)]
BRAS_D = [(205, 1816, 1852, -2, 30), (230, 1820, 1852, 18, 54),
          (256, 1828, 1856, 52, 88), (288, 1848, 1884, 54, 100),
          (316, 1856, 1898, 54, 108)]
BOSS_Y = (-85.65, 81.3)
BOSS_X, BOSS_Z = 1876.7, 316.2
BOSS_R, BOSS_L, BAGUE_R = 26.0, 61.4, 18.0
VIS = ((1831.4, 11.1), (1831.4, -35.9))
VIS_R, LAMAGE_R, LAMAGE_H = 4.5, 8.0, 4.0


def rectangle(z, x0, x1, y0, y1):
    p = [App.Vector(x0, y0, z), App.Vector(x1, y0, z),
         App.Vector(x1, y1, z), App.Vector(x0, y1, z), App.Vector(x0, y0, z)]
    return Part.makePolygon(p)


def loft(rows):
    """Regle et solide : les faces entre sections restent planes, comme dans le modele source."""
    return Part.makeLoft([rectangle(*r) for r in rows], True, True)


def cylindre_y(radius, length, x, y_centre, z):
    return Part.makeCylinder(radius, length,
                             App.Vector(x, y_centre - length / 2.0, z), App.Vector(0, 1, 0))


def cylindre_z(radius, length, x, y, z_bas):
    return Part.makeCylinder(radius, length, App.Vector(x, y, z_bas), App.Vector(0, 0, 1))


piece = loft(PLATINE)
for rows in (BRAS_G, BRAS_D):
    piece = piece.fuse(loft(rows))
for y in BOSS_Y:
    piece = piece.fuse(cylindre_y(BOSS_R, BOSS_L, BOSS_X, y, BOSS_Z))
piece = piece.removeSplitter()

for y in BOSS_Y:
    piece = piece.cut(cylindre_y(BAGUE_R, 90.0, BOSS_X, y, BOSS_Z))
for x, y in VIS:
    piece = piece.cut(cylindre_z(VIS_R, 60.0, x, y, 180.0))
    piece = piece.cut(cylindre_z(LAMAGE_R, LAMAGE_H + 2, x, y, 208.0 - LAMAGE_H))
piece = piece.removeSplitter()

box = piece.BoundBox
faces_cyl = sum(1 for f in piece.Faces if f.Surface.TypeId == "Part::GeomCylinder")
print("solide valide : %s | %d faces dont %d cylindriques | %d aretes"
      % (piece.isValid(), len(piece.Faces), faces_cyl, len(piece.Edges)))
print("volume %.1f cm3 | encombrement mm X %.0f..%.0f Y %.0f..%.0f Z %.0f..%.0f"
      % (piece.Volume / 1000.0, box.XMin, box.XMax, box.YMin, box.YMax, box.ZMin, box.ZMax))
piece.exportStep(OUT)
print("ecrit :", OUT)
