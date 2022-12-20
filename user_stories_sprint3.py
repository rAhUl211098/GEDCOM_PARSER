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