#!/usr/bin/python3

# Accounting entry dedicated to quarter Urssaf icans.
# One bank statement entry equal one Accounting entry.
# Each of them is identified by a unique number.

# Importing parent class AccountingEntry
from class_AccountingEntry import AccountingEntry

# Import configuration too.
import configuration as conf

# Import specific Urssaf ican spreading too.
import urssaf

# Import WireLine class.
from class_WireLine import WireLine

class AccountingEntryUrssaf( AccountingEntry ):

    def __init__( self, statemententry, acct, label, ecrnum ):

        # Journal setting.
        self.journal = 'OD'

        # Final account to be moved.
        self.acct = acct

        # Retrieve ecriturenum.
        self.ecriturenum = ecrnum

        # This object will be fill with a wireline list.
        self.wires = []

        # Let start with general internalwiredict feeding.
        iwd = {

          'jc': '',
          'jl': '',
          'en': self.ecriturenum,
          'ed': self.get_ecrituredate( statemententry ),
          'cn': '',
          'cl': '',
          'can': '',
          'cal': '',
          'pr': statemententry.reference, 
          'pd': self.get_piecedate( statemententry ), 
          'el': label,
          'd': self.get_debit( statemententry ),
          'c': self.get_credit( statemententry ),
          'elt': self.EcritureLet,
          'dlt': self.DateLet,
          'vd': self.get_validdate( statemententry ),
          'md': self.Montantdevise,
          'id': self.Idevise,
          'dr': self.get_daterglt( statemententry ),
          'mr': statemententry.type,
          'no': '',
          'ic': self.IdClient,
  
        }

        # If we have no piecedate defined, we've been taught
        # to put the same date as ecriture, so:
        if not iwd['pd']:

          iwd['pd'] = iwd['ed']

        # Begin spreading between internal accounts.
        # Starting with provider account.
        # Internal WireLine 1 out of 4.
        iwd['jc'] = 'BQ'
        iwd['jl'] = conf.logs['BQ']
        iwd['cn'] = '431000'
        iwd['cl'] = conf.accounts['431000'] 
        
        # Build a wireline and append object to object list.
        w = WireLine( iwd )
        self.wires.append( w )
        
        # Bank account counterpart
        # Internal WireLine 2 out of 4.
        iwd['jc'] = 'BQ'
        iwd['jl'] = conf.logs['BQ']
        iwd['cn'] = '512000'
        iwd['cl'] = conf.accounts['512000'] 
        iwd['mr'] = 'interne '
        
        # Switch debit to credit.
        iwd['c'] = iwd['d']
        iwd['d'] = 0

        # Build a wireline and append object to object list.
        w = WireLine( iwd )
        self.wires.append( w )
        
        # 
        # For each accounting account found in Urssaf quarter
        # dictionnary we build a wireline and a counterpart
        # wireline in urssaf accounting account.
        #

        # Switch journal
        iwd['jc'] = 'OD'
        iwd['jl'] = conf.logs['OD']

        # Parse quarter specifications.
        for (account, amount) in urssaf.quarters[iwd['pr']].items():

          # First wireline for final account to debit.
          iwd['cn'] = account
          iwd['cl'] = conf.accounts[account] 
          iwd['c'] = 0
          iwd['d'] = amount
          w = WireLine( iwd )
          self.wires.append( w )
        
          # second wireline for urssaf account to credit back.
          iwd['cn'] = '431000'
          iwd['cl'] = conf.accounts['431000'] 
          iwd['c'] = iwd['d']
          iwd['d'] = 0
          w = WireLine( iwd )
          self.wires.append( w )

        # Verify perfect balance for that accounting entry.
        balanced = self.isbalanced( statemententry )
        if not balanced:

          raise ValueError( f"Amount or balance issue for ecriturenum { iwd['en'] }" )

