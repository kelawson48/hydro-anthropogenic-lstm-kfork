import collections
import os
import unittest
import definitions
from data import *

import geopandas as gpd

from data.download_data import download_google_drive
from utils import spatial_join


class TestDataFuncCase(unittest.TestCase):
    config_file = definitions.CONFIG_FILE
    project_dir = definitions.ROOT_DIR
    dataset = 'gages'
    # dataset = 'camels'
    dir_db = os.path.join(project_dir, 'example/data', dataset)
    dir_out = os.path.join(project_dir, 'example/output', dataset)
    dir_temp = os.path.join(project_dir, 'example/temp', dataset)
    gages_screen_ids = ["01013500",
                        "01022500",
                        "01030500",
                        "01031500",
                        "01047000",
                        "01052500",
                        "01054200",
                        "01055000",
                        "01057000",
                        "01073000",
                        "01078000",
                        "01118300",
                        "01121000",
                        "01123000",
                        "01134500",
                        "01137500",
                        "01139000",
                        "01139800",
                        "01142500",
                        "01144000",
                        "01162500",
                        "01169000",
                        "01170100",
                        "01181000",
                        "01187300",
                        "01195100",
                        "01333000",
                        "01350000",
                        "01350080",
                        "01350140",
                        "01365000",
                        "01411300",
                        "01413500",
                        "01414500",
                        "01415000",
                        "01423000",
                        "01434025",
                        "01435000",
                        "01439500",
                        "01440000",
                        "01440400",
                        "01451800",
                        "01466500",
                        "01484100",
                        "01485500",
                        "01486000",
                        "01487000",
                        "01491000",
                        "01510000",
                        "01516500",
                        "01518862",
                        "01532000",
                        "01539000",
                        "01542810",
                        "01543000",
                        "01543500",
                        "01544500",
                        "01545600",
                        "01547700",
                        "01548500",
                        "01549500",
                        "01550000",
                        "01552000",
                        "01552500",
                        "01557500",
                        "01567500",
                        "01568000",
                        "01580000",
                        "01583500",
                        "01586610",
                        "01591400",
                        "01594950",
                        "01596500",
                        "01605500",
                        "01606500",
                        "01613050",
                        "01620500",
                        "01632000",
                        "01632900",
                        "01634500",
                        "01638480",
                        "01639500",
                        "01644000",
                        "01658500",
                        "01664000",
                        "01666500",
                        "01667500",
                        "01669000",
                        "01669520",
                        "02011400",
                        "02011460",
                        "02013000",
                        "02014000",
                        "02015700",
                        "02016000",
                        "02017500",
                        "02018000",
                        "02027000",
                        "02027500",
                        "02028500",
                        "02038850",
                        "02046000",
                        "02051000",
                        "02051500",
                        "02053200",
                        "02053800",
                        "02055100",
                        "02056900",
                        "02059500",
                        "02064000",
                        "02065500",
                        "02069700",
                        "02070000",
                        "02074500",
                        "02077200",
                        "02081500",
                        "02082950",
                        "02092500",
                        "02096846",
                        "02102908",
                        "02108000",
                        "02111180",
                        "02111500",
                        "02112120",
                        "02112360",
                        "02118500",
                        "02125000",
                        "02128000",
                        "02137727",
                        "02140991",
                        "02143000",
                        "02143040",
                        "02149000",
                        "02152100",
                        "02177000",
                        "02178400",
                        "02193340",
                        "02196000",
                        "02198100",
                        "02202600",
                        "02212600",
                        "02215100",
                        "02216180",
                        "02221525",
                        "02231000",
                        "02231342",
                        "02235200",
                        "02245500",
                        "02246000",
                        "02296500",
                        "02297155",
                        "02297310",
                        "02298123",
                        "02298608",
                        "02299950",
                        "02300700",
                        "02310947",
                        "02312200",
                        "02314500",
                        "02315500",
                        "02324400",
                        "02327100",
                        "02342933",
                        "02349900",
                        "02350900",
                        "02361000",
                        "02363000",
                        "02369800",
                        "02371500",
                        "02372250",
                        "02374500",
                        "02381600",
                        "02384540",
                        "02395120",
                        "02408540",
                        "02415000",
                        "02422500",
                        "02427250",
                        "02430085",
                        "02430615",
                        "02450250",
                        "02464000",
                        "02464146",
                        "02464360",
                        "02465493",
                        "02469800",
                        "02472000",
                        "02472500",
                        "02479155",
                        "02479300",
                        "02479560",
                        "02481000",
                        "02481510",
                        "03010655",
                        "03011800",
                        "03015500",
                        "03021350",
                        "03026500",
                        "03028000",
                        "03049000",
                        "03049800",
                        "03050000",
                        "03066000",
                        "03069500",
                        "03070500",
                        "03076600",
                        "03078000",
                        "03140000",
                        "03144000",
                        "03159540",
                        "03161000",
                        "03164000",
                        "03165000",
                        "03170000",
                        "03173000",
                        "03180500",
                        "03182500",
                        "03186500",
                        "03187500",
                        "03213700",
                        "03237280",
                        "03237500",
                        "03238500",
                        "03241500",
                        "03280700",
                        "03281100",
                        "03281500",
                        "03285000",
                        "03291780",
                        "03300400",
                        "03338780",
                        "03340800",
                        "03346000",
                        "03357350",
                        "03364500",
                        "03366500",
                        "03368000",
                        "03384450",
                        "03439000",
                        "03450000",
                        "03455500",
                        "03456500",
                        "03460000",
                        "03463300",
                        "03471500",
                        "03473000",
                        "03479000",
                        "03488000",
                        "03498500",
                        "03500000",
                        "03500240",
                        "03504000",
                        "03574500",
                        "03592718",
                        "03604000",
                        "04015330",
                        "04024430",
                        "04027000",
                        "04040500",
                        "04043050",
                        "04045500",
                        "04056500",
                        "04057510",
                        "04057800",
                        "04059500",
                        "04063700",
                        "04074950",
                        "04105700",
                        "04115265",
                        "04122200",
                        "04122500",
                        "04124000",
                        "04127918",
                        "04127997",
                        "04161580",
                        "04185000",
                        "04196800",
                        "04197100",
                        "04197170",
                        "04213000",
                        "04213075",
                        "04216418",
                        "04221000",
                        "04224775",
                        "04233000",
                        "04256000",
                        "04296000",
                        "05056000",
                        "05057000",
                        "05057200",
                        "05062500",
                        "05087500",
                        "05120500",
                        "05123400",
                        "05129115",
                        "05131500",
                        "05291000",
                        "05362000",
                        "05393500",
                        "05399500",
                        "05408000",
                        "05412500",
                        "05413500",
                        "05414000",
                        "05444000",
                        "05454000",
                        "05458000",
                        "05466500",
                        "05487980",
                        "05488200",
                        "05489000",
                        "05495000",
                        "05495500",
                        "05501000",
                        "05503800",
                        "05507600",
                        "05508805",
                        "05514500",
                        "05525500",
                        "05556500",
                        "05584500",
                        "05585000",
                        "05591550",
                        "05592050",
                        "05592575",
                        "05593575",
                        "05593900",
                        "05595730",
                        "06037500",
                        "06043500",
                        "06154410",
                        "06188000",
                        "06191500",
                        "06221400",
                        "06224000",
                        "06278300",
                        "06280300",
                        "06289000",
                        "06291500",
                        "06311000",
                        "06332515",
                        "06339100",
                        "06339500",
                        "06344600",
                        "06350000",
                        "06352000",
                        "06353000",
                        "06354000",
                        "06360500",
                        "06404000",
                        "06406000",
                        "06408700",
                        "06409000",
                        "06431500",
                        "06440200",
                        "06441500",
                        "06447000",
                        "06447500",
                        "06450500",
                        "06452000",
                        "06453600",
                        "06464500",
                        "06468170",
                        "06468250",
                        "06470800",
                        "06477500",
                        "06479215",
                        "06479438",
                        "06601000",
                        "06614800",
                        "06622700",
                        "06623800",
                        "06632400",
                        "06746095",
                        "06784000",
                        "06803510",
                        "06803530",
                        "06814000",
                        "06847900",
                        "06853800",
                        "06876700",
                        "06878000",
                        "06879650",
                        "06885500",
                        "06888500",
                        "06889200",
                        "06889500",
                        "06892000",
                        "06903400",
                        "06906800",
                        "06910800",
                        "06911900",
                        "06917000",
                        "06918460",
                        "06919500",
                        "06921070",
                        "06921200",
                        "06934000",
                        "07014500",
                        "07056000",
                        "07057500",
                        "07060710",
                        "07066000",
                        "07067000",
                        "07068000",
                        "07071500",
                        "07083000",
                        "07142300",
                        "07145700",
                        "07148400",
                        "07149000",
                        "07151500",
                        "07167500",
                        "07180500",
                        "07184000",
                        "07195800",
                        "07196900",
                        "07197000",
                        "07208500",
                        "07226500",
                        "07261000",
                        "07263295",
                        "07290650",
                        "07291000",
                        "07292500",
                        "07295000",
                        "07299670",
                        "07301410",
                        "07301500",
                        "07315200",
                        "07315700",
                        "07335700",
                        "07340300",
                        "07346045",
                        "07359610",
                        "07362100",
                        "07362587",
                        "07373000",
                        "07375000",
                        "07376000",
                        "08013000",
                        "08014500",
                        "08023080",
                        "08025500",
                        "08029500",
                        "08050800",
                        "08066200",
                        "08066300",
                        "08070000",
                        "08070200",
                        "08079600",
                        "08082700",
                        "08086212",
                        "08086290",
                        "08101000",
                        "08103900",
                        "08104900",
                        "08109700",
                        "08150800",
                        "08155200",
                        "08158700",
                        "08158810",
                        "08164000",
                        "08164300",
                        "08164600",
                        "08165300",
                        "08171300",
                        "08175000",
                        "08176900",
                        "08178880",
                        "08189500",
                        "08190000",
                        "08190500",
                        "08194200",
                        "08195000",
                        "08196000",
                        "08198500",
                        "08200000",
                        "08202700",
                        "08267500",
                        "08269000",
                        "08271000",
                        "08324000",
                        "08377900",
                        "08378500",
                        "08380500",
                        "09034900",
                        "09035800",
                        "09035900",
                        "09047700",
                        "09065500",
                        "09066000",
                        "09066200",
                        "09066300",
                        "09081600",
                        "09107000",
                        "09210500",
                        "09223000",
                        "09306242",
                        "09312600",
                        "09352900",
                        "09378170",
                        "09378630",
                        "09386900",
                        "09404450",
                        "09430500",
                        "09430600",
                        "09447800",
                        "09480000",
                        "09484000",
                        "09484600",
                        "09492400",
                        "09494000",
                        "09497800",
                        "09497980",
                        "09505200",
                        "09505350",
                        "09505800",
                        "09508300",
                        "09510200",
                        "09512280",
                        "09513780",
                        "10023000",
                        "10166430",
                        "10172700",
                        "10172800",
                        "10173450",
                        "10205030",
                        "10234500",
                        "10242000",
                        "10244950",
                        "10249300",
                        "10258000",
                        "10258500",
                        "10259000",
                        "10259200",
                        "10263500",
                        "10310500",
                        "10316500",
                        "10329500",
                        "10336645",
                        "10336660",
                        "10336740",
                        "10343500",
                        "10348850",
                        "10396000",
                        "11098000",
                        "11124500",
                        "11141280",
                        "11143000",
                        "11148900",
                        "11151300",
                        "11162500",
                        "11176400",
                        "11180500",
                        "11180960",
                        "11224500",
                        "11230500",
                        "11237500",
                        "11253310",
                        "11264500",
                        "11266500",
                        "11274500",
                        "11274630",
                        "11284400",
                        "11299600",
                        "11381500",
                        "11383500",
                        "11451100",
                        "11468500",
                        "11473900",
                        "11475560",
                        "11476600",
                        "11478500",
                        "11480390",
                        "11481200",
                        "11482500",
                        "11522500",
                        "11523200",
                        "11528700",
                        "11532500",
                        "12010000",
                        "12013500",
                        "12020000",
                        "12025000",
                        "12025700",
                        "12035000",
                        "12040500",
                        "12041200",
                        "12043000",
                        "12048000",
                        "12054000",
                        "12056500",
                        "12073500",
                        "12082500",
                        "12092000",
                        "12095000",
                        "12114500",
                        "12115000",
                        "12115500",
                        "12117000",
                        "12141300",
                        "12143600",
                        "12144000",
                        "12145500",
                        "12147500",
                        "12147600",
                        "12167000",
                        "12175500",
                        "12178100",
                        "12186000",
                        "12189500",
                        "12358500",
                        "12374250",
                        "12375900",
                        "12377150",
                        "12381400",
                        "12383500",
                        "12388400",
                        "12390700",
                        "12411000",
                        "12414500",
                        "12447390",
                        "12451000",
                        "12488500",
                        "13011500",
                        "13011900",
                        "13018300",
                        "13023000",
                        "13083000",
                        "13161500",
                        "13235000",
                        "13240000",
                        "13310700",
                        "13313000",
                        "13331500",
                        "13337000",
                        "13338500",
                        "13340000",
                        "13340600",
                        "14020000",
                        "14092750",
                        "14096850",
                        "14137000",
                        "14138800",
                        "14138870",
                        "14138900",
                        "14139800",
                        "14141500",
                        "14154500",
                        "14158500",
                        "14158790",
                        "14166500",
                        "14182500",
                        "14185000",
                        "14185900",
                        "14187000",
                        "14216500",
                        "14222500",
                        "14236200",
                        "14301000",
                        "14303200",
                        "14305500",
                        "14306340",
                        "14306500",
                        "14308990",
                        "14309500",
                        "14316700",
                        "14325000",
                        "14362250",
                        "14400000"
                        ]
    t_train = ['1995-10-01', '2000-10-01']
    t_test = ['2000-10-01', '2005-10-01']
    regions = ['bas_ref_all']
    hydroDams = ['NDAMS_2009', 'DDENS_2009',
                 'STOR_NID_2009', 'STOR_NOR_2009', 'MAJ_NDAMS_2009', 'MAJ_DDENS_2009',
                 'RAW_DIS_NEAREST_DAM', 'RAW_AVG_DIS_ALLDAMS',
                 'RAW_DIS_NEAREST_MAJ_DAM', 'RAW_AVG_DIS_ALL_MAJ_DAMS']

    # regions = ['bas_nonref_CntlPlains', 'bas_nonref_EastHghlnds']
    # t_train = ['1995-10-01', '1997-10-01']
    # t_test = ['1997-10-01', '1999-01-01']

    def setUp(self):
        self.config_data = GagesConfig(self.config_file)
        print('setUp...')

    def tearDown(self):
        print('tearDown...')

    def test_init_path(self):
        test_data = collections.OrderedDict(DB=self.dir_db, Out=self.dir_out, Temp=self.dir_temp)
        self.assertEqual(self.config_data.data_path, test_data)

    def test_init_data_param(self):
        opt_data = self.config_data.init_data_param()
        test_data = collections.OrderedDict(varT=['dayl', 'prcp', 'srad', 'swe', 'tmax', 'tmin', 'vp'],
                                            forcingDir='gagesII_forcing',
                                            forcingType='daymet',
                                            forcingUrl=None,
                                            varC=['ELEV_MEAN_M_BASIN', 'SLOPE_PCT', 'DRAIN_SQKM', 'FORESTNLCD06',
                                                  'BARRENNLCD06', 'DECIDNLCD06', 'EVERGRNLCD06', 'MIXEDFORNLCD06',
                                                  'SHRUBNLCD06',
                                                  'GRASSNLCD06', 'WOODYWETNLCD06', 'EMERGWETNLCD06', 'ROCKDEPAVE',
                                                  'AWCAVE', 'PERMAVE', 'RFACT', 'GEOL_REEDBUSH_DOM',
                                                  'GEOL_REEDBUSH_DOM_PCT', 'GEOL_REEDBUSH_SITE',
                                                  'STREAMS_KM_SQ_KM', 'STRAHLER_MAX', 'MAINSTEM_SINUOUSITY',
                                                  'REACHCODE', 'ARTIFPATH_PCT',
                                                  'ARTIFPATH_MAINSTEM_PCT', 'HIRES_LENTIC_PCT', 'BFI_AVE', 'PERDUN',
                                                  'PERHOR', 'TOPWET', 'CONTACT'
                                                  ],
                                            attrDir='basinchar_and_report_sept_2011',
                                            attrUrl=["https://water.usgs.gov/GIS/dsdl/gagesII_9322_point_shapefile.zip",
                                                     "https://water.usgs.gov/GIS/dsdl/basinchar_and_report_sept_2011.zip",
                                                     "https://water.usgs.gov/GIS/dsdl/boundaries_shapefiles_by_aggeco.zip",
                                                     "https://water.usgs.gov/GIS/dsdl/mainstem_line_covers.zip"],
                                            streamflowDir='gages_streamflow',
                                            streamflowUrl='https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb'
                                                          '&site_no={}&referred_module=sw&period=&begin_date={}-{}-{'
                                                          '}&end_date={}-{}-{}',
                                            gageIdScreen=self.gages_screen_ids,
                                            streamflowScreenParam={'missing_data_ratio': 0.1,
                                                                   'zero_value_ratio': 0.005},
                                            regions=self.regions,
                                            tRangeAll=['1980-01-01', '2015-01-01'])
        self.assertEqual(test_data, opt_data)

    def test_download_kaggle_file(self):
        dir_db_ = self.dir_db
        kaggle_json = definitions.KAGGLE_FILE
        name_of_dataset = "owenyy/wbdhu4-a-us-september2019-shpfile"
        path_download = os.path.join(dir_db_, "huc4")
        file_download = os.path.join(path_download, "HUC4.shp")
        download_kaggle_file(kaggle_json, name_of_dataset, path_download, file_download)

    def test_read_gages_config(self):
        gages_data = self.config_data.read_data_config()
        dir_db_ = self.dir_db
        test_data = collections.OrderedDict(root_dir=dir_db_, out_dir=self.dir_out, temp_dir=self.dir_temp,
                                            regions=self.regions,
                                            flow_dir=os.path.join(dir_db_, 'gages_streamflow'),
                                            flow_url='https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb'
                                                     '&site_no={}&referred_module=sw&period=&begin_date={}-{}-{'
                                                     '}&end_date={}-{}-{}',
                                            flow_screen_gage_id=self.gages_screen_ids,  # self.gages_screen_ids,
                                            flow_screen_param={'missing_data_ratio': 0.1, 'zero_value_ratio': 0.005},
                                            forcing_chosen=['dayl', 'prcp', 'srad', 'swe', 'tmax', 'tmin', 'vp'],
                                            forcing_dir=os.path.join(dir_db_, 'gagesII_forcing', 'daymet'),
                                            forcing_type='daymet',
                                            forcing_url=None,
                                            attr_chosen=['ELEV_MEAN_M_BASIN', 'SLOPE_PCT', 'DRAIN_SQKM', 'FORESTNLCD06',
                                                         'BARRENNLCD06', 'DECIDNLCD06', 'EVERGRNLCD06',
                                                         'MIXEDFORNLCD06',
                                                         'SHRUBNLCD06',
                                                         'GRASSNLCD06', 'WOODYWETNLCD06', 'EMERGWETNLCD06',
                                                         'ROCKDEPAVE',
                                                         'AWCAVE', 'PERMAVE', 'RFACT', 'GEOL_REEDBUSH_DOM',
                                                         'GEOL_REEDBUSH_DOM_PCT', 'GEOL_REEDBUSH_SITE',
                                                         'STREAMS_KM_SQ_KM', 'STRAHLER_MAX', 'MAINSTEM_SINUOUSITY',
                                                         'REACHCODE', 'ARTIFPATH_PCT',
                                                         'ARTIFPATH_MAINSTEM_PCT', 'HIRES_LENTIC_PCT', 'BFI_AVE',
                                                         'PERDUN',
                                                         'PERHOR', 'TOPWET', 'CONTACT'],
                                            attr_dir=os.path.join(dir_db_, 'basinchar_and_report_sept_2011'),
                                            attr_url=[
                                                "https://water.usgs.gov/GIS/dsdl/gagesII_9322_point_shapefile.zip",
                                                "https://water.usgs.gov/GIS/dsdl/basinchar_and_report_sept_2011.zip",
                                                "https://water.usgs.gov/GIS/dsdl/boundaries_shapefiles_by_aggeco.zip",
                                                "https://water.usgs.gov/GIS/dsdl/mainstem_line_covers.zip"],
                                            gage_files_dir=os.path.join(dir_db_, 'basinchar_and_report_sept_2011',
                                                                        'spreadsheets-in-csv-format'),
                                            gage_id_file=os.path.join(dir_db_, 'basinchar_and_report_sept_2011',
                                                                      'spreadsheets-in-csv-format',
                                                                      'conterm_basinid.txt'),
                                            gage_region_dir=os.path.join(dir_db_, 'boundaries_shapefiles_by_aggeco',
                                                                         'boundaries-shapefiles-by-aggeco'),
                                            gage_point_file=os.path.join(dir_db_, "gagesII_9322_point_shapefile",
                                                                         "gagesII_9322_sept30_2011.shp"),
                                            huc4_shp_file=os.path.join(dir_db_, "huc4", "HUC4.shp"),
                                            t_range_all=['1980-01-01', '2015-01-01'])
        self.assertEqual(test_data, gages_data)

    def test_download_small_zip(self):
        dir_db_ = self.dir_db
        data_url = 'https://water.usgs.gov/GIS/dsdl/basinchar_and_report_sept_2011.zip'
        download_small_zip(data_url, dir_db_)

    def test_read_gpd_file(self):
        dir_db_ = self.dir_db
        gage_region_dir = os.path.join(dir_db_, 'boundaries_shapefiles_by_aggeco', 'boundaries-shapefiles-by-aggeco')
        shapefile = os.path.join(gage_region_dir, 'bas_nonref_CntlPlains.shp')
        shape_data = gpd.read_file(shapefile)
        print(shape_data.columns)
        gages_id = shape_data['GAGE_ID'].values
        print(gages_id)

    def test_spatial_join(self):
        dir_db_ = self.dir_db
        points_file = os.path.join(dir_db_, "gagesII_9322_point_shapefile", "gagesII_9322_sept30_2011.shp")
        polygons_file = os.path.join(dir_db_, "huc4", "HUC4.shp")
        spatial_join(points_file, polygons_file)

    def test_download_google_drive(self):
        dir_db_ = self.dir_db
        google_drive_dir_name = "daymet"
        download_dir = os.path.join(dir_db_, 'gagesII_forcing', 'daymet')
        client_secrets_file = os.path.join(dir_db_, "mycreds.txt")
        download_google_drive(client_secrets_file, google_drive_dir_name, download_dir)


if __name__ == '__main__':
    unittest.main()
