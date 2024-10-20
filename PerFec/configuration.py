#!/usr/bin/python3

# Variables for FEC generation.
year = '2024'
accountingenddate = '1231'
siret = '421956707'
company = 'Allier Olivier - SICOA'

# Set EcritureNum starting number for this year.
ecriturenumstart = 2048

# Construct path to access bank statements.
base = '/home/sicoa/Documents'
subdir = 'justificatifs/releves_bancaires'
bank_statements_path = base + '/' + year + '/' + subdir

# Output directory for FEC and genral ledger.
output_dir = '/home/sicoa/Applications/PerFec/output'

# Logs for accounting entries.
logs = {

  'AC': 'Achats',
  'VE': 'Ventes',
  'BQ': 'Banque',
  'OD': 'OpDivr',

}

# Internal accounting details.
accounts = {

  "108000": "Compte exploitant",
  "108001": "Compte exploitant irpp",
  "108002": "Compte exploitant csg/rds",
  "401000": "Fournisseurs(cpt collectif)",
  "411000": "Clients(cpt collectif)",
  "431000": "URSSAF Ile de France",
  "442100": "Prlv source (irpp)",
  "445661": "TVA deduc achats taux normal",
  "445711": "TVA colec ventes taux normal",
  "447000": "Autres impots, taxes, etc",
  "512000": "Banque",
  "616000": "Primes assurances",
  "622000": "Remunerations et honoraires",
  "626000": "Frais postaux et telecom",
  "627000": "Services bancaires",
  "635000": "Autres impots (fisc)",
  "637000": "Autres impots (organismes)",
  "637001": "Autres impots (csg deduc)",
  "637002": "Autres impots (formation)",
  "646000": "Cotis sociales exploitant",
  "646001": "Cotis sociales maladie",
  "646002": "Cotis sociales alloc famil",
  "646003": "Cotis sociales retraite",
  "706000": "Prestations de services",

}
