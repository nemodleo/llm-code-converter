// Main JavaScript functionality for the website
document.addEventListener('DOMContentLoaded', function() {

    // --- Smooth Scrolling ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // --- Intersection Observer for Animations ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                if (entry.target.classList.contains('highlight-card')) {
                    entry.target.style.transform = 'translateY(0) rotateY(0deg)';
                }
                observer.unobserve(entry.target); // Animate only once
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in, .method-step, .highlight-card').forEach(el => {
        observer.observe(el);
    });

    // --- Number Counting Animation ---
    function animateNumber(element, start, end, duration, suffix = '') {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const current = Math.floor(progress * (end - start) + start);
            element.textContent = current + suffix;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    document.querySelectorAll('.highlight-number').forEach(el => {
        const finalValue = el.textContent;
        const duration = 2000;
        if (finalValue.includes('%')) {
            const num = parseInt(finalValue);
            animateNumber(el, 0, num, duration, '%');
        } else if (finalValue.includes('+')) {
            const num = parseInt(finalValue);
            animateNumber(el, 0, num, duration, '+');
        } else if (!isNaN(parseInt(finalValue))) {
            const num = parseInt(finalValue);
            animateNumber(el, 0, num, duration);
        }
    });

    // --- Video Error Handling ---
    const video = document.querySelector('video');
    if (video) {
        video.addEventListener('error', function(e) {
            console.error('Video loading error:', e);
            const container = this.parentElement;
            if (container) {
                const errorMsg = document.createElement('div');
                errorMsg.innerHTML = `
                    <div style="background: #f8f9fa; padding: 40px; border-radius: 8px; text-align: center; border: 2px dashed #ddd;">
                        <i class="fas fa-video-slash" style="font-size: 3em; color: #ccc; margin-bottom: 20px;"></i>
                        <h3>Demo Video Not Available</h3>
                        <p>The video could not be loaded. Please check the <a href="https://github.com/nemodleo/llm-code-converter" target="_blank">GitHub repository</a> for resources.</p>
                    </div>
                `;
                container.innerHTML = '';
                container.appendChild(errorMsg);
            }
        });
    }

    // --- Responsive Table Wrapper ---
    document.querySelectorAll('.results-table-container').forEach(wrapper => {
        if(wrapper.scrollWidth > wrapper.clientWidth) {
            wrapper.style.border = '1px solid #e0e0e0';
            wrapper.style.borderRadius = '8px';
        }
    });

    // --- Navigation Highlight on Scroll ---
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

    function updateActiveNav() {
        let currentSectionId = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= sectionTop - 100) { // Adjusted offset
                currentSectionId = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSectionId}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav(); // Initial check

});