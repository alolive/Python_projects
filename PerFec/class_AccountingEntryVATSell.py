#!/usr/bin/python3

# Accounting entry dedicated to VAT sell moves.
# One bank statement entry equal one Accounting entry.
# Each of them is identified by a unique number.

# Importing parent class AccountingEntry
from class_AccountingEntry import AccountingEntry

# Import configuration too.
import configuration as conf

# Import WireLine class.
from class_WireLine import WireLine

class AccountingEntryVATSell( AccountingEntry ):

    def __init__( self, statemententry, acct, label, ecrnum ):

        # Journal setting.
        self.journal = 'VE'

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

        # Save initial credit.
        initialdebit = iwd['c']

        # Begin spreading between internal accounts.
        # Starting with provider account.
        # Internal WireLine 1 out of 5.
        iwd['jc'] = 'BQ'
        iwd['jl'] = conf.logs['BQ']
        iwd['cn'] = '411000'
        iwd['cl'] = conf.accounts['411000'] 
        
        # Build a wireline and append object to object list.
        w = WireLine( iwd )
        self.wires.append( w )
        
        # Bank account counterpart
        # Internal WireLine 2 out of 5.
        iwd['jc'] = 'BQ'
        iwd['jl'] = conf.logs['BQ']
        iwd['cn'] = '512000'
        iwd['cl'] = conf.accounts['512000'] 
        iwd['mr'] = 'interne '
        
        # Switch debit to credit.
        iwd['d'] = iwd['c']
        iwd['c'] = 0

        # Build a wireline and append object to object list.
        w = WireLine( iwd )
        self.wires.append( w )
        
        # Final account to move
        # Internal WireLine 3 out of 5.
        iwd['jc'] = 'VE'
        iwd['jl'] = conf.logs['VE']
        iwd['cn'] = self.acct
        iwd['cl'] = conf.accounts[self.acct] 
        
        # Switch credit to debit and remove VAT amount.
        iwd['c'] = round( iwd['d'] / 1.2, 2 )
        iwd['d'] = 0

        # Build a wireline and append object to object list.
        w = WireLine( iwd )
        self.wires.append( w )
        
        # Isolate gathered VAT.
        # Internal WireLine 4 out of 5.
        iwd['jc'] = 'VE'
        iwd['jl'] = conf.logs['VE']
        iwd['cn'] = '445711'
        iwd['cl'] = conf.accounts['445711'] 
        
        # calculate VAT amount.
        iwd['c'] = round( initialdebit - iwd['c'], 2 ) 
        iwd['d'] = 0

        # Build a wireline and append object to object list.
        w = WireLine( iwd )
        self.wires.append( w )
        
        # Credit back provider account.
        # Internal WireLine 5 out of 5.
        iwd['jc'] = 'VE'
        iwd['jl'] = conf.logs['VE']
        iwd['cn'] = '411000'
        iwd['cl'] = conf.accounts['411000'] 
        
        # Switch debit to credit.
        iwd['d'] = initialdebit
        iwd['c'] = 0

        # Build a wireline and append object to object list.
        w = WireLine( iwd )
        self.wires.append( w )
        
        # Verify perfect balance for that accounting entry.
        balanced = self.isbalanced( statemententry )
        if not balanced:

          raise ValueError( f"Amount or balance issue for ecriturenum { iwd['en'] }" )
