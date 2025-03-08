import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("touristInfo.csv")
ticket_df = pd.read_csv('tickets.csv')

#st.header('Resort Comparison')

st.markdown('''
### Resort Comparison
- [Adult Day Ticket](#adult-day-ticket)
- [Vertical Drop](#vertical-drop)
- [Longest Run](#longest-run)
- [Resort Elevations](#resort-elevations)
- [Terrain](#terrain)
''', unsafe_allow_html=True)

st.subheader('Adult Day Ticket')

# Function to highlight a specific column
def highlight_column(df,column_name):
    def style_func(col):
        return ['background-color: yellow' if col.name == column_name else '' for _ in col]
    return df.style.apply(style_func, axis=0)

day_ticket_df = ticket_df[ticket_df['Ticket'].str.contains("1 Day")]
adult_day_ticket_df = day_ticket_df[['Resort', 'Ticket', 'Adult',]]
adult_day_ticket_df = adult_day_ticket_df.rename(columns={"Adult":"Price Yen"})
adult_day_ticket_df.reset_index(drop=True,inplace=True)
adult_day_ticket_df=adult_day_ticket_df.sort_values(by="Price Yen", ascending=False)
adult_day_ticket_df=adult_day_ticket_df[['Resort',"Price Yen"]]

# Highlight the price column
styled_price_df = highlight_column(adult_day_ticket_df,"Price Yen")

st.dataframe(styled_price_df,hide_index=True)

#vertical drop 
vertical_df = df[["Resort_Name",'Vertical_drop_meters']]
vertical_df=vertical_df.sort_values(by='Vertical_drop_meters', ascending=False)
vertical_df = vertical_df.reset_index(drop=True)

#Longest Run
longestRun_df = df[["Resort_Name",'Longest_Run_meters']]
longestRun_df=longestRun_df.sort_values(by='Longest_Run_meters', ascending=False)
longestRun_df = longestRun_df.reset_index(drop=True)

col1, col2 = st.columns(2)

with col1:
    
    st.subheader('Vertical Drop')
    fig, ax = plt.subplots()

    sns.barplot(x="Resort_Name", y='Vertical_drop_meters', data=vertical_df, ax=ax, palette='plasma',
            hue="Resort_Name")            

    # Add y-value labels to each bar
    for index, row in vertical_df.iterrows():
        plt.text(index, row['Vertical_drop_meters'] + 0.5, f"{row['Vertical_drop_meters']}", ha='center', va='bottom')

    # Customize the plot 
    ax.tick_params(axis='x', rotation=65)  # Rotate x-ticks by 45 degrees  # Rotate x-ticks 45 degrees
    ax.set_title('Vertical Drop')
    ax.set_xlabel('Resort')
    ax.set_ylabel('Vertical Drop(meters)')

    # Show the plot
    st.pyplot(fig)
    
with col2:
    
    st.subheader('Longest Run')
    fig, ax = plt.subplots()

    sns.barplot(x="Resort_Name", y='Longest_Run_meters', data=longestRun_df, ax=ax, palette='plasma',
                hue="Resort_Name")
                

    # Add y-value labels to each bar
    for index, row in longestRun_df.iterrows():
        plt.text(index, row['Longest_Run_meters'] + 0.5, f"{row['Longest_Run_meters']}", ha='center', va='bottom')

    # Customize the plot (optional)
    ax.tick_params(axis='x', rotation=65)  # Rotate x-ticks 45 degrees
    ax.set_title('Longest Run(metres)')
    ax.set_xlabel('Resort')
    ax.set_ylabel('metres')
    
    # Show the plot
    st.pyplot(fig)

#elevations
elevation_df = df[["Resort_Name",'Base_elevation_meters','Summit_elevation_meters']]
elevation_df=elevation_df.sort_values(by='Summit_elevation_meters', ascending=False)
elevation_df=elevation_df.reset_index(drop=True)

# Reshape the DataFrame to a long format
elevation_df_long = elevation_df.melt(id_vars='Resort_Name', var_name='Base/Summit', value_name='Elevation')
st.subheader('Resort Elevations')

fig, ax = plt.subplots()
sns.barplot(x='Resort_Name', y='Elevation', hue='Base/Summit', data=elevation_df_long, ax=ax, palette='YlGn')

# Add value labels to each bar
for bar in ax.patches:
    bar_height = bar.get_height()  # Get the height of the bar
    bar_x = bar.get_x() + bar.get_width() / 2  # Get the bar's x-coordinate
    ax.text(bar_x, bar_height + 0.3, f'{int(bar_height)}', ha='center', va='bottom', fontsize=9)

# Customize the plot
ax.set_title('Resort Elevation', fontsize=16)
ax.set_xlabel('Resort', fontsize=12)
ax.set_ylabel('Meters', fontsize=12)
plt.xticks(rotation=75)

# Display the plot in Streamlit
st.pyplot(fig)

#Terrain Comparison
st.subheader("Terrain")

#terrain subset
terrain_df = df[['Resort_Name','Begginner_Terrain_%', 'Intermediate_Terrain_%', 'Advanced_Terrain_%']]
terrain_df=terrain_df.sort_values(by=['Advanced_Terrain_%','Intermediate_Terrain_%'], ascending=False)
terrain_df = terrain_df.reset_index(drop=True)

# Plot a stacked bar plot
categories = terrain_df['Resort_Name']
values1 = terrain_df['Begginner_Terrain_%']
values2 = terrain_df['Intermediate_Terrain_%']
values3 = terrain_df['Advanced_Terrain_%']

# Bar width
bar_width = 0.6

# Create the stacked bar plot
fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis for the plot
ax.bar(categories, values1, label='Beginner', color='green', width=bar_width)
ax.bar(categories, values2, label='Intermediate', bottom=values1, color='blue', width=bar_width)
ax.bar(categories, values3, label='Advanced', bottom=values1 + values2, color='black', width=bar_width)

# Add labels for each segment
for i, category in enumerate(categories):
    # Add label for Value1
    ax.text(i, values1[i] / 2, f'{values1[i]}', ha='center', va='center', color='white', fontsize=9)

    if values2[i] > 0:
        # Add label for Value2
        ax.text(i, values1[i] + values2[i] / 2, f'{values2[i]}', ha='center', va='center', color='white', fontsize=9)

    if values3[i] > 0:
        # Add label for Value3
        ax.text(i, values1[i] + values2[i] + values3[i] / 2, f'{values3[i]}', ha='center', va='center', color='white', fontsize=9)

# Add labels, legend, and title
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, rotation=75)
ax.set_xlabel('Resort')
ax.set_ylabel('Percent')
ax.set_title('Terrain')

# Move the legend to the bottom-right corner
ax.legend(loc='lower right')

# Display the plot in Streamlit
st.pyplot(fig)

