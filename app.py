import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
import pickle 
import numpy as np
import pymongo
import SessionState
import datetime
import json
import requests
import pandas as pd
from copy import deepcopy
from fake_useragent import UserAgent

# #for resetting state
session = SessionState.get(run_id=0)

# browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
# browser_header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36'}
        

# Data Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from feedback import UserAuth
# from dotenv import load_dotenv
# load_dotenv()

engine = create_engine('sqlite:///project_db.sqlite3')
#Connect to DB
Session = sessionmaker(bind=engine)
sess = Session()

#Loading the model in read mode

model = pickle.load(open('RFmodel.pkl', 'rb'))

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def predict_covid(prediction_value):
    input = np.array([prediction_value])
    prediction = model.predict_proba(input)
    pred = '{0:.{1}f}'.format(prediction[0][0], 5)
    return float(pred)


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_mapping():
    df = pd.read_csv("district_mappingnew.csv")
    return df


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def filter_column(df, col, value):
    df_temp = deepcopy(df.loc[df[col] == value, :])
    return df_temp

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def filter_capacity(df, col, value):
    df_temp = deepcopy(df.loc[df[col] > value, :])
    return df_temp

@st.cache(allow_output_mutation=True)
def Pageviews():
    return []

def main():
    st.set_page_config(page_title="Covid 19 App ⛑️", page_icon="notebooks/mask.png", layout='wide', initial_sidebar_state='expanded')
    
    # Initialize connection.
    client = pymongo.MongoClient("mongodb+srv://visakh:feedbackforms@feedback.0r8bu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # Pull data from the collection.
    # Uses st.cache to only rerun when the query changes or after 10 min.
    @st.cache(ttl=600,show_spinner=False)
    def get_data(): 
        db = client.covidapp
        items = db.feedback.find()
        items = list(items)  # make hashable for st.cache
        return items

    def push_data(name,review,improve):
        db = client.covidapp
        post = {"name":name,
                "review":review,
                "improve":improve
                }
        db.feedback.insert_one(post)

    def oauth(username,password):
        query = sess.query(UserAuth).filter(UserAuth.username==username, UserAuth.password==password)
        result = query.first()
        return result
    # END OF MONDO DB CODE  



    

    st.title("COVID-19 Help App 🖥️")
    st.markdown("""
    <style>
    .etitle {
            font-family: "IBM Plex Sans", sans-serif;
            font-weight: bold;
            font-size: 25px;
            color: rgb(250, 250, 250);
            margin: 1.5rem 0px 0.5rem;
            padding: 0.5em 0px 0.25em;
            line-height: 1;
            position: relative;
            flex: 1 1 0%;    
    }
    .dashtitle {
            font-family: 'Noto Sans', sans-serif;
            font-size: 20px;
            color: rgb(250, 250, 250);
            margin: 1.5rem 0px 0.5rem;
            padding: 0.5em 0px 0.25em;
            line-height: 1;
            position: relative;
            flex: 1 1 0%;    
    }
    </style>
    """, unsafe_allow_html=True)

    tableau_covid_dash = """ 
                            <div class='tableauPlaceholder' id='viz1622650066687' style='position: relative'>
   <noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid_Dashboard_16226492198720&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript>
   <object class='tableauViz'  style='display:none;'>
      <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
      <param name='embed_code_version' value='3' />
      <param name='site_root' value='' />
      <param name='name' value='Covid_Dashboard_16226492198720&#47;Dashboard1' />
      <param name='tabs' value='no' />
      <param name='toolbar' value='yes' />
      <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid_Dashboard_16226492198720&#47;Dashboard1&#47;1.png' />
      <param name='animate_transition' value='yes' />
      <param name='display_static_image' value='yes' />
      <param name='display_spinner' value='yes' />
      <param name='display_overlay' value='yes' />
      <param name='display_count' value='yes' />
      <param name='language' value='en-GB' />
   </object>
</div>
            <script type='text/javascript'> 
                var divElement = document.getElementById('viz1622650066687');          
                var vizElement = divElement.getElementsByTagName('object')[0];
                if (divElement.offsetWidth > 800) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else if (divElement.offsetWidth > 500) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else {
                    vizElement.style.width = '100%';
                    vizElement.style.height = '1527px';
                }
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);             
            </script>
                            """


    tableau_covid_forecast = """ 
        <div class='tableauPlaceholder' id='viz1622652929015' style='position: relative'>
   <noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid-19Forecast_16226528481210&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript>
   <object class='tableauViz'  style='display:none;'>
      <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
      <param name='embed_code_version' value='3' />
      <param name='site_root' value='' />
      <param name='name' value='Covid-19Forecast_16226528481210&#47;Dashboard1' />
      <param name='tabs' value='no' />
      <param name='toolbar' value='yes' />
      <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid-19Forecast_16226528481210&#47;Dashboard1&#47;1.png' />
      <param name='animate_transition' value='yes' />
      <param name='display_static_image' value='yes' />
      <param name='display_spinner' value='yes' />
      <param name='display_overlay' value='yes' />
      <param name='display_count' value='yes' />
      <param name='language' value='en-GB' />
   </object>
</div>
        <script type='text/javascript'>                
                var divElement = document.getElementById('viz1622652929015'); 
                var vizElement = divElement.getElementsByTagName('object')[0];
                if (divElement.offsetWidth > 800) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else if (divElement.offsetWidth > 500) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else {
                    vizElement.style.width = '100%';
                    vizElement.style.height = '1527px';
                }
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
                                """
    

    st.write('\n\n\n')

    activities=['Home','CoWin Slot Checker','Analytics Dashboard','Admin']
    option=st.sidebar.selectbox('Welcome To COVID Detector',activities)


    symptoms_list = ['Breathing Problem','Fever','Dry Cough','Sore Throat','Running Nose','Asthma','Chronic Lung Disease','Headache','Heart Disease','Diabetes','Hyper Tension','Fatigue','Gastrointestinal','Abroad travel','Contact with COVID Patient','Attended Large Gathering','Visited Public Exposed Places','Family working inpublic exposed places']
    if option == 'Home':

        st.markdown('<p class="etitle" style="font-size: 30px;">COVID-19 Severity Prediction Model 😷 </p>', unsafe_allow_html=True)
        st.write('\n')
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

        cols = st.beta_columns((1,1,4))  #4 for centered  , 8 for Wide

        if cols[1].button("Reset 🔄"):
            session.run_id += 1

        if cols[0].button("Predict 🔮"):
            st.write('\n')
            output=predict_covid(prediction_value)
            output = abs(1-output)
            fout = '{0:.2f}'.format(output*100) 
            
            if output > 0.5:
                st.error('The probability of being COVID positive is {} % \n You are possibily covid positive , please confer with your doctor '.format(fout))
            else:
                st.success('The probability of being COVID positive is {} %, It is unlikely that you are covid postive '.format(fout))
                st.info('if you still have doubts , please contact your physician')
            
        st.write('\n\n\n')



               



        st.markdown('<p class="etitle">State Helpline Numbers 💁🏻</p>', unsafe_allow_html=True)
        # st.title('State Helpline Numbers 💁🏻')
        dfh = pd.read_excel("model_csv/helplineNumbers.xlsx")
        # st.dataframe(dfh)

        # helplineNo = list(np.unique(dfh["HelplineNo"].values))
        # st.write(helplineNo)
        helpStates = dfh["State/UT"]
        helplineNo = dfh["HelplineNo"]
        # st.write(helpStates)
        # st.write(helplineNo)
        
        st.write("\n")

        
        selectedState = st.selectbox("Select State 🗺️:", [""] + helpStates)
        colh = st.beta_columns(2)
        
        st.write("\n")
        st.write("\n")
        colh[0].subheader("State")
        colh[1].subheader("Helpline Numbers")
        colh[0].write('\n')
        colh[1].write('\n')
        for i,j in zip(helpStates,helplineNo):
            if selectedState == i:
                colh[0].write(f'{i}')
                colh[1].write(f'{j}')


        st.write("\n\n\n\n")

        st.write("\n\n\n\n")

        st.subheader('Feedback Form ⚡')
        form = st.form(key='my-form')
        name_i = form.text_input('Enter your name 👦: ')
        review_i = form.text_input('Were you satisifed with the prediction 😮 ?')
        improve_i = form.text_input('What can we do to improve 🤔 ?')
        submit = form.form_submit_button('Submit')

        
            

        if submit and name_i and review_i and improve_i:
                
            try:
                session.run_id += 1
                push_data(name_i,review_i,improve_i)
                st.success(f'Thank you {name_i} for the feedback 🥰 !, We are trying our best to improve the application :) ')
            except Exception as e:
                st.error('There seems to be some error 🤔 , please try again later :( ')


    if option == 'CoWin Slot Checker':

        hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


        st.markdown('<p class="etitle">CoWin Slot Availabilty 💉 </p>', unsafe_allow_html=True)

        st.write("\n\n")

        st.info("The CoWIN API's Requests are limited , Sometimes results may not come. Try again after 5 minutes 🌐 ")

        st.write("\n\n")
    
        
        mapping_df = load_mapping()

        rename_mapping = {
                'date': 'Date',
                'min_age_limit': 'Minimum Age Limit',
                'available_capacity': 'Available Capacity',
                'vaccine': 'Vaccine',
                'pincode': 'Pincode',
                'name': 'Hospital Name',
                'state_name' : 'State',
                'district_name' : 'District',
                'block_name': 'Block Name',
                'fee_type' : 'Fees'
                }

        # for col in mapping_df:
        #     st.write(col)

        valid_states = list(np.unique(mapping_df["state_name"].values))

        formcheck = st.form(key='my-form3')
        center_column_1, right_column_1 = st.beta_columns(2)



        with center_column_1:
            state_inp = formcheck.selectbox('Select State🗺️', [""] + valid_states)
            if state_inp != "":
                mapping_df = filter_column(mapping_df, "state_name", state_inp)



        mapping_dict = pd.Series(mapping_df["district id"].values,
                                index = mapping_df["district name"].values).to_dict()

        # numdays = st.sidebar.slider('Select Date Range', 0, 100, 10)
        unique_districts = list(mapping_df["district name"].unique())
        unique_districts.sort()
        with right_column_1:
            dist_inp = formcheck.selectbox('Select District 🏙️', unique_districts)

        DIST_ID = mapping_dict[dist_inp]

        base = datetime.datetime.today()
        numdays = 3
        date_list = [base + datetime.timedelta(days=x) for x in range(20)]
        date_str = [x.strftime("%d-%m-%Y") for x in date_list]
        temp_user_agent = UserAgent()
        browser_header = {'User-Agent': temp_user_agent.random}

        final_df = None
        for INP_DATE in date_str:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
            response = requests.get(URL, headers=browser_header)
            if (response.ok) and ('centers' in json.loads(response.text)):
                resp_json = json.loads(response.text)['centers']
                if resp_json is not None:
                    df = pd.DataFrame(resp_json)
                    if len(df):
                        df = df.explode("sessions")
                        df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
                        df['vaccine'] = df.sessions.apply(lambda x: x['vaccine'])
                        df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
                        df['date'] = df.sessions.apply(lambda x: x['date'])
                        df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
                        if final_df is not None:
                            final_df = pd.concat([final_df, df])
                        else:
                            final_df = deepcopy(df)
                else:
                    st.error("No rows in the data Extracted from the API")
        #     else:
        #         st.error("Invalid response")



        if (final_df is not None) and (len(final_df)):
            final_df.drop_duplicates(inplace=True)
            final_df.rename(columns=rename_mapping, inplace=True)

            left_column_2, center_column_2, right_column_2, right_column_2a,  right_column_2b = st.beta_columns(5)
            with left_column_2:
                valid_pincodes = list(np.unique(final_df["Pincode"].values))
                pincode_inp = formcheck.selectbox('Select Pincode 📍', [""] + valid_pincodes)
                if pincode_inp != "":
                    final_df = filter_column(final_df, "Pincode", pincode_inp)

            with center_column_2:
                valid_age = [18, 45]
                age_inp = formcheck.selectbox('Select Minimum Age 👨', [""] + valid_age)
                if age_inp != "":
                    final_df = filter_column(final_df, "Minimum Age Limit", age_inp)

            with right_column_2:
                valid_payments = ["Free", "Paid"]
                pay_inp = formcheck.selectbox('Select Free or Paid 🆓 ', [""] + valid_payments)
                if pay_inp != "":
                    final_df = filter_column(final_df, "Fees", pay_inp)
            
            with right_column_2a:
                valid_capacity = ["Available"]
                cap_inp = formcheck.selectbox('Select Availablilty ❇️', [""] + valid_capacity)
                if cap_inp != "":
                    final_df = filter_capacity(final_df, "Available Capacity", 0)

            with right_column_2b:
                valid_vaccines = ["COVISHIELD", "COVAXIN"]
                vaccine_inp = formcheck.selectbox('Select Vaccine💉', [""] + valid_vaccines)
                if vaccine_inp != "":
                    final_df = filter_column(final_df, "Vaccine", vaccine_inp)
            check = formcheck.form_submit_button("CHECK ✔️")
            if check:
                table = deepcopy(final_df)
                table.reset_index(inplace=True, drop=True)
                st.write("\n")
                st.subheader(" RESULT :📋 ")
                st.write("\n\n")
                st.write(table)
                
        else:
            formcheck.form_submit_button("CHECK ✔️")
            st.error("THE API call limit has been reached , please try again after 5 minutes.")

        st.write("\n\n\n\n")


    if option == 'Analytics Dashboard':

        hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


        st.markdown("<style> @import url('https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap'); </style>", unsafe_allow_html=True)
        st.markdown('<p class="etitle" style="font-size:30px">Analytics Dashboard 📈</p>', unsafe_allow_html=True)
        st.write("\n")
        st.write("\n")
        st.info("Best Viewed On Desktop , We Are Working On A Better Mobile Experience")
        st.markdown('<p class="etitle" style="font-size:25px">Covid 19 Country Wise Case Visualization 🌎</p>', unsafe_allow_html=True)
        st.write("\n")
        st.subheader("The Below Interactive Dashboard Displays The Covid 19 Country Wise Cases Aggregated By Continents.")
        st.markdown('<p class="dashtitle> <b> The measures used for the original data collection are: <b>  </p>', unsafe_allow_html=True)
        st.write("⛣ Number of Cases Worldwide")
        st.write("⛣ Number of Active Cases In Each Country")
        st.write("⛣ The Aggregrate of the Deaths Prevalent Country Wise")
        st.markdown('<p class="dashtitle"> </p>', unsafe_allow_html=True)
        st.subheader("The Given Dashboard has been produced with the help of Tableau and the data has been updated as of 02/06/21")
        st.markdown('<p class="dashtitle"> <b> KEY INSIGHTS </b> </p>', unsafe_allow_html=True)
        st.markdown('<p class="dashtitle"> <ul> <li> At present, USA has the highest number of covid cases(32.9 M) as well as the highest number of deaths (0.58 M) </li>  <li> India still holds second position with 28.3 M covid cases and 0.33 M deaths </li> <li> While Brazil has 0.46 M deaths with 16.5 M covid cases.</li> <li>Greenland is marked as one of the safest place with 40 cases and 0 deaths.</li> </ul></p>', unsafe_allow_html=True)
        st.subheader("We Presently Have Two Filters for both daily & cumulative reports for all the metrics used, which is also reflected in the world map")
        st.write("\n")
        st.write("\n")
        components.html(tableau_covid_dash , width=1600, height=800 )
        st.markdown('<p class="etitle" style="font-size:25px">Covid-19 Forecast Graph 🔮 </p>', unsafe_allow_html=True)
        st.write("\n")
        st.write("\n")
        st.subheader("The Below Interactive Dashboard Displays The Time Series Forecasting of the Confirmed Cases of COVID-19 ,Recovered Cases & Death Rates for Covid Cases")
        st.markdown('<p class="dashtitle> <b> The measures used for the original data collection are: <b>  </p>', unsafe_allow_html=True)
        st.write("⛣ Confirmed Cases of Covid-19 Worldwide ")
        st.write("⛣ Death Rate of Covid-19 ")
        st.write("⛣ Recovered Cases of Covid-19 Worldwide ")
        st.markdown('<p class="dashtitle"> The Given Dashboard has been produced with the help of Tableau and the data has been updated as of 02/06</p>', unsafe_allow_html=True)
        st.markdown('<p class="dashtitle"> <b> KEY INSIGHTS </b> </p>', unsafe_allow_html=True)
        st.markdown('<p class="dashtitle"> <ul> <li> Number of confirmed cases for next 3 months will be somewhere in the range of 27 M to 60 M.  </li>  <li> Number of recovered cases will also increase approximately upto 150 M with a death rate 1-2 % </li> </ul></p>', unsafe_allow_html=True)
        st.subheader("Don\'t get worried looking at the increasing number of covid cases, the recovery rate is also increasing. Doesn\'t mean you should take it leniently. Take proper precautions and possibly stay in your home. India is fighting, stay home and let us defeat corona 😁")
        st.write("\n")
        st.write("\n")
        components.html(tableau_covid_forecast , width=1600, height=900 )
    
    if option == 'Admin':
      
        caching.clear_cache()
        
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

        st.write("\n\n\n")

        f=0
        if login:
            f =1
        
        result = oauth(username_i,password_i)

        if login and username_i and password_i and result:
            f=0
            try:
                feedbacks = get_data()
                st.success("Feedbacks Recieved")
                st.write('\n\n\n')
                col1, col2,col3,col4 = st.beta_columns((1,1,3,3))
                col1.subheader("ID")
                col2.subheader("Name")
                col3.subheader("Review")
                col4.subheader("Improve")
                # results = sess.query(UserInput).all()
                q = 1
                for feedback in feedbacks:
                    col1.write(q)
                    col1.write("\n")
                    col2.write(feedback['name'])
                    col2.write("\n")
                    col3.write(feedback['review'])
                    col3.write("\n")
                    col4.write(feedback['improve']) 
                    col4.write("\n")
                    q = q+1
            except Exception as e:
                st.error('There seems to be some error 🤔 , please try again later :( ')
        else:    
            if f==1:
                st.error('Wrong Username / Password !👽')

    

    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    navOptions= ["Home","Cowin Slot Checker","Analytics"]
    my_expander = st.beta_expander("Quick Navigation Links", expanded=False)
    selectedHome = my_expander.button(navOptions[0])
    selectedCowin = my_expander.button(navOptions[1])
    selectedAdmin = my_expander.button(navOptions[2])
    if selectedHome :
        option = "Home"
    elif selectedCowin :
        option = "Cowin Slot Checker"
    elif selectedAdmin :
        option = "Admin"

if __name__=='__main__':
    main()