const fallbackLang = 'en'
const browserLang = navigator.language.toLowerCase()

function detectPreferredLang() {
    if (['sr', 'hr', 'bs', 'me', 'mk', 'sl', 'sr-latn', 'sr-cyrl'].some(l => browserLang.startsWith(l))) {
        return 'sr'
    }
    if (['ru', 'uk', 'by', 'be', 'kz'].some(l => browserLang.startsWith(l))) {
        return 'ru'
    }
    return fallbackLang
}

window.addEventListener("DOMContentLoaded", () => {
  const lang = detectPreferredLang();
  document.getElementById("lang-select").value = lang;
  document.getElementById("lang-select").dispatchEvent(new Event("change"));
});