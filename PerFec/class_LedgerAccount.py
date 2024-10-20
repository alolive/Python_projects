#!/usr/bin/python3

# Ledger to summarize each account state and balance
# and some methods to manipulate them.

import configuration as conf

class LedgerAccount:

    # Define formating of string to display
    # ledger account properly.
    fheader = '%-64s'
    fdate = '%8s '
    fjournal = '| %2s '
    flabel = '| %-16.16s - %-24.24s '
    fdebit = '| %9.2f '
    fcredit = '| %9.2f '
    fbalance = '| %9.2f '
    fbalanceletter = '%1s'
    voidcolumn = '|           '
    seplength = 98 
    ffooter = '%59s '

    def __init__( self, fecfile, acctnum ):

        # Get Fec file.
        self.fecfile = fecfile
 
        # Set account number as an attribute.
        self.accountnumber = acctnum

        # Header.
        self.header = acctnum + ' : ' + conf.accounts[ acctnum ]

        # Footer.
        self.footer = 'Total pour le compte : ' + acctnum

        # Lines as a list.
        self.ledgerlines = []
        self.ledgerlines = self.get_ledgerlines()

    def get_ledgerlines( self ):
        
        # Start with header.
        self.ledgerlines.append( self.separator() )
        self.ledgerlines.append( self.fheader % self.header )
        self.ledgerlines.append( self.separator() )

        # Start with nul balance, totaldebit
        # and totalcredit.
        balance = 0
        totaldebit = 0
        totalcredit = 0

        # Filter FEC file to get all accountnumber moves
        for ae in self.fecfile.acctent:

          for wl in ae.wires:

            # Trigger only the correct account...
            if wl.CompteNum == self.accountnumber:

              lls = self.fdate % wl.DateRglt
              lls = lls + self.fjournal % wl.JournalCode
              lls = lls + self.flabel % ( wl.PieceRef, wl.EcritureLib )

              # Caution with debits
              totaldebit = totaldebit + wl.Debit
              if wl.Debit != 0:

                lls = lls + self.fdebit % wl.Debit

              else:      

                lls = lls + self.voidcolumn

              # Caution with credits
              totalcredit = totalcredit + wl.Credit
              if wl.Credit != 0:

                lls = lls + self.fcredit % wl.Credit

              else:      

                lls = lls + self.voidcolumn

              # Continue with last balance field.
              balance = balance + wl.Credit - wl.Debit
              lls = lls + self.fbalance % abs( balance )
    
              # We have a credit situation.
              if balance > 0:
    
                balanceletter = 'C'
                lls = lls + self.fbalanceletter % balanceletter
    
              # We have a dedit situation.
              if balance < 0:
    
                balanceletter = 'D'
                lls = lls + self.fbalanceletter % balanceletter
    
              # We have a well balanced situation.
              if balance == 0:
    
                balanceletter = ' '
                lls = lls + self.fbalanceletter % balanceletter

              self.ledgerlines.append( lls ) 

        # Time to display footer.
        self.ledgerlines.append( self.separator() )
        lls = self.ffooter % self.footer
        lls = lls + self.fdebit % totaldebit
        lls = lls + self.fcredit % totalcredit
        lls = lls + self.fbalance % abs( balance ) 
        lls = lls + balanceletter
        self.ledgerlines.append( lls ) 
        self.ledgerlines.append( self.separator() )

        return( self.ledgerlines )

    def separator( self ):

        sep = ''
        for i in range( 1, self.seplength ):

          sep = sep + '-'

        return( sep )
