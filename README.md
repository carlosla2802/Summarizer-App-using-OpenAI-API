# Summarizer-App-using-OpenAI-API
Summarizer App using OpenAI API

This is an app to summarize texts with Azure OpenAI and Dockerization, which includes the files for the text summarisation app, which are the following:
- **scripts.py**: python file with the functions implemented to connect to the Azure Open AI chat and make the summaries.
- **app.py**: python file to build the application with streamlit.
- **example_text.txt**, **example_text2.txt**, **example_text3.txt**: text files with content (more than 3 pages) to summarize.
- **Dockerfile**: file to build a docker image to dockerise the app.

To be able to run the app (with docker) the following steps must be taken:
- Download the repository
- Enter through the terminal to the directory of the folder **summarizer_app** inside the repository .
- Add an **.env** file (I have not added it for security reasons) into the folder **summarizer_app** with the variables **AZURE_OPENAI_ENDPOINT**, **AZURE_OPENAI_API_KEY** and **AZURE_OPENAI_DEPLOYMENT_NAME**, with their respective values.
- Build a docker image from the app's DockerFile with the following command: **'docker build -t image_app .'**   .
- Create and run a container from the created image with the following command: **'docker run -p 8501:8501 image_app'**   .
- Access the app by pasting the link **http://localhost:8501** in a web browser.

Once inside the app in the browser, it works as follows:
- There is a sidebar where we can add a text by clicking on **Browse files** and taking the text we want in the **summarizer_app** folder.
- Once loaded, click on **Add Data** to start summarising the text. If all goes well, you will see a message saying 'File uploaded, well chunked!'.
- Once the text has been summarised, you have the option to download the summary by clicking the **Download the summary** button.
