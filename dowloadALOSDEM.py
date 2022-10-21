def DownloadALOSDEM(MinLat:int, MaxLat:int, MinLong:int, 
                    MaxLong:int, E:str, N:str, SavePath:str, ) -> None:
    
    """
    
    This is a convenient function to download ALOS DEM from opentopography, 
    the Long and Lat information are given in D°M°S.
    
    E: EASTING 'W' or 'E'
    N:NORTHING: 'N' or 'S'
    
     
    
    The following Packages are required boto3 to connect to AWS S3 bucket, botocore, numpy and os
    
    """
    
    import boto3
    from botocore.config import Config
    import numpy as np
    from botocore import UNSIGNED
    import numpy as np
    import os
    s3 = (boto3
          .resource('s3',endpoint_url='https://opentopography.s3.sdsc.edu', 
                    config=Config(signature_version=UNSIGNED)))
    
    bucket = s3.Bucket("raster")
    
    #Create a list of all the ALOS tiles available 
    List_ALOSDEM = []

    for obj in bucket.objects.filter(Prefix="AW3D30/AW3D30_global/ALPSMLC30").all():
        List_ALOSDEM.append(obj.key)
        
    Lat = []
    Long = []
    EASTING = []
    NORTHING = []

    for i in range(len(List_ALOSDEM)):
        EASTING.append(List_ALOSDEM[i][35])
        NORTHING.append(List_ALOSDEM[i][31])
        Lat.append(int(List_ALOSDEM[i][32:35]))
        Long.append(int(List_ALOSDEM[i][36:39]))

    Lat = np.array(Lat)
    Long = np.array(Long)
    EASTING = np.array(EASTING)
    NORTHING = np.array(NORTHING)
    
    List_ALOSDEM = np.array(List_ALOSDEM)
    DemLS = (List_ALOSDEM[(Lat > MinLat)&(Lat < MaxLat) 
                              &(Long > MinLong)&(Long < MaxLong)
                              &(EASTING == E)&(NORTHING == N)])
    
    print(f"The number of DEM that will be download is: {len(DemLS)}")
    
    for i in range(DemLS.shape[0]):
    
        Pth = os.path.join(os.path.normpath(SavePath), DemLS[i][31:])
        bucket.download_file(DemLS[i], Pth)
