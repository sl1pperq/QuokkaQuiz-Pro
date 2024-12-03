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

function uncolor() {
    document.getElementById('mainMenuLink').className = "nav-link link-body-emphasis"
    document.getElementById('cardQuizLink').className = "nav-link link-body-emphasis"
    document.getElementById('pricingLink').className = "nav-link link-body-emphasis"
    document.getElementById('groupsLink').className = "nav-link link-body-emphasis"
    document.getElementById('boxLink').className = "nav-link link-body-emphasis"
    document.getElementById('cloudLink').className = "nav-link link-body-emphasis"
    document.getElementById('tutorialLink').className = "nav-link link-body-emphasis"
    document.getElementById('supportLink').className = "nav-link link-body-emphasis"
}

function hideCards() {
    document.getElementById('mainMenu').style.display = "none"
    document.getElementById('cardQuiz').style.display = "none"
    document.getElementById('pricing').style.display = "none"
    document.getElementById('groups').style.display = "none"
    document.getElementById('box').style.display = "none"
}

function showMainMenu() {
    window.location.href = "/constructor?focusmain"
}

function showCardQuiz() {
    window.location.href = "/constructor?focusquiz"
}

function showPricing() {
    window.location.href = "/constructor?focusprice"
}

function showGroups() {
    window.location.href = "/constructor?focusgroup"
}

function showBox() {
    window.location.href = "/constructor?focusbox"
}

if (window.location.href.includes("?focusmain")) {
    hideCards()
    uncolor()
    document.getElementById('mainMenu').style.display = "block";
    document.getElementById('mainMenuLink').className = "nav-link active"
}

if (window.location.href.includes("?focusquiz")) {
    hideCards()
    uncolor()
    document.getElementById('cardQuiz').style.display = "block";
    document.getElementById('cardQuizLink').className = "nav-link active"
}

if (window.location.href.includes("?focusgroup")) {
    hideCards()
    uncolor()
    document.getElementById('groups').style.display = "block";
    document.getElementById('groupsLink').className = "nav-link active"
}

if (window.location.href.includes("?focusbox")) {
    hideCards()
    uncolor()
    document.getElementById('box').style.display = "block";
    document.getElementById('boxLink').className = "nav-link active"
}

if (window.location.href.includes("?focusprice")) {
    hideCards()
    uncolor()
    document.getElementById('pricing').style.display = "block";
    document.getElementById('pricingLink').className = "nav-link active"
}

function showPrice() {
    document.getElementById('priceButton').style.display = "none"
    document.getElementById('price').style.display = "block"
}

function calcQuizPrice() {
    var price = 1
    var val = parseInt(document.getElementById('quizRange').value)
    if (val <= 15) {
        price = val * 15
    } else if (val > 15 && val <= 30) {
        price = val * 12
    } else if (val > 31 && val <= 50) {
        price = val * 10
    } else if (val > 50 && val <= 75) {
        price = val * 8
    } else if (val > 75 && val <= 100) {
        price = val * 6
    }
    var word = trueWord(price)
    document.getElementById('quizPrice').innerHTML = `Стоимость ~ ${price} ₽ за ${val} ${word}`
}

function trueWord(s) {
    var n1 = "квизов"
    var n2 = "квиз"
    var n3 = "квиза"
    if (s === 0) {
        return n1
    } else if (s % 100 >= 10 && s % 100 <= 20) {
        return n1
    } else if (s % 10 === 1) {
        return n2
    } else if (s % 10 >= 2 && s % 10 <= 4) {
        return n3
    } else {
        return n1
    }
}