#!/usr/bin/python3

# Ledger to summarize each account state and balance
# and some methods to manipulate them.

import configuration as conf
import datetime
from class_FecFile import FecFile
from class_LedgerAccount import LedgerAccount

class GeneralLedger:

    # First attribute is current year.
    year = conf.year

    # SIRET number also.
    siret = conf.siret

    # Get company name.
    company = conf.company

    # Define formating of string to display
    # general ledger header.
    fheader = '%-32s | %-24s | %35s'
    seplength = 98 

    def __init__( self, fecfile ):

        # Get Fec file.
        self.fecfile = fecfile

        # Get list of all internal accounting accounts.
        self.accounts = []
        self.accounts = self.fecfile.list_accounts()

        # Get all ledger accounts.
        self.ledgeraccounts = []
        self.ledgeraccounts = self.get_ledgeraccounts()

    def get_ledgeraccounts( self ):

        # For all accounts get ledger form with
        # all moves in and summary.
        for account in self.accounts:

          # Feed one LedgerAccount.
          la = LedgerAccount( self.fecfile, account )

          # Just append to ledgeraccounts.
          self.ledgeraccounts.append( la )

        return( self.ledgeraccounts )

    def dump( self ):

        # Construct absolute general ledger file name.
        galedger = conf.output_dir + '/' + \
                   self.siret + 'GeneralLegder' + self.year + \
                   '.txt'

        # Open it for writing.
        fd = open( galedger, 'w' )

        # Begin with a decent header.
        # one separator, two lines with three fields
        # and one separator with newline.
        
        # First line.
        ex = 'Exercice ' + self.year
        d = datetime.datetime.today().strftime('%d %b %Y')
        ed = 'Edition le ' + d
        line1 = self.fheader % ( self.company, ex , ed )
     
        # Second line.
        f1 = 'Monnaie tenue / edition : EUR'
        f2 = 'GRAND LIVRE GENERAL'
        f3 = 'siret : ' + self.siret
        line2 = self.fheader % ( f1, f2, f3 )

        # Write header in file.
        fd.write( self.separator() + '\n' )
        fd.write( line1 + '\n' )
        fd.write( self.separator() + '\n' )
        fd.write( line2 + '\n' )
        fd.write( self.separator() + '\n' + '\n' )

        # Start browsing each ledger account entry.
        for la in self.ledgeraccounts:

          # Display content.
          for i in range( len( la.ledgerlines ) ):

            fd.write( la.ledgerlines[i] + '\n' )

        # Close ledger file.
        fd.close()

        return( self )

    def separator( self ):

        sep = ''
        for i in range( 1, self.seplength ):

          sep = sep + '-'

        return( sep )

