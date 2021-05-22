import streamlit as st
import pickle 
import numpy as np

#Loading the model in read mode

model = pickle.load(open('RFmodel.pkl', 'rb'))

def predict_covid(Breathing_Problem,Fever,Dry_Cough,Sore_Throat,Running_Nose,Asthma,Chronic_LungDisease,Headache,Heart_Disease,Diabetes,Hyper_Tension,Fatigue,Gastrointestinal,Abroad_travel,Contact_with_COVID_Patient,Attended_Large_Gathering,Visited_Public_Exposed_Places,Family_working_in_public_exposed_places):
    input = np.array([[Breathing_Problem,Fever,Dry_Cough,Sore_Throat,Running_Nose,Asthma,Chronic_LungDisease,Headache,Heart_Disease,Diabetes,Hyper_Tension,Fatigue,Gastrointestinal,Abroad_travel,Contact_with_COVID_Patient,Attended_Large_Gathering,Visited_Public_Exposed_Places,Family_working_in_public_exposed_places]])
    prediction = model.predict_proba(input)
    pred = '{0:.{1}f}'.format(prediction[0][0], 5)
    return float(pred)


def main():
    st.title("Streamlit Tutorial")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;"> Covid 19 Severity Prediction </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)


    Breathing_Problem = st.text_input("Breathing Problem?","")
    Fever = st.text_input("Fever ?","")
    Dry_Cough = st.text_input("Dry Cough ?","")
    Sore_Throat = st.text_input("Sore Throat ?","")
    Running_Nose = st.text_input("Running Nose","")
    Asthma = st.text_input("Asthma","")
    Chronic_LungDisease = st.text_input("Chronic Lung Disease","")
    Headache = st.text_input("Headache","")
    Heart_Disease = st.text_input("Heart Diseases?","")
    Diabetes = st.text_input("Diabetes","")
    Hyper_Tension = st.text_input("Hyper Tension?","")
    Fatigue = st.text_input("Fatigue ?","")
    Gastrointestinal = st.text_input("Gastrointestinal ?","")
    Abroad_travel = st.text_input("Abroad travel ?","")
    Contact_with_COVID_Patient = st.text_input("Contact with COVID Patient?","")
    Attended_Large_Gathering = st.text_input("Attended any large gatherings ?","")
    Visited_Public_Exposed_Places = st.text_input("Visited Public Exposed Places ?","")
    Family_working_in_public_exposed_places = st.text_input("Family working in public exposed places ?","")
    

    safe_html="""  
      <div style="background-color:#F4D03F;padding:10px >
       <h2 style="color:white;text-align:center;"> You're most likely SAFE from COVID 19</h2>
       </div>
    """
    danger_html="""  
      <div style="background-color:#F08080;padding:10px >
       <h2 style="color:black ;text-align:center;"> You possibly could be COVID positive , Confer with a doctor </h2>
       </div>
    """

    if st.button("Predict"):
        output=predict_covid(Breathing_Problem,Fever,Dry_Cough,Sore_Throat,Running_Nose,Asthma,Chronic_LungDisease,Headache,Heart_Disease,Diabetes,Hyper_Tension,Fatigue,Gastrointestinal,Abroad_travel,Contact_with_COVID_Patient,Attended_Large_Gathering,Visited_Public_Exposed_Places,Family_working_in_public_exposed_places)
        output = abs(1-output)
        st.success('The probability of being COVID positive is {} %'.format(output*100))

        if output > 0.5:
            st.markdown(danger_html,unsafe_allow_html=True)
        else:
            st.markdown(safe_html,unsafe_allow_html=True)

if __name__=='__main__':
    main()