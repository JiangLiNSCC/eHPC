import pandas as pd

def str_to_dict(output , split = None):
    output = output.splitlines()
    output = [x.split(split) for x in output]
    outputdir = {}
    for linei in range(len(output)):
        if linei == 0 : continue
        outputdir[ output[linei][0]  ] = {}
        for itemi in range(len( output[linei] )) :
            name = output[0][itemi]
            value = output[linei][itemi]
            outputdir[ output[linei][0]  ][ name ] = value
    return outputdir

def str_to_dataframe( output , split = None  , index = None , parser_cls=None):
    output = output.splitlines()
    output = [x.split(split) for x in output]
    outputdir = {}
    for linei in range(len(output)):
        for itemi in range(len( output[linei] )) :
            name = output[0][itemi]
            if linei == 0 :
                outputdir[ name  ] = []
            else :
                value = output[linei][itemi]
                outputdir[name].append( value )
    df = pd.DataFrame(outputdir)
    if index and index in df.columns :
        df.index = df[ index ]
    if parser_cls :
        df = parser_cls.parser(df)
    return df

class ResultParser(object):
    filter = None # { from : [ ] , to : [ ] }
    convert = None # { 'key' : { from : to  } or 'key' : function convert( ) }
    @classmethod
    def parser(cls , dataframe ):
        df = dataframe
        if cls.filter and cls.filter.get('from' , None) :
            df = df[ cls.filter.get('from' , None)   ]
            if cls.filter.get('to' , None) and  len( df.columns ) == len( cls.filter.get('to' , None)  ) :
                df.columns =  cls.filter.get('to')
        if cls.convert :
            pass
            for coli in cls.convert.keys() :
                if callable( cls.convert[ coli  ] )  :
                    for itemi in df.index : 
                        df[ coli ][ itemi ] = cls.convert[ coli  ] ( df[ coli ][ itemi ]  )
                elif isinstance( cls.convert[ coli  ] ,dict) :
                    for itemi in df.index :
                        if df[ coli ][ itemi ] in cls.convert[ coli  ].keys() :
                            tmpv = df[ coli ][ itemi ] 
                            #print( coli , itemi , tmpv )
                            #print( cls.convert[ coli  ].get(  tmpv   ))
                            #tmpv2 = cls.convert[ coli  ].get(  tmpv   )
                            #df[ coli ][ itemi ] = tempv2
                            df[ coli ][ itemi ] = cls.convert[ coli  ].get(  tmpv   )
        return df
    def __run__(cls , dataframe) :
        return cls.parser( dataframe )
