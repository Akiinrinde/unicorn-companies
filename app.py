import streamlit as st
import plotly.express as px
import pandas as pd


st.set_page_config(page_title='Unicorn Dashboard', page_icon='bar_chart:',layout='wide')
st.title(':bar_chart: Unicorn Dashboard')

df_cleaned = pd.read_csv('cleaned_unicorn_data.csv')

#metrics 
total_num_companies = df_cleaned['Company'].count()
avg_valuation = df_cleaned['Valuation_num'].mean()
total_funding = df_cleaned['Funding_num'].sum()

col1, col2, col3 = st.columns(3, gap = "large")
col1.metric("Total number of Unicorns", total_num_companies, "100%")
col2.metric("Average Valuation", "$344.83 million", '100%')
col3.metric("Total Funds Raised", "26.7882 billion", '100%')

st.divider() 
st.subheader('Number of unicorn by Industry')
agg_df = df_cleaned.groupby(['Industry'])['Company'].count().reset_index()
agg_df.columns = agg_df.columns.str.replace('Company', 'Count')
fig = px.bar(agg_df, x='Industry', y='Count')
fig.update_layout(xaxis = {"categoryorder":"total descending"})
st.plotly_chart(fig, use_container_width=True, height= 200)

st.write('It is clear that the highest performing industries are Fintech, Internet software and services, Artificail Intelligence and Health.')

st.divider()
st.subheader('Treemap Distrubution of Unicorn by Industry')
fig3 = px.treemap(df_cleaned, path=['Industry', 'Company'],
                color='Industry')
st.plotly_chart(fig3,use_container_width=True, height= True )

st.divider()
st.subheader('Countries By Unicorn count')
#get the data ready for a bar chart 
countries_df = df_cleaned.groupby(['Country'])['Company'].count().reset_index()
countries_df.columns = countries_df.columns.str.replace('Company', 'Count')
mask_df = countries_df['Count'] > 20
#bar chart 
fig4 = px.bar(countries_df[mask_df], x='Country', y='Count')
fig4.update_layout(xaxis = {"categoryorder":"total descending"})
st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Distrubtion of Industries across different countries")
fig5 = px.treemap(df_cleaned, path=['Country','Industry', 'Company'],
                  color='Country')
st.plotly_chart(fig5, use_container_width=True)

st.divider()
st.subheader("Examine the correlation between funding and valuation")
fig6 = px.scatter(df_cleaned,x=df_cleaned['Funding_num'], y=df_cleaned['Valuation_num'], color=df_cleaned['Industry'])
st.plotly_chart(fig6, use_container_width=True)
st.write('This indicates little to no linear correlation between funding and valution. However there is no negative correlation between funding and valution')
st.divider()

yearly_counts = df_cleaned['Year Founded'].value_counts().sort_index().reset_index()
yearly_counts.columns = ['Year Founded', 'Number of Unicorn Companies']
fig7 = px.line(yearly_counts, x='Year Founded', y='Number of Unicorn Companies',
              labels={'Year Founded': 'Year Founded', 'Number of Unicorn Companies': 'Number of Unicorn Companies'},
              title='Growth of Unicorn Companies Over Time')
st.plotly_chart(fig7, use_container_width=True)

st.divider()
yearly_mean_valuation = df_cleaned.groupby('Year Founded')['Valuation_num'].mean().reset_index()
fig8 = px.line(yearly_mean_valuation, x='Year Founded', y='Valuation_num',
              labels={'Year Founded': 'Year Founded', 'Valuation_num': 'Average Valuation (Billions)'},
              title='Average Valuation of Unicorn Companies Over Time')
st.plotly_chart(fig8, use_container_width=True)
st.divider()


