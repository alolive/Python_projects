#!/usr/bin/python3

# Bank statement contains all statement entries as
# StatementEntry python class object stored in a list.
# During initializiation of object the bank provided
# csv files subdir is parsed and loaded in object

import configuration as conf
import class_StatementEntry as se
import os, time

class BankStatements:

    def __init__( self ):

        # We want a list of StatementEntry object.
        self.statent = []

        # Time to load statements through raw csv files.
        self.statent = self.load_entries()

    def entries_count( self ):

        # Just return the number of statements entries in.

        return( len( self.statent ) )

    def sort_oldest_newest( self ):

        # Sort the StatementEntry by date from oldest
        # to newest to get a perfect BankStatement.
        senumber = len( self.statent )
        dstlist = []

        # Let's browse statement entries and sort them
        # in destination list.
        for se in self.statent:

          # Evaluate destination list size.
          dslistsize = len( dstlist )

          # Retrieve dates field.
          sedate = se.date

          # if we have no entry yet time to append.
          if dslistsize == 0:

            dstlist.append( se )

          else:

            # If we have a dstlist initialized then browse it.
            # initialize boolean to mark if we insert.
            insert = False
            for index, dse in enumerate( dstlist ):
  
              # Retrieve date field.
              dsedate = dse.date
  
              # Is sedate before current entry in dstlist ?
              if sedate < dsedate:
  
                # Save index in list for insertion.
                savedindex = index
                insert = True
                break
            
            # Did we insert something in destination list ?
            if not insert:
  
              # Time to append to destination list.
              dstlist.append( se )
       
            else:
  
              dstlist.insert( savedindex, se )

        # Replace in object itself the sorted statent list.
        self.statent = dstlist

        return( self )

    def load_entries( self ):

        # Iniatialize empty list.
        lst = []

        # Retrieve list of all bank raw csv files.
        bspath = conf.bank_statements_path
        rcsv = os.listdir( bspath )

        # Start open an read them.
        for file in rcsv:

          file2open = bspath + '/' + file
          fd = open( file2open, 'r' )
          # Parse it line by line.
          for line in fd.readlines():

            # Convert raw line in a StatementEntry.
            entry = se.StatementEntry( line )
            # Append to list.
            lst.append( entry )

        return( lst )
