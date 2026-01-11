 // Switch between Login and Sign Up
        function switchTab(tab) {
            const tabs = document.querySelectorAll('.tab');
            const loginForm = document.getElementById('loginForm');
            const signupForm = document.getElementById('signupForm');
            const footerText = document.getElementById('footerText');

            tabs.forEach(t => t.classList.remove('active'));
            
            if (tab === 'login') {
                tabs[0].classList.add('active');
                loginForm.style.display = 'block';
                signupForm.style.display = 'none';
                footerText.innerHTML = 'Don\'t have an account? <a href="#" onclick="switchTab(\'signup\'); return false;">Sign up now</a>';
            } else {
                tabs[1].classList.add('active');
                loginForm.style.display = 'none';
                signupForm.style.display = 'block';
                footerText.innerHTML = 'Already have an account? <a href="#" onclick="switchTab(\'login\'); return false;">Login here</a>';
            }

            hideError();
        }

        // Toggle Password Visibility
        function togglePassword(inputId) {
            const input = document.getElementById(inputId);
            const icon = input.nextElementSibling;
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.textContent = '🙈';
            } else {
                input.type = 'password';
                icon.textContent = '👁️';
            }
        }

        // Show Error Message
        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }

        // Hide Error Message
        function hideError() {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.classList.remove('show');
        }

        // Show Success Message
        function showSuccess(message) {
            const successDiv = document.getElementById('successMessage');
            successDiv.textContent = message;
            successDiv.classList.add('show');
            
            setTimeout(() => {
                successDiv.classList.remove('show');
            }, 3000);
        }

        // Validate Email
        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        // Login Form Submit
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            hideError();

            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            // Validation
            if (!isValidEmail(email)) {
                showError('⚠️ Please enter a valid email address');
                return;
            }

            if (password.length < 6) {
                showError('⚠️ Password must be at least 6 characters');
                return;
            }

            // Demo credentials
            if (email === 'demo@cinematch.com' && password === 'demo123') {
                showSuccess('✓ Login Successful! Welcome to CineMatch 🎬');
                
                // Simulate redirect after 2 seconds
                setTimeout(() => {
                    console.log('Redirecting to dashboard...');
                    // window.location.href = '/dashboard';
                }, 2000);
            } else {
                showError('⚠️ Invalid email or password. Try: demo@cinematch.com / demo123');
            }
        });

        // Sign Up Form Submit
        document.getElementById('signupForm').addEventListener('submit', function(e) {
            e.preventDefault();
            hideError();

            const name = document.getElementById('signupName').value;
            const email = document.getElementById('signupEmail').value;
            const password = document.getElementById('signupPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            // Validation
            if (name.length < 3) {
                showError('⚠️ Name must be at least 3 characters');
                return;
            }

            if (!isValidEmail(email)) {
                showError('⚠️ Please enter a valid email address');
                return;
            }

            if (password.length < 6) {
                showError('⚠️ Password must be at least 6 characters');
                return;
            }

            if (password !== confirmPassword) {
                showError('⚠️ Passwords do not match');
                return;
            }

            // Success
            showSuccess(`✓ Account created successfully! Welcome ${name} 🎉`);
            
            // Switch to login after 2 seconds
            setTimeout(() => {
                switchTab('login');
                document.getElementById('loginEmail').value = email;
            }, 2000);
        });

        // Social Login
        function socialLogin(provider) {
            showSuccess(`✓ Logging in with ${provider}... 🚀`);
            
            setTimeout(() => {
                console.log(`${provider} login successful`);
                // window.location.href = '/dashboard';
            }, 2000);
        }

        // Auto-fill demo credentials on page load
        window.addEventListener('load', function() {
            console.log('Demo Login: demo@cinematch.com / demo123');
        });