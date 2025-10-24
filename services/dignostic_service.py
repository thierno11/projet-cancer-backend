from sqlalchemy.orm import Session
from schema.dignostic_schema import RisqueMammaire
import joblib
import pandas as pd
import numpy as np

model = joblib.load("Pink_October/Code/elmalick_ml.joblib")
def effectuer_dignostic(data:RisqueMammaire):
    print(data)
    df = pd.DataFrame([data.model_dump()])

    onhot = joblib.load("Pink_October/Code/onehot_encoder_cancer.joblib")

    cat_col = ['ant_familiaux', 'ant_personnels', 'tabac', 'alcool', 'activite_physique']

    df1 = onhot.transform(df [cat_col])

    df1_encoded = pd.DataFrame(df1,columns=onhot.get_feature_names_out(cat_col))

    df_final = pd.concat([df.drop(columns=cat_col).reset_index(drop=True),df1_encoded],axis=1)
    print(df.columns)
    score = model.predict(df_final)[0]
    return {"score_risque": round(score, 2)}