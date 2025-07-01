document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('login-btn')
    const registerBtn = document.getElementById('register-btn')
    const loginForm = document.getElementById('login-form')
    const registerForm = document.getElementById('register-form')


    loginBtn.addEventListener('click', () => {
        loginForm.classList.remove('hidden')
        loginBtn.classList.add('hover')
        registerForm.classList.add('hidden')
        registerBtn.classList.remove('hover')
    })

    registerBtn.addEventListener('click', () => {
        loginForm.classList.add('hidden')
        loginBtn.classList.remove('hover')
        registerForm.classList.remove('hidden')
        registerBtn.classList.add('hover')
    })

})