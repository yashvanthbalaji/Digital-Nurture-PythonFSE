# ============================================================
# HANDS-ON 1 — TASK 1: Web Framework Foundations
# File: notes.py
# ============================================================

# --- 1. REQUEST-RESPONSE CYCLE: GET /api/courses/ ---
# Step 1: Browser sends GET /api/courses/ to the Django server
# Step 2: Django URL Router (urls.py) matches the URL to a view function
# Step 3: The matched View function (views.py) is called with the request
# Step 4: The View queries the Model (models.py) which talks to the database
# Step 5: The View builds and returns an HTTP Response to the browser
# Step 6: Browser receives and displays the response to the user

# --- 2. WHERE MIDDLEWARE SITS ---
# Middleware sits BETWEEN the browser and URL router (incoming request)
# AND BETWEEN the view and browser (outgoing response).
# It is like a two-way security checkpoint for every request/response.

# Two built-in Django middleware classes:
# a) SecurityMiddleware (django.middleware.security.SecurityMiddleware)
#    Enforces HTTPS, adds security headers to prevent XSS and clickjacking.
# b) SessionMiddleware (django.contrib.sessions.middleware.SessionMiddleware)
#    Enables user session management across multiple requests (e.g., login state).

# --- 3. WSGI vs ASGI ---
# WSGI (Web Server Gateway Interface):
#   - Synchronous, handles one request at a time per worker
#   - Django uses WSGI by default (via wsgi.py)
#   - Suitable for standard HTTP request-response web apps

# ASGI (Asynchronous Server Gateway Interface):
#   - Asynchronous, handles multiple concurrent connections
#   - Switch to ASGI when you need WebSockets, async views,
#     real-time features, or long-polling

# Django default: WSGI. Switch to ASGI for real-time or async needs.

# --- 4. MVC PATTERN vs DJANGO MVT PATTERN ---
# MVC (general software pattern):
#   Model      -> Manages data and database logic
#   View       -> What the user sees (the HTML/UI)
#   Controller -> Handles business logic, connects Model and View

# Django MVT (Django's version of MVC):
#   Model    -> Same as MVC Model. Handles data and DB queries.
#   View     -> Acts like the CONTROLLER in MVC.
#               Handles request logic, calls the model, returns response.
#   Template -> Acts like the VIEW in MVC.
#               The HTML file displayed to the user.

# KEY MAPPING:
#   MVC Controller = Django View
#   MVC View       = Django Template
#   MVC Model      = Django Model (same)