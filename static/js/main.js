/**
 * CampusBoard — Main JavaScript
 * Handles navigation, form interactions, and UI polish.
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeSwitcher();
    initNavigation();
    initAlertDismiss();
    initCategoryFields();
    initActiveNavLink();
    initFormSubmitProtection();
    initImagePreview();
});


/* ═══════════════════════════════════════════════
   RESPONSIVE NAVIGATION
   ═══════════════════════════════════════════════ */
function initNavigation() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');

    if (!hamburger || !navLinks) return;

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('show');
    });

    // Close menu when clicking a link (mobile)
    navLinks.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('show');
            }
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('show');
        }
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            hamburger.classList.remove('active');
            navLinks.classList.remove('show');
        }
    });
}


/* ═══════════════════════════════════════════════
   ALERT DISMISS
   ═══════════════════════════════════════════════ */
function initAlertDismiss() {
    document.querySelectorAll('.alert-close').forEach(btn => {
        btn.addEventListener('click', () => {
            const alert = btn.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-12px)';
                setTimeout(() => alert.remove(), 200);
            }
        });
    });

    // Auto-dismiss success messages after 6 seconds
    document.querySelectorAll('.alert-success, .alert-info').forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-12px)';
                setTimeout(() => alert.remove(), 200);
            }
        }, 6000);
    });
}


/* ═══════════════════════════════════════════════
   CATEGORY-DEPENDENT FORM FIELDS
   ═══════════════════════════════════════════════ */
function initCategoryFields() {
    const categorySelect = document.getElementById('id_category');
    if (!categorySelect) return;

    const eventFields = document.getElementById('event-fields');
    const lostFoundFields = document.getElementById('lostfound-fields');

    function updateFields() {
        const value = categorySelect.value;

        // Hide all conditional fields
        if (eventFields) {
            eventFields.classList.remove('visible');
        }
        if (lostFoundFields) {
            lostFoundFields.classList.remove('visible');
        }

        // Show relevant fields
        if (value === 'events' && eventFields) {
            eventFields.classList.add('visible');
        } else if (value === 'lost_found' && lostFoundFields) {
            lostFoundFields.classList.add('visible');
        }
    }

    categorySelect.addEventListener('change', updateFields);

    // Initialize on page load (for edit forms with pre-selected category)
    updateFields();
}


/* ═══════════════════════════════════════════════
   ACTIVE NAV LINK HIGHLIGHTING
   ═══════════════════════════════════════════════ */
function initActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;

        // Exact match for home, prefix match for other pages
        if (currentPath === '/' && href === '/') {
            link.classList.add('active');
        } else if (href !== '/' && currentPath.startsWith(href)) {
            link.classList.add('active');
        }
    });
}


/* ═══════════════════════════════════════════════
   FORM SUBMIT PROTECTION (prevent double-submit)
   ═══════════════════════════════════════════════ */
function initFormSubmitProtection() {
    document.querySelectorAll('form').forEach(form => {
        // Skip search forms
        if (form.method === 'get' || form.classList.contains('hero-search') || form.classList.contains('browse-form')) {
            return;
        }

        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('loading')) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;

                // Re-enable after 5 seconds in case of error
                setTimeout(() => {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}


/* ═══════════════════════════════════════════════
   BROWSE FORM AUTO-SUBMIT ON FILTER CHANGE
   ═══════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
    const browseForm = document.getElementById('browseForm');
    if (!browseForm) return;

    browseForm.querySelectorAll('.filter-select').forEach(select => {
        select.addEventListener('change', () => {
            browseForm.submit();
        });
    });
});


/* ═══════════════════════════════════════════════
   THEME SWITCHER (Dark / Light Mode)
   ═══════════════════════════════════════════════ */
function initThemeSwitcher() {
    const switcher = document.getElementById('themeSwitcher');
    if (!switcher) return;

    function getPreferredTheme() {
        const stored = localStorage.getItem('cb_theme');
        if (stored) return stored;
        return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('cb_theme', theme);
    }

    switcher.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
        const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
        setTheme(newTheme);
    });

    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('cb_theme')) {
                setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
}


/* ═══════════════════════════════════════════════
   IMAGE UPLOAD LIVE PREVIEW
   ═══════════════════════════════════════════════ */
function initImagePreview() {
    const imageInput = document.getElementById('id_image');
    if (!imageInput) return;

    const previewContainer = document.getElementById('image-preview-container');
    const previewImg = document.getElementById('image-preview-img');
    const previewName = document.getElementById('image-preview-name');
    const previewSize = document.getElementById('image-preview-size');
    const removeBtn = document.getElementById('image-remove-btn');

    imageInput.addEventListener('change', () => {
        const file = imageInput.files && imageInput.files[0];
        if (file) {
            if (previewName) previewName.textContent = file.name;
            if (previewSize) previewSize.textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';

            const reader = new FileReader();
            reader.onload = (e) => {
                if (previewImg) previewImg.src = e.target.result;
                if (previewContainer) {
                    previewContainer.style.display = 'block';
                    previewContainer.classList.add('visible');
                }
            };
            reader.readAsDataURL(file);
        } else {
            if (previewContainer) {
                previewContainer.style.display = 'none';
                previewContainer.classList.remove('visible');
            }
        }
    });

    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            imageInput.value = '';
            if (previewContainer) {
                previewContainer.style.display = 'none';
                previewContainer.classList.remove('visible');
            }
        });
    }
}
