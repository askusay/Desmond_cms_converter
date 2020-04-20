# Desmond-cms-converter

This is a simple script that converts .cms to .pdb format using PyMOL and renames residues/atoms to facilitate parameterisation using AMBER/CHARMM

**Renaming**: water residues, lipid atoms (only DPPC and DMPC), charged residues to neutral, ions to CHARMM naming, histidines to "HIS" or CHARMM naming

**Requires**: PyMOL from [command line](https://pymolwiki.org/index.php/Launching_From_a_Script)
