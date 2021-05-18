#
# All configuration information should be stored hereafter.
# Every module can use all parameters with only
# one import line.
#
# Changelog:
#
# v 1.0 - 2020/03/02: Creation
# v 1.1 - 2020/03/10: BPCE-IT fine facts adds
# v 1.2 - 2020/06/03: BPCE-IT inventory file name
# v 1.3 - 2020/06/29: Meta groups classification

# General vars for input/ouput snippet files.
logs_dir = "/appli/home/ADMB0023234/projects/Ansible/logs"
logs_file = "bpceit_inventory_factory.log"
output_dir = input_dir = "/appli/home/ADMB0023234/projects/Ansible/output"
output_hosts_file = input_hosts_file = "sat6_hosts_list.json"
inv_skel_file = "bpceit_inventory_skeleton.json"
inv_file = "bpceit_inventory.json"

# Satellite v6 part.
url_base = "https://bilpsat001.dom101.prdres/"
sat_user = "satenregistrement"
sat_pass = "enregistrementsat"
endpoint = "api/v2/hosts"

# Gconf part.
gconf_dir = "/mntcifs/EXPORT_GCONF/query/40"
gconf_json_file = "relations-serveurs-application.json"

#
# BPCE-IT fine facts for algorithm evaluation
#

# Below responsibles to identify monetique boxes.
# Please provide it as a python list.
monetique_resp = [ 'DPM_PMT_MON_MBO', 'DPM_PMT_MON_MFO' ]

# Below Satellite source bunker capsule.
bunker_capsule = "content_source_bilpsat003"

# Below Mars source capsule.
# Please provide it as a python list.
mars_capsule = [ 'content_source_bilpsat007', 'content_source_bilpsat008' ]

# Below responsibles to identify bigdata boxes.
# Please provide it as a python list.
bigdata_resp = [ 'DPM_PAP_DTA_PRD', 'DPM_PAP_DTA_EXD', 'DPM_PAP_DTA_PJD' ]

# Meta groups classification through hard defined list.
# Please provide it as a python list.
MAP = [ 'Projet' , 'Mise_au_point' , 'Formation' , 'Hors_Production_Divers' ,\
        'Certification_Statique' , 'GDCTech' , 'POC' , 'Certification_Dynamique' ]
INT = [ 'Recette' , 'Intgration' ]
PRD = [ 'Pr-Production' , 'Production' ]
