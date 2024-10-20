#!/usr/bin/python3

# FEC file contains all accounting entries for the year.
# and some methods to manipulate them.

import configuration as conf

class FecFile:

    # First attribute is current year.
    year = conf.year

    # SIRET number also.
    siret = conf.siret

    # End of accounting year date.
    accountingenddate = conf.accountingenddate

    def __init__( self ):

        # Also initialize ecriturenum.
        self.ecriturenum = conf.ecriturenumstart

        # List of accounting entries.
        self.acctent = []

    def entries_count( self ):

        # Just return the number of accounting entries in.

        return( len( self.acctent ) )

    def append( self, accountingentry ):

        # Just add to the list
        self.acctent.append( accountingentry )

        # Also increment ecriturenum.
        self.ecriturenum = self.ecriturenum + 1

        return( self )

    def dump( self ):

        # Construct absolute file name.
        fecfile = conf.output_dir + '/' + \
                  self.siret + 'FEC' + self.year + \
                  self.accountingenddate

        # Open it for writing.
        fd = open( fecfile, 'w' )

        # Start browsing each statement entries and display every
        # wirelines in perfect FEC formated strings.
        for ae in self.acctent:

          for wl in ae.wires:

            # Build the standard FEC string line...
            sfsl = wl.JournalCode + ';'
            sfsl = sfsl + wl.JournalLib + ';'
            sfsl = sfsl + str( wl.EcritureNum ) + ';'
            sfsl = sfsl + wl.EcritureDate + ';'
            sfsl = sfsl + wl.CompteNum + ';'
            sfsl = sfsl + '%-33s' % wl.CompteLib + ';'
            sfsl = sfsl + wl.CompAuxNum + ';'
            sfsl = sfsl + wl.CompAuxLib + ';'
            sfsl = sfsl + '%-20.20s' % wl.PieceRef + ';'
            sfsl = sfsl + wl.PieceDate + ';'
            sfsl = sfsl + '%-24.24s' % wl.EcritureLib + ';'
            sfsl = sfsl + str( '%8.2f' % wl.Debit ) + ';'
            sfsl = sfsl + str( '%8.2f' % wl.Credit ) + ';'
            sfsl = sfsl + wl.EcritureLet + ';'
            sfsl = sfsl + wl.DateLet + ';'
            sfsl = sfsl + wl.ValidDate + ';'
            sfsl = sfsl + wl.Montantdevise + ';'
            sfsl = sfsl + wl.Idevise + ';'
            sfsl = sfsl + wl.DateRglt + ';'
            sfsl = sfsl + wl.ModeRglt + ';'
            sfsl = sfsl + wl.NatOp + ';'
            sfsl = sfsl + wl.IdClient + '\n'

            # Write in file.
            fd.write( sfsl )

        # Close FEC file.
        fd.close()

        return( self )
    
    def list_accounts( self ):

        # Return a list of all internal accouting
        # accounts used in FEC file.
        acctlist = []

        for ae in self.acctent:

          for wl in ae.wires:

            if wl.CompteNum not in acctlist:

              acctlist.append( wl.CompteNum )

        return( acctlist )
