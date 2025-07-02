import pandas as pd
import streamlit as st
import altair as alt

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df["listed_in"] = df["listed_in"].fillna("")
    return df

df = load_data()
st.title("🎬 Netflix Tracker")

# 2. Filters
col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("Genre", sorted({g for row in df["listed_in"].str.split(", ") for g in row}))
    year = st.slider("Release Year", int(df["release_year"].min()), int(df["release_year"].max()), (2015, 2022))
with col2:
    typ = st.selectbox("Type", ["Movie", "TV Show", "Both"])

# Apply filters
filtered = df[df["release_year"].between(*year)]
if genre:
    filtered = filtered[filtered["listed_in"].str.contains(genre)]
if typ != "Both":
    filtered = filtered[filtered["type"] == typ]

# 3. Show results
st.write(f"Found {len(filtered)} titles:")
for _, row in filtered.head(10).iterrows():
    st.subheader(row["title"])
    st.write(f"{row['type']} • {row['release_year']} • {row['listed_in']}")
    st.write(row["description"])

# 4. Bonus: “Surprise Me” recommendation
if st.button("🎲 Surprise Me"):
    sample = filtered.sample(1).iloc[0]
    st.write(f"**{sample['title']}** — {sample['type']} ({sample['release_year']})")

# 5. Explore trends
year_counts = filtered["release_year"].value_counts().reset_index()
chart = alt.Chart(year_counts).mark_bar().encode(
    x=alt.X("index:O", title="Year"),
    y=alt.Y("release_year:Q", title="Count")
)
st.altair_chart(chart, use_container_width=True)
