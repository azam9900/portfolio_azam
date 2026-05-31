/* ============================================================
   Mohd Azam — Portfolio JavaScript
   Backend API se fully connected
   ============================================================ */

const API_BASE = 'http://localhost:8000';

/* ── Token helpers ─────────────────────────────────────────── */
const Auth = {
  getToken: () => sessionStorage.getItem('access_token'),
  setTokens: (access, refresh) => {
    sessionStorage.setItem('access_token', access);
    sessionStorage.setItem('refresh_token', refresh);
  },
  clearTokens: () => {
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
  },
  headers: () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${Auth.getToken()}`
  }),
};

/* ── Generic API fetch ──────────────────────────────────────── */
async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `API error ${res.status}`);
  }
  return res.json();
}

/* ============================================================
   1. LOAD PROJECTS FROM API
   ============================================================ */
async function loadProjects() {
  const grid = document.querySelector('.projects-grid');
  if (!grid) return;

  try {
    const projects = await apiFetch('/api/projects/');
    if (projects.length === 0) return; // Keep static content if API empty

    grid.innerHTML = '';

    projects.forEach((p, i) => {
      const featured = p.featured && i === 0;
      const card = document.createElement('div');
      card.className = `project-item${featured ? ' featured' : ''}`;
      card.innerHTML = featured ? `
        <div>
          <div class="project-num">${String(i + 1).padStart(2, '0')}</div>
          <div class="project-stack">${p.stack.map(s => `<span class="project-stack-tag">${s}</span>`).join('')}</div>
          <div class="project-name">${p.name}</div>
          <div class="project-desc">${p.description}</div>
          <div class="project-footer">
            <a href="${p.link}" class="project-link" target="_blank">${p.link_label}</a>
            <span class="project-arrow">↗</span>
          </div>
        </div>
        <div class="featured-visual">${p.name.charAt(0)}</div>
      ` : `
        <div class="project-num">${String(i + 1).padStart(2, '0')}</div>
        <div class="project-stack">${p.stack.map(s => `<span class="project-stack-tag">${s}</span>`).join('')}</div>
        <div class="project-name">${p.name}</div>
        <div class="project-desc">${p.description}</div>
        <div class="project-footer">
          <a href="${p.link}" class="project-link" target="_blank">${p.link_label}</a>
          <span class="project-arrow">↗</span>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (e) {
    console.warn('[Projects] Could not load from API, using static content.', e.message);
  }
}

/* ============================================================
   2. LOAD BLOG POSTS FROM API
   ============================================================ */
async function loadBlog() {
  const grid = document.querySelector('.blog-grid');
  if (!grid) return;

  try {
    const posts = await apiFetch('/api/blog/');
    if (posts.length === 0) return;

    grid.innerHTML = '';

    posts.slice(0, 3).forEach(post => {
      const card = document.createElement('div');
      card.className = 'blog-item';
      const date = new Date(post.created_at).toLocaleDateString('en-GB', { month: 'short', year: 'numeric' });
      card.innerHTML = `
        <div class="blog-cat">${post.category}</div>
        <div class="blog-title">${post.title}</div>
        <div class="blog-excerpt">${post.excerpt}</div>
        <div class="blog-meta">
          <span class="blog-date">${date}</span>
          <span class="blog-read">${post.read_time}</span>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (e) {
    console.warn('[Blog] Could not load from API, using static content.', e.message);
  }
}

/* ============================================================
   3. CONTACT FORM — Formspree se connected
   Seedha aa3981863@gmail.com pe email aata hai
   Formspree free account banao: https://formspree.io
   Apna form ID neeche daalo (FORMSPREE_ID)
   ============================================================ */

const FORMSPREE_ID = 'YOUR_FORM_ID'; // 👈 Replace with your Formspree form ID e.g. 'xpwzgkla'

async function setupContactForm() {
  const submitBtn = document.querySelector('.form-submit');
  if (!submitBtn) return;

  submitBtn.addEventListener('click', async () => {
    const name    = document.querySelector('.form-input[placeholder="Your name"]');
    const email   = document.querySelector('.form-input[placeholder="you@example.com"]');
    const subject = document.querySelector('.form-input[placeholder="Project inquiry, collaboration..."]');
    const message = document.querySelector('.form-textarea');

    if (!name || !email || !subject || !message) return;

    // ── Validation ──────────────────────────────────────────
    if (!name.value.trim() || !email.value.trim() || !subject.value.trim() || !message.value.trim()) {
      showFormFeedback('Please fill in all fields.', 'error');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
      showFormFeedback('Please enter a valid email address.', 'error');
      return;
    }
    if (message.value.trim().length < 10) {
      showFormFeedback('Message must be at least 10 characters.', 'error');
      return;
    }

    // ── Sending state ────────────────────────────────────────
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';

    try {
      const res = await fetch(`https://formspree.io/f/${FORMSPREE_ID}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          name:    name.value.trim(),
          email:   email.value.trim(),
          subject: subject.value.trim(),
          message: message.value.trim(),
        }),
      });

      if (res.ok) {
        // ── Success ─────────────────────────────────────────
        submitBtn.textContent = 'Message Sent ✓';
        submitBtn.style.background = '#4CAF89';
        submitBtn.style.opacity = '1';
        showFormFeedback('Message received! Mohd Azam will reply within 24 hours.', 'success');

        name.value = '';
        email.value = '';
        subject.value = '';
        message.value = '';

        setTimeout(() => {
          submitBtn.textContent = 'Send Message →';
          submitBtn.style.background = '';
          submitBtn.disabled = false;
        }, 4000);

      } else {
        const data = await res.json();
        throw new Error(data?.errors?.[0]?.message || 'Send failed');
      }

    } catch (err) {
      submitBtn.textContent = 'Send Message →';
      submitBtn.style.opacity = '1';
      submitBtn.disabled = false;

      // If Formspree ID not set yet, show helpful message
      if (FORMSPREE_ID === 'YOUR_FORM_ID') {
        showFormFeedback('Setup needed: Get your free Formspree ID at formspree.io and add it to script.js', 'error');
      } else {
        showFormFeedback('Failed to send. Please email directly: aa3981863@gmail.com', 'error');
      }
    }
  });
}

function showFormFeedback(msg, type) {
  let el = document.getElementById('form-feedback');
  if (!el) {
    el = document.createElement('p');
    el.id = 'form-feedback';
    el.style.cssText = 'font-size:12px;margin-top:0.75rem;letter-spacing:0.5px;padding:0.75rem 1rem;border-left:3px solid;transition:all 0.3s;';
    document.querySelector('.form-submit').after(el);
  }
  if (type === 'success') {
    el.style.color = '#4CAF89';
    el.style.borderColor = '#4CAF89';
    el.style.background = 'rgba(76,175,137,0.08)';
  } else {
    el.style.color = '#E57373';
    el.style.borderColor = '#E57373';
    el.style.background = 'rgba(229,115,115,0.08)';
  }
  el.textContent = msg;
  if (type === 'error') {
    setTimeout(() => { if (el) el.textContent = ''; }, 5000);
  }
}

/* ============================================================
   4. SCROLL REVEAL
   ============================================================ */
function setupReveal() {
  const reveals = document.querySelectorAll('.reveal');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  reveals.forEach(r => obs.observe(r));
}

/* ============================================================
   5. SKILL BAR ANIMATION
   ============================================================ */
function setupSkillBars() {
  const fills = document.querySelectorAll('.skill-fill');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.width = e.target.dataset.w + '%';
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  fills.forEach(f => obs.observe(f));
}

/* ============================================================
   6. NAV ACTIVE HIGHLIGHT ON SCROLL
   ============================================================ */
function setupNavHighlight() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        navLinks.forEach(l => {
          l.classList.remove('active');
          if (l.getAttribute('href') === '#' + e.target.id) l.classList.add('active');
        });
      }
    });
  }, { threshold: 0.4 });
  sections.forEach(s => obs.observe(s));
}

/* ============================================================
   7. SMOOTH SCROLL
   ============================================================ */
function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
  });
}

/* ============================================================
   INIT — Run everything on DOM ready
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  setupReveal();
  setupSkillBars();
  setupNavHighlight();
  setupSmoothScroll();
  setupContactForm();
  loadProjects();
  loadBlog();
});
