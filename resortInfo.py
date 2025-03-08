import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


info_df = pd.read_csv('touristInfo.csv',index_col='Resort_Name')
ticket_df = pd.read_csv('tickets.csv')

st.header("Resort Information")

resort = st.selectbox(
    "Choose Resort",
    ['Suginohara','Akakura Onsen', 'Akakura Kanko',  'Ikenotaira', 'Arai', 'Madarao', 'Tangram', 'Seki Onsen', 'Myoko RunRun'],
)

st.subheader(resort)

description = info_df.loc[resort, 'Description']
st.markdown(description)

website = info_df.loc[resort, 'Website']
st.link_button(label = "website", url=website)

st.markdown('''
- [Facilities](#facilities)
- [Tickets](#tickets)
- [Lifts](#lifts)
- [Terrain](#terrain)
- [Elevation](#elevation)
- [Trail Stats](#trail-stats)
- [Hours](#hours)
''', unsafe_allow_html=True)



facilities = info_df.loc[resort, 'Facilities']
# Add a space after every comma
facilities = facilities.replace(",", ", ")
# Add a full stop if it doesn't already end with one
if not facilities.endswith('.'):
   facilities += '.'
st.markdown("#### Facilities")
st.markdown(facilities)

resort_df = ticket_df[ticket_df['Resort']==resort]
resort_df = resort_df.dropna(axis=1, how='all')
resort_df.drop(columns=['Resort'], inplace=True)

# Function to highlight a specific column
def highlight_column(df,column_name):
    def style_func(col):
        return ['background-color: yellow' if col.name == column_name else '' for _ in col]
    return df.style.apply(style_func, axis=0)
    
# Highlight the 'TIcket' column
styled_df = highlight_column(resort_df,'Ticket')

#get lift data frame
lift_headings = ['Gondola','Quad_chair', 'Triple_chair', 'Double_chair','Single_chair', 'Lift_other']
lift_df = pd.DataFrame(info_df.loc[resort, lift_headings][info_df.loc[resort, lift_headings] != 0])
lift_df.reset_index(inplace=True)
lift_df.columns = ['Lift Type'," "]

# Function to center-align a specific column
def center_align_column(df, column_name):
    styles = {
        'selector': 'td:nth-child({})'.format(df.columns.get_loc(column_name) + 1),
        'props': [('text-align', 'center')]
    }
    return df.style.set_table_styles([styles])

# Highlight the 'Ticket' column
styled_lift_df = highlight_column(lift_df,'Lift Type')

# Center align the 'Age' column
#styled_lift_df = center_align_column(lift_df, "Lift Count")


col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Tickets")
    #Display the styled DataFrame
    st.dataframe(styled_df,hide_index=True, use_container_width=True)
    
with col2:
    st.markdown("#### Lifts")
    #Display the lift DataFrame
    st.dataframe(styled_lift_df,hide_index=True)
    

col1, col2 = st.columns(2)

#terrain pie chart
terrain = info_df.loc[resort, ['Begginner_Terrain_%', 'Intermediate_Terrain_%','Advanced_Terrain_%']].to_list()

if terrain[2]==0:
    labels = ['Begginner', '', '']
else:
    labels = ['Begginner', 'Intermediate', 'Advanced']
sizes = terrain
colors = ['green', 'blue', 'black']

# Custom function to format the percentages
def fmt_pct(pct):
    return f'{int(pct)}%' if pct > 0 else ''
    #return f'{int(pct)}%'  # Convert to integer and add %

# Create the pie chart
fig, ax = plt.subplots()
#plt.figure(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes, 
    labels=labels, 
    colors=colors, 
    autopct=fmt_pct,  # Use the custom function
    startangle=140
)

ax.axis('equal')
# Change the color of the percentage text to white
for autotext in autotexts:
    autotext.set_color('white')


with col1:
    st.markdown("#### Terrain")
    # show the plot
    st.pyplot(fig)
 
elevation_headings = ['Summit_elevation_meters','Vertical_drop_meters', 'Base_elevation_meters']

elevation_df = pd.DataFrame(info_df.loc[resort, elevation_headings])
elevation_df.reset_index(inplace=True)
elevation_df['index'] = ['Peak', 'Vertical Decent', 'Base']
elevation_df.columns = [' ', "meters "] 

# Highlight the 'Ticket' column
styled_elevation_df = highlight_column(elevation_df,' ')
  
with col2:
    st.markdown("#### Elevation")
    #Display the lift DataFrame
    st.dataframe(styled_elevation_df,hide_index=True)
    
#get course info
course_headings = ['Number_of_Courses','Maximim_Gradient_Degrees', 'Longest_Run_meters']
course_df = pd.DataFrame(info_df.loc[resort, course_headings])
courses = course_df[resort].to_list()
courses[1] = str(courses[1])+" Degrees"
courses[2] = str(courses[2])+" Meters"
keys = ["Number of Courses", "Maximum Gradient", "Longest Run"]
# Create dictionary
courses_dict = dict(zip(keys, courses))


col1, col2,col3,col4 = st.columns([5,3,5,3])
# Print each key-value pair line by line

with col1:
    st.markdown("#### Trail Stats")
    for key, value in courses_dict.items():
        #st.markdown(f"{key}:| {value}")
        st.markdown(f"{key}:")
        
with col2:
    st.subheader(" ")
    for key, value in courses_dict.items():
        st.markdown(f"{value}")

#get opening times info        
hours_headings = ['Opening_time', 'Closing_time', 'Opening_date', 'Closing_date']

#hours_df = pd.DataFrame(df.loc[resort, hours_headings])
hours = info_df.loc[resort, hours_headings]
hours.loc['Opening_time'] = hours.loc['Opening_time'] + "am"
hours.loc['Closing_time'] = hours.loc['Closing_time'] + "pm"

keys = ["Opening Time", "Closing Time", "Opening Date", "Closing Date"]

with col3:
    st.markdown("#### Hours")
    for key in keys:
        st.markdown(f"{key}:")

with col4:
    st.subheader(" ")
    for value in hours.values:
        st.markdown(value)
        



# Apply styling to highlight the first column
# styled_df = resort_df.iloc[:, 1:].style.apply(highlight_first_column)
# st.subheader(resort)
# table = display(styled_df.hide(axis='index'))
# st.write(table)

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.header(resort)
#     st.dataframe(resort_df)

# with col2:
#     st.header("A dog")
#     st.image("https://static.streamlit.io/examples/dog.jpg")

# with col3:
#     st.header("An owl")
#     st.image("https://static.streamlit.io/examples/owl.jpg")