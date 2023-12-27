import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor

model = CatBoostRegressor()
model.load_model(r'C:\Users\Nikita Krotkov\Desktop\VAH_APP\reg_model.cbm')


st.title('A web service for predicting the concentration of a corrosion inhibitor')
st.markdown("---")
name_inh = st.text_input("Enter the name of the corrosion inhibitor")


cva = st.file_uploader('Please upload an file with cyclic voltammogram in .edf format')

if cva is not None:
    current, voltage = [], []

    data = cva.getvalue().decode('latin-1').splitlines()

    current_temp, volt_temp = [], []

    for line in data[25:]:
        values = line.strip().split()
        if len(values) == 4:
            current_temp.append(float(values[3]))
            volt_temp.append(float(values[2]))
        elif values[0] == 'de':
            current.append(current_temp)
            voltage.append(volt_temp)
            current_temp, volt_temp = [], []
        else:
            continue
    cor = pd.DataFrame(current)[4:]
    val = pd.DataFrame(voltage)[4:]


    if current and voltage:
        st.write("Current, A")
        st.write(cor)
        st.write("Voltage, V")
        st.write(val)
    else:
        st.write("No valid data found in the uploaded file.")

    
    if len(current) > 0 and len(voltage) > 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(val.T, cor.T)
        ax.set_xlabel('Voltage, V')
        ax.set_ylabel('Current, A')
        ax.set_title(f'Cyclic Voltammogram for {name_inh}')
        st.pyplot(fig)
    else:
        st.write("No valid data found in the uploaded file.")


    if len(cor.T) == 967:
        cor[967] = cor[966]


    if st.button("Predict"):
        predictions = model.predict(cor.iloc[0])
        st.write("Result:", predictions)