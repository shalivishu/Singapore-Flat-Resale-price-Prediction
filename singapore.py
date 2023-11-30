from datetime import date
import numpy as np
import pickle
import streamlit as st
from datetime import datetime

# Streamlit page custom design

def streamlit_config():

    # page configuration
    st.set_page_config(page_title='Industrial Copper Modeling')

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # title and position
    st.markdown(f'<h1 style="text-align: center;">Singapore Flat Resale Price Predictor</h1>',
                unsafe_allow_html=True)



# custom style for submit button - color and width

def style_submit_button():

    st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                                                        background-color: #367F89;
                                                        color: white;
                                                        width: 70%}
                    </style>
                """, unsafe_allow_html=True)



# custom style for prediction result text - color and position

def style_prediction():

    st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
                color: #20CA0C
            }
            </style>
            """,
            unsafe_allow_html=True
        )



# user input options

class options:
        # Define the possible values for the dropdown menus
        town = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
                'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
                'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
                'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
                'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
                'TOA PAYOH', 'WOODLANDS', 'YISHUN', "nan"]
        
        flat_type = ['3 ROOM', '4 ROOM', '5 ROOM', '2 ROOM', 'EXECUTIVE', '1 ROOM',
                'MULTI-GENERATION', 'nan']
        
        storey_range = ['07 TO 09', '01 TO 03', '13 TO 15', '10 TO 12', '04 TO 06',
                '19 TO 21', '16 TO 18', '22 TO 24', '25 TO 27', '28 TO 30',
                '34 TO 36', '46 TO 48', '31 TO 33', '37 TO 39', '43 TO 45',
                '40 TO 42', '49 TO 51', 'nan', '06 TO 10', '01 TO 05', '11 TO 15',
                '16 TO 20', '21 TO 25', '26 TO 30', '36 TO 40', '31 TO 35']
        
        flat_model = ['Improved', 'New Generation', 'Model A', 'Standard', 'Simplified',
                'Premium Apartment', 'Maisonette', 'Apartment', 'Model A2',
                'Type S1', 'Type S2', 'Adjoined flat', 'Terrace', 'DBSS',
                'Model A-Maisonette', 'Premium Maisonette', 'Multi Generation',
                'Premium Apartment Loft', 'Improved-Maisonette', '2-room', 'nan',
                '3Gen']
        block = ['174','541','163','446','557','603','709','333','109','564','218','556','156','471','434','560','332','421',
                '506','631','153','442','558','212','152','331','121','130','646','424','584','412','612','562','223','150',
                '468','177','415','254','207','432','117','428','573','418','324','596B','234','648','253A','439','306','729',
                '315B','700C','620','38','504','545','546','18','550','502','509','525','534','542','76','703','27','42','426',
                '530','420','105','519','548','537','28','100','103','522','551','608','135','40','57','401','2','116','419',
                '107','221B','219A','512','131','147','82','536','517','34','6','37','35','724','523','65','132','62','772',
                '774','768','180','611','602','101','99','553','804','659','405','172','406','55','66','67','114','10D',
                '629','104','308','271','239','264','281','113','227','167','112','251','302','289','248','310','447',
                '217','128','183','192','201','450','501','410','408','423','272','229','407','240','179','414','269',
                '146','533','157','540','249','316','250','164','312','208','311','319','417','307','138','124','291B',
                '288D','186','386','337','165','290D''291D','291A','384','193','243','388','102','623','621','622','202',
                '524','48','8','5','26','129','60','11','77','26D','26C','29','46','59','54','106A','53','14','112B','20','120',
                '70','68','69','21','8A','27A','2A','50','106B','95','119B','75C','2C','142','409','435','466','140',
                '123','402','520','615','609','404','440','204','136','652','656','448','507','625','610','627','626','182',
                '606','478','470','653','184','543','1','3','538','532','1A','1F','1C','1B','1E','15','459','206','690A',
                '295','110','688A','485A','16','687A','160','686C','670A','238','296A','616','155','422','296','226',
                '472','673','788','641','765','473','691B','689A','760','763','503','474','441','282','287','690B','457',
                '757','604','513','346','354','515','351','429','304','374','511','318','605','342','43','58','61','93',
                '25','23','9','31','126','45','10','22','44','352','125','309','317','242','327','328','644','335','303',
                '323','619','17','154','301','636','943','690','514','970','566','699C','111','436','696','363','916','134',
                '456','463','438','220','976','699A','567','924','837','967','357','577','633','455','712','851','33',
                '257','231','244','210','236','321','265','268','276','216','185','495','215','480','915','914','475',
                '462','339A','337B','276A','273D','275B','816','749','823','655A','843','718','725','411','855',
                '338A','673A','465','755','675A','662B','659D','681C','684B','516','660B','921','273B','268C',
                '275D','275C','221','667D','756','736','677C','366','539','673B','650C','653B','748','825','686B',
                '650B','988A','989B','658B','262','660C','987B','330','689','115','842','752','830A','549','671C',
                '656C','669D','607','336','679A','97','4','94','96','684','49','84','106','681','13','3C','38D','5A',
                '12','461','108','79','256','632','634','738','487','232','425','122','571','746','739','190','777',
                '707','708','199','614','266','270','241','714','645','583','196B','647','642A','642B','303C','636A',
                '126C','638C','204B','299','201B','633B','635A','303A','302B','302D','301D','301A','302C','302A',
                '303D','126A','101C','641C','199B','176B','643','196C','173C','160A','160B','293','171A','166','83',
                '98','161','61B','168A','28B','181','30A','18C','91','19','28A','18D','483','589B','359B','501B','320',
                '507B','466A','300','510B','354B','341B','468D','502A','209A','183C','290B','306C','185D','116A',
                '303B','124C','123E','226A','322A','200A','412B','406C','247','325A','259B','208B','438B','261C','439A',
                '264D','271B','265A','272D','271A','275A','277B','273C','157D','158C','183B','200B','122E','123B',
                '187A','188B','191A','207B','298A','228C','158A','186D','297B','228A','319B','319C','201C','262D',
                '268A','298B','250B','306B','202B','299B','263','245','531','329','224','228','315','255','508','544',
                '820','885','444','810','139','285','213','469','898','809','261','369','476','880A','856','347','846',
                '277','871A','489B','367','355','852','222','722','230B','450F','450E','842C','946','872','278','498L',
                '742','149','731','497B','383','518C','842B','148','842D','515C','518A','874A','430','857','856C','863',
                '194','195','51','168','118','85A','143','214','79E','145','575','831','845','853','751','786E','737','173',
                '775','873','761','701','704','710','552','896B','723','681B','896A','681A','162','786C','689C','624B',
                '689D','881','859','824','862','894D','895C','370','581','356','788D','658','847','403','284','274',
                '141','617','861','741','771','246','639','787','362','279','660','829','802','322','325','170','151','559',
                '127','561','445','443','230','433','535','586','209','235','175','649','700A','74','75','554','89','521',
                '529','92','32','526','211','52','119','133','81','427','651','220C','711','773','176','313','290','252','259',
                '267','233','341','385','395','390','188','288B','289C','7','118D','26B','76A','119C','111B','131B','73A',
                '431','505','527','601','630','178','528','451','133A','30','334','1G','1D','413','353','486','692A','687C',
                '685A','684D','686A','454','790','764','706','713','715','205','358','364','349','373','340','203','41',
                '844','36','39','642','682','985A','676','980C','923','613','909','950','326','688','699B','979C','624',
                '339','830','579','64','280','273','288E','908','904','477','821','618','932','826','832','834','836',
                '268B','747','679C','460','663C','657A','672A','667A','664D','510','274D','743','949','953','272C',
                '271D','673C','198','648C','661A','654B','654C','652C','766','661C','517C','906','754','159','671B',
                '86','4C','73','416','769','479','128A','175B','175C','637C','163B','167B','128D','126D','174D','191',
                '102D','176A','105C','176C','638B','102B','110B','637B','204A','199D','175D','297','102A','641A',
                '162B','85','90','169''47','23A','23B','62A','314','482','340A','589A','341A','350B','509B','489',
                '466C','469B','484','588C','467A','501A','467B','295A','124B','295B','309C','308B','159A','184C',
                '311D','309B','203A','292A','408A','311B','309A','438A','265E','441A','320A','257C','264A','266B',
                '272A','268D','266A','158B','188A','157A','157B','122D','318D','307D','116C','123A','405B','323C',
                '122A','413A','116B','312B','117A','299A','144','822','467','813','225','291','237','497C','735','359',
                '487B','864','858A','862A','896','498J','868','874','391','857B','518B','938','495E','230D','79A','82A',
                '730','588','667','682B','683A','841','689F','753','689E','897C','796','678','807','780','789','283','806',
                '288','786','664','800','716','115A','805','778','758','640','576','570','585','565','315A','518','78','767',
                '657','219D','221A','24','189','368','393','289G','290F','289A','111A','118A','6A','75B','25B','109A',
                '87','219','437','650','635','687B','692B','792','569','638','680','484B','690D','687D','665','770','305',
                '784','343','662','759','728','379','380','939','925','452','981C','655','972','563','698C','253','990B',
                '490','492','338B','339D','945','961','838','839','854','980','667C','649B','649A','663A','271C','276C',
                '819','902','676B','677A','337C','337D','653A','678A','986A','987A','656A','669B','63','685','3D','3B',
                '38A','700','572','776','628','721','568','782','449','547','580','128C','203B','632B','195B','301B','102C',
                '107A','204D','172B','173A','107D','199C','637A','294','166A','165A','187','88','171','28C','508B','491',
                '493','360A','357C','353C','469A','357A','355A','588B','360B','359A','439B','298D','305D','120A','196',
                '204C','207A','157C','290A','201A','313C','209C','404B','265C','439C','441C','277C','267A','273A',
                '206C','117C','310A','316C','260A','301C','403A','292B','403C','191B','201D','321B','200D','258D',
                '412A','307B','262B','202A','506A','236A','808','361','486C','365','877','867','493C','888','275','907',
                '861A','936','888A','491D','912','450C','494C','496B','488A','389','498A','732','394','496C','497H',
                '859A','842E','230G','495A','893','867A','894','85B','200','10B','79B','79C','99B','624A','762','733',
                '786D','892A','897A','895B','371','787C','688F','882','589','898B','628A','685C','719','891B','654',
                '360','137','702','734','726','115C','865','858','880','345','587','348','596D','596C','71','705','219C',
                '219B','221C','94D','338','288C','260','290G','387','298','26A','17A','63A','131C','75A','453','485D',
                '297A','484D','670','555','350','381','372','669','984A','911','661','980A','984C','984D','966','941',
                '959','850','944','727','720','948','675B','717','464','655B','986C','651A','661D','676A','517E',
                '678D','814','815','659A','817','648A','682C','660D','662A','274A','72','4B','2B','744','174C','110C',
                '107C','167D','633A','195D','195A','167A','642C','109B','109C','171C','162A','18B','508A','354A',
                '351A','504A','306A','183D','323B','317A','190B','207D','262A','208A','408B','121B','121A','206D',
                '318A','312A','316B','121C','206B','305A','314C','403D','223A','404A','299C','317D','250C','258',
                '848','899','871','913','487C','818','889A','891','897','891A','929','886','392','450A','922','490A',
                '492C','518D','515A','515B','942','856D','158','153A','101A','787B','625B','786B','628B','681D','582',
                '671','827','893C','397','399','803','833','745','398','799','875','798','828','700B','596A','291C',
                '291E','289D','288A','119D','8B','25A','77A','335A','484A','691A','690C','910','920','958','975','940',
                '375','225A','286D','287D','287A','287B','485','903','276D','674B','488','979','680C','651B','337A',
                '660A','659B','650A','664B','652B','654A','684C','685B','669C','687','683B','637','458','781','176D',
                '205A','103C','105B','128B','104B','56','3A','510A','508C','354C','466B','356B','354D','295C','305C',
                '185C','308C','186C','260D','324A','436B','441B','270A','441D','269A','272B','264F','277D','188D',
                '296B','184B','313B','403B','318C','407B','257A','260B','879','866','491C','489C','498E','498D','498F',
                '930','842G','486A','493E','842F','515D','856B','79D','849','666','684A','801','895A','688C','764A',
                '788C','783','812','286','115B','795','308A','344','310B','94C','10E','118B','668','672B','683C','689B',
                '297C','377','674','686','981D','574','984B','978C','980D','698B','931','960','698D','215A','286B','498',
                '481','917','926','933','668D','987D','811','659C','988B','678C','989A','653C','664A','989D','987C',
                '666B','671A','860','665B','665A','108C','38B','750','196D','107B','638A','101D','173B','126B',
                '105D','175A','61C','507C','466D','359C','353A','352A','504D','468A','436C','307A','228B','120B',
                '314B','311C','307C','409B','269B','264E','226B','408C','413B','258B','320B','317B','261B','206A',
                '258C','325B','318B','225B','259C','261A','261D','224D','250D','878','496E','869','491B','489A',
                '494B','496F','842H','856F','840','897B','787E','892B','899B','690F','679','688E','787D','893B','310C',
                '740','613B','10F','290E','112A','74A','663','296E','484C','677','672','2D','693','969','981A','971',
                '956','286A','287C','285A','928','919','657B','668A','648B','678B','664C','679B','695','656D','14A',
                '199A','635C','632C','642D','173D','171B','62B','28D','589C','589D','503B','356A','350C','507D',
                '185B','184A','304A','314A','119A','227A','407A','325C','257B','188C','304B','192C','324D','203E',
                '884','870','934','495C','892','85C','82B','682A','683D','793','791','896C','682D','795A','80','197',
                '124A','688B','297D','692','697','954','339C','667B','989C','662D','274C','669A','683','108B','500',
                '779','635B','161B','195C','104A','103A','103B','197A','172A','504B','509A','352B','501C','351B',
                '468B','351D','436A','406A','314D','259A','436D','183A','296C','322B','315C','406B','321C','267B',
                '324C','250A','506B','450D','898A','690E','688D','794','788B','288G','289B','335B','686D','378','835',
                '979A','979B','985B','955','963','578','285B','285C','947','677B','691','339B','662C','918','59C','39A',
                '601C','106D','360C','352C','503A','123C','223D','209B','409A','322C','223C','189C','225C','232A',
                '201E','487A','876','491F','492B','498G','486B','495D','14B','899C','94E','29A','289E','6B','127D',
                '694','675','980B','974','286C','952','990C','668C','658C','658A','652A','656B','168B','174B','602A',
                '196A','101B','110D','163A','197B','166B','18A','507A','357B','503C','298C','323A','269D','224A',
                '319A','120C','269C','277A','187B','186B','260C','313D','485B','935','497D','497G','937','894C',
                '797','796A','220B','27B','485C','674A','92A','964','990A','494','978','988C','38C','637D','601D',
                '161A','195E','604B','601A','603A','172C','350A','227C','443A','290C','405C','117B','203D',
                '320C','488B','899A','450G','491E','498M','230E','292','127A','376','962','957','668B','658D','602C',
                '602B','636B','306D','632A','603B','603C','265D','265B','313A','123D','202C','205B','883','887','894A',
                '491A','493A','367A','492D','495F','889','894B','220A','42A','905','663B','661B','680A','174A','61A',
                '410A','211D','210B','210A','266C','264C','121D','207C','122C','234A','495B','785','94B','118C','968',
                '274B','165B','410C','192B','224C','305B','227D','226C','498H','491G','895','788E','289F','986B',
                '698','965','927','601B','604C','614B','613D','110A','468C','443C','443B','158D','321A','210C','211A',
                '224B','189B','857A','887A','230J','230H','80A','893A','127C','4A','663D','604A','612A','641B',
                '405A','411A','411B','410B','264B','186A','192A','262C','168C','167C','493D','168D','285D','59B',
                '612D','613C','615C','614A','340B','356C','501D','213B','212C','213A','445B','445A','317C','205C',
                '189A','864A','496G','230C','786F','296D','978D','699','615B','613A','504C','353B','351C','211B',
                '190A','227B','122B','84B','43A','977','612C','211C','212B','212A','309D','886A','491H','493B',
                '497A','63B','951','517D','615A','612B','105A','311A','324B','81A','226E','981B','648D','320D',
                '860B','497J','893D','588D','267C','185A','498B','99C','270B','270C','490B','80C','476C','59A',
                '617C','618B','435A','434A','223B','81B','nan','150A','497F','7A','217A','80B','99A','645A','496D',
                '863A','856E','640A','666A','382','84A','48A','535A','230F','860A','863B','625A','828A','288F',
                '698A','517A','973','680B','203C','258A','10C','109D','858B','617B','446C','476B','617D','434B',
                '435B','619C','619A','618C','447A','435C','572B','12B','476A','476D','618D','618A','619B','12A','12C',
                '138B','623C','623A','619D','624C','446B','139A','138A','570C','633C','623B','447B','138C','139B',
                '169B','570A','570B','633D','622A','617A','571A','169C','571C','571B','181A','622B','170C','208C',
                '170B','169A','572A','180A','622C','499B','180B','180C','170A','450B','178D','448A','430D','499A',
                '887C','181B','180D','430C','433B','432B','178A','886D','448B','887B','886C','9B','430A','430B','886B',
                '9A','213C','178B','433A','432A','10A','463B','178C','426A','347A','463C','451A','348D','426C','336B',
                '426D','336C','463A','426B','428B','452B','452A','782A','348A','347B','348C','590A','451B','326A',
                '780B','782D','782B','348B','546B','266D','591A','592B','593A','592C','780E','424D','335C','336A',
                '546A','471A','197C','592A','590B','326B','327A','327C','282B','281B','282A','522A','522C','782C',
                '780A','780C','780D','424A','333B','333A','334B','547D','547A','546C','470A','470C','471B','593B',
                '590C','281A','332C','327B','332A','332B','333D','280A','869A','869B','780F','424C','428A','431C',
                '431B','547B','470B','197D','312C','453B','334A','326C','333C','280B','282C','868A','522B','782E',
                '424B','429B','431D','334C','432D','432C','527A','453A','331C','279C','326D','868C','523B','523C',
                '342B','334D','526A','525C','524A','453D','279A','440A','329A','453C','279B','519C','431A','547C',
                '527B','440C','329B','440B','331B','520A','519B','523A','519D','342C','550B','528B','525A','526D',
                '526B','520C','523D','548B','549B','634A','549A','528A','525B','526C','330B','331A','336D','890C',
                '890A','519A','429A','505C','747A','748A','748C','747B','550A','475C','475B','138D','527C','528C',
                '672D','330A','890B','342A','505B','505D','634B','477A','475D','524C','416B','414A','494E','505A',
                '748B','747C','475A','477B','527D','672C','414B','416C','415B','548A','636C','477C','415A','416A',
                '415C','472C','494D','807B','665C','489D','490D','471C','472A','807A','488C','469C','442D','490C',
                '376A','376B','530C','670C','807C','808A','443D','488D','17B','670B','472B','293D','871C','808C',
                '96A','442B','442C','256C','256D','868B','376C','530B','530A','473A','294A','164A','808B','95C','815A',
                '256B','256A','164B','293A','164C','870A','871B','809B','803A','805A','808D','809A','530D','293C',
                '216A','520B','889C','697A','676D','316D','163C','293B','215B','889B','96B','70A','803B','804A','815C',
                '697B','677D','216B','889D','95B','70B','804B','815B','473B','8C','162C','95A','811A','803C','816A',
                '805B','816B','473C','217C','217B','878B','717B','511A','70C','803D','810A','473D','217D','506C',
                '511B','817A','805C','817B','278B','717A','194B','194A','810B','812C','805D','802A','801A','216C',
                '278A','879B','878A','512A','801C','801B','818B','812B','932B','216D','511C','818A','812A','818C',
                '811B','801D','817C','932A','364B','697C','879A','512B','802B','365A','364A','365B','113C','933A',
                '113D','512C','802C','365C','113B','113A','278C','365D','218C','509C','502B','813A','502D','455C',
                '218B','502C','455A','455B','120D','418A','813B','513A','218D','561B','561A','222A','130B','130A',
                '129A','574B','785B','226F','560A','218A','129C','338C','785C','513D','513B','104D','338D','784C',
                '785D','513C','129B','418B','784A','675D','675C','418C','417A','131A','574A','573A','784B',
                '693A','783A','231B','108A','573B','573C','691D','691C','783C','783D','91A','231A','104C','115D',
                '492G','693B','694A','783B','446A','448C','449B','694B','694D','440D','292C','93A','90B','233B',
                '234B','694C','693C','449A','93B','92B','90A','997A','997C','997B','233A','232C','233C','232B',
                '494G','494H','442A','363A','494J','322D','362C','140B','366A','363B','140A','362B','362A','366B',
                '992B','461A','461D','998B','991A','992A','140D','140C','996A','996B','998A','991B','182A','462A',
                '461C','461B','995A','996C','182B','462C','462B']
                
        

        street_name = ['ANG MO KIO AVE 4', 'ANG MO KIO AVE 10', 'ANG MO KIO AVE 5',
                'ANG MO KIO AVE 8', 'ANG MO KIO AVE 1', 'ANG MO KIO AVE 3',
                'ANG MO KIO AVE 6', 'ANG MO KIO ST 52', 'ANG MO KIO ST 21',
                'ANG MO KIO ST 31', 'BEDOK RESERVOIR RD', 'BEDOK STH RD',
                'BEDOK NTH ST 3', 'BEDOK NTH AVE 1', 'BEDOK NTH RD',
                'NEW UPP CHANGI RD', 'CHAI CHEE ST', 'BEDOK NTH ST 1',
                'BEDOK NTH AVE 4', 'BEDOK NTH ST 2', 'CHAI CHEE AVE',
                'BEDOK NTH AVE 3', 'BEDOK STH AVE 1', 'BEDOK CTRL',
                'BEDOK NTH AVE 2', 'BEDOK STH AVE 2', 'BEDOK RESERVOIR VIEW',
                'CHAI CHEE RD', 'JLN TENAGA', 'BEDOK STH AVE 3', 'LENGKONG TIGA',
                'SHUNFU RD', 'BISHAN ST 24', 'BISHAN ST 12', 'BISHAN ST 22',
                'BISHAN ST 13', 'BISHAN ST 23', 'BRIGHT HILL DR', 'SIN MING AVE',
                'BT BATOK ST 52', 'BT BATOK WEST AVE 4', 'BT BATOK WEST AVE 2',
                'BT BATOK EAST AVE 4', 'BT BATOK EAST AVE 3', 'BT BATOK ST 21',
                'BT BATOK EAST AVE 5', 'BT BATOK WEST AVE 8', 'BT BATOK ST 11',
                'BT BATOK WEST AVE 6', 'BT BATOK ST 51', 'BT BATOK ST 32',
                'BT BATOK ST 33', 'BT BATOK ST 31', 'BT BATOK CTRL',
                'BT BATOK ST 24', 'BT BATOK ST 25', 'BT BATOK WEST AVE 5',
                'BT BATOK ST 34', 'JLN KLINIK', 'LOWER DELTA RD', 'BT MERAH VIEW',
                'JLN BT HO SWEE', 'JLN BT MERAH', 'TELOK BLANGAH CRES',
                'TELOK BLANGAH HTS', 'KIM TIAN RD', 'BEO CRES', 'CANTONMENT CL',
                'TELOK BLANGAH DR', 'JLN MEMBINA', 'LIM LIAK ST', 'SENG POH RD',
                'LENGKOK BAHRU', 'DEPOT RD', 'KIM TIAN PL', 'REDHILL CL',
                'BOON TIONG RD', 'HOY FATT RD', 'HAVELOCK RD', 'REDHILL LANE',
                'REDHILL RD', 'GANGSA RD', 'PETIR RD', 'BANGKIT RD', 'SAUJANA RD',
                'BT PANJANG RING RD', 'SEGAR RD', 'PENDING RD', 'FAJAR RD',
                'JELAPANG RD', 'SENJA RD', 'SENJA LINK', 'JELEBU RD', 'CASHEW RD',
                'TOH YI DR', 'FARRER RD', 'UPP CROSS ST', 'TG PAGAR PLAZA',
                'CHIN SWEE RD', 'CANTONMENT RD', 'TECK WHYE AVE', 'TECK WHYE LANE',
                'CHOA CHU KANG AVE 4', 'CHOA CHU KANG CTRL', 'CHOA CHU KANG CRES',
                'CHOA CHU KANG AVE 2', 'CHOA CHU KANG AVE 3', 'CHOA CHU KANG DR',
                'CHOA CHU KANG AVE 5', 'JLN TECK WHYE', 'CHOA CHU KANG AVE 1',
                'CHOA CHU KANG ST 62', 'CHOA CHU KANG NTH 6',
                'CHOA CHU KANG ST 64', 'CHOA CHU KANG NTH 5',
                'CHOA CHU KANG ST 51', 'WEST COAST RD', 'CLEMENTI AVE 5',
                'CLEMENTI AVE 2', 'CLEMENTI WEST ST 1', 'CLEMENTI AVE 3',
                'CLEMENTI AVE 4', 'CLEMENTI WEST ST 2', 'WEST COAST DR',
                'CIRCUIT RD', 'ALJUNIED CRES', 'MACPHERSON LANE', 'BALAM RD',
                'PAYA LEBAR WAY', 'EUNOS CRES', 'HAIG RD', 'GEYLANG EAST AVE 1',
                'SIMS DR', 'CASSIA CRES', 'UBI AVE 1', 'ALJUNIED RD', 'PINE CL',
                'JLN TIGA', 'HOUGANG AVE 3', 'HOUGANG AVE 6', 'HOUGANG AVE 5',
                'HOUGANG AVE 1', 'HOUGANG AVE 7', 'HOUGANG ST 22', 'HOUGANG AVE 8',
                'HOUGANG AVE 10', 'HOUGANG ST 11', 'LOR AH SOO', 'HOUGANG ST 92',
                'HOUGANG ST 61', 'HOUGANG AVE 4', 'HOUGANG ST 91', 'HOUGANG ST 51',
                'HOUGANG ST 52', 'HOUGANG AVE 9', 'HOUGANG ST 21', 'HOUGANG CTRL',
                'HOUGANG AVE 2', 'TEBAN GDNS RD', 'JURONG EAST ST 24',
                'JURONG EAST ST 21', 'JURONG EAST ST 13', 'JURONG EAST ST 32',
                'JURONG EAST ST 31', 'TOH GUAN RD', 'PANDAN GDNS', 'BOON LAY AVE',
                'BOON LAY PL', 'JURONG WEST ST 41', 'HO CHING RD',
                'JURONG WEST ST 51', 'JURONG WEST AVE 1', 'JURONG WEST ST 91',
                'KANG CHING RD', 'TAH CHING RD', 'JURONG WEST ST 25',
                'JURONG WEST AVE 3', 'JURONG WEST ST 81', 'JURONG WEST ST 42',
                'JURONG WEST ST 73', 'JURONG WEST ST 61', 'JURONG WEST ST 71',
                'JURONG WEST AVE 5', 'JURONG WEST ST 65', 'YUNG LOH RD',
                'JURONG WEST ST 74', 'JURONG WEST ST 64', 'JURONG WEST CTRL 1',
                'JURONG WEST ST 52', 'JURONG WEST ST 92', 'YUNG SHENG RD',
                'BOON LAY DR', 'JURONG WEST ST 75', 'CORPORATION DR',
                'JURONG WEST ST 93', 'YUNG AN RD', 'JLN BAHAGIA', 'GEYLANG BAHRU',
                'JLN BATU', 'KALLANG BAHRU', 'UPP BOON KENG RD', 'RACE COURSE RD',
                'GLOUCESTER RD', 'BEACH RD', 'BENDEMEER RD', 'WHAMPOA STH',
                'WHAMPOA DR', "ST. GEORGE'S RD", 'JLN DUSUN', 'JLN TENTERAM',
                'BOON KENG RD', 'FARRER PK RD', 'MCNAIR RD', 'AH HOOD RD',
                'WHAMPOA RD', 'CRAWFORD LANE', 'JLN RAJAH', 'MARINE TER',
                'MARINE DR', 'MARINE CRES', 'CHANGI VILLAGE RD', 'PASIR RIS ST 21',
                'PASIR RIS DR 3', 'PASIR RIS DR 6', 'PASIR RIS DR 10',
                'PASIR RIS ST 11', 'PASIR RIS ST 71', 'PASIR RIS DR 1',
                'PASIR RIS DR 4', 'PASIR RIS ST 52', 'PASIR RIS ST 51',
                'PASIR RIS ST 53', 'PASIR RIS ST 12', 'ELIAS RD',
                'PASIR RIS ST 72', 'EDGEDALE PLAINS', 'PUNGGOL FIELD',
                'PUNGGOL CTRL', 'PUNGGOL DR', 'PUNGGOL PL', 'EDGEFIELD PLAINS',
                'STIRLING RD', "C'WEALTH CL", "C'WEALTH CRES", "C'WEALTH DR",
                'DOVER CRES', 'GHIM MOH RD', 'HOLLAND AVE', 'HOLLAND DR',
                'DOVER RD', 'MEI LING ST', 'STRATHMORE AVE', 'QUEENSWAY',
                'HOLLAND CL', 'TANGLIN HALT RD', 'ADMIRALTY LINK', 'SEMBAWANG DR',
                'MONTREAL DR', 'ADMIRALTY DR', 'WELLINGTON CIRCLE', 'SEMBAWANG CL',
                'SEMBAWANG VISTA', 'CANBERRA RD', 'ANCHORVALE LINK',
                'COMPASSVALE LANE', 'RIVERVALE CRES', 'RIVERVALE ST',
                'COMPASSVALE CRES', 'RIVERVALE DR', 'COMPASSVALE WALK',
                'ANCHORVALE DR', 'SENGKANG EAST RD', 'FERNVALE LINK',
                'COMPASSVALE DR', 'RIVERVALE WALK', 'FERNVALE RD',
                'COMPASSVALE RD', 'SENGKANG EAST WAY', 'SENGKANG WEST AVE',
                'COMPASSVALE BOW', 'SENGKANG CTRL', 'COMPASSVALE LINK',
                'COMPASSVALE ST', 'SERANGOON NTH AVE 1', 'SERANGOON AVE 4',
                'SERANGOON CTRL', 'SERANGOON CTRL DR', 'SERANGOON AVE 2',
                'SERANGOON NTH AVE 4', 'SERANGOON NTH AVE 3', 'SERANGOON AVE 3',
                'SERANGOON AVE 1', 'TAMPINES ST 43', 'TAMPINES ST 22',
                'TAMPINES ST 81', 'TAMPINES ST 83', 'TAMPINES ST 44',
                'TAMPINES ST 42', 'TAMPINES ST 41', 'TAMPINES AVE 4',
                'TAMPINES ST 11', 'TAMPINES ST 21', 'TAMPINES ST 23',
                'TAMPINES ST 12', 'SIMEI ST 1', 'TAMPINES ST 34', 'TAMPINES AVE 8',
                'TAMPINES ST 82', 'TAMPINES ST 33', 'TAMPINES ST 84',
                'TAMPINES ST 45', 'TAMPINES ST 71', 'SIMEI ST 4', 'TAMPINES ST 91',
                'TAMPINES ST 24', 'TAMPINES ST 72', 'TAMPINES ST 32',
                'TAMPINES CTRL 7', 'SIMEI RD', 'LOR 2 TOA PAYOH', 'KIM KEAT AVE',
                'UPP ALJUNIED LANE', 'LOR 1 TOA PAYOH', 'LOR 6 TOA PAYOH',
                'LOR 5 TOA PAYOH', 'LOR 7 TOA PAYOH', 'TOA PAYOH EAST',
                'LOR 3 TOA PAYOH', 'LOR 4 TOA PAYOH', 'TOA PAYOH CTRL',
                'POTONG PASIR AVE 2', 'LOR 8 TOA PAYOH', 'POTONG PASIR AVE 1',
                'JOO SENG RD', 'KIM KEAT LINK', 'MARSILING RISE', 'MARSILING DR',
                'WOODLANDS ST 31', 'WOODLANDS ST 41', 'WOODLANDS DR 16',
                'WOODLANDS ST 83', 'WOODLANDS ST 82', 'WOODLANDS CIRCLE',
                'WOODLANDS DR 60', 'WOODLANDS ST 13', 'WOODLANDS CRES',
                'WOODLANDS ST 81', 'WOODLANDS AVE 6', 'WOODLANDS DR 40',
                'WOODLANDS DR 52', 'WOODLANDS DR 70', 'WOODLANDS DR 44',
                'WOODLANDS DR 50', 'WOODLANDS DR 42', 'WOODLANDS DR 62',
                'WOODLANDS AVE 1', 'WOODLANDS DR 14', 'WOODLANDS DR 53',
                'WOODLANDS RING RD', 'WOODLANDS ST 11', 'WOODLANDS DR 75',
                'WOODLANDS AVE 5', 'WOODLANDS ST 32', 'YISHUN RING RD',
                'YISHUN AVE 5', 'YISHUN AVE 6', 'YISHUN ST 22', 'YISHUN CTRL',
                'YISHUN AVE 2', 'YISHUN AVE 4', 'YISHUN ST 21', 'YISHUN ST 11',
                'YISHUN AVE 11', 'YISHUN AVE 3', 'YISHUN AVE 9', 'YISHUN ST 61',
                'YISHUN ST 72', 'YISHUN ST 81', 'ANG MO KIO ST 32',
                'BEDOK NTH ST 4', 'BT BATOK WEST AVE 7', 'JLN RUMAH TINGGI',
                'TELOK BLANGAH WAY', 'TIONG BAHRU RD', 'TELOK BLANGAH RISE',
                'HENDERSON CRES', 'BT PURMEI RD', 'SPOTTISWOODE PK RD',
                'LOMPANG RD', 'SELEGIE RD', 'KELANTAN RD', 'KRETA AYER RD',
                'CHOA CHU KANG ST 53', 'CLEMENTI AVE 6', 'CLEMENTI ST 13',
                'SIMS PL', 'EUNOS RD 5', 'SIMS AVE', 'BUANGKOK CRES',
                'HOUGANG ST 31', 'JURONG EAST AVE 1', 'JURONG WEST ST 24',
                'YUNG PING RD', 'LOR LIMAU', 'TOWNER RD', 'NTH BRIDGE RD',
                'KG ARANG RD', 'DORSET RD', "ST. GEORGE'S LANE", 'PASIR RIS ST 13',
                'PUNGGOL FIELD WALK', 'PUNGGOL EAST', "QUEEN'S CL", "C'WEALTH AVE",
                'CLARENCE LANE', 'DOVER CL EAST', 'ANCHORVALE RD',
                'ANCHORVALE LANE', 'FERNVALE LANE', 'LOR LEW LIAN',
                'SERANGOON NTH AVE 2', 'TAMPINES AVE 5', 'TAMPINES CTRL 1',
                'SIMEI ST 5', 'TAMPINES AVE 7', 'MARSILING LANE',
                'WOODLANDS AVE 4', 'WOODLANDS DR 73', 'WOODLANDS DR 72',
                'MARSILING RD', 'YISHUN ST 71', 'YISHUN ST 20', 'ANG MO KIO AVE 9',
                'ANG MO KIO AVE 2', 'CHAI CHEE DR', 'SIN MING RD', 'MOH GUAN TER',
                'BT MERAH CTRL', "QUEEN'S RD", 'EMPRESS RD', 'JLN KUKOH',
                'VEERASAMY RD', 'WATERLOO ST', 'KLANG LANE', 'CHOA CHU KANG ST 52',
                'CHOA CHU KANG LOOP', 'CHOA CHU KANG ST 54', 'CHOA CHU KANG NTH 7',
                'CLEMENTI ST 12', "C'WEALTH AVE WEST", 'GEYLANG EAST CTRL',
                'GEYLANG SERAI', 'PIPIT RD', 'YUAN CHING RD', 'JURONG WEST ST 72',
                'JURONG WEST ST 62', 'KG KAYU RD', 'WHAMPOA WEST', "JLN MA'MOR",
                'CAMBRIDGE RD', 'PUNGGOL RD', 'SEMBAWANG CRES', 'SEMBAWANG WAY',
                'TAMPINES AVE 9', 'SIMEI ST 2', 'TOA PAYOH NTH', 'JLN DAMAI',
                'BT BATOK ST 22', 'DELTA AVE', 'QUEEN ST', 'DAKOTA CRES',
                'BUANGKOK LINK', 'UPP SERANGOON RD', "KING GEORGE'S AVE",
                'LOR 3 GEYLANG', 'JELLICOE RD', 'PASIR RIS ST 41',
                'WOODLANDS AVE 3', 'WOODLANDS DR 71', 'TAMAN HO SWEE',
                'EVERTON PK', 'ROWELL RD', 'SMITH ST', 'CLEMENTI ST 14',
                'YUNG HO RD', 'KENT RD', 'POTONG PASIR AVE 3', 'YISHUN AVE 7',
                'BISHAN ST 11', 'INDUS RD', 'SAGO LANE', 'NEW MKT RD',
                'CHANDER RD', 'OLD AIRPORT RD', 'WOODLANDS AVE 9', 'KIM PONG RD',
                'BUFFALO RD', 'CANBERRA LINK', 'BAIN ST', 'JLN DUA', 'OWEN RD',
                'TESSENSOHN RD', 'GHIM MOH LINK', 'MARSILING CRES',
                'ANG MO KIO ST 11', 'SILAT AVE', 'KIM CHENG ST', 'MOULMEIN RD',
                'CLEMENTI ST 11', 'YISHUN CTRL 1', 'JLN BERSEH', 'FRENCH RD',
                'BT MERAH LANE 1', 'SIMEI LANE', 'JOO CHIAT RD', 'TAO CHING RD',
                'CLEMENTI AVE 1', 'YISHUN ST 41', 'TELOK BLANGAH ST 31', 'nan',
                'ZION RD', 'ROCHOR RD', 'JLN PASAR BARU', 'YUNG KUANG RD',
                'SELETAR WEST FARMWAY 6', 'MARGARET DR', 'WOODLANDS CTR RD',
                'HENDERSON RD', 'EAST COAST RD', 'KG BAHRU HILL',
                'GEYLANG EAST AVE 2', 'MARINE PARADE CTRL', 'JLN KAYU',
                'LOR 1A TOA PAYOH', 'PUNGGOL WALK', 'SENGKANG WEST WAY',
                'BUANGKOK GREEN', 'PUNGGOL WAY', 'YISHUN ST 31', 'TECK WHYE CRES',
                'MONTREAL LINK', 'UPP SERANGOON CRES', 'SUMANG LINK',
                'SENGKANG EAST AVE', 'YISHUN AVE 1', 'ANCHORVALE CRES',
                'ANCHORVALE ST', 'TAMPINES CTRL 8', 'YISHUN ST 51',
                'UPP SERANGOON VIEW', 'TAMPINES AVE 1', 'BEDOK RESERVOIR CRES',
                'ANG MO KIO ST 61', 'DAWSON RD', 'FERNVALE ST', 'HOUGANG ST 32',
                'TAMPINES ST 86', 'SUMANG WALK', 'CHOA CHU KANG AVE 7',
                'KEAT HONG CL', 'JURONG WEST CTRL 3', 'KEAT HONG LINK',
                'ALJUNIED AVE 2', 'CANBERRA CRES', 'SUMANG LANE', 'CANBERRA ST',
                'ANG MO KIO ST 44', 'WOODLANDS RISE', 'CANBERRA WALK',
                'ANG MO KIO ST 51', 'BT BATOK EAST AVE 6', 'BT BATOK WEST AVE 9']



# Define the validation function for checking input completeness
def validate_input(value):
    return value is not None and value != ''
    
def regression():
    # Define options (town, flat_type, block, etc.)
    # Include these options based on your data and model requirements

    with st.form("Regression"):
        town = st.selectbox(label='Town',  options=options.town)
        flat_type = st.selectbox(label='flat_type', options=options.flat_type)
        block = st.selectbox(label='Block', options=options.block)
        floor_area_sqm = st.number_input(label='floor_area_sqm', min_value=1, max_value=350, value=28)
        storey_range = st.selectbox(label='storey_range', options=options.storey_range)
        street_name = st.selectbox(label='street_name', options=options.street_name)
        month_month = st.number_input(label='month_month (Min: 1 & Max: 12)')
        flat_model = st.selectbox(label='flat_model', options=options.flat_model)
        #month_year = st.number_input(label='month_year (Min: 1990  Max: 2020 and above)')
        #lease_commence_year = st.number_input(label='lease_commence_year (Min: 1800  Max: 2000 and above)')
        
        month_year = st.selectbox(label='month_year', options=range(1990, 2100), index=30)  
        lease_commence_year = st.selectbox(label='lease_commence_year', options=range(1800, 2100), index=200)  



        submitted = st.form_submit_button("Submit")

        if submitted:
            # Load pickled model, scaler, and ordinal_encoder
            with open(r'C:\Users\shali\ML Folder\scaler_sg.pkl', 'rb') as file:
                scaler = pickle.load(file)

            with open(r'C:\Users\shali\ML Folder\ordinal_encoder.pkl', 'rb') as file:
                ordinal_encoder = pickle.load(file)

            with open(r'C:\Users\shali\ML Folder\sg_model.pkl', 'rb') as file:
                model = pickle.load(file)

            lease_commence_date = datetime(lease_commence_year, 1, 1)
    
            # Calculate property_current_age
            current_date = datetime.now()
            property_current_age = current_date.year - lease_commence_date.year
            
            # Calculate current_remaining_lease_years
            current_year = datetime.now().year
            total_lease_year = 99 + lease_commence_date.year
            current_remaining_lease_years = total_lease_year - current_year

            # Prepare user input as a list

            user_input = np.array([[town, flat_type, block, street_name, storey_range, floor_area_sqm, flat_model, month_month, month_year, lease_commence_year]])
            print("user_input:")
            print(user_input)
            
            # Apply ordinal encoding to categorical features
            user_input_encoded = ordinal_encoder.transform(user_input[:, [0, 1, 2, 3, 4, 6]])

            numerical_indices = [5, 7, 8, 9]

            # Separating numerical and categorical features
            numerical_data = user_input[:, numerical_indices]
            print("numerical_data:")
            print(numerical_data)
            
            categorical_data = user_input_encoded  # Encoded categorical features
            print("categorical_data:")
            print(categorical_data)
            
            # Combine numerical and categorical features
            all_features = np.concatenate((numerical_data, categorical_data), axis=1)
            print("all_features:")
            print(all_features)
            
            # Scale all 10 features
            all_features_scaled = scaler.transform(all_features)
            print(all_features_scaled)
            
            # Make the prediction
            y_pred = model.predict(all_features_scaled)[0]
            selling_price = round(y_pred, 2)
            print("Predicted Selling Price:")
            print(selling_price)
            
            #st.write(y_pred)
            # Display the predicted selling price
            st.markdown(f'### Predicted Selling Price = {selling_price}')
            st.write('Property Current Age:', property_current_age)
            st.write('Current Remaining Lease Years:', current_remaining_lease_years)
            st.snow()
            
# Streamlit configuration
def streamlit_config():
    st.set_page_config(page_title='Singapore Flat Resale Price Predictor')
    page_background_color = """
        <style>
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        </style>
        """
    st.markdown(page_background_color, unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align: center;">Singapore Flat Resale Price Predictor</h1>', unsafe_allow_html=True)

# Entry point
def main():
    streamlit_config()
    tabs = st.tabs(['PREDICT SELLING PRICE'])
    
    if tabs[0]:
        try:
            regression()
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
            