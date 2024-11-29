import os
import pandas as pd
import streamlit as st
from isodate import parse_duration
import googleapiclient.discovery

# Function to fetch video information from YouTube API
def get_video_info(api_key, video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    response = youtube.videos().list(
        part="statistics,contentDetails",
        id=video_id
    ).execute()
    if response["items"]:
        item = response["items"][0]
        views = int(item["statistics"].get('viewCount', 0))
        duration = item["contentDetails"]["duration"]
        return views, duration
    else:
        return None, None

# Function to convert duration in ISO 8601 format (PT2M33S) to seconds
def duration_to_seconds(duration_str):
    if pd.notna(duration_str) and duration_str:
        try:
            duration = parse_duration(duration_str)
            return duration.total_seconds()
        except:
            return 0  # Default value for durations that cannot be parsed
    else:
        return 0  # Default value for missing durations

# Function to calculate the cost using user input for benchmarks and costs (contact for more)


# Function to process old and new data files, calculate differences, and update cost calculations
def process_data_files(api_key, old_file, new_file, benchmarks, costs):
    # Read old and new data files
    df_old = pd.read_excel(old_file, sheet_name="*", skiprows=4)
    df_new = pd.read_excel(new_file, sheet_name="*", skiprows=4)
    
    # Ensure the necessary columns exist in both dataframes
    required_columns_old = ["Link", "Number of Reactions, Comments & Shares", "Views per Video"]
    required_columns_new = ["Link", "Number of Reactions, Comments & Shares"]
    for col in required_columns_old:
        if col not in df_old.columns:
            raise ValueError(f"Column '{col}' is missing from the old file")
    for col in required_columns_new:
        if col not in df_new.columns:
            raise ValueError(f"Column '{col}' is missing from the new file")
    
    # Map old data to new data based on video URLs
    df_old.set_index("Link", inplace=True)
    df_new.set_index("Link", inplace=True)
    
    # Calculate differences
    df_new["Reactions_Diff"] = df_new["Number of Reactions, Comments & Shares"] - df_old["Number of Reactions, Comments & Shares"]
    df_new["Views_Old"] = df_old["Views per Video"]
    
    # Fetch and update video information for the new data
    df_new["Views_New"] = ""
    df_new["Duration"] = ""
    for index, row in df_new.iterrows():
        video_url = index
        video_id = video_url.split("watch?v=")[-1]
        views, duration = get_video_info(api_key, video_id)
        if views is not None:
            df_new.at[index, "Views_New"] = views
        if duration is not None:
            df_new.at[index, "Duration"] = duration
    
    # Convert the 'Views_New' column to numeric and fill NaN with 0
    df_new["Views_New"] = pd.to_numeric(df_new["Views_New"], errors='coerce').fillna(0).astype(int)
    
    # Calculate the difference in views
    df_new["Views_Diff"] = df_new["Views_New"] - df_new["Views_Old"]
    
    # Convert the duration to seconds
    df_new["duration_seconds"] = df_new["Duration"].apply(duration_to_seconds)
    
    # Add a new column called "ad.format"
    df_new["ad.format"] = df_new.apply(
        lambda row: "bumper" if row["duration_seconds"] < * else (
            "skippable_reach" if row["duration_seconds"] < * and row["Views_Diff"] < * else "skippable_view"
        ),
        axis=1,
    )
    
    # Calculate and add the cost using the user-input benchmarks and costs
    df_new['Cost'] = df_new.apply(lambda row: calculate_cost(row, benchmarks, costs), axis=1)
    return df_new.reset_index()

# Streamlit app
def main():
    st.title("YouTube Video Data Fetcher and Cost Calculator")
    
    # User inputs for API key and file upload
    api_key = st.text_input("Enter your YouTube API Key", type="password")
    old_file = st.file_uploader("Upload your old Excel file", type=["xlsx"])
    new_file = st.file_uploader("Upload your new Excel file", type=["xlsx"])
    
    # User input for benchmarks and costs
    facebook_benchmark = st.number_input("Enter Facebook Benchmark")
    youtube_bumper_benchmark = st.number_input("Enter YouTube Bumper Benchmark")
    youtube_skippable_reach_benchmark = st.number_input("Enter YouTube Skippable Reach Benchmark")

    facebook_cost = st.number_input("Enter Facebook Cost")
    youtube_bumper_cost = st.number_input("Enter YouTube Bumper Cost")
    youtube_skippable_view_cost = st.number_input("Enter YouTube Skippable View Cost")
    
    # Create a dictionary for benchmarks and costs
    benchmarks = {
        'FACEBOOK': facebook_benchmark,
        'YOUTUBE_BUMPER': youtube_bumper_benchmark,
        'YOUTUBE_SKIPPABLE_REACH': youtube_skippable_reach_benchmark,
    }
    
    costs = {
        'FACEBOOK': facebook_cost,
        'YOUTUBE_BUMPER': youtube_bumper_cost,
        'YOUTUBE_SKIPPABLE_VIEW': youtube_skippable_view_cost,
    }
    
    if api_key and old_file and new_file:
        # Process data files and calculate costs
        try:
            df_result = process_data_files(api_key, old_file, new_file, benchmarks, costs)
            
            # Display the DataFrame
            st.dataframe(df_result)
            
            # Download button for the updated DataFrame
            output_file_path = "Output.xlsx"
            df_result.to_excel(output_file_path, index=False)
            st.success("DataFrame updated and ready for download!")
            st.download_button(
                label="Download Excel file",
                data=open(output_file_path, "rb").read(),
                file_name=output_file_path,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
