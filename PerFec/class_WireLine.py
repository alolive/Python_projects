#!/usr/bin/python3

# Single line of FEC file object with all wanted fields.
# To be used for every transfert between internal accounts.

class WireLine:

    def __init__( self, internalwiredict ):

        # Get from child AccountEntry class.
        self.JournalCode = internalwiredict['jc']
    
        # Get from journal json conf. 
        self.JournalLib = internalwiredict['jl']

        # Get from parent method AccountEntry class. 
        self.EcritureNum = internalwiredict['en']

        # Get from parent method AccountEntry class. 
        self.EcritureDate = internalwiredict['ed']

        # Get from child AccountEntry class.
        self.CompteNum = internalwiredict['cn']

        # Get from accounts dict in conf.
        self.CompteLib = internalwiredict['cl']

        # Get from AUX conf and StatementEntry class.
        self.CompAuxNum = internalwiredict['can']

        # Get from AUX conf and StatementEntry class.
        self.CompAuxLib = internalwiredict['cal']

        # Get from StatementEntry class.
        self.PieceRef = internalwiredict['pr']

        # Get from parent method AccountEntry class. 
        self.PieceDate = internalwiredict['pd']

        # Get from AccountEntryBuy arguments.
        self.EcritureLib = internalwiredict['el']

        # Get from StatementEntry class.
        self.Debit = internalwiredict['d']

        # Get from StatementEntry class.
        self.Credit = internalwiredict['c']

        # Get from parent AccountEntry class.
        self.EcritureLet = internalwiredict['elt']

        # Get from parent AccountEntry class.
        self.DateLet = internalwiredict['dlt']

        # Get from parent method AccountEntry class. 
        self.ValidDate = internalwiredict['vd']

        # Get from parent AccountEntry class. 
        self.Montantdevise = internalwiredict['md']

        # Get from parent AccountEntry class. 
        self.Idevise = internalwiredict['id']

        # Get from StatementEntry class.
        self.DateRglt = internalwiredict['dr']

        # Get from StatementEntry class.
        self.ModeRglt = internalwiredict['mr']

        # Get from StatementEntry class.
        self.NatOp = internalwiredict['no']

        # Get from parent AccountEntry class. 
        self.IdClient = internalwiredict['ic']
