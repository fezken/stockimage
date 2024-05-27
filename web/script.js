let expandTextField = false;  // Set initial state to false

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('expand-toggle').checked = expandTextField;

    const rangeTypeRadios = document.getElementsByName('range-type');
    rangeTypeRadios.forEach(radio => {
        radio.addEventListener('change', toggleRangeType);
    });
});

async function checkKeywords() {
    showNotification('Checking keywords...');
    let keywords = document.getElementById('keywords').value;
    let category = document.querySelector('input[name="category"]:checked').value;
    let generative_ai = document.getElementById('generative-ai-keywords').checked;
    let result = await eel.check_keywords(keywords, category, generative_ai)();
    showNotification(result);
    if (result === "CSV file updated with search results.") {
        document.getElementById('keywords').value = '';
    }
}

async function scrapeTitles() {
    showNotification('Scraping titles...');
    let keywords = document.getElementById('title-keywords').value;
    let pages = document.getElementById('pages').value || "1"; // Default to page 1 if empty
    let sort = document.querySelector('input[name="sort"]:checked').value;
    let category = document.querySelector('input[name="title-category"]:checked').value;
    let generative_ai = document.getElementById('generative-ai-titles').checked;

    let result = await eel.scrape_titles(keywords, pages, sort, category, generative_ai)();
    showNotification(result);
    if (result === "CSV file updated with titles.") {
        document.getElementById('title-keywords').value = '';
        document.getElementById('pages').value = '';
    }
}

function showNotification(message) {
    const notificationBox = document.getElementById('notification-box');
    const notification = document.createElement('div');
    notification.classList.add('notification');
    notification.innerText = message;
    notificationBox.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 2000);
}

function toggleRangeType() {
    const rangeType = document.querySelector('input[name="range-type"]:checked').value;
    const resultsRange = document.getElementById('results-range');
    const pagesRange = document.getElementById('pages-range');

    if (rangeType === 'results') {
        resultsRange.style.display = 'block';
        pagesRange.style.display = 'none';
    } else {
        resultsRange.style.display = 'none';
        pagesRange.style.display = 'block';
    }
}

function handleInput() {
    let inputField = document.getElementById('keywords');
    if (expandTextField) {
        if (inputField.tagName.toLowerCase() === 'input') {
            expandToTextArea(inputField);
        } else {
            adjustTextAreaHeight(inputField);
            if (shouldCollapseToTextField(inputField)) {
                collapseToTextField(inputField);
            }
        }
    }
}

function expandToTextArea(inputField) {
    let textWidth = getTextWidth(inputField.value, getComputedStyle(inputField).font);

    if (textWidth >= inputField.clientWidth - 20) {
        const textArea = document.createElement('textarea');
        textArea.id = 'keywords';
        textArea.placeholder = 'Enter keywords separated by commas';
        textArea.value = inputField.value;
        textArea.style.width = '80%';
        textArea.style.padding = '10px';
        textArea.style.margin = '10px 0';
        textArea.style.border = '1px solid #ccc';
        textArea.style.borderRadius = '4px';
        textArea.style.maxHeight = '200px';
        textArea.style.overflowY = 'auto';
        textArea.style.resize = 'vertical';  // Allow vertical resizing
        textArea.style.fontFamily = getComputedStyle(inputField).fontFamily;
        textArea.style.fontSize = getComputedStyle(inputField).fontSize;
        textArea.style.lineHeight = getComputedStyle(inputField).lineHeight;

        inputField.parentNode.replaceChild(textArea, inputField);
        textArea.addEventListener('input', handleInput);
        textArea.focus();
    }
}

function collapseToTextField(textArea) {
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.id = 'keywords';
    inputField.placeholder = 'Enter keywords separated by commas';
    inputField.value = textArea.value;
    inputField.style.width = '80%';
    inputField.style.padding = '10px';
    inputField.style.margin = '10px 0';
    inputField.style.border = '1px solid #ccc';
    inputField.style.borderRadius = '4px';
    inputField.style.fontFamily = getComputedStyle(textArea).fontFamily;
    inputField.style.fontSize = getComputedStyle(textArea).fontSize;
    inputField.style.lineHeight = getComputedStyle(textArea).lineHeight;

    textArea.parentNode.replaceChild(inputField, textArea);
    inputField.addEventListener('input', handleInput);
    inputField.focus();
}

function adjustTextAreaHeight(textArea) {
    textArea.style.height = 'auto'; // Reset the height to allow it to shrink if necessary
    textArea.style.height = Math.min(textArea.scrollHeight, 200) + 'px';
}

function shouldCollapseToTextField(textArea) {
    return getLineCount(textArea.value) <= 1 && getTextWidth(textArea.value, getComputedStyle(textArea).font) < textArea.clientWidth - 20;
}

function getTextWidth(text, font) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = font;
    return context.measureText(text).width;
}

function getLineCount(text) {
    return text.split('\n').length;
}

document.getElementById('keywords').addEventListener('input', handleInput);

function toggleExpand(isChecked) {
    expandTextField = isChecked;
}


async function performAnalysis() {
    showNotification('Performing analysis...');
    let method = document.getElementById('analysis-method').value;
    let count = document.getElementById('analysis-count').value;
    let result = await eel.perform_analysis(method, parseInt(count))();
    showNotification(result);
}

async function automateProcess() {
    showNotification('Automating process...');
    let keywords = document.getElementById('keywords').value;
    let category = document.querySelector('input[name="category"]:checked').value;
    let result = await eel.automate_process(keywords, category)();
    showNotification(result);
}
