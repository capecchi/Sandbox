def main(stock):
    import numpy as np
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation
    import pandas as pd
    from matplotlib import cm
    plt.rcParams['animation.ffmpeg_path'] = 'C:/FFMPEG/bin/ffmpeg'


    #data from 1-78
    direc = 'C:/Users/Owner/Desktop/Projects/Upwork/Causa/'
    fsav = direc+stock+'_analysis'
    f = np.load(fsav+'.npz')
    scan = f['scan']
    roi = f['in_inv_scan']
    #norm = [(d-np.min(roi))/np.max(roi) for d in roi]
    norm = np.load(direc+'norm.npy')

    a = [i[0] for i in scan]
    b = [i[1] for i in scan]
    c = [i[2] for i in scan]
    df = pd.DataFrame({"roi":roi,"a":a,"b":b,"c":c,"norm":norm})
    steps = 100
    setnorm = pd.DataFrame({"roi":[1,1],"a":[0,0],"b":[0,0],"c":[0,0],"norm":[0,1]})
    
    def update_graph(num):
        data=df[df['norm']>= num/100.]
        data = data[data['norm'] < (num+1)/100.]
        data = data.append(setnorm)
        plt.clf()
        ax = fig.add_subplot(111, projection='3d')
        title = ax.set_title('3D Test')
        ax.set_xlim3d([0.0, 78.0])
        ax.set_xlabel('A')
        ax.set_ylim3d([0.0, 78.0])
        ax.set_ylabel('B')
        ax.set_zlim3d([0.0, 78.0])
        ax.set_zlabel('C')
        graph = ax.scatter(data.a, data.b, data.c,cmap=cm.nipy_spectral,c=data.norm,s=2)
        #graph = ax.scatter(data.a, data.b, data.c,s=1)
        title.set_text('Optimization, ROI(norm)={}'.format(num/100.))


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    title = ax.set_title('Optimization')

    ax.set_xlim3d([0.0, 78.0])
    ax.set_xlabel('A')
    ax.set_ylim3d([0.0, 78.0])
    ax.set_ylabel('B')
    ax.set_zlim3d([0.0, 78.0])
    ax.set_zlabel('C')

    data = df
    graph = ax.scatter(data.a, data.b, data.c,cmap=cm.bwr,c=norm,s=1)
    graph.remove()

    ani = matplotlib.animation.FuncAnimation(fig, update_graph, frames=steps, 
                                   interval=100, blit=False)

    mywriter = matplotlib.animation.FFMpegWriter(fps=20,extra_args=['-vcodec', 'libx264'])
    ani.save('scan3d_animation.mp4',writer=mywriter)
    plt.show()
