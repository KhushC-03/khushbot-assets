var licenseKey = ""
const ALL_TASKS = [];
var instanceID = ""

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function counter(obj1, obj, start, end, duration, text) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = `${text}${Math.floor(progress * (end - start) + start)}`
        obj1.value = Math.floor(progress * (end - start) + start)
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function downloadExtension() {
    window.open('https://s3.eu-west-2.amazonaws.com/files.khushbot/extension/Khush+Bot+Extension.zip')
}

function download() {
    window.open('{{DOWNLOAD}}')
}

function copyKey() {
    navigator.clipboard.writeText(licenseKey)
}


function unbind() {
    fetch(`https://khushbot.co.uk/unbindmachine?key=${licenseKey}`, {
        method: 'GET',
    }).then(response => response.json()).then(data => {
        if (data.status == 'success') {
            document.getElementById('unbind').innerHTML = 'Machine Reset'
        }
    });
}

async function sendQT() {
    var identifier = document.getElementById('identifier').value
    var store = document.getElementById('stores').value
    if (identifier.length == 0) {
        document.querySelector(".errorHeader").innerHTML = "Please Enter A Valid Identifier"
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        await sleep(2500)
        document.querySelector(".errorHeader").innerHTML = ""
        return
    }
    if (store == "stores") {
        document.querySelector(".errorHeader").innerHTML = "Please Enter A Valid Store"
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        await sleep(2500)
        document.querySelector(".errorHeader").innerHTML = ""
        return
    }

    fetch(`https://quicktask.khushbot.ngrok.app/quicktask/start/${licenseKey}?STORE=${store}&IDENTIFIER=${identifier}`, {
        method: 'GET',
    }).then(response => response.json()).then(data => {
        if (data.success == true) {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            document.querySelector('.successHeader').innerHTML = data.message;
            document.querySelector(".errorHeader").innerHTML = ""
        } else {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            document.querySelector('.successHeader').innerHTML = ""
            document.querySelector('.errorHeader').innerHTML = data.message;
        }
    });
}

function unbindDiscord() {
    if (confirm('Are you sure you want to unbind your discord account?')) {
        window.location.assign(`https://khushbot.co.uk/unbinddiscord/${licenseKey}`)
    }
}

function showkey() {
    if (document.getElementById('key').innerHTML == 'KB-XXXXX-XXXXXX-XXXXX') {
        document.getElementById('key').innerHTML = licenseKey
    } else {
        document.getElementById('key').innerHTML = 'KB-XXXXX-XXXXXX-XXXXX'
    }

}

async function checkQT() {
    if (document.location.href.toLocaleLowerCase().includes("store")) {
        await sleep(3000);
        window.location.assign(`https://khushbot.co.uk/dashboard?displayoption=tasks`)
    }
}

function removeTasks(isTasks = true) {
    const elementsToRemove = document.querySelectorAll('.checkoutList');
    var currentInstance = document.getElementById('instance').value
    if (currentInstance == "none") {
        document.getElementById('stopinstance').value = "none"
        document.getElementById('stopinstance').innerHTML = `No Instances Connected`
    } else {
        if (isTasks) {
            document.getElementById('stopinstance').value = currentInstance
            document.getElementById('stopinstance').innerHTML = `Stop Instance ${currentInstance}`
        }

    }

    for (let i = 0; i < elementsToRemove.length; i++) {
        ALL_TASKS.pop(i + 1)
        elementsToRemove[i].remove();
    }
}
async function stopTasks() {
    if (document.getElementById('stopinstance').value != "none") {
        fetch(`https://quicktask.khushbot.ngrok.app/webtasks/stop/${licenseKey}/${instanceID}`, {
            method: 'GET',
        }).then(response => response.json()).then(async data => {
            document.getElementById('stopinstance').innerHTML = data.message
            if (!data.success) {
                await sleep(2500);
                var currentInstance = document.getElementById('instance').value
                document.getElementById('stopinstance').innerHTML = `Stop Instance ${currentInstance}`
            }
        });
    }
}


function getInstancevalues() {
    var dropValues = document.querySelectorAll('.dropvalues');
    var valuesArray = [];
    for (let i = 0; i < dropValues.length; i++) {
        valuesArray.push(parseInt(dropValues[i].value));
    }
    return valuesArray
}

function createDropdown(amount) {
    if (document.querySelectorAll('.dropvalues').length < amount) {
        for (let i = 0; i < amount; i++) {
            if (!getInstancevalues().includes(i + 1)) {

                document.getElementById('instance').insertAdjacentHTML("beforeend", `<option class="dropvalues" id="instance${i+1}" value="${i+1}">Instance ${i+1}</option>`);
                if (i + 1 == 1) {
                    document.getElementById('instance').value = i + 1
                }
            }
        }
    } else if (document.querySelectorAll('.dropvalues').length > amount) {
        var elementsToRemove = Array.from(document.querySelectorAll('.dropvalues')).reverse()
        for (let i = 0; i < (document.querySelectorAll('.dropvalues').length - amount); i++) {
            elementsToRemove[i].remove();
        }

    }

}

function getInstance(socketResponse, instance) {
    const timestamps = Object.keys(socketResponse);
    timestamps.sort()
    instanceID = timestamps[instance - 1]
    return timestamps[instance - 1]

}
async function getTasks() {
    const socket = new WebSocket(`wss://quicktask.khushbot.ngrok.app/tasks/${licenseKey}`);
    socket.addEventListener('open', event => {
        setInterval(() => {
            socket.send(JSON.stringify({
                "ping": "pong"
            }));
        }, 250);
    });
    socket.addEventListener("message", (event) => {
        var selectedInstance = parseInt(document.getElementById('instance').options[document.getElementById('instance').selectedIndex].value);
        var instanceTasks = JSON.parse(event.data)
        if (Object.keys(instanceTasks).length > 0) {
            var currentInstanceID = instanceID
            var instance = getInstance(instanceTasks, selectedInstance)
            if (parseInt(currentInstanceID) != parseInt(instance) && instanceID != "") {
                removeTasks()
            }
            createDropdown(Object.keys(instanceTasks).length)

            if (instanceTasks.hasOwnProperty(instance) && Object.keys(instanceTasks[instance]).length > 0) {
                for (let i = 0; i < Object.keys(instanceTasks[instance]).length; i++) {
                    try {
                        var store = instanceTasks[instance][i + 1].store
                        var message = instanceTasks[instance][i + 1].status
                        if (message.toLowerCase().includes("checkout successful")) {
                            var message = "Successful Checkout! Check Your Webhook For More Info."
                        }
                        if (message.toLowerCase().includes("checkout failed")) {
                            var message = "Checkout Failed! Check Your Webhook For More Info."
                        }
                    } catch {
                        continue
                    }



                    if (message.includes("x1b") || message.includes("1;") || message.includes("[38")) {
                        var index = message.indexOf('m');
                        var value = message.slice(0, index);

                        var message = message.slice(index + 1);
                    }

                    if (!ALL_TASKS.includes(i + 1)) {
                        ALL_TASKS.push(i + 1)
                        document.querySelector('.userCheckouts').insertAdjacentHTML("beforeend", `<div class="checkoutList">
                            <span id="${i+1}store" style="margin-left:15px; white-space: nowrap;">${store}</span>
                            <span id="${i+1}task" style="margin-left:18px">${i+1}</span>
                            <span id="${i+1}status" style="margin-left:18px; margin-right:2px">${message}</span>
                            </div>`);
                        if (message.toLowerCase().includes("successful") || message.toLowerCase().includes("successfully")) {
                            document.getElementById(`${i+1}status`).style.color = "#8bda97";
                        } else if (message.includes("error")) {
                            document.getElementById(`${i+1}status`).style.color = "#ff7272";
                        } else if (message.includes("OOS") || message.toLowerCase().includes("saved session not found")) {
                            document.getElementById(`${i+1}status`).style.color = "#fffa58";
                        } else {
                            document.getElementById(`${i+1}status`).style.color = "#e7e7e7";
                        }

                    } else {
                        if (message.toLowerCase().includes("successful") || message.toLowerCase().includes("successfully")) {
                            document.getElementById(`${i+1}status`).style.color = "#8bda97";
                        } else if (message.toLowerCase().includes("error") || message.toLowerCase().includes("failed")) {
                            document.getElementById(`${i+1}status`).style.color = "#ff7272";
                        } else if (message.includes("OOS") || message.toLowerCase().includes("saved session not found")) {
                            document.getElementById(`${i+1}status`).style.color = "#fffa58";
                        } else {
                            document.getElementById(`${i+1}status`).style.color = "#e7e7e7";
                        }
                        document.getElementById(`${i+1}store`).innerHTML = store
                        document.getElementById(`${i+1}task`).innerHTML = i + 1
                        document.getElementById(`${i+1}status`).innerHTML = message
                    }

                }
            }
        } else {

            removeTasks()
            document.getElementById('instance').value = "none"
            try {
                document.getElementById('instance1').remove()
            } catch {}

        }
    });
}


checkQT()

getTasks()
counter(document.getElementById("checkoutsp"), document.getElementById("checkouts"), 0, 230, 1000, 'Successful Checkouts ');
