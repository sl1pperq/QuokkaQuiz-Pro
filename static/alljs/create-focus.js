
if (window.location.href.includes("focusmain")) {
    hideCards()
    uncolor()
    document.getElementById('main').style.display = "block";
    document.getElementById('mainLink').className = "nav-link active"
}

if (window.location.href.includes("focusquiz")) {
    hideCards()
    uncolor()
    document.getElementById('ask').style.display = "block";
    document.getElementById('askLink').className = "nav-link active"
}

if (window.location.href.includes("focusresult")) {
    hideCards()
    uncolor()
    document.getElementById('result').style.display = "block";
    document.getElementById('resultLink').className = "nav-link active"
}

if (window.location.href.includes("focussettings")) {
    hideCards()
    uncolor()
    document.getElementById('settings').style.display = "block";
    document.getElementById('settingsLink').className = "nav-link active"
}

if (window.location.href.includes("focusshare")) {
    hideCards()
    uncolor()
    document.getElementById('share').style.display = "block";
    document.getElementById('shareLink').className = "nav-link active"
}

if (window.location.href.includes("#")) {
    showLiveToast()
}

function copyQuizLink(text) {
    navigator.clipboard.writeText(text);
    alert("Ссылка на квиз успешно скопирована в буфер обмена!")
}

function copyQuizNum(num) {
    navigator.clipboard.writeText(num);
    alert("Номер квиза успешно скопирован в буфер обмена!")
}

function showLiveToast() {
    const toastLiveExample = document.getElementById('liveToast')
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    toastBootstrap.show()
}

function showSettings() {
    document.getElementById('set').style.display = "block"
    document.getElementById('setButton').style.display = "none"
}