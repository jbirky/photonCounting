def plotImg(arr, **kwargs):
    
    avg = mean(arr.flatten())
    std = stdev(arr.flatten())
    
    sigma = kwargs.get('sigma', 5)
    rng = kwargs.get('rng', [avg-sigma*std, avg+sigma*std])
    
    pl = plt.imshow(arr, origin='lower', interpolation='nearest', cmap='gray', vmin=rng[0], vmax=rng[1])
    if 'sigma' in kwargs: 
        plt.colorbar(pl).set_label('Detector Value %s-$\sigma$ scale (ADU)'%(sigma))
    else:
        plt.colorbar(pl).set_label('Detector Value (ADU)')
    plt.xlabel('pixels(x)')
    plt.ylabel('pixels(y)')
    plt.show()

def plotHist(arr, **kwargs):
    
    avg = mean(arr)
    std = stdev(arr)
    med = np.median(arr)
    
    sigma = kwargs.get('sigma', 5)
    low = int(np.round((avg-sigma*std)))
    high = int(np.round((avg+sigma*std)))
    rng = kwargs.get('rng', [low, high])
    exp = kwargs.get('exp')
    
    hr = np.arange(rng[0], rng[1])
    hist = []
    for i in hr:
        counts = len(np.where(arr==i)[0])
        hist.append(counts)
    plt.step(hr, hist, color='k')

    plt.axvline(avg, color='b', label=r'$\bar{x}=%s$'%(np.round(avg,2)))
    plt.axvline(med, color='b', label=r'$\tilde{x}=%s$'%(np.round(med,2)), linestyle='dashed')
    if kwargs.get('show_level', True) == True:
        for i in np.arange(1,sigma+1):
            if i == 1:
                plt.axvspan(avg-i*std, avg+i*std, facecolor='g', alpha=0.05, label=r'$\sigma=\pm %s$'%(np.round(std,2)))
            else:
                plt.axvspan(avg-i*std, avg+i*std, facecolor='g', alpha=0.05)
    
    plt.legend(loc='upper left')
    plt.xlabel('Counts (ADU)')
    plt.ylabel('Frequency')
    if 'exp' in kwargs:
        plt.title('Exposure Time: %s sec'%(exp))
    plt.xlim(rng)
    plt.show()

def factorial(n, **kwargs):
    
    method = kwargs.get('method', 'sterling')
    
    if method == 'exact':
        nfact = 1
        for i in range(n):
            nfact *= (i+1)
    # sterling approximation
    elif method == 'sterling': 
        nfact = math.sqrt(2*math.pi) * n**(n+.5) / math.e**n
        
    return nfact

def cutData(array, **kwargs):
    
    avg = mean(array)
    std = stdev(array)
    arr_rng = [min(array), max(array)]
    
    if 'sigma' in kwargs:
        sigma = kwargs.get('sigma')
        low = int(np.round((avg-sigma*std)))
        high = int(np.round((avg+sigma*std)))
        cut = kwargs.get('cut', [low, high])
    elif 'rng' in kwargs:
        cut = kwargs.get('rng')
    else:
        cut = kwargs.get('cut', arr_rng)
    pixel_keep = np.where((array > cut[0]) & (array < cut[1]))[0]
    
    cut_array = array[pixel_keep]
    per_rem = np.round((1 - len(cut_array)/len(array))*100,2)
    print('Cut from range %s to %s, removing %s percent of data points'%(arr_rng, cut, per_rem))
    
    return cut_array