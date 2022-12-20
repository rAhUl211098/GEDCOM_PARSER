from GEDCOM_Parser import GedcomParser,ClassForInd
import datetime

#To check the birthdays of people in last 30 days
def us11_births_in_last_month ( obj , pt = False , debug = False , write = False ) :

    births_in_last_month = [ ]
    debugger = [ ]
    time_period_of_last_month = datetime.timedelta ( days = 30 )
    for ind in obj.individuals.values ( ) :
        if ind.dob >= (GedcomParser.getDate - time_period_of_last_month) :
            births_in_last_month.append ( ind.ptbl_row ( ) )
            debugger.append ( GedcomParser.getDate - ind.dob )

    table_of_births_in_lastmonth = obj.print_in_table ( ClassForInd.columns , births_in_last_month )

    if pt :
        print ( f'Recently Born: \n{table_of_births_in_lastmonth}' )

    if debug :
        return debugger

    if write :
        head = "US11: Birth in last month:"
        obj.updated_file.append ( [ head , table_of_births_in_lastmonth ] )

#To check the people who died in last 30 days
def us12_deaths_in_last_month ( obj , pt = False , debug = False , write = False ) :

    deaths_in_last_month = [ ]
    debugger = [ ]
    time_period_of_last_month = datetime.timedelta ( days = 30 )
    for ind in obj.individuals.values ( ) :
        if ind.death_date :
            if ind.death_date >= (GedcomParser.getDate - time_period_of_last_month) :
                deaths_in_last_month.append ( ind.ptbl_row ( ) )
                debugger.append ( GedcomParser.getDate - ind.death_date )

    table_of_deaths_in_lastmonth = obj.print_in_table ( ClassForInd.columns , deaths_in_last_month )

    if pt :
        print ( f'Died Recently : \n{table_of_deaths_in_lastmonth}' )

    if debug :
        return debugger

    if write :
        head = "US12:Died Recently :"
        obj.updated_file.append ( [ head , table_of_deaths_in_lastmonth ] )
        
#To check if children are born before or after marriage of their parents
def us9_children_pre_marriage ( obj , debug = False ) :

    debugger = [ ]
    for fam in obj.families.values ( ) :
        if fam.date_of_wedding :
            childs = [ ]

            for ind in obj.individuals.values ( ) :
                for childs in fam.child_lst :
                    if ind.indi_id == childs :
                        childs.append ( ind )

            for child in childs :
                if child.dob < fam.date_of_wedding :
                    obj.logger ( "ANOMALY" , "FAMILY" , "US08" , fam.l_num [ "CHIL" ] [ 0 ] [ 1 ] , fam.fam_id ,
                                  f"Child with id {child.indi_id} born {child.dob.strftime ( GedcomParser.dateFormatter )} before marriage of parents on {fam.date_of_wedding.strftime ( GedcomParser.dateFormatter )}" )
                    debugger.append ( child.indi_id )
                if fam.divorced and child.dob > (fam.date_of_divorce + datetime.timedelta ( 9 * 365 / 12 )) :
                    obj.logger ( "ANOMALY" , "FAMILY" , "US08" , fam.l_num [ "CHIL" ] [ 0 ] [ 1 ] , fam.fam_id ,
                                  f"Child with id {child.indi_id} born {child.dob.strftime ( GedcomParser.dateFormatter )} after the divorce of parents on {fam.date_of_divorce.strftime ( GedcomParser.dateFormatter )}" )
                    debugger.append ( child.indi_id )

    if debug :
        return debugger
# To chek if children are born before death of mother or after 9 months of death of the father
def us10_child_before_parents_death ( obj , debug = False ) :

    debugger = [ ]
    for fam in obj.families.values ( ) :
        if fam.husband and fam.wife and len ( fam.child_lst ) != 0 :
            childs = [ ]

            for ind in obj.individuals.values ( ) :
                if ind.indi_id == fam.husband :
                    husband = ind

                if ind.indi_id == fam.wife :
                    wife = ind

                for c in fam.child_lst :
                    if ind.indi_id == c :
                        childs.append ( ind )

            for c in childs :
                if wife.death_date and c.dob > wife.death_date :
                    obj.logger ( "ANOMALY" , "FAMILY" , "US10" , fam.l_num [ "CHIL" ] [ 0 ] [ 1 ] , fam.fam_id ,
                                  f"Child with id {c.indi_id} born {c.dob.strftime ( GedcomParser.dateFormatter )} after mother's death on date: {wife.death_date.strftime ( GedcomParser.dateFormatter )}" )
                    debugger.append ( c.indi_id )

                if husband.death_date and c.dob > (husband.death_date + datetime.timedelta ( 9 * 365 / 12 )) :
                    obj.logger ( "ANOMALY" , "FAMILY" , "US10" , fam.l_num [ "CHIL" ] [ 0 ] [ 1 ] , fam.fam_id ,
                                  f"Child with id {c.indi_id} born {c.dob.strftime ( GedcomParser.dateFormatter )} after father's death later than 9 months. Father's death date: {husband.death_date.strftime ( GedcomParser.dateFormatter )}" )
                    debugger.append ( c.indi_id )

    if debug :
        return debugger    
    
