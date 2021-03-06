
        set term post eps color enhanced 12
        set out "likelihood_projection_for_mass6.eps"
        set xlabel "{/=28 mass:6}"
        set title "{/=28 likelihood: projection for mass:6}" 
        a=190.0
        b=-20.0
        c=834.5098106
        f(x)=1/(2*b**2)*(x-a)**2+c
        fit f(x) 'likelihood_projection_for_mass6.dat' u 1:2:3 via a,b,c
        plot 'likelihood_projection_for_mass6.dat' u 1:2:3 with errorbar title "" , 1/(2*b**2)*(x-a)**2+c title "fit" 
