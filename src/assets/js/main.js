(() => {
  // ---- reduced motion ----
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- burger ----
  const burger = document.querySelector('[data-burger]');
  const mobile = document.querySelector('[data-mobile]');
  if (burger && mobile) {
    burger.addEventListener('click', () => {
      const open = !burger.classList.contains('open');
      burger.classList.toggle('open', open);
      mobile.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open);
      mobile.setAttribute('aria-hidden', !open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }

  // ---- lang switcher ----
  const langSwitcher = document.querySelector('.lang-switcher');
  if (langSwitcher) {
    langSwitcher.addEventListener('change', () => {
      window.location.href = langSwitcher.value;
    });
  }

  // ---- scroll reveal ----
  if (!reduce) {
    const items = document.querySelectorAll('[data-reveal]');
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('revealed');
          // io.unobserve? keep for reuse
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    items.forEach(el => io.observe(el));
  }

  // ---- form ----
  const form = document.querySelector('[data-form]');
  const feedback = document.querySelector('.form-feedback');
  if (form && feedback) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('.btn-submit');
      const fields = new FormData(form);
      const name = String(fields.get('name') || '').trim();
      const email = String(fields.get('email') || '').trim();
      const type = String(fields.get('type') || '').trim();
      const msg = String(fields.get('message') || '').trim();

      if (!name || !email || !msg) {
        feedback.style.display = 'block';
        feedback.textContent = form.getAttribute('data-error') || 'Please fill all required fields.';
        return;
      }

      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Sending…';
      }
      feedback.style.display = 'block';
      feedback.textContent = 'Sending your enquiry…';

      try {
        const response = await fetch('/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, email, type, message: msg }),
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || result.success !== true || result.crmSynced !== true) {
          throw new Error(result.error || 'CRM submission failed');
        }
        const notifications = result.notifications || {};
        const emailStatus = notifications.email === 'sent' ? 'Email notification sent.' : 'Email notification is not configured yet.';
        const telegramStatus = notifications.telegram === 'sent' ? 'Telegram notification sent.' : 'Telegram notification is not configured yet.';
        feedback.textContent = (form.getAttribute('data-success') || 'Your enquiry has been registered.') + ' ' + emailStatus + ' ' + telegramStatus;
        feedback.style.color = (getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#2E3A33').trim();
        form.reset();
      } catch (error) {
        console.error('Central CRM form submission failed:', error);
        feedback.textContent = form.getAttribute('data-error') || 'We could not register your enquiry. Please try again or email hello@brunovinicius.design directly.';
        feedback.style.color = '#b42318';
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.textContent = 'Send message';
        }
      }
    });
  }

  // ---- theme toggle ----
  const themeToggle = document.querySelector('[data-theme-toggle]');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (_) {}
    });
  }

  // ---- gallery thumbs ----
  const heroImg = document.querySelector('.gallery-hero');
  const thumbs = document.querySelectorAll('.gthumb');
  if (heroImg && thumbs.length) {
    thumbs.forEach((btn) => {
      btn.addEventListener('click', () => {
        heroImg.src = btn.dataset.img;
        thumbs.forEach((b) => b.classList.toggle('is-active', b === btn));
      });
    });
    thumbs[0].classList.add('is-active');
  }

  // ---- parallax hero + nav shrink ----
  const nav = document.querySelector('nav');
  const heroMedia = document.querySelector('.hero-media');
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const y = window.scrollY;
        if (nav) {
          if (y > 80) nav.classList.add('shrunk');
          else nav.classList.remove('shrunk');
        }
        if (heroMedia && y < window.innerHeight) {
          heroMedia.style.transform = `translateY(${y * 0.08}px)`;
        }
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

})();