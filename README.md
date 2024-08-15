# BTS-Data-Analysis

This project is a Flask web application that analyzes BTS's data using the Spotify API. It retrieves and stores information about BTS’s albums, tracks, and popularity metrics in a SQLite database, and then displays the results in a web interface.

## Features

- **Spotify OAuth Integration**: Authenticates the user with Spotify and retrieves data.
- **Data Storage**: Stores artist, album, and track information in a SQLite database.
- **Data Visualization**: Displays the top artists and albums from the database in a user-friendly web interface.

## Project Structure

```
SpotifyKpop/
│
├── app.py               # Main application logic
├── config.py            # Configuration settings (Not included in the repository)
├── db.py                # Database initialization
├── models.py            # Database models (Artist, Album, Track)
├── .env                 # Environment variables (Not included in the repository)
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # HTML template for displaying data
├── static/
│   └── styles.css       # CSS for styling the HTML template
└── spotify.db           # SQLite database file
```

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jardondaful/BTS-Data-Analysis.git
   cd BTS-Data-Analysis
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On MacOS/Linux
   .\venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the `.env` file**:

   The `.env` file is used to store environment variables, including your Spotify API credentials. This file is not included in the repository for security reasons. Here’s how to create it:

   - Create a file named `.env` in the root directory of the project:

     ```bash
     touch .env
     ```

   - Open the `.env` file in a text editor and add the following content:

     ```plaintext
     SPOTIPY_CLIENT_ID=your_spotify_client_id_here
     SPOTIPY_CLIENT_SECRET=your_spotify_client_secret_here
     SECRET_KEY=your_flask_secret_key_here
     ```

   - Replace `your_spotify_client_id_here`, `your_spotify_client_secret_here`, and `your_flask_secret_key_here` with your actual Spotify API credentials and a secret key for Flask.

5. **Run the application**:

   ```bash
   python3 app.py
   ```

6. **Access the application**:

   Open your browser and navigate to `http://localhost:8000` to authenticate with Spotify and view the data.

## Usage

- The application will display BTS's top artists and albums from the last 6 months.
- Data is stored in a SQLite database and can be queried for further analysis.

## .gitignore Configuration

This project includes a `.gitignore` file that excludes sensitive files such as `config.py` and `.env` from being tracked by Git:

```plaintext
# Ignore environment variables file
.env

# Ignore configuration file
config.py

# Ignore SQLite database files
*.sqlite3
*.db

# Ignore compiled Python files
__pycache__/
*.py[cod]
*$py.class

# Ignore log files
*.log
*.log.*

# Ignore virtual environment directory
venv/
ENV/
env.bak/
env/

# Ignore IDE-specific files
.idea/
.vscode/
*.sublime-project
*.sublime-workspace

# Ignore Flask instance folder
instance/
```

## License

This project is licensed under the MIT License.
