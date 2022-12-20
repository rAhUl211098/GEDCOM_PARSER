from GEDCOM_Parser import GedcomParser,ClassForInd
import datetime



#To list the age of people with the table
def us15_add_age_in_table ( obj , pt = False , debug = False , write = False ) :

    debugger = [ ]
    ind_lst = list ( )
    columns = [ 'ID' , 'Name' , 'Age' ]
    for ind in obj.individuals.values ( ) :
        ind_lst.append ( [ ind.indi_id , ind.name , ind.age ] )

    tbl = obj.print_in_table ( columns , ind_lst )

    if not isinstance ( ind.age , int ) :
        obj.logger ( "ERROR" , "INDIVIDUAL" , "US15" , ind.l_num [ "NAME" ] , ind.indi_id ,
                      f"Individual with id {ind.indi_id} has date incomprehensible." )
        debugger.append ( ind.indi_id )

    if pt :
        print ( f'Age of Individual: \n{tbl}' )

    if debug :
        return debugger

    if write :
        header = "US15: Age of Individual"
        obj.updated_file.append ( [ header , tbl ] )


#To check if the divorce between a couple while they were alive
def us16_check_divorce_while_alive ( obj  , pt = True , debug = False ) :

    debugger = [ ]
    for fam in obj.families.values ( ) :
        if fam.divorced :
            for ind in obj.individuals.values ( ) :
                if ind.indi_id == fam.husband :
                    husband = ind

                if ind.indi_id == fam.wife :
                    wife = ind

            if husband.death_date :
                if husband.death_date < fam.date_of_divorce :
                    obj.logger ( "ERROR" , "FAMILY" , "US16" , fam.l_num [ "HUSB" ] , fam.fam_id ,
                                  f"Husband with id {husband.indi_id} passed away {husband.death_date.strftime ( GedcomParser.dateFormatter )} prior to his divorce on date: {fam.date_of_divorce.strftime ( GedcomParser.dateFormatter )}" )
                    debugger.append ( husband.indi_id )

            if wife.death_date and wife.death_date < fam.date_of_divorce :
                obj.logger ( "ERROR" , "FAMILY" , "US16" , fam.l_num [ "WIFE" ] , fam.fam_id ,
                              f"Wife with id {wife.indi_id} passed away {wife.death_date.strftime ( GedcomParser.dateFormatter )} prior to her divorce on date {fam.date_of_divorce.strftime ( GedcomParser.dateFormatter )}" )
                debugger.append ( wife.indi_id )

    if debug :
        return debugger