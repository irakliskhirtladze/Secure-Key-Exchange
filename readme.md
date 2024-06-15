# Overview of the Project
This project is designed to allow two users to securely exchange secret information and generate a 
shared key that they can use for secure communication.

### Example Scenario
1. User A and User B Register:


2. User A Creates a Channel:
- User A starts a new secure channel and invites User B.
- User B accepts the invitation.

3. Exchanging Secrets:
- User A sends a secret number to the platform.
- User B sends a different secret number to the platform.

4. Generating the Shared Key:
- User A requests the platform to generate the shared key.
- The platform uses User B's secret and the secret key provided by User A to generate a shared key.
- Alternatively, User B can also request the platform to generate the shared key using User A's secret
and the secret key provided by User B.

5. Using the Shared Key:
- Both users now have a shared key that they can use to securely communicate with each other.

### Security Measures
- Only registered and logged-in users can participate in the secure channel.
- The exchange of secrets and generation of the shared key is done using secure cryptographic methods.
- Only users who are part of the accepted channel can exchange secrets and generate the shared key.

# Project setup

1. Clone the repository:
```
git clone https://github.com/irakliskhirtladze/Library-management-system.git
```
2. Create a virtual environment and activate it. To install dependencies run the command:
```
pip install -r requirements.txt
```
3. In project root directory (where manage.py file lives) create .env file. Write these lines in this file:
```
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
```
If you already have actual email setup for app testing, then replace placeholder values in .env file. Otherwise, leave it
as shown above.

4. Apply migrations:
```
python manage.py migrate
```
5. Populate the database with initial data (random book names, authors and genres):
```
python manage.py populate_db
```
6. To create admin user run the command below and then follow the instructions:
```
python manage.py createsuperuser
```
7. Run the development server:
``` 
python manage.py runserver
```
