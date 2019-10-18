import numpy as np

'''
Finds the mean across a set of models.

Input: 
models = dataset for a variable, within which each "variable" is a model
names = string list of model names, aka the titles of the "variables" in models
(optional) loc = [lonmin, lonmax, latmin, latmax] = list of lat/lon bounds for a region to do an area average (but global is default)

Output:
multimodel mean with dimension [time]
'''

def multiModelMean(ds,names,loc=None):
    
    nmod = len(names)
    ntime = len(ds.time)
    print('Number time steps: ' + str(ntime))
    print('Number of models: ' + str(nmod))
    
    tempdata = np.empty((nmod,ntime))
    
    ### average the data over the lat-lon range you need:###
    for m in range(nmod):
        print('Averaging for model ' + str(m+1) + '...')
        modelname = names[m]
        model = ds[modelname] 
        
        # global mean:
        if loc == None:
            tempdata[m,:] = model.mean(dim=['lat','lon'])
            
        # specific location:
        else:
            if len(loc) != 4:
                raise Exception('Must enter location in the form [minlon, maxlon, minlat, maxlat]!')
            lonmin = loc[0]
            lonmax = loc[1]
            latmin = loc[2]
            latmax = loc[3]
            
            tempdata[m,:] = model.sel(lat=slice(latmin,latmax),lon=slice(lonmin,lonmax)).mean()
   
    print('Model averaging done.')
    
    ### multimodel mean and spread:### 
    print(type(tempdata))
    print('Computing multimodel statistics...')
    mm_mean = np.nanmean(tempdata,axis=0)
    print('...done!')
    
    return mm_mean