from user_stories_sprint2 import *

def sprint_second ( filename = None ) :
    spr = GedcomParser ( path = r'./data/test_data.ged' , pt = False )
    us8_same_family_name (spr )
    us7_uid ( spr)
    us6_singles_alive (spr, pt = True )
    us5_married_alive ( spr,pt = True )



    for err in spr.logError :
        print ( err )

    if filename :
        try :
            filePath = open ( filename , 'a' )

        except FileNotFoundError :
            print ( "File not found!" )
        else :
            with filePath :
                spr = GedcomParser ( path = r'./data/test_data.ged' , pt = True )
                filePath.write ( "Sprint 2 Results\n" )
                us8_same_family_name ( spr )
                us7_uid ( spr )
                us6_singles_alive ( spr , pt = True ,write = True)
                us5_married_alive ( spr , pt = True ,write = True)

                for i in spr.updated_file :
                    for content in i :
                        filePath.write ( f'{str ( content )}\n' )

                filePath.write ( "Sprint 2 Error Log\n" )

                for err in spr.logError :
                    filePath.write ( f'{err}\n' )

                filePath.write ( "\n" )

#sprint_second ( )
sprint_second ( r'./sprint2/results.txt' )
