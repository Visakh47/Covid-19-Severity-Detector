import streamlit as st
import pickle 
import numpy as np

#Loading the model in read mode

model = pickle.load(open('RFmodel.pkl', 'rb'))

def predict_covid(prediction_value):
    input = np.array([prediction_value])
    prediction = model.predict_proba(input)
    pred = '{0:.{1}f}'.format(prediction[0][0], 5)
    return float(pred)


def main():
    st.title("COVID-19 CLASSIFICATION MODEL")
    html_temp = """
    <div style="background-color:#FF0000 ;padding:3px">
    <h2 style="color:white;text-align:center;"> Covid 19 Severity Prediction </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    st.write('\n')
    symptoms_list = ['Breathing_Problem','Fever','Dry_Cough','Sore_Throat','Running_Nose','Asthma','Chronic_LungDisease','Headache','Heart_Disease','Diabetes','Hyper_Tension','Fatigue','Gastrointestinal','Abroad_travel','Contact_with_COVID_Patient','Attended_Large_Gathering','Visited_Public_Exposed_Places','Family_working_in_public_exposed_places']
    st.subheader('Please Select The Applicable Properties:')
    symptoms = st.multiselect('',[*symptoms_list],key='symptoms')



    prediction_value = ['0' for i in range(18)]
    for sym in symptoms:
        index = symptoms_list.index(sym)
        # assigning encoded value to testing frame
        prediction_value[index] = '1'

    st.write("\n")

    if st.button("Predict"):
        output=predict_covid(prediction_value)
        output = abs(1-output)
        fout = '{0:.2f}'.format(output*100) 
        
        if output > 0.5:
            st.error('The probability of being COVID positive is {} % \n You are possibily covid positive , please confer with your doctor '.format(fout))
        else:
            st.success('The probability of being COVID positive is {} %, It is unlikely that you are covid postive '.format(fout))
            st.error('if you still have doubts , please contact your physician')

if __name__=='__main__':
    main()