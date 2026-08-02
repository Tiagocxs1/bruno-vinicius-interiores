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
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = form.querySelector('.btn-submit');
      const name = form.name.value.trim();
      const email = form.email.value.trim();
      const type = form.type.value.trim();
      const msg = form.message.value.trim();

      if (!name || !email || !msg) {
        feedback.style.display = 'block';
        feedback.textContent = form.getAttribute('data-error') || 'Please fill all required fields.';
        return;
      }

      const subject = `Project enquiry — ${name}`;
      const body = `Name: ${name}%0D%0AEmail: ${email}%0D%0AType: ${type}%0D%0A%0D%0A${msg}`;
      const mailto = `mailto:hello@brunovinicius.design?subject=${encodeURIComponent(subject)}&body=${body}`;

      feedback.style.display = 'block';
      feedback.textContent = form.getAttribute('data-success') || 'Thank you — your message is on its way.';
      feedback.style.color = (getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#2E3A33').trim();

      window.open(mailto, '_blank');
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

  // ---- parallax hero + nav shrink ----
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