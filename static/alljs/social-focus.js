if (window.location.href.includes("focusmain")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('main').style.display = "block";
    document.getElementById('mainLink').className = "nav-link active"
}

if (window.location.href.includes("focusquiz")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('ask').style.display = "block";
    document.getElementById('askLink').className = "nav-link active"
}

if (window.location.href.includes("focusresult")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('result').style.display = "block";
    document.getElementById('resultLink').className = "nav-link active"
}

if (window.location.href.includes("focussettings")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('settings').style.display = "block";
    document.getElementById('settingsLink').className = "nav-link active"
}

if (window.location.href.includes("focusshare")) {
    hideStudCards()
    uncolorStud()
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

function uncolorStud() {
    document.getElementById('statMenuLink').className = "nav-link link-body-emphasis"
    document.getElementById('teachTaskLink').className = "nav-link link-body-emphasis"
    document.getElementById('storeLink').className = "nav-link link-body-emphasis"
    document.getElementById('ordersLink').className = "nav-link link-body-emphasis"
    document.getElementById('prepareLink').className = "nav-link link-body-emphasis"
    document.getElementById('solveHistory').className = "nav-link link-body-emphasis"
    document.getElementById('tutorialLink1').className = "nav-link link-body-emphasis"
    document.getElementById('supportLink1').className = "nav-link link-body-emphasis"
}

function hideStudCards() {
    document.getElementById('stat').style.display = "none"
    document.getElementById('teachTask').style.display = "none"
    document.getElementById('store').style.display = "none"
    document.getElementById('orders').style.display = "none"
    document.getElementById('prepare').style.display = "none"
    document.getElementById('solveHistoryCard').style.display = "none"
}

function showStatMenu() {
    window.location.href = "/social/my?focusstat"
}

function showTeachTask() {
    window.location.href = "/social/my?focustask"
}

function showStore() {
    window.location.href = "/social/my?focusstore"
}

function showOrders() {
    window.location.href = "/social/my?focusorders"
}

function showSolveHistory() {
    window.location.href = "/social/my?focushistory"
}

function showPrepare() {
    window.location.href = "/social/my?focusprepare"
}

if (window.location.href.includes("?focusstat")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('stat').style.display = "block";
    document.getElementById('statMenuLink').className = "nav-link active"
}

if (window.location.href.includes("?focustask")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('teachTask').style.display = "block";
    document.getElementById('teachTaskLink').className = "nav-link active"
}

if (window.location.href.includes("?focusorders")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('orders').style.display = "block";
    document.getElementById('ordersLink').className = "nav-link active"
}

if (window.location.href.includes("?focushistory")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('solveHistoryCard').style.display = "block";
    document.getElementById('solveHistory').className = "nav-link active"
}

if (window.location.href.includes("?focusstore")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('store').style.display = "block";
    document.getElementById('storeLink').className = "nav-link active"
}

if (window.location.href.includes("?focusprepare")) {
    hideStudCards()
    uncolorStud()
    document.getElementById('prepare').style.display = "block";
    document.getElementById('prepareLink').className = "nav-link active"
}

function showPrice() {
    document.getElementById('priceButton').style.display = "none"
    document.getElementById('price').style.display = "block"
}

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

function showInfo() {
    document.getElementById('infoQC').style.display = "block"
    document.getElementById('infoBut').style.display = "none"
}

function showOrders1() {
    document.getElementById('ordersCard').style.display = "block"
    document.getElementById('ordersBut').style.display = "none"
}

function showQuizes() {
    document.getElementById('quizCard').style.display = "block"
    document.getElementById('quizBut').style.display = "none"
}

function showShop() {
    document.getElementById('shop').style.display = "block"
    document.getElementById('shopBut').style.display = "none"
}