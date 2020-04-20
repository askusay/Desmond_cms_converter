'''
Uses PyMOL to convert cms structure into pdb

Supports renaming of lipid atoms (currently DPPC and DMPC only) to their amber/charmm counter parts

Also supports renaming: 
> non-standard residues (i.e. GLH) to standard (i.e. GLU)
> solvent (i.e. SPC) to HOH
> ions (i.e. Na) to charmm names (i.e. SOD)
> histidines to HIS or charmm names

-2020- ali.kusay@sydney.edu.au
'''

from __future__ import print_function

import sys
import argparse
from os import path
import logging

from pymol import cmd

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')

parser = argparse.ArgumentParser()
parser.add_argument('structure',help='Desmond input file')
parser.add_argument('output', help='Output file name')
parser.add_argument('--rename_water', dest='solvent', type=bool, help='Renames solvent atoms to HOH', default=True)
parser.add_argument('--rename_lipids', dest='lipid', type=bool, help='Rename lipids from OPLS naming to AMBER (only POPC is supported currently)', default=False)
parser.add_argument('--rename_residues', dest='poly', type=bool, help='Rename non-standard residues like ASH and GLH to their non-charged equivalents', default=False)
parser.add_argument('--rename_ions_charmm', dest='ions', type=bool, help='Renames ions from OPLS', default=False)
parser.add_argument('--rename_his', dest='his', choices=('HIS','CHARMM'), help='Rename histidines from OPLS i.e. HIP, HIE and HID to HIS or CHARMM format (HSP, HSE, HSD)')

args = parser.parse_args()

lipid_dict =  {
    'O1':'O11',
    'O2':'O12',
    'O3':'O13',
    'O4':'O14'
    }

residue_dict = {
    'ASH':'ASP',
    'GLH':'GLU',
    'LYN':'LYS',
    'CYX':'CYS'
    }

ion_dict = {
    'Na':'SOD',
    'Cl':'CLA',
    'K':'POT',
    'CA':'CAL'
    }

histidine_dict = {
    'HIE':'HSE',
    'HID':'HSD',
    'HIP':'HSP'
    }

# load structure 
cmd.load(args.structure,'structure')

# change lipid atom names
if args.lipid:
    logging.info('---Renaming lipid atoms---')
    if cmd.count_atoms('resn popc+pope') > 0:
        logging.warning('This script does not support converting POPC or POPE atom names!')
    
    for key, val in lipid_dict.items():
        out = cmd.alter('structure and resn DPPC+DMPC and name "%s"' % key, 'name = "%s"' % val)
        logging.info('Renamed %s atoms from %s to %s' % (out, key, val))

# Change Solvent name
if args.solvent:
    logging.info('---Renaming water---')
    out = cmd.alter('solvent', 'resn = "HOH"')
    logging.info('Renamed %s water residue atoms to HOH' % (out))

# Change non-standard residue names
if args.poly:
    logging.info('---Renaming non-standard residues---')
    for key, val in residue_dict.items():
        out = cmd.alter('structure and resn "%s"' % key, 'resn = "%s"' % val)
        logging.info('Renamed %s residue atom from %s to %s' % (out, key, val))

# Change ion names
if args.ions:
    logging.info('---Renaming ions---')
    for key, val in ion_dict.items():
        out = cmd.alter('structure and resn "%s"' % key, 'resn = "%s"' % val)
        logging.info('Renamed %s ions from %s to %s' % (out, key, val))

# Change histidine names
if args.his:
    logging.info('---Renaming histidines to %s naming---' % (args.his))
    if args.his == 'CHARMM':
        for key, val in histidine_dict.items():
            out = cmd.alter('structure and resn "%s"' % key, 'resn = "%s"' % val)
            logging.info('Renamed %s residue atoms from %s to %s' % (out, key, val))
    elif args.his == 'HIS':
        out = cmd.alter('structure and resn HIP+HIE+HID', 'resn = "HIS"')
        logging.info('Renamed %s histidine residue atoms to HIS' % (out))

cmd.save(args.output, 'structure')