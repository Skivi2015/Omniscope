OmniScope Agents
================

Purpose
-------
Modular agent framework with tool registry, hot-reloadable skills, UCB1 exploration, retries, circuit breaker, multiprocessing, and a FastAPI server. Firebase wrapper provided.

Features
--------
- 🤖 Multiple AI agents (scouty, seomi, soshie, Cookie, Rusty, Browny)
- 🔐 Firebase Authentication with Google and Facebook login
- 🌐 Progressive Web App (PWA) support
- ☁️ Firebase Hosting and Cloud Functions integration
- 🚀 One-click deployment to Google Cloud Run

Quick start
-----------
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python repo_pack.py --init
uvicorn server:app --reload --port 8080
```

Firebase Authentication Setup
----------------------------

### 1. Firebase Console Configuration

1. **Create/Access Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Select your existing project or create a new one
   - Note your Project ID

2. **Enable Authentication**:
   - In Firebase Console, go to Authentication > Sign-in method
   - Enable **Google** provider:
     - Click on Google provider
     - Enable the toggle
     - Set support email
     - Click Save
   - Enable **Facebook** provider:
     - Click on Facebook provider
     - Enable the toggle
     - You'll need App ID and App Secret from Facebook

### 2. Facebook App Setup (for Facebook Login)

1. **Create Facebook App**:
   - Go to [Facebook Developers](https://developers.facebook.com/)
   - Click "Create App" > "Consumer" > Next
   - Enter app name and contact email
   - Create App ID

2. **Configure Facebook Login**:
   - In Facebook App dashboard, add "Facebook Login" product
   - Go to Facebook Login > Settings
   - Add Valid OAuth Redirect URIs:
     ```
     https://YOUR-PROJECT-ID.firebaseapp.com/__/auth/handler
     ```
   - Copy App ID and App Secret

3. **Add Facebook Credentials to Firebase**:
   - In Firebase Console > Authentication > Sign-in method > Facebook
   - Paste App ID and App Secret
   - Copy the OAuth redirect URI and add it to Facebook App settings

### 3. Get Firebase Configuration

1. **Web App Configuration**:
   - In Firebase Console, go to Project Settings > General
   - Scroll to "Your apps" section
   - Click "Add app" > Web (</>) if no web app exists
   - Register app with nickname
   - Copy the Firebase configuration object

2. **Update web/index.html**:
   ```javascript
   const firebaseConfig = {
     apiKey: "your-actual-api-key",
     authDomain: "your-project-id.firebaseapp.com",
     projectId: "your-project-id",
     storageBucket: "your-project-id.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abcdef123456789012"
   };
   ```

### 4. Domain Authorization

1. **Authorized Domains** (for production):
   - In Firebase Console > Authentication > Settings > Authorized domains
   - Add your production domain (e.g., `your-domain.com`)
   - `localhost` is authorized by default for development

### 5. Optional: Backend Token Validation

To validate Firebase ID tokens on the backend:

1. **Install Firebase Admin SDK**:
   ```bash
   pip install firebase-admin
   ```

2. **Download Service Account Key**:
   - Firebase Console > Project Settings > Service accounts
   - Click "Generate new private key"
   - Download JSON file and save securely

3. **Enable Backend Validation**:
   - Uncomment the Firebase Admin code in `server.py`
   - Update the credentials path:
     ```python
     cred = credentials.Certificate("path/to/serviceAccountKey.json")
     ```

### 6. Testing Authentication

1. **Local Development**:
   ```bash
   # Terminal 1: Start API server
   uvicorn server:app --reload --port 8080
   
   # Terminal 2: Serve web files
   python -m http.server 8081 --directory web
   ```
   
2. **Open browser**: http://localhost:8081
3. **Test login**: Click "Login with Google" or "Login with Facebook"
4. **Verify**: User info should display, bot interface should appear

### Callback URLs Reference

For OAuth setup, use these callback URLs:

- **Firebase Auth Handler**: `https://YOUR-PROJECT-ID.firebaseapp.com/__/auth/handler`
- **Local Development**: `http://localhost` (automatically authorized)
- **Production**: `https://your-custom-domain.com` (add to authorized domains)

Cloud Run
---------
```bash
export PROJECT_ID=your-project
gcloud builds submit --tag gcr.io/$PROJECT_ID/omniscope
gcloud run deploy omniscope --image gcr.io/$PROJECT_ID/omniscope --platform managed --allow-unauthenticated
```

Firebase Deployment
------------------
```bash
cd functions && npm i && npm run build
firebase functions:config:set run.url="https://<cloud-run-url>"
firebase deploy --only functions,hosting
```

Update `.firebaserc` with your project ID:
```json
{
  "projects": {
    "default": "your-actual-project-id"
  }
}
```

PyPI Release
------------
On GitHub Release "published", CI builds the package and publishes to PyPI using Trusted Publishing. See .github/workflows/pypi-publish.yml.

Troubleshooting
--------------

**Authentication Issues**:
- Verify Firebase configuration in `web/index.html`
- Check authorized domains in Firebase Console
- Ensure OAuth redirect URIs are correctly configured
- Check browser console for detailed error messages

**CORS Issues**:
- Firebase Hosting automatically handles CORS
- For local development, ensure both servers are running
- Production should use Firebase Hosting with proper rewrites

**Token Validation**:
- Service account key must have proper permissions
- Check server logs for token validation errors
- Ensure Firebase Admin SDK is properly initialized