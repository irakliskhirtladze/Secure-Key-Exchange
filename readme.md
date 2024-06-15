# Overview of the Project
This project is designed to allow two users to securely exchange secret information and generate a 
shared key that they can use for secure communication.

### Example Scenario
1. User A and User B Register and log in to their accounts.


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
git clone https://github.com/irakliskhirtladze/Secure-Key-Exchange.git
```
2. Create a virtual environment and activate it. To install dependencies run the command:
```
pip install -r requirements.txt
```
3. Apply migrations:
```
python manage.py migrate
```
4. Run the development server:
``` 
python manage.py runserver
```
5. Run tests:
```
python manage.py test security
```
