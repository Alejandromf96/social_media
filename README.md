## Vista previa de la aplicación

### Página de Inicio
![Página de inicio](images/social.png)

### Feed de Publicaciones
![Feed de publicaciones](images/social2.png)

### Crear Publicación
![Crear publicación](images/social3.png)




# Social Network Application

This is a social networking web application inspired by the classic designs of early social media platforms like Facebook and Twitter. The app allows users to create accounts, log in, and post updates to a central feed. Users can also edit or delete their own posts. The UI is designed to be responsive, user-friendly, and offers both light and dark mode themes.

## Features

- **User Authentication**: Register and log in to your account.
- **Post Feed**: View a feed of posts from all users, sorted by the latest entries.
- **Create, Edit, and Delete Posts**: Users can add new posts, as well as edit or delete their own posts.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Dark Mode**: Toggle between light and dark themes for a comfortable viewing experience.

## Technologies Used

- **Backend**: Flask (Python), SQLAlchemy for ORM and database management
- **Frontend**: HTML5, CSS3, JavaScript (including DOM manipulation for light/dark mode toggle)
- **Database**: SQLite (or PostgreSQL for production environments)
- **Form Handling**: Flask-WTF for form validation and rendering
- **Version Control**: Git for tracking changes and managing collaboration

## Setup and Installation


5. **Initialize the database**:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. **Run the application**:
    ```bash
    flask run
    ```

   The application will be available at `http://127.0.0.1:5000`.

## Usage

1. Register a new user account on the registration page.
2. Log in to access the main feed and start creating posts.
3. Toggle between light and dark mode using the button in the navigation bar.


