import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import AllChem
import sys
import codecs

if len(sys.argv) != 2:
	print("usage: python compound.py [compound name]")
	
file = codecs.open('data/compound.txt', 'w', 'utf-8')
	
compounds = pcp.get_compounds(sys.argv[1], 'name')
print("Search:{}".format(sys.argv[1]), file=file)
for compound in compounds:
	print('CID:{}\nName:{}'.format(compound.cid, compound.iupac_name), file=file)
	smiles = compound.canonical_smiles
	print('Smiles:{}'.format(smiles), file=file)
	mol_ben = Chem.MolFromSmiles(smiles)
	mol_h = Chem.AddHs(mol_ben)
	AllChem.EmbedMolecule(mol_h)
	print(Chem.MolToMolBlock(mol_h), file=file)

