

def cool_scatter(rx, show_plot = True):
    from matplotlib.pyplot import figure, plot, grid, subplots_adjust, tick_params, scatter, axhline, axvline, xlim, ylim, show
    from numpy import max
    
    figure('cool_scatter', figsize=(7,7))
    grid(linewidth=0.5)
    colors = range(len(rx.real))
    subplots_adjust(left=0.07, bottom=0.045, top=0.96, right=0.93)
    tick_params(axis='both', direction='in', right=True, top=True, labelright=True, labeltop=True)

    scatter(rx.real, rx.imag, s=10, c=colors, cmap='hsv', alpha=0.9) # jet   rainbow   Wistia  Grays  brg   gist_rainbow 
    #plt.plot(rx.real, rx.imag, color='grey', linewidth=0.2)

    axhline(y = 0, color = 'black', linestyle = '--', linewidth=1)
    axvline(x = 0, color = 'black', linestyle = '--', linewidth=1)
    
    maxi = max(abs(rx)) 
    maxi *= 1.05
    xlim(-maxi,maxi)
    ylim(-maxi,maxi)
    
    if show_plot is True:
        show()
        