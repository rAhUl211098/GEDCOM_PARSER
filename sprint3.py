from user_stories_sprint3 import *

def sprint_third ( filename = None ) :
    spr = GedcomParser (path =  r'./data/test2_data.ged' , pt = True , write = True )
    us9_children_pre_marriage ( spr)
    us10_child_before_parents_death ( spr)
    us11_births_in_last_month ( spr,pt = True )
    us12_deaths_in_last_month (spr, pt = True )

    for err in spr.logError :
        print ( err )

    if filename :
        try :
            filePath = open ( filename , 'a' )

        except FileNotFoundError :
            print ( "File Not Found!" )
        else :
            with filePath :
                filePath.write ( "Sprint 3 Results\n" )
                spr = GedcomParser (path =  r'./data/test2_data.ged' , pt = True )
                us9_children_pre_marriage ( spr )
                us10_child_before_parents_death ( spr )
                us11_births_in_last_month ( spr , pt = True , write = True )
                us12_deaths_in_last_month ( spr , pt = True , write = True )

                for i in spr.updated_file :
                    for content in i :
                        filePath.write ( f'{str ( content )}\n' )

                filePath.write ( "Sprint 3 Error Log\n" )

                for err in spr.logError :
                    filePath.write ( f'{err}\n' )

                filePath.write ( "\n" )

sprint_third( )
sprint_third ( r'./sprint3/results.txt' )