#!/usr/bin/python3

# Import BankStatement to get all bank moves.
from class_BankStatements import BankStatements

# Import needed accouting entry types. 
from class_AccountingEntryBuy import AccountingEntryBuy
from class_AccountingEntryVATBuy import AccountingEntryVATBuy
from class_AccountingEntryIncomeTax import AccountingEntryIncomeTax
from class_AccountingEntryVAT import AccountingEntryVAT
from class_AccountingEntryVATSell import AccountingEntryVATSell
from class_AccountingEntryPersoIcan import AccountingEntryPersoIcan
from class_AccountingEntryUrssaf import AccountingEntryUrssaf

# Import needed FEC file class.
from class_FecFile import FecFile

# Import Ledger classes.
from class_GeneralLedger import GeneralLedger
from class_LedgerAccount import LedgerAccount

# Get current bank year details.
print( '%-50.50s' % 'Retrieve statement entries from raw csv files', end = '' )
year = BankStatements()
print( ' ... Done' )

# Sort the BankStatements by date.
print( '%-50.50s' % 'Sort entries from oldest to newest', end = '' )
year.sort_oldest_newest()
print( ' ... Done' )

# Count bank statement entries.
print( '%-50.50s' % 'Counting bank statement entries', end = '' )
ec = year.entries_count()
print( ' ... Done ( %3d entries found )' % ec )

# Initialize FEC file.
fec = FecFile()

# Start accounting entries creation.
print( '%-50.50s' % 'Start populating FEC file', end = '' )
for i in range( len( year.statent ) ):

  # Extract the statement entry.
  se = year.statent[i]

  ### Ascora RCP pro ###
  if se.who == 'ascora':

    # Feed arguments before instantiation.
    label = 'ascora resp civ pro'
    acnum = '616000'
    ecnum = fec.ecriturenum

    # Instantiate a non VAT buy accounting entry.
    aeb = AccountingEntryBuy( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### SG ican alliage life insurance ###
  elif se.who == 'societe generale':

    # Feed arguments before instantiation.
    label = 'comm alliage assu vie'
    acnum = '627000'
    ecnum = fec.ecriturenum

    # Instantiate a non VAT buy accounting entry.
    aeb = AccountingEntryBuy( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### Prixtel mobile phone ###
  elif se.who == 'prixtel':

    # Feed arguments before instantiation.
    label = 'forfait tel mobile'
    acnum = '626000'
    ecnum = fec.ecriturenum

    # Instantiate a VAT buy accounting entry.
    aeb = AccountingEntryVATBuy( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### Bouygtel internet box ###
  elif se.who == 'bouygues telecom':

    # Feed arguments before instantiation.
    label = 'forfait box internet'
    acnum = '626000'
    ecnum = fec.ecriturenum

    # Instantiate a VAT buy accounting entry.
    aeb = AccountingEntryVATBuy( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### AGIL trusted association ###
  elif se.who == 'agil aga':

    # Feed arguments before instantiation.
    label = 'cotisation annuelle aga'
    acnum = '622000'
    ecnum = fec.ecriturenum

    # Instantiate a VAT buy accounting entry.
    aeb = AccountingEntryVATBuy( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### Personal income tax ###
  elif se.who == 'bnp joint courant':

    # Feed arguments before instantiation.
    label = 'irpp part mensuelle'
    acnum = '108001'
    ecnum = fec.ecriturenum

    # Instantiate a VAT buy accounting entry.
    aeb = AccountingEntryIncomeTax( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### Monthly VAT payment ###
  elif se.who == 'dgfip impot':

    # Feed arguments before instantiation.
    label = 'paiement tva ca3'
    acnum = '445711'
    ecnum = fec.ecriturenum

    # Instantiate a VAT payment entry.
    aeb = AccountingEntryVAT( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### Services payment ###
  elif se.who == 'collaboration betters the world':

    # Feed arguments before instantiation.
    label = 'Rglt facture prestations'
    acnum = '706000'
    ecnum = fec.ecriturenum

    # Instantiate a VAT payment entry.
    aeb = AccountingEntryVATSell( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### Personal ican ###
  elif se.who == 'olivier allier':

    # Feed arguments before instantiation.
    if se.amount > 0:

      label = 'apport perso exploitant'

    else:
      
      label = 'prlvt perso exploitant'

    acnum = '108000'
    ecnum = fec.ecriturenum

    # Instantiate a VAT payment entry.
    aeb = AccountingEntryPersoIcan( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

  ### Urssaf ###
  elif se.who == 'urssaf ile de france':

    # Feed arguments before instantiation.
    label = 'Prlvt trimestriel urssaf'
    acnum = '431000'
    ecnum = fec.ecriturenum

    # Instantiate a urssaf ican entry.
    aeb = AccountingEntryUrssaf( se, acnum, label, ecnum )

    # Add to FEC file.
    fec.append( aeb )

print( ' ... Done' )

# Count accounting entries in FEC file.
print( '%-50.50s' % 'Counting FEC accounting entries', end = '' )
ec = fec.entries_count()
print( ' ... Done ( %3d entries found )' % ec )

# Dump FEC file.
fec.dump()

# Initialize general ledger from FEC file.
gl = GeneralLedger( fec )

# Dump General Ledger to file.
gl.dump()

exit( 0 )
