#!/usr/env python

from pathlib import Path
import pandas as pd

import matplotlib as mpl
from dateutil import parser

# %matplotlib inline
mpl.use('pgf')
pgf_with_custom_preamble = {
    'text.usetex': True,    # use inline math for ticks
    'pgf.rcfonts': False,   # don't setup fonts from rc parameters
    'pgf.texsystem': 'xelatex',
    'verbose.level': 'debug-annoying',
    "pgf.preamble": [
        r'\usepackage{fontspec}',
        r"""\usepackage{fontspec}
\setsansfont{HelveticaLTStd-Light}[
Extension=.otf,
BoldFont=HelveticaLTStd-Bold,
ItalicFont=HelveticaLTStd-LightObl,
BoldItalicFont=HelveticaLTStd-BoldObl,
]
\setmainfont{HelveticaLTStd-Light}[
Extension=.otf,
BoldFont=HelveticaLTStd-Bold,
ItalicFont=HelveticaLTStd-LightObl,
BoldItalicFont=HelveticaLTStd-BoldObl,
]
""",
        r'\renewcommand\familydefault{\sfdefault}',
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)


def get_parser():
    """Build parser object"""
    from argparse import ArgumentParser
    from argparse import RawTextHelpFormatter

    parser = ArgumentParser(description='MRIQC-WebAPI: massaging bson dumps',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('input_folder', action='store', type=Path, help='input')
    parser.add_argument('output_file', action='store', type=Path, help='output')
    return parser


def main():
    import matplotlib.pyplot as plt
    import seaborn as sns
    args = get_parser().parse_args()
    df_t1w_unique = pd.read_csv(args.input_folder / 'T1w.csv')
    df_t2w_unique = pd.read_csv(args.input_folder / 'T2w.csv')
    df_bold_unique = pd.read_csv(args.input_folder / 'bold.csv')

    plt.clf()

    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1)

    dates_t1w_u = [parser.parse(d) for d in df_t1w_unique['created'].values]
    dates_t1w_u.sort()

    dates_t2w_u = [parser.parse(d) for d in df_t2w_unique['created'].values]
    dates_t2w_u.sort()

    dates_bold_u = [parser.parse(d) for d in df_bold_unique['created'].values]
    dates_bold_u.sort()
    # mindate = dates_t1w[0]
    ax = plt.subplot(111)
    ax.plot(dates_t1w_u, list(range(1, len(dates_t1w_u) + 1)), label='T1w')
    ax.plot(dates_t2w_u, list(range(1, len(dates_t2w_u) + 1)), label='T2w')
    ax.plot(dates_bold_u, list(range(1, len(dates_bold_u) + 1)), label='BOLD')
    ax.set_ylabel('Thousands of unique records in database')
    ax.grid(False)
    sns.despine(offset=10, trim=True)
    ax.legend()
    ax.set_yticks([0, 1e4, 2e4, 3e4, 4e4, 5e4, 6e4])
    ax.set_yticklabels(['0', '10', '20', '30', '40', '50', '60'])
    plt.xticks(rotation=60)
    plt.savefig(str(args.output_file), dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    main()
