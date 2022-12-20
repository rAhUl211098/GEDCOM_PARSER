from user_stories_sprint4 import *

def sprint_fourth ( filename = None ) :
    spr = GedcomParser ( r'./data/test2_data.ged' , pt = True , write = True )
    spr2 = GedcomParser ( r'./data/test3_data.ged' , pt = False , write = False )
    us15_add_age_in_table ( spr,pt = True )
    us16_check_divorce_while_alive (spr )
    us14_check_married_to_child (spr2 )
    us13_check_gender_of_spouse ( spr2)

    print ( 'Error Log:' )
    for err in spr.logError :
        print ( f'{err}' )

    for err in spr2.logError :
        print ( f'{err}' )

    if filename :
        try :
            filePath = open ( filename , 'a' )

        except FileNotFoundError :
            print ( "File Not Found!" )
        else :
            with filePath :
                filePath.write ( "Sprint 4 Results\n" )
                spr = GedcomParser ( r'./data/test2_data.ged' , pt = False , write = True )
                spr2 = GedcomParser ( r'./data/test3_data.ged' , pt = False , write = False )
                us15_add_age_in_table ( spr , pt = True )
                us16_check_divorce_while_alive ( spr )
                us14_check_married_to_child ( spr2 )
                us13_check_gender_of_spouse ( spr2 )

                for i in spr.updated_file :
                    for content in i :
                        filePath.write ( f'{str ( content )}\n' )

                filePath.write ( "Sprint 4 Error Log\n" )

                for err in spr.logError :
                    filePath.write ( f'{err}\n' )

                for err in spr2.logError :
                    filePath.write ( f'{err}\n' )

                filePath.write ( "\n" )

#sprint_fourth( )
sprint_fourth ( r'./sprint4/results.txt' )