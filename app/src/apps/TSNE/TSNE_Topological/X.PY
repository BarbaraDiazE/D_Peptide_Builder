#5 FDA_PEP
        Marines = ["Marines",]
        df_Marines = []
        for col in properties:
            for row in Marines:
                df_Marines.append([col, row, TSNE_sim.at[row, col]]) 
        X_Marines = list(df_Marines[0][2])
        Y_Marines = list(df_Marines[1][2])
        S_Marines= list(df_Marines[3][2])
        N_Marines= list(df_Marines[4][2])