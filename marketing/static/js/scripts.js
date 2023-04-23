const BASE_URL = 'http://localhost:8000';
const BASE_API = BASE_URL + '/api/';
const REGISTER_API = BASE_API + 'user';
const VERIFY_OTP_API = BASE_API + 'user/verify_otp';
const EXTENSION_PACKAGE_API = BASE_URL + '/extension/';
const registerFormId = document.getElementById('registerFormId');
const registerSectionId = document.getElementById('registerSectionId');
const verifyOTPSectionId = document.getElementById('verifyOTPSectionId');
const successRegistrationSectionId = document.getElementById('successRegistrationSectionId');
const downloadExtensionId = document.getElementById('downloadExtensionId');

registerFormId.addEventListener('submit', (e) => {
    e.preventDefault();
    const emailInput = document.getElementById('emailInput').value;
    const passwordInput = document.getElementById('passwordInput').value;
    const confirmPasswordInput = document.getElementById('confirmPasswordInput').value;

    if (passwordInput !== confirmPasswordInput) {
        alert('Passwords do not match!');
        return;
    }

    const registerData = {
        email: emailInput,
        password: passwordInput
    };

    fetch(REGISTER_API, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(registerData)
    })
    .then(resp => {
        if(resp.status===200){
          return resp.json()
        }
      return Promise.reject(resp);
    })
    .then(data => {
        localStorage.setItem('email', emailInput);
        registerSectionId.style.display = 'none';
        verifyOTPSectionId.style.display = 'block';
        alert('OTP has been sent to your email!');
    })
    .catch(error => {
        error.json().then((err) => {
            let errorMsg = '';
            for (const [key, value] of Object.entries(err)) {
                errorMsg += `${key}: ${value}`;
            }
            alert(errorMsg);
        });
    })
});


otpFormId.addEventListener('submit', (e) => {
    e.preventDefault();
    const otpInput = document.getElementById('otpInput').value;
    const email = localStorage.getItem('email');

    const verifyOTPData = {
        email: email,
        otp: otpInput
    };

    fetch(VERIFY_OTP_API, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(verifyOTPData)
    })
    .then(resp => {
        if(resp.status===200){
            return resp.json()
          }
        return Promise.reject(resp);
    })
    .then(data => {
        verifyOTPSectionId.style.display = 'none';
        successRegistrationSectionId.style.display = 'block';
        downloadExtension();
    })
    .catch(error => {
        error.json().then((err) => {
            let errorMsg = '';
            for (const [key, value] of Object.entries(err)) {
                errorMsg += `${key}: ${value}`;
            }
            alert(errorMsg);
        }); 
    })
});

downloadExtensionId.addEventListener('click', () => {
    downloadExtension();
});

function downloadExtension(){
    fetch(EXTENSION_PACKAGE_API)
    .then(response => {
        if(response.status===200){
            return response.json()
          }
        return Promise.reject(response);
    })
    .then(data => {
        const extensionPackageUrl = data.zip;
        window.open(BASE_URL + extensionPackageUrl, '_blank');
    })
    .catch(error => {
        error.json().then((err) => {
            let errorMsg = '';
            for (const [key, value] of Object.entries(err)) {
                errorMsg += `${key}: ${value}`;
            }
            alert(errorMsg);
        }); 
    })
}
