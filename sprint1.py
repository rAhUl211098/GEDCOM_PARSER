from User_stories import *

def sprint_first ( filename = None ) :
    spr = GedcomParser ( path = r'./data/test_data.ged' , pt = True )
    us1_birth_less_than_6 ( spr)
    us2_less_than_15_siblings ( spr)
    us4_next_dob (spr, pt = True, write = True )
    us3_orphans_list (spr, pt = True,write = True )

    for err in spr.logError :
        print ( err )

    if filename :
        try :
            filePath = open ( filename , 'a' )

        except FileNotFoundError :
            print ( "File not found!" )
        else :
            with filePath :
                filePath.write ( "Sprint 1 Results\n" )
                us1_birth_less_than_6 ( spr )
                us2_less_than_15_siblings ( spr )
                us4_next_dob ( spr , pt = True )
                us3_orphans_list ( spr , pt = True )

                for i in spr.updated_file :
                    for content in i :
                        filePath.write ( f'{str ( content )}\n' )

                filePath.write ( "Sprint 1 Error Log\n" )

                for err in spr.logError :
                    filePath.write ( f'{err}\n' )

                filePath.write ( "\n" )

sprint_first ( )
#sprint_first ( r'./sprint1/results.txt' )



