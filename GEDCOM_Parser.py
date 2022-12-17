# imported modules

import math
import numpy
from prettytable import PrettyTable
import os
import uuid
import datetime


#Class to handle Individual data
class ClassForInd :
    #Columns for the Ind table
    columns = [ 'ID' , 'Name' , 'Gender' , 'Birthday' , 'Age' , 'Alive' , 'Death' , 'Child' , 'Spouse' ]

    # dictionary of individuals
    individual_dictionary = {
        'NAME' : 'name' ,
        'SEX' : 'sex' ,
        'BIRT' : 'birth_date' ,
        'DEAT' : 'death_date' ,
        'FAMC' : 'fam_c' ,
        'FAMS' : 'fam_s'
    }

    def __init__ ( self , indi_id ) :

        self.indi_id = indi_id
        self.name = ''
        self.sex = ''
        self.birth_date = None
        self.death_date = None
        self.fam_c = 'NA'
        self.fam_s = 'NA'
        self.data = [ ]

    @property
    def l_num ( self ) :

        iterator = iter ( self.data )
        dict_ele = { }

        for l in iterator :
            if l [ 1 ] in ('INDI' , 'NAME' , 'SEX' , 'FAMC' , 'FAMS') :
                dict_ele [ l [ 1 ] ] = l [ 3 ]

            elif l [ 1 ] in ('BIRT' , 'DEAT') :
                next_line = next ( iterator )
                dict_ele [ l [ 1 ] ] = next_line [ 3 ]

        return dict_ele

    @property
    def age ( self ) :

        if self.dob :
            if not self.death_date :
                a = GedcomParser.getDate - self.dob
            else :
                a = self.death_date - self.dob
            return (a.days + a.seconds // 86400) // 365

    #Check if the person is alive or not
    @property
    def alive ( self ) :

        a = True
        if self.death_date :
            a = False

        return a

    #returns the value of date of birth
    @property
    def dob ( self ) :

        if self.birth_date :
            dob = datetime.datetime ( self.birth_date.year , self.birth_date.month , self.birth_date.day )
            return dob

    @property
    def full_name ( self ) :

        if self.name:
            if len ( self.name.split ( '/' ) ) >= 2 :
                n = [ x.strip ( ) for x in self.name.split ( '/' ) ]
                return { 'firstName' : n [ 0 ] , 'lastName' : n [ 1 ] }

    def ptbl_row ( self ) :

        return [ self.indi_id , self.name , self.sex , self.dob.strftime ( "%Y-%m-%d" ) , self.age , self.alive ,
                 self.death_date.strftime ( "%Y-%m-%d" ) if self.death_date else 'NA' , self.fam_c , self.fam_s ]
    def __str__ ( self ) :

        #print(self.name ,self.sex , self.birth_date , self.death_date , self.indi_id)
        return ""

# Class to handle family data
class ClassForFam :

    # Columns for the family table
    columns = [ 'ID' , 'Married' , 'Divorced' , 'Husband ID' , 'Husband Name' , 'Wife ID' , 'Wife Name' , 'Children' ]

    # dictionary of family
    family_dictionary = {
        'MARR' : 'marriage_date' ,
        'HUSB' : 'husband' ,
        'WIFE' : 'wife' ,
        'DIV' : 'divorce_date' ,
        'CHIL' : 'children' ,
    }


    def __init__ ( self , fam_id ) :

        self.fam_id = fam_id
        self.date_of_wedding = None
        self.date_of_divorce = None
        self.husband = None
        self.wife = None
        self.child_lst = [ ]
        self.element_list = [ ]

    @property
    def l_num ( self ) :

        iterator = iter ( self.element_list )
        dict_ele = { }
        children_lst = [ ]
        for l in iterator :
            if l [ 1 ] in ('FAM' , 'HUSB' , 'WIFE') :
                dict_ele [ l [ 1 ] ] = l [ 3 ]

            elif l [ 1 ] in ('MARR' , 'DIV') :
                next_line = next ( iterator )
                dict_ele [ l [ 1 ] ] = next_line [ 3 ]

            elif l [ 1 ] == 'CHIL' :
                children_lst.append ( (l [ 2 ] , l [ 3 ]) )

        dict_ele [ 'CHIL' ] = children_lst
        return dict_ele

    @property
    def divorced ( self ) :

        divorced = False
        if self.date_of_divorce :
            divorced = True
        return divorced

    def __str__ ( self ) :

        #print(self.date_of_wedding ,self.date_of_divorce , self.wife , self.husband , self.fam_id)
        return ""

# Parser to process GEDCOM data
class GedcomParser (  ClassForFam, ClassForInd ):

    # tags to be excempted and handled differently
    exp_list = [ 'FAM' , 'INDI' ]

    # dictionary of tags
    dict_true = { '0' : [ 'INDI' , 'FAM' , 'HEAD' , 'TRLR' , 'NOTE' ] ,
                  '1' : [ 'NAME' , 'SEX' , 'BIRT' , 'DEAT' , 'FAMC' , 'FAMS' , 'MARR' , 'HUSB' , 'WIFE' , 'CHIL' ,
                          'DIV' ] ,
                  '2' : [ 'DATE' ] }

    getDate = datetime.datetime.today ( )
    dateFormatter = "%Y-%m-%d"


    # Initializing class
    def __init__ ( self , path , pt = False , write = False ) :
        self.path = path
        self.individuals = dict ( )
        self.families = dict ( )
        self.original_data = [ ]
        self.loggerComment = [ ]
        self.logError = [ ]
        self.invalid_tags = [ ]
        self.updated_file = [ ]

        if not os.path.exists ( self.path ) :
            raise FileNotFoundError

        try :
            filePath = open ( self.path , 'r' )

        except FileNotFoundError :
            print ( "Could not open:" )   #error handling for filenotfound

        else :
            with filePath :
                for index , line in enumerate ( filePath ) :
                    line = line.strip ( '\n' )
                    splitInLine = line.split ( ' ' , 2 )
                    # splitting the line to check tag validity

                    splitInLine = self.verify_excp_tag_validity ( splitInLine )
                    self.verify_tag_validity ( index , splitInLine )

        self.process_info ( )


        # Adding individual data
        individualRows = [ indi.ptbl_row ( ) for indi in self.individuals.values ( ) ]
        individualTable = self.print_in_table ( ClassForInd.columns , individualRows )

        # Adding family data
        familyRows = [ ]
        #print(self.families.values ( ))
        for fam in self.families.values ( ) :
            if fam.husband :
                husbandId = fam.husband

            if fam.wife :
                wifeId = fam.wife


            for individual in self.individuals.values ( ) :
                if husbandId == individual.indi_id :
                    husbandFullName = individual.name

                if wifeId == individual.indi_id :
                    wifeFullName = individual.name

            familyRows.append ( [ fam.fam_id , fam.date_of_wedding.strftime (
                GedcomParser.dateFormatter ) if fam.date_of_wedding else 'NA' , fam.divorced , husbandId ,
                                  husbandFullName , wifeId , wifeFullName , [ child for child in fam.child_lst ] ] )
        familyTable = self.print_in_table ( ClassForFam.columns , familyRows )

        if pt :
            print ( f'Summary of Individual :\n{individualTable}' )
            print ( f'Summary of Family : \n{familyTable}' )

        if write :
            indi_header = "Summary of Individual:"
            self.updated_file.append ( [ indi_header , individualTable ] )
            fam_header = "Summary of Family:"
            self.updated_file.append ( [ fam_header , familyTable ] )


    # funtion to verify validity of tag
    def verify_tag_validity ( self , index , splitInLine ) :

        level = splitInLine [ 0 ]
        if level in GedcomParser.dict_true.keys ( ) :
            if splitInLine [ 1 ] in GedcomParser.dict_true [ level ] :
                self.original_data.append ( (*splitInLine , index) )

            else :
                self.invalid_tags.append ( (*splitInLine , index) )

        else :
            self.invalid_tags.append ( (*splitInLine , index) )

    @staticmethod
    def verify_excp_tag_validity ( splitInLine ) :

        for i in GedcomParser.exp_list :
            if i in splitInLine:
                if splitInLine.index ( i ) == 2 :
                    splitInLine.insert ( 1 , i )
                    splitInLine.pop ( )

        return splitInLine



    def process_info ( self ) :
        #add process info method
        iterator = iter ( self.original_data )

        while True :
            try :
                line = next ( iterator )

            except StopIteration :
                break

            else :
                if line [ 0 ] == '0' and line [ 1 ] in ('HEAD' , 'TRLR' , 'NOTE') :
                    self.loggerComment.append ( line )

                while len ( line ) == 4 and line [ 0 ] == '0' and line [ 1 ] == "INDI" :

                    indi = ClassForInd ( line [ 2 ] )
                    indi.data.append ( line )
                    self.individuals [ uuid.uuid4 ( ) ] = indi
                    line = next ( iterator )

                    while line [ 0 ] != '0' :
                        indi.data.append ( line )
                        if line [ 0 ] == '1' and line [ 1 ] in GedcomParser.individual_dictionary.keys ( ) :
                            if line [ 1 ] in ('DEAT' , 'BIRT') :
                                next_line = next ( iterator )
                                indi.data.append ( next_line )
                                try :

                                    setattr ( indi , GedcomParser.individual_dictionary [ line [ 1 ] ] ,
                                              datetime.datetime.strptime ( next_line [ 2 ] ,
                                                                           '%d %b %Y' ) )  # set individual attribute
                                except ValueError :
                                    next_line [ 2 ].split ( )
                                    setattr ( indi , GedcomParser.individual_dictionary [ line [ 1 ] ] ,
                                              datetime.datetime ( 9999 , 1 , 1 ) )
                                # print(indi)

                            else :
                                setattr ( indi , GedcomParser.individual_dictionary [ line [ 1 ] ] , line [ 2 ] )

                        line = next ( iterator )

                while len ( line ) == 4 and line [ 0 ] == '0' and line [ 1 ] == "FAM" :
                    fam = ClassForFam ( line [ 2 ] )
                    fam.element_list.append ( line )
                    self.families [ uuid.uuid4 ( ) ] = fam
                    line = next ( iterator )

                    while line [ 0 ] != '0' :
                        fam.element_list.append ( line )
                        if line [ 0 ] == '1' and line [ 1 ] in GedcomParser.family_dictionary.keys ( ) :
                            if line [ 1 ] in ('MARR' , 'DIV') :
                                next_line = next ( iterator )
                                fam.element_list.append ( next_line )
                                try :
                                    setattr ( fam , GedcomParser.family_dictionary [ line [ 1 ] ] ,
                                              datetime.datetime.strptime ( next_line [ 2 ] , '%d %b %Y' ) )
                                    # print(GedcomParser.family_dictionary [ line [ 1 ] ])
                                    # print(datetime.datetime.strptime(next_line[2],'%d %b %Y'))
                                    # print()

                                except ValueError :
                                    next_line [ 2 ].split ( )
                                    setattr ( fam , GedcomParser.family_dictionary [ line [ 1 ] ] ,
                                              datetime.datetime ( 9999 , 1 , 1 ) )
                                # print ( fam )

                            elif line [ 1 ] in ('HUSB' , 'WIFE') :
                                setattr ( fam , GedcomParser.family_dictionary [ line [ 1 ] ] , line [ 2 ] )
                            elif line [ 1 ] == 'CHIL' :
                                fam.child_lst.append ( line [ 2 ] )

                            line = next ( iterator )

        pass
    


    # creating logger to log errors and anomalies in the program
    def logger ( self , err_type , attr_type , usr_story , l_num , attr_id , err_str ) :

        if err_type in ("ERROR" , "ANOMALY") :
            if attr_type in ("FAMILY" , "INDIVIDUAL") :
                self.logError.append ( f'{err_type}: {attr_type}: {usr_story}: {l_num}: {attr_id}: {err_str}' )


    # Printing the data in Tabular Format
    @staticmethod
    def print_in_table ( fields , data_rows ) :

        tbl = PrettyTable ( )
        tbl.field_names = fields
        if len ( data_rows ) != 0 :
            for row in data_rows :
                tbl.add_row ( row )

            return tbl

        return "Data Unavailable"

obj = GedcomParser(path = r'./data/test_data.ged',pt = True)
temp = []
obj.print_in_table(ClassForInd.columns,temp)