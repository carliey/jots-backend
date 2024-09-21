# KlassNaut Flask Server

The KlassNaut Flask server is a backend service for the [KlassNaut ReactJs app](https://github.com/itcentralng/autoNoteApp). They are connected for notification via a [SocketIO server for KlassNaut](https://github.com/itcentralng/klassnautsocket). The server uses OpenAI and Stability AI APIs to generate study notes in both text and image format for teachers. The server can handle simple prompts such as subject name and topic, as well as audio lectures.

## TO RUN:

To run the autoNote Flask server, follow the steps below:

1. Add a `.env` file to the root of the project with the following details:

   ```
   DATABASE_URI=postgresql://localhost/klassNaut
   FLASK_DEBUG=True
   SECRET_KEY=can-be-any-secret

   OPENAI_API_KEY=ysk-zRmwrArvRtwE9l8qHTScT3BlbkFJhQgvlaGyvXjrxbsYtofy
   STABILITY_API_KEY=sk-8M61ofKZlYbAh4cFkBN3nXDLsx4stwafStPunMEeQeHVViZL

   SPACE_REGION=fra1
   SPACE_NAME=dhfspace
   SPACE_KEY=JOXURNEKMRJRK5VB7YOH
   SPACE_SECRET=shvDm7YkHBtn+G9EAOLP3h5Bkw0mEcKsLVL2X0RD1V4
   SPACE_ENDPOINT=https://dhfspace.fra1.digitaloceanspaces.com/
   SPACE_EDGE_ENDPOINT=https://dhfspace.fra1.digitaloceanspaces.com/
   ```

   Note that you'll need to obtain the necessary API keys and DigitalOcean Spaces information to fill out the values.

2. Install Python on your computer.

3. Install dependencies by running `pip install -r requirements.txt`.

4. Set the `FLASK_APP` environment variable to `main.py` by running `export FLASK_APP=main.py`.

5. Run migration by running `flask db upgrade`.

6. Start the Flask server by running `flask run`.

## Endpoints

The following endpoints are available:

- `/notes` - a GET request to the notes URL will return a JSON response with a list of generated notes
- `/note` - a POST request to this URL with appropriate parameters will generate study notes and return them in both text and image format.

### Request Parameters

The `/note` endpoint accepts the following parameters in a JSON payload:

- `subject` (required): The name of the subject for which notes are to be generated.
- `topic` (required): The topic of the subject for which notes are to be generated.
- `level` (required): The level of the students for which notes are to be generated.
- `curriculum` (required): The context arround which notes are to be generated.

### Response

The `/note` endpoint returns a JSON payload containing the following fields:

- `clean`: A cleaner version of the generated notes with images placed appropraitely by their ids
- `raw`: The raw response from the content generator
- `images`: An array of the generated images with id, url and caption

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome any contributions or suggestions that can improve the application's functionality.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

This project makes use of the following libraries and APIs:

- Flask
- OpenAI API
- Stability AI API
- DigitalOcean Spaces API
