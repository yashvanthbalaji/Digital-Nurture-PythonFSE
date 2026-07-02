# Hands-On 10 — Microservices Architecture

## Service Decomposition

| Service | Responsibility | Endpoints | Database |
|----------|----------------|-----------|----------|
| **Course Service** (Port **5001**) | Manages departments and courses | `GET /api/courses/`<br>`POST /api/courses/`<br>`GET /api/courses/{id}/`<br>`DELETE /api/courses/{id}/` | `course_service.db` |
| **Student Service** (Port **5002**) | Manages students and enrollments | `GET /api/students/`<br>`POST /api/students/`<br>`POST /api/students/{id}/enroll` | `student_service.db` |
| **Auth Service** *(Concept)* | User registration, login, and JWT authentication | `POST /api/auth/register/`<br>`POST /api/auth/login/` | `auth_service.db` |
| **Notification Service** *(Concept)* | Sends email confirmations and alerts | Internal event-driven communication | `notification_service.db` |
| **API Gateway** (Port **5000**) | Routes client requests to the appropriate microservice | `/api/courses/*`<br>`/api/students/*` | None |

---

## 🔑 Key Microservices Rule

Each microservice **owns its own database**.

- ❌ No service directly accesses another service's database.
- ✅ Services communicate through APIs or messaging.

**Example:**

> The **Student Service** never accesses `course_service.db` directly.  
> Instead, it communicates with the **Course Service** via HTTP requests.

---

## ▶️ Running All Services

Open **three separate terminals**.

### Terminal 1

```bash
cd course_service
python app.py
```

### Terminal 2

```bash
cd student_service
python app.py
```

### Terminal 3

```bash
cd gateway
python app.py
```

---

## 🔄 Inter-Service Communication Trade-offs

### 1. Synchronous Communication (HTTP) — *Implemented*

- Student Service calls Course Service using **HTTP requests**.

**Advantages**
- ✔️ Simple to implement
- ✔️ Immediate response
- ✔️ Easy to debug

**Disadvantages**
- ❌ Tight coupling
- ❌ If Course Service is unavailable, enrollment requests fail

---

### 2. Asynchronous Communication (RabbitMQ / Kafka)

- Student Service publishes an **`enrollment.created`** event.
- Other services consume the event independently.

**Advantages**
- ✔️ Services remain loosely coupled
- ✔️ One service failure does not stop others
- ✔️ Better scalability

**Disadvantages**
- ❌ Eventual consistency
- ❌ More complex architecture

**Recommended For**
- Email notifications
- Analytics
- Logging
- Background processing

---

## 📌 Rule of Thumb

| Use HTTP | Use Message Queue |
|----------|-------------------|
| Immediate response is required | Delayed processing is acceptable |
| Request/Response communication | Event-driven communication |
| CRUD operations | Notifications, Analytics, Background Tasks |

---

## ✅ Conclusion

This hands-on demonstrates how a **monolithic application** can be decomposed into **independent microservices**, each owning its own data and communicating through well-defined interfaces. It also highlights the trade-offs between **synchronous (HTTP)** and **asynchronous (Message Queue)** communication patterns.