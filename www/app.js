let currIndex = 0;
let maxIndex = 2;

let forms = document.getElementsByTagName("form");
forms[currIndex].classList.remove("d-none");

const mainContainer = document.getElementById('main-container');
const submitLoader = document.getElementById('submit_loader');
const indicators = document.getElementsByClassName("screen-indicator");
const progressElm = document.getElementsByClassName("progress")[0];
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
const submitBtn = document.getElementById("submit-btn");

disableControls();

function previous() {
    // Delay should not be applied when removing class
    indicators[currIndex].style.transitionDelay = "0s";
    indicators[currIndex].classList.remove("completed");
    --currIndex;
    progressElm.style.width = `${(currIndex / (indicators.length - 1)) * 100}%`;
    hideForms()
    forms[currIndex].classList.remove("d-none");
    disableControls();
}

function next() {
    submitForm();
    ++currIndex;
    // Delay should be applied when adding class
    indicators[currIndex].style.transitionDelay = "0.6s";
    indicators[currIndex].classList.add("completed");
    progressElm.style.width = `${(currIndex / (indicators.length - 1)) * 100}%`;
    hideForms()
    forms[currIndex].classList.remove("d-none");
    disableControls();

}

function disableControls() {
    if (currIndex <= 0) {
        prevBtn.disabled = true;
    } else if (currIndex >= indicators.length - 1) {
        nextBtn.disabled = true;
    } else {
        prevBtn.disabled = false;
        nextBtn.disabled = false;
    }

    if (currIndex == maxIndex) {
        nextBtn.classList.add("d-none");
        submitBtn.classList.remove("d-none");
    } else {
        submitBtn.classList.add("d-none");
        nextBtn.classList.remove("d-none");
    }

}

function hideForms() {

    for (let i = 0; i < forms.length; i++) {
        if (i != currIndex) {
            forms[i].classList.add("d-none");
        }
    }
}


function submitForm() {
    if (currIndex == 0) {
        submitWifiForm();
    }
    if (currIndex == 1) {
        submitMqttForm();
    }
    if (currIndex == 2) {
        promoteToMqttForm();
    }

    showLoader()
}

function showLoader() {
    submitLoader.classList.remove("d-none");
}

function hideLoader() {
    submitLoader.classList.add("d-none");
}

function showSnackbar(msg, duration= 3000) {
    let x = document.getElementById("snackbar");
    x.innerHTML = msg
    x.className = "show";
    setTimeout(() => { x.className = x.className.replace("show", ""); x.innerHTML = "" }, duration);
}

function submitWifiForm() {
    console.log('Submit Wifi Form');

    let wifiForm = document.getElementById('wifiSetup');

    let formData = new FormData(wifiForm);
    console.log('Form Data:', formData);

    var object = {};
    formData.forEach((value, key) => object[key] = value);

    console.log('Form Data to Object:', object);

    (async () => {
        const rawResponse = await fetch('/set-up-ssid', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(object)
        });
        const content = await rawResponse.json();
        console.log('Wifi Form Submit Content:', content);

        if (content.data && content.data.status) {
            console.log('Wifi Credentials saved successfully.');
            showSnackbar('Wifi Credentials saved successfully.')
        } else {
            showSnackbar('Some error occured in saving WIFI Credentials.')
        }

        hideLoader();
    })();
}

function submitMqttForm() {
    console.log('Submit MQTT Form');

    let wifiForm = document.getElementById('mqttSetup');

    let formData = new FormData(wifiForm);
    console.log('Form Data:', formData);

    var object = {};
    formData.forEach((value, key) => object[key] = value);

    console.log('Form Data to Object:', object);

    (async () => {
        const rawResponse = await fetch('/set-up-mqtt', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(object)
        });
        const content = await rawResponse.json();
        console.log('MQTT Form Submit Content:', content);

        if (content.data && content.data.status) {
            console.log('MQTT Credentials saved successfully.');
            showSnackbar('MQTT Credentials saved successfully.')
        } else {
            showSnackbar('Some error occured in saving MQTT Credentials.')
        }

        hideLoader();
    })();
}

function promoteToMqttForm() {
    console.log('Submit Promote to MQTT Form');

    let fetchRes = fetch("/promote-to-mqtt");
    fetchRes.then(res => res.json()).then(d => {
        console.log('Promote to MQTT:', d);

        if(d.status) {
            showSnackbar(d.message)
        } else {
            showSnackbar('Some error occurred, may be mqtt credentials are invalid.')
        }

        hideLoader();
    })
}

function getDeviceInfo() {
    let fetchRes = fetch("/device-info");
    fetchRes.then(res => res.json()).then(d => {
        console.log('Device Info:', d);
        if (d) {
            let machineIdHolder = document.getElementById('machine_id');
            machineIdHolder.innerHTML = `Machine ID: ${d.MACHINE_ID}`

            let deviceIPHolder = document.getElementById('device_ip');
            deviceIPHolder.innerHTML = `Your IP: ${d.ClientAddr}`

            let machineIdHolder2 = document.getElementById('machine_id_holder2');
            machineIdHolder2.innerHTML = `${d.MACHINE_ID}`
        }
    })
}

function getSSIDInfo() {
    let fetchRes = fetch("/get-ssid");
    fetchRes.then(res => res.json()).then(d => {
        console.log('SSID:', d);
        if (d && d.data) {
            let wifiSsidInputEl = document.getElementById('wifi_ssid');
            let wifiPasswordInputEl = document.getElementById('wifi_passwd');
            wifiSsidInputEl.value = d.data.ssid;
            wifiPasswordInputEl.value = d.data.passwd;
        }
    })
}

function getMQTTInfo() {
    let fetchRes = fetch("/get-mqtt-config");
    fetchRes.then(res => res.json()).then(d => {
        console.log('MQTT:', d);
        if (d && d.data) {
            let mqqtHost = document.getElementById('mqtt_host');
            let mqttPort = document.getElementById('mqtt_port');
            let mqttUser = document.getElementById('mqtt_user');
            let mqttPassword = document.getElementById('mqtt_passwd');
            mqqtHost.value = d.data.host;
            mqttPort.value = d.data.port;
            mqttUser.value = d.data.user;
            mqttPassword.value = d.data.passwd;
        }
    })
}

document.addEventListener("DOMContentLoaded", function () {
    getDeviceInfo();
    setTimeout(() => {
        getSSIDInfo();
    }, 1000)
    setTimeout(() => {
        getMQTTInfo();
    }, 2000)
    mainContainer.classList.remove("d-none");
    submitLoader.classList.add("d-none");
});