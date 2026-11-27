"""AoIR executive committees, 1999 to now (AoIRchive list + current committee page).
Each term: (years, [(role, name), ...]). Portraits are matched by slug; see tools/sketch_portraits.py.
Edit here, then run:  python3 tools/sketch_portraits.py && python3 tools/build_committees.py
"""
import re, unicodedata

TERMS = [
    ("2025–2027", "current", [
        ("President", "Sarah T. Roberts"), ("Vice President", "Andra Siibak"), ("Past President", "Nicholas John"),
        ("Treasurer", "Robert W. Gehl"), ("Secretary", "Nathalie Schäfer"), ("Graduate Student Representative", "Lynrose Jane Genon"),
        ("Open Seat", "Admire Mare"), ("Open Seat", "Rebecca Scharlach"), ("Open Seat", "Meg Jing Zeng")]),
    ("2023–2025", "", [
        ("President", "Nicholas John"), ("Vice President", "Sarah T. Roberts"), ("Past President", "Tama Leaver"),
        ("Secretary", "Gabriel Pereira"), ("Treasurer", "Sam Srauy"), ("Graduate Student Representative", "Tom Divon"),
        ("Open Seat", "Sophie Bishop"), ("Open Seat", "Ariadna Matamoros-Fernández"), ("Open Seat", "Job Mwaura")]),
    ("2021–2023", "", [
        ("President", "Tama Leaver"), ("Vice President", "Nicholas John"), ("Past President", "Lynn Schofield Clark"),
        ("Secretary", "Emily van der Nagel"), ("Treasurer", "Kelly Quinn"), ("Graduate Student Representative", "Ozlem Demirkol-Tønnesen"),
        ("Open Seat", "Job Mwaura"), ("Open Seat", "Raquel Recuero"), ("Open Seat", "Cindy Tekobbe")]),
    ("2019–2021", "", [
        ("President", "Lynn Schofield Clark"), ("Vice President", "Tama Leaver"), ("Past President", "Axel Bruns"),
        ("Treasurer", "Kelly Quinn"), ("Secretary", "Katrin Tiidenberg"), ("Graduate Student Representative", "Zoë Glatt"),
        ("Open Seat", "Crystal Abidin"), ("Open Seat", "Fabio Giglietto"), ("Open Seat", "Erika Pearson")]),
    ("2017–2019", "", [
        ("President", "Axel Bruns"), ("Vice President", "Lynn Schofield Clark"), ("Past President", "Jenny Stromer-Galley"),
        ("Treasurer", "Kelly Quinn"), ("Secretary", "Katrin Tiidenberg"), ("Secretary (resigned)", "Daren Brabham"),
        ("Graduate Student Representative", "Kate Miltner"),
        ("Open Seat", "Crystal Abidin"), ("Open Seat", "Luca Rossi"), ("Open Seat", "Jack Qiu")]),
    ("2015–2017", "", [
        ("President", "Jenny Stromer-Galley"), ("Vice President", "Axel Bruns"), ("Past President", "Lori Kendall"),
        ("Treasurer", "Kelly Quinn"), ("Secretary", "Annette Markham"), ("Graduate Student Representative", "Jenny Korn"),
        ("Open Seat", "André Brock"), ("Open Seat", "Jang Hyun Kim"), ("Open Seat", "Adrienne Massanari"), ("Open Seat", "Susanna Paasonen")]),
    ("2013–2015", "", [
        ("President", "Lori Kendall"), ("Vice President", "Jenny Stromer-Galley"), ("Past President", "Alexander Halavais"),
        ("Treasurer", "Michael Zimmer"), ("Secretary", "Andrew Herman"), ("Graduate Student Representative", "Anna Lauren Hoffmann"),
        ("Open Seat", "Sun Sun Lim"), ("Open Seat", "Annette Markham"), ("Open Seat", "Kelly Quinn")]),
    ("2011–2013", "", [
        ("President", "Alexander Halavais"), ("Vice President", "Lori Kendall"), ("Past President", "Mia Consalvo"),
        ("Treasurer", "Michael Zimmer"), ("Secretary", "Catherine Middleton"), ("Graduate Student Representative", "Kelly Quinn"),
        ("Open Seat", "Andrea Baker"), ("Open Seat", "Andrew Herman"), ("Open Seat", "Soraj Hongladarom"),
        ("Systems Administrator", "Holly Kruse")]),
    ("2009–2011", "", [
        ("President", "Mia Consalvo"), ("Vice President", "Alexander Halavais"), ("Past President", "Charles Ess"),
        ("Treasurer", "Michael Zimmer"), ("Secretary", "Catherine Middleton"), ("Graduate Student Representative", "Gordon Carlson"),
        ("Open Seat", "Ted Coopman"), ("Open Seat", "Elizabeth Buchanan"), ("Open Seat", "Suely Fragoso")]),
    ("2007–2009", "", [
        ("President", "Charles Ess"), ("Vice President", "Mia Consalvo"), ("Past President", "Matthew Allen"),
        ("Treasurer", "Monica Murero"), ("Secretary", "Sabryna Cornish"), ("Graduate Student Representative", "Åsa Rosenberg"),
        ("Systems Officer", "Alexander Halavais"), ("Systems Officer", "Holly Kruse"),
        ("Open Seat", "Axel Bruns"), ("Open Seat", "Heidi Campbell"), ("Open Seat", "Marcus Foth")]),
    ("2005–2007", "", [
        ("President", "Matthew Allen"), ("Vice President", "Charles Ess"), ("Past President", "Nancy Baym"),
        ("Treasurer", "Monica Murero"), ("Secretary", "Irene Berkowitz"), ("Graduate Student Representative", "Ted Coopman"),
        ("Open Seat", "Caroline Haythornthwaite"), ("Open Seat", "Randy Kluver"), ("Open Seat", "Kate O’Riordan"),
        ("Systems Officer", "Alexander Halavais"), ("Systems Officer", "Holly Kruse")]),
    ("2003–2005", "", [
        ("President", "Nancy Baym"), ("Vice President", "Matthew Allen"), ("Past President", "Steve Jones"),
        ("Secretary", "Ulla Bunz"), ("Treasurer", "Benjamin Bates"),
        ("Open Seat", "Radhika Gajjala"), ("Open Seat", "Annette Markham"),
        ("Appointed Seat", "Randy Kluver"), ("Appointed Seat", "Monica Murero"), ("Student Seat", "Leslie Tkach Kawasaki"),
        ("Publications Officer", "Jeremy Hunsinger"), ("Publications Officer", "Charlie Breindahl")]),
    ("2001–2003", "", [
        ("President", "Steve Jones"), ("Vice President", "Nancy Baym"), ("Secretary", "Ulla Bunz"),
        ("Treasurer (on leave)", "Benjamin Bates"), ("Interim Treasurer", "Wes Shrum"),
        ("Open Seat", "David Silver"), ("Open Seat", "Barry Wellman"),
        ("Appointed Seat", "Matthew Allen"), ("Appointed Seat", "Leslie Regan Shade"), ("Student Seat", "Lisbeth Klastrup"),
        ("Publications Officer", "Jeremy Hunsinger"), ("Publications Officer", "Charlie Breindahl")]),
    ("1999–2001", "", [
        ("President", "Steve Jones"), ("Vice President", "Nancy Baym"), ("Secretary", "Matt Stoner"), ("Treasurer", "Benjamin Bates"),
        ("Open Seat", "Beth Kolko"), ("Open Seat", "Sean Cubitt"),
        ("Appointed Seat", "Diane Witmer"), ("Appointed Seat", "Fay Sudweeks"), ("Student Seat", "Matt Williams"),
        ("Publications Officer", "Jeremy Hunsinger"), ("Publications Officer", "Charlie Breindahl")]),
]


def slugify(name):
    for a, b in (("ø", "o"), ("Ø", "O"), ("æ", "ae"), ("ß", "ss"), ("’", ""), ("'", "")):
        name = name.replace(a, b)
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = s.replace(".", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


PEOPLE = {}
for _y, _n, members in TERMS:
    for _r, name in members:
        PEOPLE.setdefault(slugify(name), name)
