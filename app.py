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
    symptoms_list = ['Breathing Problem','Fever','Dry Cough','Sore Throat','Running Nose','Asthma','Chronic Lung Disease','Headache','Heart Disease','Diabetes','Hyper Tension','Fatigue','Gastrointestinal','Abroad travel','Contact with COVID Patient','Attended Large Gathering','Visited Public Exposed Places','Family working inpublic exposed places']
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