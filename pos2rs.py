import pandas as pd
import numpy as np
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--position_file', help='Text file that lists SNP positions; must end with .txt')
parser.add_argument('-b', '--bim', help='Bim file name; must end with .bim')
parser.add_argument('-o', '--output', help='Output file name; preferrably ending with .txt')
args = parser.parse_args()

pfile = args.position_file
bfile = args.bim


print ''
print 'The SNP position file is: %s' % pfile
print 'The BIM file is: %s ' % bfile

if not pfile.endswith('.txt'):
	print 'Error: SNP position file must end with .txt'
	sys.exit()
if not bfile.endswith('.bim'):
	print 'Error: BIM file must end with .bim'


pvals = pd.read_csv(pfile, header=None)[0].values
pvals = np.array(sorted(pvals))
df = pd.read_table(bfile, sep='\t', header=None)
df.columns = ['Chromo', 'RS', 'IDK', 'Position', 'A1', 'A2']
df['Chromo'] = map(str, map(int, df.Chromo))
df['Position'] = map(str, map(int, df.Position))
df['Location'] = df.Chromo.values + ':' + df.Position.values
df = df[df.Location.isin(pvals)].sort_values('Location')


print 'SNP position file has %s locations listed' % len(pvals)
print 'Found RS numbers for %s SNPs' % len(df)
if len(df) != len(pvals):
	
	print 'Error: did not find all SNP to RS translations'
	print ''
	sys.exit()

else:
	df['Target'] = pvals
	if df['Target'].equals(df['Location']):
		out_df = pd.DataFrame()
		out_df['SNP'] = df.RS.values
		if args.output:
			oname = args.output
		else:
			oname = pfile.replace('.txt', '_rs.txt')
		print 'Saving list of RS numbers to: ', oname
		out_df.to_csv(oname, header=None, index=False)
		print ''
	else:
		print 'Error: List of locations does not match list translation'
		print ''
		sys.exit()