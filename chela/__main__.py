from configparser import ConfigParser
from chela import check_formula, csv_to_dataframe
import argparse

def main():
    #Define the parser
    my_parser = argparse.ArgumentParser(prog='chela',
                                        description = "Handle chemical formulas",
                                        usage = '%(prog)s [options]',
                                        )
    #Add option -c to use check_formula function
    my_parser.add_argument('-check',
                          action= 'store',
                          metavar=('formula'),
                          help="Check correctness chemical formula",
                          )

    #Add option -d to use csv_to_dataframe function
    my_parser.add_argument('-dataframe',
                           nargs=2,
                           metavar=('SOURCE','DEST'),
                           action='store',
                           help="Transform chemical formula into dataframe Source Dest",
                           )
    #Flag if need to add header into the dataframe
    my_parser.add_argument('--header',
                           action='store_true',
                           default=False,
                           help="Flag if csv file doesn't contain an header",
                           )
    #Flag if csv fine contain wrong chemical formula that have to be ignored
    my_parser.add_argument('--robust',
                          action='store_true',
                          default=False,
                          help="Flag if csv file contain wrong formula that will be excluded from the dataframe",
                          )


    #Parse the args
    args = my_parser.parse_args()

    if args.check:
        print('Checking...')
        check_formula(args.check)
        print('Correct formula.')

    elif args.dataframe:
        print('Transforming file into a Dataframe...')
        source, destination = args.dataframe
        header = args.header
        robust = args.robust
        dataframe = csv_to_dataframe(path = source,header=header,robust=robust)
        dataframe.to_csv(destination,index=False)
        print('Dataframe saved.')



if __name__ == "__main__":
    main()
