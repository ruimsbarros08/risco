

#ABRAHAMSON_ET_AL_2014           = 'AbrahamsonEtAl2014'
#ABRAHAMSON_ET_AL_2015           = 'AbrahamsonEtAl2015'
ABRAHAMSON_AND_SILVA_2008       = 'AbrahamsonSilva2008'
AKKAR_AND_BOMMER_2010           = 'AkkarBommer2010'
AKKAR_AND_CAGNAN_2010           = 'AkkarCagnan2010'
BOORE_AND_ATKINSON_2008         = 'BooreAtkinson2008'
CAUZZI_AND_FACCIOLI_2008        = 'CauzziFaccioli2008'
CHIOU_AND_YOUNGS_2008           = 'ChiouYoungs2008'
FACCIOLI_ET_AL_2010             = 'FaccioliEtAl2010'
SADIGH_ET_AL_1997               = 'SadighEtAl1997'
ZHAO_ET_AL_2006_ASC             = 'ZhaoEtAl2006Asc'
ATKINSON_AND_BOORE_2003_INTER   = 'AtkinsonBoore2003SInter'
ATKINSON_AND_BOORE_2003_IN_SLAB = 'AtkinsonBoore2003SSlab'
LIN_AND_LEE_2008_INTER          = 'LinLee2008SInter'
LIN_AND_LEE_2008_IN_SLAB        = 'LinLee2008SSlab'
YOUNGS_ET_AL_1997_INTER         = 'YoungsEtAl1997SInter'
YOUNGS_ET_AL_1997_IN_SLAB       = 'YoungsEtAl1997SSlab'
ZHAO_ET_AL_2006_INTER           = 'ZhaoEtAl2006SInter'
ZHAO_ET_AL_2006_IN_SLAB         = 'ZhaoEtAl2006SSlab'
ATKINSON_AND_BOORE_2006         = 'AtkinsonBoore2006'
CAMPBELL_2003                   = 'Campbell2003'
TORO_ET_AL_2002                 = 'ToroEtAl2002'

GMPE_CHOICES = (
    #(ABRAHAMSON_ET_AL_2014              ,'Abrahamson et Al. 2014'),
    (ABRAHAMSON_AND_SILVA_2008          ,'Abrahamson and Silva 2008'),
    (AKKAR_AND_BOMMER_2010              ,'Akkar and Boomer 2010'),
    (AKKAR_AND_CAGNAN_2010              ,'Akkar and Cagnan 2010'),
    (BOORE_AND_ATKINSON_2008            ,'Boore and Atkinson 2008'),
    (CAUZZI_AND_FACCIOLI_2008           ,'Cauzzi and Faccioli 2008'),
    (CHIOU_AND_YOUNGS_2008              ,'Chiou and Youngs 2008'),
    (FACCIOLI_ET_AL_2010                ,'Faccioli et al. 2010'),
    (SADIGH_ET_AL_1997                  ,'Sadigh et al. 1997'),
    (ZHAO_ET_AL_2006_ASC                ,'Zhao et al. 2006 (ASC)'),
    (ATKINSON_AND_BOORE_2003_INTER      ,'Atkinson and Boore 2003 (Inter)'),
    (ATKINSON_AND_BOORE_2003_IN_SLAB    ,'Atkinson and Boore 2003 (In-slab)'),
    (LIN_AND_LEE_2008_INTER             ,'Lin and Lee 2008 (Inter)'),
    (LIN_AND_LEE_2008_IN_SLAB           ,'Lin and Lee 2008 (In-slab)'),
    (YOUNGS_ET_AL_1997_INTER            ,'Youngs et al. 1997 (Inter)'),
    (YOUNGS_ET_AL_1997_IN_SLAB          ,'Youngs et al. 1997 (In-slab)'),
    (ZHAO_ET_AL_2006_INTER              ,'Zhao et al. 2006 (Inter)'),
    (ZHAO_ET_AL_2006_IN_SLAB            ,'Zhao et al. 2006 (In-slab)'),
    (ATKINSON_AND_BOORE_2006            ,'Atkinson and Boore 2006'),
    (CAMPBELL_2003                      ,'Campbell 2003'),
    (TORO_ET_AL_2002                    ,'Toro et al. 2002'),
)



ACTIVE = 'Active Shallow Crust'
STABLE = 'Stable Shallow Crust'
SUBDUCTION = 'Subduction Interface'
ACTIVE_INTERSLAB = 'Active Interslab'
VOLCANIC = 'Volcanic'
TECTONIC_CHOICES = (
    (ACTIVE, 'Active Shallow Crust'),
    (STABLE, 'Stable Shallow Crust'),
    (SUBDUCTION, 'Subduction Interface'),
    (ACTIVE_INTERSLAB, 'Active Interslab'),
    (VOLCANIC, 'Volcanic'),
    )