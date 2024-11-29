# **YouTube Video Data Fetcher and Cost Calculator**

## **Overview**

This application allows users to fetch video statistics from YouTube, compare old and new data for specific videos, and calculate advertising costs based on custom benchmarks and cost parameters. The app processes Excel files containing video data, calculates the differences in views and reactions, and then estimates the advertising costs based on the input benchmarks and costs provided by the user.

---

## **Features**

- **Fetch YouTube Video Information**: Fetches video statistics such as views and duration using the YouTube Data API.
- **Calculate Cost**: Calculates the advertising cost based on the difference in views and reactions for Facebook and YouTube videos.
- **Custom Benchmarks and Cost Input**: Users can input custom benchmarks for calculating cost and reaction differences, including for Facebook and YouTube formats.
- **File Upload**: Users can upload old and new Excel files containing video data for processing.
- **Download Result**: Users can download the processed data as an updated Excel file.

---

## **How It Works**

1. **Input API Key**: 
   The user provides their YouTube API key to allow the app to fetch video statistics.

2. **Upload Excel Files**:
   - Users upload an old Excel file and a new Excel file. These files should contain video URLs (links) and relevant statistics like "Number of Reactions, Comments & Shares" and "Views per Video".
   - The app will compare data from the old file with the new file to calculate the differences.

3. **Input Benchmarks and Costs**: 
   Users enter benchmark values and cost parameters for different platforms (Facebook, YouTube Bumper, YouTube Skippable View, etc.). These values are used to calculate the cost for each video based on the differences in views and reactions.

4. **Fetch Video Data**: 
   The app uses the YouTube Data API to retrieve the views and duration for the videos specified in the new Excel file.

5. **Calculate Advertising Costs**: 
   The app calculates the advertising cost based on the user's custom benchmarks and cost parameters for each video.

6. **Download Results**:
   Once the processing is complete, the user can download the updated Excel file containing the calculated costs along with the video data.

---

## **User Inputs**

1. **YouTube API Key**:
   - **Type**: Password input field
   - **Description**: The YouTube Data API key that allows the app to fetch video statistics.
   - **Usage**: Enter the API key in the text field.

2. **Old Excel File**:
   - **Type**: File uploader
   - **Description**: The old Excel file containing the previous data for videos. This file should include columns like "Link", "Number of Reactions, Comments & Shares", and "Views per Video".

3. **New Excel File**:
   - **Type**: File uploader
   - **Description**: The new Excel file containing updated video data. It should have the same structure as the old file.

4. **Benchmarks**:
   - **Type**: Number input
   - **Description**: Custom benchmark values used for cost calculations. These values control how the differences in views or reactions are used in cost estimation.
   - **Fields**:
     - **Facebook Benchmark**: The benchmark used for calculating reactions for Facebook.
     - **YouTube Bumper Benchmark**: The benchmark used for YouTube Bumper ads.
     - **YouTube Skippable Reach Benchmark**: The benchmark used for YouTube Skippable Reach ads.

5. **Cost Parameters**:
   - **Type**: Number input
   - **Description**: Custom cost values used in the cost calculation for ads.
   - **Fields**:
     - **Facebook Cost**: The cost per thousand reactions for Facebook ads.
     - **YouTube Bumper Cost**: The cost per thousand views for YouTube Bumper ads.
     - **YouTube Skippable View Cost**: The cost per view for YouTube Skippable View ads.

---

## **Output**

After processing the input files and calculations:

- **Dataframe Output**: A table is displayed with the following columns:
  - **Link**: The URL of the video.
  - **Number of Reactions, Comments & Shares**: The number of interactions for the video.
  - **Views per Video**: The number of views for the video.
  - **Reactions_Diff**: The difference in reactions between the new and old files.
  - **Views_New**: The updated number of views fetched from the YouTube API.
  - **Views_Diff**: The difference in views between the new and old files.
  - **Duration**: The duration of the video fetched from the YouTube API.
  - **ad.format**: The ad format (bumper, skippable_view, or skippable_reach).
  - **Cost**: The calculated cost for the video based on the custom benchmarks and costs.

- **Downloadable Excel File**: 
  - Once the calculations are complete, the user can download the updated data in an Excel file.

---

## **Error Handling**

- **Missing Columns**: The app checks that the necessary columns ("Link", "Number of Reactions, Comments & Shares", "Views per Video") exist in the uploaded files. If any are missing, an error message is displayed.
- **API Errors**: If there are issues fetching data from the YouTube API, the app will display an error message indicating the problem.
- **Invalid Input**: If the user enters invalid data or missing files, appropriate error messages will be shown.

---

## **Dependencies**

- `pandas`: For data manipulation.
- `streamlit`: For creating the interactive web application.
- `isodate`: For parsing ISO 8601 duration format.
- `google-api-python-client`: For interacting with the YouTube Data API.

---

## **Conclusion**

This app provides an easy-to-use interface for YouTube video cost calculation, enabling users to fetch video data, compare performance, and calculate ad costs based on custom parameters. It’s particularly useful for advertisers and analysts who need to assess the effectiveness of their video campaigns across multiple platforms.

--- 

Feel free to adjust or expand upon this documentation depending on additional features or requirements you may have!
