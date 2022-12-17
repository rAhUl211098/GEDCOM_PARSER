from GEDCOM_Parser import GedcomParser,ClassForInd
import datetime


# To find the orphan individuals
def us3_orphans_list ( obj , pt = False , debug = False , write = False ) :

    list_of_orphans = [ ]
    for fam in obj.families.values ( ) :
        if fam.husband and fam.wife :
            for individual in obj.individuals.values ( ) :
                if fam.husband == individual.indi_id :
                    husband = individual

                if fam.wife == individual.indi_id :
                    wife = individual

            if husband.death_date and wife.death_date and len ( fam.child_lst ) != 0 :
                for child in fam.child_lst :
                    for individual in obj.individuals.values ( ) :
                        if child == individual.indi_id :
                            child_indi = individual

                    if child_indi.age < 18 :
                        list_of_orphans.append ( child_indi.ptbl_row ( ) )

    orphan_tbl = obj.print_in_table ( ClassForInd.columns , list_of_orphans )

    if pt :
        print ( f'Details of Orphans: \n{orphan_tbl}' )

    if debug :
        return list_of_orphans

    if write :
        orphan_heading = "US3: Summary of Orphans:"
        obj.updated_file.append ( [ orphan_heading , orphan_tbl ] )

# To find the people who have their birthdates in next 30 days
def us4_next_dob ( obj , pt = False , debug = False , write = False ) :

    nxt_dob_lst = [ ]
    debugger_lst = [ ]
    time_diff = datetime.timedelta ( days = 30 )
    #epoch_time = datetime ( 1950 , 1 , 1 )
    #today = GedcomParser.getDate - epoch_time
    for ind in obj.individuals.values ( ) :
        if not ind.death_date :
            if GedcomParser.getDate <= ind.dob <= (GedcomParser.getDate + time_diff) :
                nxt_dob_lst.append ( ind.ptbl_row ( ) )
                debugger_lst.append ( ind.dob - GedcomParser.getDate )
                #print("hey")
                #print(nxt_dob_lst)

    dob_tbl = obj.print_in_table ( ClassForInd.columns , nxt_dob_lst )

    if pt :
        print ( f'Next Birthdays: \n{dob_tbl}' )

    if debug :
        return debugger_lst

    if write :
        birthday_header = "US4: Next Birthdays:"
        obj.updated_file.append ( [ birthday_header , dob_tbl ] )
