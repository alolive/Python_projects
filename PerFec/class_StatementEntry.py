#!/usr/bin/python3

# Statement entry is a single line of CSV file provided
# by bank itself. Each valuable field is modelized and
# stored.

import datetime, re

class StatementEntry:

    currency = 'EUR'

    def __init__( self, csvline ):

        # Datetime object for date.
        self.date = self.get_date( csvline )

        # Type of entry (str).
        self.type = self.get_type( csvline )
        if self.type == '':

          raise ValueError( f'Cannot identify bank type in { csvline }' )

        # Sender or receiver name (str).
        # DE: value or POUR: value
        self.who = self.get_who( csvline )
        if self.who == '':

          raise ValueError( f'Cannot identify who in { csvline }' )


        # Identifiant of operation (str).
        self.id = self.get_id( csvline )

        # Reason of operation (str).
        self.reason = self.get_reason( csvline )

        # Reference of operation if any (str).
        self.reference = self.get_ref( csvline )

        # Amount. Positive or negative (float).
        self.amount = self.get_amount( csvline )

        # We should have at least a reason or a ref.
        if self.reason == '' and self.reference == '':

          raise ValueError( f'Missing reason o reference in { csvline }' )

    def get_date( self, csvline ):

        fields = csvline.split( ';' )
        ds = fields[0]
        do = datetime.datetime.strptime( ds, '%d/%m/%Y' )
        return( do )

    def get_type( self, csvline ):

        fields = csvline.split( ';' )
        # Keep only the first three.
        typefield = fields[1].split()[:3]

        if 'PRELEVEMENT' in typefield or \
           'PRLV'        in typefield or \
           'COMMISSION'  in typefield:

          return( 'prlvment' )
        
        if 'VIR' in typefield:

          return( 'virement' )

        if 'CHEQUE' in typefield:

          return( 'cheque  ' )

        else:

          return( '' )

    def get_subfield( self, keyword, string ):

        # All allowed keywords.
        keywords = [ 'DE', 'POUR', 'ID', 'MOTIF', 'REF' ]

        # We first remove all until keyword.
        pattern = r'^.*' + keyword + ':'
        s1 = re.sub( pattern, '', string )        

        # We then remove every keywords other parts
        # if any.
        for kw in keywords:

          pattern = kw + ':' + r'.*$'
          s2 = re.sub( pattern, '', s1 )        
          s1 = s2

        # We lower, strip and cut after 32 chars.
        subfield = s1.lower().strip()[:32]

        return( subfield )

    def get_who( self, csvline ):

        who = ''
        fields = csvline.split( ';' )
        # First case ican line.
        ican = re.search( 'DE:', fields[1] )
        if ican:

          who = self.get_subfield( 'DE', fields[1] )

        # Second case transfert line.
        trsf = re.search( 'POUR:', fields[1] )
        if trsf:

          who = self.get_subfield( 'POUR', fields[1] )

        # Small adjustments for me and urssaf.
        gotme = re.search( 'olivier allier', who )
        if gotme:

          who = 'olivier allier'
       
        goturssaf = re.search( 'urssaf.*france', who )
        if goturssaf:

          who = 'urssaf ile de france'
 
        return( who )

    def get_id( self, csvline ):

        id = ''
        fields = csvline.split( ';' )
        gotid = re.search( 'ID:', fields[1] )
        if gotid:

          id = self.get_subfield( 'ID', fields[1] )

        return( id )

    def get_reason( self, csvline ):

        reason = ''
        fields = csvline.split( ';' )
        gotreason = re.search( 'MOTIF:', fields[1] )
        if gotreason:

          reason = self.get_subfield( 'MOTIF', fields[1] )

        return( reason )

    def get_ref( self, csvline ):

        ref = ''
        fields = csvline.split( ';' )
        gotref = re.search( 'REF:', fields[1] )
        if gotref:

          ref = self.get_subfield( 'REF', fields[1] )

        else:

          # Do some complement as we know some bad guys
          # failing to provide REF field...
          gotsg = re.search( 'societe', self.who )
          if gotsg:

            # We are facing monthly life insurance ican.
            ref = 'sgcaav' + str( self.date.year ) + f'{self.date.month:02d}' 

          goturssaf = re.search( 'urssaf', self.who )
          if goturssaf:

            # We are facing a quarter year ican.
            ref = 'urssaf' + self.reason.split()[2]

          gotprixtel = re.search( 'prixtel', self.who )
          if gotprixtel:

            # We convert motif to ref...
            ref = self.reason.split('/')[1]

        # Also refining some refs with motifs for better clarity.
        gotvat = re.search( 'dgfip impot', self.who )
        if gotvat:

          ref = self.reason

        return( ref )

    def get_amount( self, csvline ):

        amount = 0
        fields = csvline.split( ';' )
        # Convert coma to dot.
        amounts = fields[2].replace( ',' , '.' )
        # Convert to float for future arithmetics.
        amount = float( amounts )

        return( amount )
