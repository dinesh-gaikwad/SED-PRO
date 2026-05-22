  
document.addEventListener('DOMContentLoaded', function(){

    // Auto close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl){
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl){
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add fade-in animation to cards on scroll
    const observerOptions = {
        threshold:0.1,
        rootMargin:'0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries){
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card,.mentor-card,.course-card').forEach(el => {
        observer.observe(el);
    });

    // AJAX CSRF token setup
    function getCookie(name){
        let cookieValue = null;
        if(document.cookie && document.cookie!== ''){
            const cookies = document.cookie.split(';');
            for(let i=0; i<cookies.length; i++){
                const cookie = cookies[i].trim();
                if(cookie.substring(0, name.length+1) === (name+'=')){
                    cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Global AJAX setup
    const originalFetch = window.fetch;
    window.fetch = function(){
        const args = arguments;
        if(args[1] && args[1].method && args[1].method!== 'GET'){
            args[1].headers = args[1].headers || {};
            args[1].headers['X-CSRFToken'] = csrftoken;
        }
        return originalFetch.apply(this, args);
    };

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event){
            if(!form.checkValidity()){
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Password strength checker
    const passwordInputs = document.querySelectorAll('input[type="password"][name*="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function(){
            const strength = checkPasswordStrength(this.value);
            let indicator = this.parentElement.querySelector('.password-strength');
            if(!indicator){
                indicator = document.createElement('div');
                indicator.className = 'password-strength mt-2';
                this.parentElement.appendChild(indicator);
            }
            indicator.innerHTML = strength.text;
            indicator.className = 'password-strength mt-2 text-' + strength.color;
        });
    });

    function checkPasswordStrength(password){
        let strength = 0;
        if(password.length >= 8) strength++;
        if(password.match(/[a-z]/)) strength++;
        if(password.match(/[A-Z]/)) strength++;
        if(password.match(/[0-9]/)) strength++;
        if(password.match(/[^a-zA-Z0-9]/)) strength++;

        if(strength < 3) return {text:'Weak Password', color:'danger'};
        if(strength < 5) return {text:'Medium Password', color:'warning'};
        return {text:'Strong Password', color:'success'};
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e){
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if(target){
                target.scrollIntoView({behavior:'smooth', block:'start'});
            }
        });
    });

    // Back to top button
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTop.className = 'btn btn-primary rounded-circle position-fixed';
    backToTop.style.cssText = 'bottom:30px;right:30px;width:50px;height:50px;display:none;z-index:999;';
    backToTop.id = 'backToTop';
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', function(){
        if(window.pageYOffset > 300){
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });

    backToTop.addEventListener('click', function(){
        window.scrollTo({top:0, behavior:'smooth'});
    });

    // Loading overlay for forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(){
            const submitBtn = this.querySelector('button[type="submit"]');
            if(submitBtn){
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            }
        });
    });

    // Copy to clipboard
    window.copyToClipboard = function(text){
        navigator.clipboard.writeText(text).then(function(){
            showToast('Copied to clipboard', 'success');
        });
    };

    // Toast notification
    window.showToast = function(message, type='info'){
        const toastContainer = document.getElementById('toastContainer') || createToastContainer();
        const toastId = 'toast-' + Date.now();
        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, {delay:3000});
        toast.show();
        toastEl.addEventListener('hidden.bs.toast', function(){
            toastEl.remove();
        });
    };

    function createToastContainer(){
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }

    // Confirm delete
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function(e){
            e.preventDefault();
            const url = this.getAttribute('href') || this.dataset.url;
            if(confirm('Are you sure you want to delete this item?')){
                window.location.href = url;
            }
        });
    });

    // Auto save form data to localStorage
    document.querySelectorAll('form[data-autosave]').forEach(form => {
        const formId = form.id || 'form-' + Date.now();
        const inputs = form.querySelectorAll('input, textarea, select');

        inputs.forEach(input => {
            const savedValue = localStorage.getItem(formId + '-' + input.name);
            if(savedValue && input.type!== 'password'){
                input.value = savedValue;
            }
            input.addEventListener('input', function(){
                localStorage.setItem(formId + '-' + input.name, this.value);
            });
        });

        form.addEventListener('submit', function(){
            inputs.forEach(input => {
                localStorage.removeItem(formId + '-' + input.name);
            });
        });
    });

    // Image preview
    document.querySelectorAll('input[type="file"][data-preview]').forEach(input => {
        input.addEventListener('change', function(){
            const previewId = this.dataset.preview;
            const preview = document.getElementById(previewId);
            if(preview && this.files && this.files[0]){
                const reader = new FileReader();
                reader.onload = function(e){
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if(darkModeToggle){
        const isDarkMode = localStorage.getItem('darkMode') === 'true';
        if(isDarkMode){
            document.body.classList.add('dark-mode');
        }
        darkModeToggle.addEventListener('click', function(){
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
    }

    // Countdown timer
    window.startCountdown = function(elementId, seconds, callback){
        const el = document.getElementById(elementId);
        let remaining = seconds;
        const interval = setInterval(function(){
            const mins = Math.floor(remaining / 60);
            const secs = remaining % 60;
            el.textContent = String(mins).padStart(2,'0') + ':' + String(secs).padStart(2,'0');
            remaining--;
            if(remaining < 0){
                clearInterval(interval);
                if(callback) callback();
            }
        }, 1000);
        return interval;
    };

    console.log('EntreSkill Hub JS Loaded Successfully');
});