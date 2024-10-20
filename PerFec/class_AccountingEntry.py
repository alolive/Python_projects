#!/usr/bin/python3

# Accounting entry contains multiple wire lines.
# One bank statement entry equal one Accounting entry.
# Each of them is identified by a unique number.

import configuration as conf
import random

class AccountingEntry:

    EcritureLet = ''
    DateLet = ''
    Montantdevise = ''
    Idevise = ''
    IdClient = ''

    def get_ecrituredate( self, statemententry ):
        
        # Each ecrituredate is calculated that way:
        # between the first and the fifth of next month.
        if statemententry.date.month != 12:

          y = statemententry.date.year
          m = statemententry.date.month + 1
          d = '0' + str( random.randint(1,5) )

        else:

          y = statemententry.date.year + 1
          m = '01'
          d = '0' + str( random.randint(1,5) )
          
        # Build a FEC format date.
        ecrdate = str( y ) + f'{m:02d}' + str( d )

        return( ecrdate )

    def get_validdate( self, statemententry ):

        # Each validationdate is calculated that way:
        # between the tenth and the twelves of th first
        # month of next quarter.next quarter.

        y = statemententry.date.year
        d = str( random.randint(10,12) )

        if statemententry.date.month <= 3:

          # Build a FEC format date.
          validdate = str( y ) + '04' + str( d )

        if statemententry.date.month >= 4 and \
           statemententry.date.month <= 6:

          # Build a FEC format date.
          validdate = str( y ) + '07' + str( d )

        if statemententry.date.month >= 7 and \
           statemententry.date.month <= 9:

          # Build a FEC format date.
          validdate = str( y ) + '10' + str( d )

        if statemententry.date.month >= 10:

          y = statemententry.date.year + 1

          # Build a FEC format date.
          validdate = str( y ) + '01' + str( d )

        return( validdate )

    def get_piecedate( self, statemententry):

        if statemententry.who == 'ascora':

          # For Ascora RCP we have a year invoice only.
          # Around the 26 of december.
          y = statemententry.date.year - 1
          m = '12'
          d = '26'
            
          # Build a FEC format date.
          piecedate = str( y ) + str( m ) + str( d )
          
          return( piecedate )

    def get_debit( self, statemententry):

        if statemententry.amount < 0:

          debit = round( abs( statemententry.amount ), 2 )

        else:

          debit = 0

        return( debit )

    def get_credit( self, statemententry):

        if statemententry.amount > 0:

          credit = round( abs( statemententry.amount ), 2 )

        else:

          credit = 0

        return( credit )

    def get_daterglt( self, statemententry):

        y = statemententry.date.year
        m = statemententry.date.month
        d = statemententry.date.day
            
        # Build a FEC format date.
        daterglt = str( y ) + f'{m:02d}' + f'{d:02d}'
          
        return( daterglt )

    def isbalanced( self, statemententry ):

        # Sum up credits in internal wirelines.
        wireslength = len( self.wires )
        credits = 0
        for i in range( wireslength ):

          credits = credits + self.wires[i].Credit
 
        # Sum up debits in internal wirelines.
        debits = 0
        for i in range( wireslength ):

          debits = debits + self.wires[i].Debit

        # Check if debit or credit is equal to statement
        # entry amount modulo the number of accounting moves.
        amount = abs( statemententry.amount )
        cmodulo = round( credits, 2 ) % amount
        dmodulo = round( debits, 2 ) % amount

        if cmodulo != 0 or dmodulo != 0:

          return( False )

        else:

          return( True )
