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
