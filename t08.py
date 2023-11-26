import json

def incrementer_code_postal(base_code, increment):
    return f"{base_code}-{increment:03d}"

def lire_json(nom_fichier):
    try:
        with open(nom_fichier, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []

def ecrire_json(nom_fichier, data):
    with open(nom_fichier, 'w') as file:
        json.dump(data, file, indent=4)

nom_fichier_db = 'localites_postal_codes.json'
localites = lire_json(nom_fichier_db)

def obtenir_increment(code_postal_base):
    max_increment = 0
    for entree in localites:
        if entree["Code Postal de Base"] == code_postal_base and entree["increment"] > max_increment:
            max_increment = entree["increment"]
    return max_increment + 1

def localite_existe(section_communale, localite):
    return any(entree["Section Communale"] == section_communale and entree["Localité"] == localite.lower() for entree in localites)

while True:
    section_communale = input("Entrez la section communale ou 'q' pour quitter : ")
    if section_communale.lower() == 'q':
        break

    code_postal_base = input("Entrez le code postal de base pour cette section communale (ex. 1234) : ")

    while True:
        localite = input("Entrez le nom de la localité (ou 'f' pour finir avec cette section) : ")
        localite.lower()
        if localite == 'f':
            break

        if localite_existe(section_communale, localite):
            print("Cette localité existe déjà dans cette section, veuillez en saisir une autre.")
            continue

        increment = obtenir_increment(code_postal_base)
        nouveau_code_postal = incrementer_code_postal(code_postal_base, increment)

        entree = {
            "Section Communale": section_communale,
            "Localité": localite,
            "Code Postal de Base": code_postal_base,
            "Nouveau Code Postal": nouveau_code_postal,
            "increment": increment
        }
        localites.append(entree)

        print(f"Localité: {localite} ajoutée avec le Nouveau Code Postal: {nouveau_code_postal}")

    ecrire_json(nom_fichier_db, localites)

print("Les codes postaux ont été sauvegardés dans 'localites_postal_codes.json'")

