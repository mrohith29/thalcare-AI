# Team Collaboration Workflow - Step by Step

This guide explains how team members can make changes locally and update the shared codebase and Docker images.

## 📋 Overview

There are **TWO separate workflows**:
1. **Git**: Code version control and collaboration
2. **Docker Hub**: Container image distribution

## 🎯 Complete Workflow Example

### Scenario: Team Member Makes Changes

Let's say **Alice** wants to add a new feature:

---

## Step 1: Setup (First Time Only)

```bash
# Clone the repository
git clone <your-repo-url>
cd thalcare-AI/backend

# Build and start containers locally
docker-compose up -d

# Initialize database
docker-compose exec backend python create_tables.py
```

---

## Step 2: Make Local Changes

Alice makes changes to the code:
```bash
# Edit files locally (e.g., api/routes.py)
# Add new features, fix bugs, etc.
```

---

## Step 3: Test Changes Locally

```bash
# Rebuild container to test changes
docker-compose up --build

# Test the changes
curl http://localhost:8000/health

# If everything works, commit to Git
```

---

## Step 4: Update Shared Codebase (Git)

**This updates the SOURCE CODE for the entire team:**

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Added new feature: user profile search"

# Push to repository
git push origin main
```

✅ **Result**: All team members can now see Alice's changes in the Git repository.

---

## Step 5: Update Docker Image (Optional but Recommended)

**This updates the CONTAINER IMAGE for the entire team:**

### For the Team Lead or Person Publishing Images:

```bash
# 1. Pull latest code from Git
git pull origin main

# 2. Build the Docker image with latest changes
docker build -t your-username/thalcare-backend:latest .

# 3. Push to Docker Hub
docker push your-username/thalcare-backend:latest
```

✅ **Result**: Docker image on Docker Hub is updated with latest code.

---

## Step 6: Other Team Members Pull Updates

**Team Member Bob wants to get Alice's changes:**

### Option A: Get Code Changes Only (Git)
```bash
# Pull latest code from Git
git pull origin main

# Rebuild container locally with new code
docker-compose up --build
```

### Option B: Get Pre-built Image (Docker Hub)
```bash
# Pull the latest image
docker pull your-username/thalcare-backend:latest

# Run with docker-compose (if using image instead of build)
docker-compose up
```

---

## 📊 Visual Workflow Diagram

```
Developer's Workflow:
┌─────────────────────────────────────────────────────┐
│  1. Make changes locally                            │
│  2. Test: docker-compose up --build                 │
│  3. Commit: git add . && git commit -m "..."        │
│  4. Push: git push origin main                      │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Shared Git Repository (Source Code)                │
│  • All team members have access                     │
│  • Everyone can pull updates                        │
└─────────────────────────────────────────────────────┘
                      ↓
            (Optional but Recommended)
                      ↓
┌─────────────────────────────────────────────────────┐
│  5. Build Docker image from latest code             │
│     docker build -t username/repo:latest .          │
│  6. Push to Docker Hub                              │
│     docker push username/repo:latest                │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Docker Hub (Pre-built Container)                   │
│  • Team can pull pre-built image                    │
│  • Faster setup for new members                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔄 Two Collaboration Approaches

### Approach 1: Always Use Git (Recommended for Development)

**How it works:**
- All code changes go through Git
- Each team member builds their own Docker container
- Most flexible and common approach

**Commands:**
```bash
# When you make changes
git add .
git commit -m "Your changes"
git push origin main

# When you want updates from others
git pull origin main
docker-compose up --build
```

✅ **Pros**: Flexible, fast iteration, easy to collaborate
❌ **Cons**: Each member builds their own container

---

### Approach 2: Use Pre-built Docker Images

**How it works:**
- Code changes go through Git
- One person builds and pushes Docker image
- Team members use pre-built image

**Commands:**
```bash
# Person publishing the image
git pull origin main  # Get latest code
docker build -t username/repo:latest .
docker push username/repo:latest

# Other team members
docker pull username/repo:latest
docker-compose up
```

✅ **Pros**: Consistent containers, faster setup
❌ **Cons**: Requires image publisher, less flexible for development

---

## 💡 Recommended Team Setup

### For Active Development (Day-to-Day)

**Use Git for everything:**
```bash
# Daily workflow
git pull origin main          # Get latest code
# Make your changes...
docker-compose up --build     # Test locally
git add . && git commit -m "..." && git push origin main
```

### For Releases/Deployments

**Use Docker Hub:**
```bash
# When ready to share stable version
git pull origin main
docker build -t username/repo:latest .
docker push username/repo:latest

# Team can now pull stable image
```

---

## 🎯 Complete Example: Collaborative Feature Development

### Day 1: Alice adds a feature

```bash
# Alice's workflow
cd thalcare-AI/backend
git pull origin main                           # Get latest
# Edit api/routes.py (add new endpoint)
docker-compose up --build                      # Test
git add .
git commit -m "Added GET /api/users endpoint"
git push origin main                           # ✅ Code updated
```

### Day 2: Bob wants to add database changes

```bash
# Bob's workflow
cd thalcare-AI/backend
git pull origin main                           # Get Alice's changes
docker-compose up --build                      # Rebuild with new code
# Edit models.py (add new table)
docker-compose exec backend python create_tables.py  # Update DB
docker-compose up --build                      # Test
git add .
git commit -m "Added notifications table"
git push origin main                           # ✅ Code updated
```

### Day 3: Team Lead publishes Docker image

```bash
# Team Lead's workflow
git pull origin main                           # Get all changes
docker build -t teamname/thalcare-backend:latest .
docker push teamname/thalcare-backend:latest   # ✅ Image updated
```

### Day 4: New team member joins

```bash
# New member's workflow
git clone <repo-url>
cd thalcare-AI/backend
docker pull teamname/thalcare-backend:latest   # Use pre-built
docker-compose up                              # ✅ Running latest
```

---

## ⚠️ Important Rules

### DO:
✅ Always pull latest code before making changes:
```bash
git pull origin main
```

✅ Test locally before pushing:
```bash
docker-compose up --build
```

✅ Write descriptive commit messages:
```bash
git commit -m "Added password reset feature"
```

✅ Pull latest code regularly:
```bash
# At start of each day
git pull origin main
docker-compose up --build
```

### DON'T:
❌ Push untested code
❌ Commit broken code
❌ Push directly to main (use branches if team is large)
❌ Delete other people's changes

---

## 🔧 Conflict Resolution

If multiple people edit the same file:

```bash
# When you try to push and it fails
git pull origin main  # Merge conflicts

# Git will show conflicts
# Edit the file to resolve conflicts
# Then commit the merge
git add .
git commit -m "Merged conflicts"
git push origin main
```

---

## 📝 Summary Checklist

### When You Make Changes:
- [ ] Pull latest code: `git pull origin main`
- [ ] Make your changes
- [ ] Test locally: `docker-compose up --build`
- [ ] Commit: `git add . && git commit -m "..."`
- [ ] Push: `git push origin main`
- [ ] (Optional) Update Docker image if releasing

### When You Want Updates:
- [ ] Pull latest code: `git pull origin main`
- [ ] Rebuild: `docker-compose up --build`
- [ ] (Optional) Pull pre-built image from Docker Hub

---

## 🚀 Quick Commands Reference

```bash
# Get latest code and rebuild
git pull origin main && docker-compose up --build

# Make and push changes
git add . && git commit -m "message" && git push origin main

# Publish Docker image
docker build -t username/repo:latest . && docker push username/repo:latest

# Start fresh (if things break)
git reset --hard origin/main
docker-compose down -v
docker-compose up --build
```

---

## 🎓 Key Takeaways

1. **Git is for code**: All source code changes go through Git
2. **Docker Hub is for containers**: Pre-built images for easier deployment
3. **Always pull before pushing**: Avoid conflicts
4. **Test before sharing**: Don't break things for others
5. **Use branches** for features if team is large (advanced)

---

## 💬 Questions?

**Q: Can multiple people edit the same file?**
A: Yes, but you'll need to resolve merge conflicts when pushing.

**Q: Do I need to rebuild the Docker image every time?**
A: No! Just rebuild locally when testing. Only push to Docker Hub for releases.

**Q: What if I break something?**
A: Pull the latest code and rebuild: `git pull origin main && docker-compose up --build`

**Q: Should I always use the pre-built Docker image?**
A: No, it's better to build from source code during development for flexibility.
