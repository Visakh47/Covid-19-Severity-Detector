import streamlit as st
import pickle 
import numpy as np

# Data Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from feedback import UserInput

engine = create_engine('sqlite:///project_db.sqlite3')
#Connect to DB
Session = sessionmaker(bind=engine)
sess = Session()


#Loading the model in read mode

model = pickle.load(open('RFmodel.pkl', 'rb'))

def predict_covid(prediction_value):
    input = np.array([prediction_value])
    prediction = model.predict_proba(input)
    pred = '{0:.{1}f}'.format(prediction[0][0], 5)
    return float(pred)


def main():
    st.set_page_config(page_title="Covid 19 App", page_icon=None, layout='centered', initial_sidebar_state='collapsed')
    st.title("COVID-19 Severity Prediction Model 🖥️")
    # html_temp = """
    # <div style="background-color:#FF0000 ;padding:3px">
    # <h2 style="color:white;text-align:center;"> Covid 19 Severity Prediction </h2>
    # </div>
    # """
    # st.markdown(html_temp, unsafe_allow_html=True)

    st.write('\n')

    activities=['Main Page', 'Admin Page']
    option=st.sidebar.selectbox('Welcome To COVID Detector?',activities)


    symptoms_list = ['Breathing Problem','Fever','Dry Cough','Sore Throat','Running Nose','Asthma','Chronic Lung Disease','Headache','Heart Disease','Diabetes','Hyper Tension','Fatigue','Gastrointestinal','Abroad travel','Contact with COVID Patient','Attended Large Gathering','Visited Public Exposed Places','Family working inpublic exposed places']
    if option == 'Main Page':
        st.subheader('Please Select The Applicable Properties: ✔️')
        symptoms = st.multiselect('',[*symptoms_list],key='symptoms')
        
        hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    
        

        prediction_value = ['0' for i in range(18)]
        for sym in symptoms:
            index = symptoms_list.index(sym)
            # assigning encoded value to testing frame
            prediction_value[index] = '1'

        st.write("\n")

        if st.button("Predict 🔮"):
            output=predict_covid(prediction_value)
            output = abs(1-output)
            fout = '{0:.2f}'.format(output*100) 
            
            if output > 0.5:
                st.error('The probability of being COVID positive is {} % \n You are possibily covid positive , please confer with your doctor '.format(fout))
            else:
                st.success('The probability of being COVID positive is {} %, It is unlikely that you are covid postive '.format(fout))
                st.error('if you still have doubts , please contact your physician')

        st.write('\n')

        st.subheader('Feedback Form ⚡')
        form = st.form(key='my-form')
        name_i = form.text_input('Enter your name 👦: ')
        review_i = form.text_input('Were you satisifed with the prediciton 😮 ?')
        improve_i = form.text_input('What can we do to improve 🤔 ?')
        submit = form.form_submit_button('Submit')


        
        if submit and name_i and review_i and improve_i:
            try:
                entry = UserInput(name=name_i,review=review_i,improve = improve_i)
                sess.add(entry)
                sess.commit()
                st.success(f'Thank you {name_i} for the feedback 🥰 !, We are trying our best to improve the application :) ')
            except Exception as e:
                st.error('There seems to be some error 🤔 , please try again later :( ')



    
    if option == 'Admin Page':
        username= "covid_team"
        password = "vp3205"
        
        hide_streamlit_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
        
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

        st.error("Only Administrator Access Allowed")
        st.subheader("Admin Login")
        formlogin = st.form(key='my-form2')
        username_i = formlogin.text_input('Enter UserName 👦: ')
        password_i = formlogin.text_input('Enter Password :', type = "password")
        login = formlogin.form_submit_button('Login') 

        for i in range (3):
            st.write('\n')

        f=0
        if login:
            f =1
        if login and username_i==username and password_i==password: 
            f=0
            
            try:
                st.success("Feedbacks Recieved")
                for i in range (3):
                    st.write('\n')
                col1, col2,col3,col4 = st.beta_columns(4)
                col1.subheader("ID")
                col2.subheader("Name")
                col3.subheader("Review")
                col4.subheader("Improve")
                results = sess.query(UserInput).all()
                for item in results:
                    col1.write(item.id)
                    col2.write(item.name)
                    col3.write(item.review)
                    col4.write(item.improve)  
            except Exception as e:
                st.error('There seems to be some error 🤔 , please try again later :( ')
        else:    
            if f==1:
                st.error('Wrong Username / Password !👽')

if __name__=='__main__':
    main()