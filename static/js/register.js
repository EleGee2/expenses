const usernameField = document.querySelector("#usernameField")
const emailField = document.querySelector("#emailField")
const feedbackField = document.querySelector(".username-invalid-feedback")
const emailFeedbackField = document.querySelector(".email-invalid-feedback")
const usernameSuccess = document.querySelector(".username-success")
const emailSuccess = document.querySelector(".email-success")
const showPasswordToggle = document.querySelector(".show-password-toggle")
const passwordField = document.querySelector("#passwordField")
const submitBtn = document.querySelector(".submit-btn")

usernameField.addEventListener("keyup", (e) => {
    const usernameValue = e.target.value
    usernameSuccess.style.display = "block"

    // usernameSuccess.textContent = `Checking ${usernameValue}`
    usernameField.classList.remove("is-invalid")
    feedbackField.style.display = "none"

    if (usernameValue.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameValue }),
            method: "POST"
        }).then(response => response.json())
            .then(data => {
                usernameSuccess.style.display = "none"
                if (data.error) {
                    usernameField.classList.add("is-invalid")
                    feedbackField.style.display = "block"
                    feedbackField.innerHTML = `<p>${data.error}</p>`
                    submitBtn.disabled = true
                } else {
                    submitBtn.removeAttribute('disabled')
                }
            })
    }
})

emailField.addEventListener("keyup", (e) => {
    console.log("listened to email event")

    const emailValue = e.target.value
    emailSuccess.style.display = "block"
    // emailSuccess.textContent = `Checking ${emailValue}`

    emailField.classList.remove("is-invalid")
    emailFeedbackField.style.display = "none"

    if (emailValue.length > 0) {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailValue }),
            method: "POST"
        }).then(response => response.json())
            .then(data => {
                emailSuccess.style.display = "none"
                if (data.error) {
                    // submitBtn.setAttribute('disabled', 'disabled')
                    emailField.classList.add("is-invalid")
                    emailFeedbackField.style.display = "block"
                    emailFeedbackField.innerHTML = `<p>${data.error}</p>`
                    submitBtn.disabled = true
                } else {
                    submitBtn.removeAttribute('disabled')
                    submitBtn.disabled = true
                }
            })
    }
})

showPasswordToggle.addEventListener("click", (e) => {
    if (showPasswordToggle.textContent === "Show Password") {
        showPasswordToggle.textContent = "Hide Password"
        passwordField.setAttribute("type", "text")
    } else {
        showPasswordToggle.textContent = "Show Password"
        passwordField.setAttribute("type", "password")
    }
})