from GEDCOM_Parser import GedcomParser,ClassForInd
import datetime

# Check the diffrent Id's of all famalies
def us7_uid ( obj , debug = False ) :

    ind_uids = [ ]
    fam_uids = [ ]
    uids = [ ]
    dup_uids = [ ]
    for ind in obj.individuals.values ( ) :
        if ind.indi_id in ind_uids :
            obj.logger ( "ERROR" , "INDIVIDUAL" , "US7" , ind.l_num [ "INDI" ] , ind.indi_id ,
                          f"{ind.indi_id} already present." )
            dup_uids.append ( ind.indi_id )

        else :
            ind_uids.append ( ind.indi_id )
            uids.append ( ind.indi_id )

    for fam in obj.families.values ( ) :
        if fam.fam_id in fam_uids :
            obj.logger ( "ERROR" , "FAMILY" , "US7" , fam.l_num [ "FAM" ] , fam.fam_id ,
                          f"{fam.fam_id} already present." )
            dup_uids.append ( ind.indi_id )
        else :
            fam_uids.append ( fam.fam_id )
            uids.append ( ind.indi_id )


    if debug :
        return uids , dup_uids

# To check if all family members have same last name or not
def us8_same_family_name ( obj , debug = False ) :

    err = [ ]
    for fam in obj.families.values ( ) :
        ind_child = [ ]
        if fam.husband :
            for ind in obj.individuals.values ( ) :
                if fam.husband == ind.indi_id :
                    hub_fam_name = ind.full_name [ "lastName" ]
                    break
            if hub_fam_name and len ( fam.child_lst ) != 0 :
                for id_of_child in fam.child_lst :
                    for ind in obj.individuals.values ( ) :
                        if id_of_child == ind.indi_id :
                            ind_child.append ( ind )

                for c in ind_child :
                    child_last_name = c.full_name [ "lastName" ]
                    if c.sex == 'M' :
                        if child_last_name != hub_fam_name :
                            obj.logger ( "ERROR" , "FAMILY" , "US16" , fam.l_num [ "CHIL" ] [ 0 ] [ 1 ] ,
                                         fam.fam_id ,
                                          f"Children with id {c.indi_id} do not have the same family name" )
                            err.append ( fam )

    if debug :
        return err
    
# To check the single people alive
def us6_singles_alive ( obj , pt = False , debug = False , write = False ) :

    alive_single = [ ]
    for ind in obj.individuals.values ( ) :
        if not ind.death_date :
            if ind.fam_s == 'NA' :
                alive_single.append ( ind.ptbl_row ( ) )

    alive_single_tbl = obj.print_in_table ( ClassForInd.columns , alive_single )

    if pt :
        print ( f'Alive Single: \n{alive_single_tbl}' )

    if debug :
        return alive_single

    if write :
        header = "US6: Alive Single:"
        obj.updated_file.append ( [ header , alive_single_tbl ] )   
        
# To check the if married people are alive or not
def us5_married_alive ( obj , pt = False , debug = False , write = False ) :

    alive_married = [ ]
    for ind in obj.individuals.values ( ) :
        if not ind.death_date :
            if ind.fam_s != 'NA' :
                alive_married.append ( ind.ptbl_row ( ) )

    alive_married_tbl = obj.print_in_table ( ClassForInd.columns , alive_married )

    if pt :
        print ( f'Living Married: \n{alive_married_tbl}' )

    if debug :
        return alive_married

    if write :
        header = "US5: Alive Married:"
        obj.updated_file.append ( [ header , alive_married_tbl ] )

