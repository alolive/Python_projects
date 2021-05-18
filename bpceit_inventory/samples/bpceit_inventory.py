#!/usr/bin/env python

# Set inventory JSON file.
#inventory = "/home/ADMB0023234/projects/Ansible/output/bpceit_inventory.json"
inventory = "./json_inventory.example.save"

# Open it.
fd_inventory = open( inventory, 'r' )

# Raw display.
print fd_inventory.read()
