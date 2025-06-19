// Main JavaScript functionality for the website

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
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

    // Animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all fade-in elements
    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });

    // Add hover effects to method steps
    document.querySelectorAll('.method-step').forEach(step => {
        step.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
            this.style.transition = 'all 0.3s ease';
        });

        step.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        });
    });

    // Add click tracking for download buttons
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const btnText = this.textContent.trim();
            console.log(`Download clicked: ${btnText}`);
            
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Video error handling
    const video = document.querySelector('video');
    if (video) {
        video.addEventListener('error', function(e) {
            console.error('Video loading error:', e);
            const container = this.parentElement;
            const errorMsg = document.createElement('div');
            errorMsg.innerHTML = `
                <div style="background: #f8f9fa; padding: 40px; border-radius: 8px; text-align: center; border: 2px dashed #ddd;">
                    <i class="fas fa-video" style="font-size: 3em; color: #ccc; margin-bottom: 20px;"></i>
                    <h3>Demo Video</h3>
                    <p>Video file not available. Please check the <a href="../src/demo.mov" target="_blank">direct link</a> or visit the <a href="../" target="_blank">GitHub repository</a>.</p>
                </div>
            `;
            container.replaceChild(errorMsg, this);
        });

        // Video load success
        video.addEventListener('loadeddata', function() {
            console.log('Video loaded successfully');
        });
    }

    // Add table responsiveness
    const tables = document.querySelectorAll('.results-table');
    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.style.overflowX = 'auto';
        wrapper.style.marginBottom = '20px';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });

    // Navigation highlight on scroll
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

    function updateActiveNav() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav);

    // Add print styles
    const printStyles = `
        @media print {
            .nav, .download-section, .footer { display: none; }
            .container { max-width: none; margin: 0; padding: 0; }
            .section { page-break-inside: avoid; }
            .method-step { page-break-inside: avoid; }
            body { font-size: 12pt; line-height: 1.4; }
        }
    `;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = printStyles;
    document.head.appendChild(styleSheet);
});

// Add CSS for active navigation
const activeNavStyles = `
    .nav-link.active {
        background: #0066cc !important;
        color: white !important;
        border-color: #0066cc !important;
    }
`;

const navStyleSheet = document.createElement('style');
navStyleSheet.textContent = activeNavStyles;
document.head.appendChild(navStyleSheet);

// Utility function for smooth animations
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Add copy to clipboard functionality for code blocks
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.code-example').forEach(codeBlock => {
        const copyBtn = document.createElement('button');
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #666;
            color: white;
            border: none;
            padding: 5px 8px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            opacity: 0;
            transition: opacity 0.2s;
        `;
        
        codeBlock.style.position = 'relative';
        codeBlock.appendChild(copyBtn);
        
        codeBlock.addEventListener('mouseenter', () => {
            copyBtn.style.opacity = '1';
        });
        
        codeBlock.addEventListener('mouseleave', () => {
            copyBtn.style.opacity = '0';
        });
        
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(codeBlock.textContent).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
        });
    });
});