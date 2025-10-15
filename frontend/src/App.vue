<script setup>
import { ref } from 'vue'

const currentYear = new Date().getFullYear()
</script>

<template>
  <div class="app">
    <main class="landing-page">
      <div class="content">
        <h1 class="title">The Chronicler</h1>
        <p class="tagline">AI-Powered RPG Gamemaster Experience</p>
        <div class="coming-soon">
          <h2>Coming Soon</h2>
          <p>We're building an advanced web-based AI gamemaster that provides:</p>
          <ul class="features">
            <li>Appropriate challenge and meaningful resistance</li>
            <li>Seamless narrative and mechanical integration</li>
            <li>Persistent world state and NPC continuity</li>
            <li>Multi-device access with cloud-based campaigns</li>
          </ul>
        </div>
        <footer class="footer">
          <p>&copy; {{ currentYear }} The Chronicler. All rights reserved.</p>
        </footer>
      </div>
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.landing-page {
  width: 100%;
  max-width: 800px;
}

.content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.title {
  font-size: 3.5rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 1rem 0;
  text-align: center;
  letter-spacing: -0.02em;
}

.tagline {
  font-size: 1.5rem;
  color: #4a5568;
  text-align: center;
  margin: 0 0 3rem 0;
  font-weight: 300;
}

.coming-soon {
  background: #f7fafc;
  border-radius: 0.5rem;
  padding: 2rem;
  margin-bottom: 2rem;
}

.coming-soon h2 {
  font-size: 2rem;
  color: #667eea;
  margin: 0 0 1rem 0;
}

.coming-soon p {
  font-size: 1.125rem;
  color: #4a5568;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.features {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0 0 0;
}

.features li {
  font-size: 1.125rem;
  color: #2d3748;
  padding: 0.75rem 0;
  padding-left: 2rem;
  position: relative;
  line-height: 1.6;
}

.features li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #667eea;
  font-weight: bold;
  font-size: 1.5rem;
}

.footer {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
  margin-top: 2rem;
}

.footer p {
  color: #718096;
  font-size: 0.875rem;
  margin: 0;
}

@media (max-width: 768px) {
  .content {
    padding: 2rem;
  }

  .title {
    font-size: 2.5rem;
  }

  .tagline {
    font-size: 1.25rem;
  }

  .coming-soon h2 {
    font-size: 1.5rem;
  }

  .features li {
    font-size: 1rem;
  }
}
</style>
