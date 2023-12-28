from flask import Flask, render_template 
import math 
import random 

app = Flask(__name__) 

@app.route('/') 
def principal(): 
    return render_template("index.html") 

@app.route('/resultado')
def resultado(): 
    coord = { 
        'Jiloyork' :(19.916012, -99.580580),
        'Toluca':(19.289165, -99.655697),
        'Atlacomulco':(19.799520, -99.873844),
        'Guadalajara':(20.677754472859146, -103.34625354877137),
        'Monterrey':(25.69161110159454, -100.321838480256),
        'QuintanaRoo':(21.163111924844458, -86.80231502121464),
        'Michohacan':(19.701400113725654, -101.20829680213464),
        'Aguascalientes':(21.87641043660486, -102.26438663286967),
        'CDMX':(19.432713075976878, -99.13318344772986),
        'QRO':(20.59719437542255, -100.38667040246602)
    }
    
    def distancia(coord1, coord2): 
        lat1 = coord1[0] 
        lon1 = coord1[1] 
        lat2 = coord2[0] 
        lon2 = coord2[1] 
        return math.sqrt((lat1-lat2)**2+(lon1-lon2)**2) 

    def evalua_ruta(ruta): 
        total=0 
        for i in range(0,len(ruta)-1): 
            ciudad1=ruta[i] 
            ciudad2=ruta[i+1] 
            total=total+distancia(coord[ciudad1], coord[ciudad2]) 
        ciudad1=ruta[i+1] 
        ciudad2=ruta[0] 
        total=total+distancia(coord[ciudad1], coord[ciudad2]) 
        return total
    
    def busqueda_tabu(ruta): 
        mejor_ruta=ruta 
        memoria_tabu={} 
        persistencia=5 
        mejora=False 
        iteraciones=100 
    
        while iteraciones>0: 
            iteraciones = iteraciones-1 
            dist_actual=evalua_ruta(ruta) 
            # evaluar vecinos 
            mejora=False 
            for i in range(0,len(ruta)): 
                if mejora: 
                    break 
            for j in range(0,len(ruta)): 
                if i!=j: 
                    ruta_tmp=ruta[:] 
                    ciudad_tmp=ruta_tmp[i] 
                    ruta_tmp[i]=ruta_tmp[j] 
                    ruta_tmp[j]=ciudad_tmp 
                    dist=evalua_ruta(ruta_tmp)

                # comprobar si el movimiento es tabú 
                tabu=False 
                if ruta_tmp[i]+"_"+ruta_tmp[j] in memoria_tabu: 
                    if memoria_tabu[ruta_tmp[i]+"_"+ruta_tmp[j]]>0: 
                        tabu=True 
                if ruta_tmp[j]+"_"+ruta_tmp[i] in memoria_tabu: 
                    if memoria_tabu[ruta_tmp[j]+"_"+ruta_tmp[i]]>0: 
                        tabu=True
                if dist<dist_actual and not tabu: 
                    # encontrado vecino que mejora el resultado 
                    ruta=ruta_tmp[:] 
                    if evalua_ruta(ruta)<evalua_ruta(mejor_ruta): 
                        mejor_ruta=ruta[:] 
                    # almacenamos en memoria tabú 
                    memoria_tabu[ruta_tmp[i]+"_"+ruta_tmp[j]]=persistencia 
                    mejora=True 
                    break 
                elif dist<dist_actual and tabu: 
                    # comprobamos criterio de aspiración 
                    # aunque sea movimiento tabú 
                    if evalua_ruta(ruta_tmp)<evalua_ruta(mejor_ruta): 
                        mejor_ruta=ruta_tmp[:] 
                        ruta=ruta_tmp[:] 
                    # almacenamos en memoria tabú 
                    memoria_tabu[ruta_tmp[i]+"_"+ruta_tmp[j]]=persistencia 
                    mejora=True 
                    break
            
            # rebajar persistencia de los movimientos tabú 
        if len(memoria_tabu)>0: 
            for k in memoria_tabu: 
                if memoria_tabu[k]>0: 
                    memoria_tabu[k]=memoria_tabu[k]-1 

        return mejor_ruta 
    
    ruta = list(coord.keys())  # Crear una ruta inicial aleatoria 
    random.shuffle(ruta) 
    mejor_ruta = busqueda_tabu(ruta) 
    distancia_total = evalua_ruta(mejor_ruta) 

    return render_template("resultado.html", mejor_ruta=mejor_ruta, distancia_total=distancia_total) 

if __name__ == "__main__": 
    app.run()