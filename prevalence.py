import streamlit as st
import altair as alt
import pandas as pd


st.title("Interactive Visualization: Disability Prevalence")
st.write("Yunong Xue")


# Prepare for the data
disability = pd.read_csv("disability_by_state.csv")
disability.drop(columns=['Year'], inplace = True)
disability_wide=pd.pivot(disability, index=['LocationAbbr', 'LocationDesc'], columns = 'Response', values = 'Data_Value') #Reshape from long to wide
cols = disability['Response'].unique()
disability_wide=disability_wide[cols]
# disability_wide.drop(columns = 'No Disability').to_csv('prevalence.csv')
# prevalence = pd.read_csv('prevalence.csv')

# df = df.drop(df[df['age'] < 30].index)
disability.drop(disability[disability['Response']== 'No Disability'].index, inplace=True)
# disability.drop(disability[disability['Response']== 'Any Disability'].index, inplace=True)
disability = disability.rename(columns={'Response': 'Disability Type', 'Data_Value': 'Prevalence'})

# st.table(disability.head(10))

### Make my plot:

locations = list(disability['LocationDesc'].unique())

selection1 = alt.selection_single(
    fields=['LocationDesc'],
    bind = alt.binding_select(options=locations, name='Select State/Region'),
    on="keyup", 
    clear="false"
)

selection2 = alt.selection_single(nearest=False, on='mouseover')

chart = alt.Chart(disability).mark_bar().encode(
    y=alt.X('Disability Type:N',axis=alt.Axis(labelAngle= 0), title=None),
    x=alt.Y('mean(Prevalence):Q', title='Disability Prevalence(%)', 
            scale=alt.Scale(domain=[0, 35])),  # specify the domain for the x-axis
    color= "Disability Type:N",
    opacity=alt.value(0.7),
    tooltip=['Disability Type:N', alt.Tooltip('mean(Prevalence):Q', title='Prevalence', format='.1f')]
).properties(
    width=850,
    height=450,
    title=alt.TitleParams(text='Disability Prevalence by Disability Type and by Region/State', fontSize=26),
    padding = {'top':30}
).add_selection(selection1, selection2).transform_filter(selection1).configure_axis(
    labelFontSize=12,  
    titleFontSize=16,
    grid=False   # remove the grid lines in the background
).configure_legend(
    titleFontSize=14,
    labelFontSize=13
).configure_view(
    strokeOpacity=0  # remove the outer border of the chart
)

chart

